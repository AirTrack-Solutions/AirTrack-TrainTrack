# TrainTrack 1.0.0 "Stephenson" — Release 1
# Copyright (c) 2025 Trevor ('Subhuti'). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# scripts/file_sync.py
# Run on the dev machine (NOT inside Docker).
# Computes hashes of deployable files, writes update.json,
# copies changed files to static/updates/, then SFTPs everything to Pi.
#
# Usage:
#   cd ~/docker/TrainTrack/TrainTrack1/app
#   python3 scripts/file_sync.py

from __future__ import annotations

import hashlib
import json
import logging
import os
import posixpath
import shutil
import sys
from fnmatch import fnmatch
from pathlib import Path

# ---------------------------------------------------------------------------
# Guard: must not run inside Docker
# ---------------------------------------------------------------------------

def _in_docker() -> bool:
    if Path('/.dockerenv').exists():
        return True
    try:
        return 'docker' in Path('/proc/1/cgroup').read_text()
    except Exception:
        return False

if _in_docker():
    print("❌ file_sync.py must run on the host, not inside Docker. Aborting.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR    = Path(__file__).resolve().parent.parent   # .../TrainTrack1/app
SCRIPTS_DIR = BASE_DIR / 'scripts'
LOG_DIR     = BASE_DIR / 'logs'
UPDATE_DIR  = BASE_DIR / 'static' / 'updates'
UPDATE_JSON = UPDATE_DIR / 'update.json'
LOCAL_HASH_FILE = UPDATE_DIR / 'local_hashes.json'

LOG_DIR.mkdir(parents=True, exist_ok=True)
UPDATE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / 'file_sync.log'),
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True,
)

# ---------------------------------------------------------------------------
# Pi SFTP configuration
# ---------------------------------------------------------------------------
PI_HOST       = '192.168.0.153'
PI_PORT       = 22
PI_USER       = 'airtrack'
PI_REMOTE_DIR = '/home/airtrack/docker/airtrack-website/updates/traintrack'
SSH_KEY_PATH  = os.path.expanduser('~/.ssh/id_ed25519')

# ---------------------------------------------------------------------------
# What to include / exclude
# ---------------------------------------------------------------------------
VALID_EXTENSIONS = {'.py', '.html', '.css', '.js', '.json', '.txt', '.sh',
                    '.ico', '.png', '.jpg', '.jpeg', '.svg', '.dockerignore',
                    '.gitignore'}

TOP_LEVEL_ALLOWED = {
    'app.py', 'wsgi.py', 'requirements.txt',
    '.dockerignore', 'wait-for-mariadb.sh',
    'extensions.py', 'version.py', 'schema.sql',
}

ALLOWED_SUBDIRS = {'static', 'templates', 'routes', 'utils', 'security', 'config', 'models'}

SKIP_DIRS = {
    'static/updates', 'static/uploads', '__pycache__',
    '.git', 'backups', 'database', 'uploads', 'app_data',
    'logs',
}

SKIP_PATTERNS = {
    '*.env', '.env*', '*.lic', 'local_hashes.json',
    'update.json', '*.pyc', '*.log', 'config.json',
    '*.yml', 'themes.json', 'themes.css',
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}


def _save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def _should_skip_dir(rel_dir: str) -> bool:
    for skip in SKIP_DIRS:
        if rel_dir == skip or rel_dir.startswith(skip + '/'):
            return True
    return False


def _should_skip_file(rel_path: str) -> bool:
    filename = Path(rel_path).name
    for pat in SKIP_PATTERNS:
        if fnmatch(filename, pat) or fnmatch(rel_path, pat):
            return True
    return False


def _is_deployable(rel_path: str) -> bool:
    p = Path(rel_path)
    parts = p.parts

    if len(parts) == 1:
        return rel_path in TOP_LEVEL_ALLOWED

    if parts[0] not in ALLOWED_SUBDIRS:
        return False

    if p.suffix.lower() not in VALID_EXTENSIONS and p.name not in {'Dockerfile', '.dockerignore'}:
        return False

    return True


def _local_version() -> str:
    version_file = BASE_DIR / 'version.py'
    try:
        for line in version_file.read_text(encoding='utf-8').splitlines():
            if line.startswith('TRAINTRACK_VERSION'):
                return line.split('=')[1].strip().strip("'\"")
    except Exception:
        pass
    return '1.0.0'


# ---------------------------------------------------------------------------
# Collect changed files
# ---------------------------------------------------------------------------

