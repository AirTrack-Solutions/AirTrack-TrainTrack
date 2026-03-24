#!/usr/bin/env python3
# TrainTrack 1.0.0 "Stephenson" — Release 1
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# utils/generate_update_manifest.py
# Walks the TrainTrack app directory, hashes all deployable files,
# and writes update.json to the website updates/traintrack/ directory.
#
# Usage:
#   python3 app/utils/generate_update_manifest.py
#
# Run from ~/docker/TrainTrack/TrainTrack1/

import hashlib
import json
import os
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
APP_DIR      = Path(__file__).resolve().parent.parent          # /app
OUTPUT_DIR   = Path.home() / "docker/TrainTrack/TrainTrack1/updates/traintrack"
OUTPUT_FILE  = OUTPUT_DIR / "update.json"
VERSION_FILE = APP_DIR / "version.py"

# Directories to skip entirely
SKIP_DIRS = {
    "__pycache__",
    ".git",
    "logs",
    "backups",
    "data",
    "app_data",
    "updates",
    ".pytest_cache",
    ".mypy_cache",
}

# File extensions to skip
SKIP_EXTS = {
    ".pyc", ".pyo", ".pyd",
    ".log", ".bak",
    ".db", ".sqlite",
    ".lic",
}

# Individual files to skip
SKIP_FILES = {
    ".env",
    ".env.server",
    ".env.client",
    "config.json",
    "config/license.lic",
    "license.lic",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_version() -> str:
    try:
        for line in VERSION_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("TRAINTRACK_VERSION"):
                return line.split("=")[1].strip().strip("'\"")
    except Exception:
        pass
    return "1.0.0"


def should_skip(rel_path: str, path: Path) -> bool:
    parts = Path(rel_path).parts

    # Skip dirs
    for part in parts[:-1]:
        if part in SKIP_DIRS:
            return True

    # Skip extensions
    if path.suffix.lower() in SKIP_EXTS:
        return True

    # Skip individual files
    normalized = Path(rel_path).as_posix()
    if normalized in SKIP_FILES:
        return True

    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate():
    version = get_version()
    today = date.today().isoformat()

    files = []
    for dirpath, dirnames, filenames in os.walk(APP_DIR):
        # Prune skip dirs in place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in sorted(filenames):
            full_path = Path(dirpath) / filename
            rel_path = full_path.relative_to(APP_DIR).as_posix()

            if should_skip(rel_path, full_path):
                continue

            file_hash = sha256(full_path)
            files.append({"path": rel_path, "hash": file_hash})

    # Sort by path for consistency
    files.sort(key=lambda x: x["path"])

    manifest = {
        "version": version,
        "released": today,
        "files": files,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"✅ update.json generated")
    print(f"   Version:  {version}")
    print(f"   Released: {today}")
    print(f"   Files:    {len(files)}")
    print(f"   Output:   {OUTPUT_FILE}")


if __name__ == "__main__":
    generate()
