# TrainTrack 1.0.0 "Stephenson" — Release 1
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/admin_tools_routes.py
# Admin tool endpoints: update check, run updater, logs.

import os
import logging
from pathlib import Path

from flask import Blueprint, jsonify, current_app

admin_tools_bp = Blueprint("admin_tools", __name__, url_prefix="/admin/tools")

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def _ok(**kwargs) -> tuple:
    return jsonify({"status": "ok", **kwargs}), 200


def _err(detail: str, **kwargs) -> tuple:
    return jsonify({"status": "error", "detail": detail, **kwargs}), 200


# ---------------------------------------------------------------------------
# Update routes (client only)
# ---------------------------------------------------------------------------

@admin_tools_bp.route("/check_updates", methods=["GET", "POST"])
def check_updates():
    try:
        from utils.traintrack_updater import check_for_updates
        result = check_for_updates()
        if result.get("error") and result.get("up_to_date"):
            return _err(result["error"])
        return _ok(
            up_to_date=result["up_to_date"],
            local_version=result["local_version"],
            remote_version=result["remote_version"],
            files_needing_update=result["files_needing_update"],
        )
    except Exception as e:
        return _err(f"❌ Update check failed: {e}")


@admin_tools_bp.route("/run_updater", methods=["GET", "POST"])
def run_updater():
    if os.getenv("TRAINTRACK_ROLE", "client") != "client":
        return _err("Updates are disabled on server installations.")
    try:
        from utils.traintrack_updater import run_full_update
        result = run_full_update()
        return _ok(**result)
    except Exception as e:
        return _err(f"❌ Updater failed: {e}")


# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------

@admin_tools_bp.route("/logs", methods=["GET"])
def logs():
    """Return list of available log files."""
    try:
        log_files = []
        if LOG_DIR.exists():
            for f in sorted(LOG_DIR.iterdir()):
                if f.is_file() and f.suffix in (".log", ".csv"):
                    log_files.append({
                        "name": f.name,
                        "size": f.stat().st_size,
                    })
        return _ok(logs=log_files)
    except Exception as e:
        return _err(f"❌ Log listing failed: {e}")


@admin_tools_bp.route("/logs/<filename>", methods=["GET"])
def logs_view(filename):
    """Return last 100 lines of a log file."""
    try:
        log_path = LOG_DIR / filename
        if not log_path.exists() or not log_path.is_file():
            return _err("Log file not found.")
        lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
        return _ok(lines=lines[-100:], total=len(lines))
    except Exception as e:
        return _err(f"❌ Log read failed: {e}")