def collect_updates() -> list[dict]:
    history = _load_json(LOCAL_HASH_FILE)
    tracked: set[str] = set()
    updates: list[dict] = []

    for root, dirs, files in os.walk(BASE_DIR):
        rel_root = Path(root).relative_to(BASE_DIR).as_posix()
        if rel_root == '.':
            rel_root = ''

        dirs[:] = [
            d for d in dirs
            if not _should_skip_dir((rel_root + '/' + d).lstrip('/'))
        ]

        for filename in files:
            rel_path = (
                (rel_root + '/' + filename).lstrip('/')
                if rel_root else filename
            )

            if _should_skip_file(rel_path):
                continue
            if not _is_deployable(rel_path):
                continue

            abs_path = BASE_DIR / rel_path
            new_hash = _sha256(abs_path)
            old_hash = history.get(rel_path)
            tracked.add(rel_path)

            if new_hash != old_hash:
                updates.append({'path': rel_path, 'hash': new_hash})
                history[rel_path] = new_hash
                logging.info(f'📝 Changed: {rel_path}')

    for stale in list(history):
        if stale not in tracked:
            del history[stale]
            logging.info(f'🧹 Removed stale: {stale}')

    _save_json(LOCAL_HASH_FILE, history)

    if updates:
        print(f'✅ {len(updates)} file(s) changed.')
    else:
        print('🔍 No changes found.')

    return updates


# ---------------------------------------------------------------------------
# Copy changed files to static/updates/
# ---------------------------------------------------------------------------

def copy_to_update_dir(updates: list[dict]) -> None:
    for entry in updates:
        src  = BASE_DIR / entry['path']
        dest = UPDATE_DIR / entry['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        logging.info(f'📦 Staged: {entry["path"]}')


# ---------------------------------------------------------------------------
# Write update.json
# ---------------------------------------------------------------------------

def write_update_json(updates: list[dict]) -> None:
    version = _local_version()
    history = _load_json(LOCAL_HASH_FILE)
    all_files = [{'path': p, 'hash': h} for p, h in sorted(history.items())]
    data = {
        'version': version,
        'released': __import__('datetime').datetime.now().strftime('%Y-%m-%d'),
        'files': all_files,
    }
    _save_json(UPDATE_JSON, data)
    print(f'📄 update.json written (v{version}, {len(all_files)} files tracked, {len(updates)} changed)')
    logging.info(f'update.json written v{version}')


# ---------------------------------------------------------------------------
# SFTP upload to Pi
# ---------------------------------------------------------------------------

def upload_to_pi() -> None:
    try:
        import paramiko
    except ImportError:
        print('❌ paramiko not installed. Run: pip install paramiko')
        sys.exit(1)

    if not Path(SSH_KEY_PATH).exists():
        print(f'❌ SSH key not found: {SSH_KEY_PATH}')
        sys.exit(1)

    print(f'🔑 Connecting to {PI_USER}@{PI_HOST}:{PI_PORT}…')

    try:
        key = paramiko.Ed25519Key.from_private_key_file(SSH_KEY_PATH)
        transport = paramiko.Transport((PI_HOST, PI_PORT))
        transport.connect(username=PI_USER, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        if sftp is None:
            raise RuntimeError("Failed to create SFTP client.")

        def _ensure_remote_dir(remote_path: str) -> None:
            parts = remote_path.replace(PI_REMOTE_DIR, '').strip('/').split('/')
            path = PI_REMOTE_DIR
            for part in parts:
                if not part:
                    continue
                path = posixpath.join(path, part)
                try:
                    sftp.stat(path)
                except (FileNotFoundError, IOError):
                    sftp.mkdir(path)

        # Upload update.json first
        sftp.put(str(UPDATE_JSON), posixpath.join(PI_REMOTE_DIR, 'update.json'))
        print('⬆️  Uploaded: update.json')
        logging.info('Uploaded update.json to Pi')

        # Upload all staged files
        for local_file in UPDATE_DIR.rglob('*'):
            if not local_file.is_file():
                continue
            if local_file.name == 'update.json':
                continue
            if local_file.name in {'local_hashes.json', 'last_applied_hash.txt'}:
                continue

            rel = local_file.relative_to(UPDATE_DIR).as_posix()
            remote_file = posixpath.join(PI_REMOTE_DIR, rel)
            remote_dir  = posixpath.dirname(remote_file)
            _ensure_remote_dir(remote_dir)
            sftp.put(str(local_file), remote_file)
            print(f'⬆️  Uploaded: {rel}')
            logging.info(f'Uploaded {rel} to Pi')

        sftp.close()
        transport.close()
        print('✅ Upload to Pi complete.')
        logging.info('Upload to Pi complete')

    except Exception as e:
        print(f'❌ SFTP upload failed: {e}')
        logging.error(f'SFTP upload failed: {e}')
        sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print('🚀 TrainTrack file_sync starting…')
    logging.info('file_sync started')

    updates = collect_updates()
    write_update_json(updates)

    if updates:
        copy_to_update_dir(updates)
        upload_to_pi()
        print('🎉 Sync complete.')
    else:
        upload_to_pi()
        print('📭 No file changes. update.json refreshed on Pi.')

    logging.info('file_sync complete')


if __name__ == '__main__':
    main()
