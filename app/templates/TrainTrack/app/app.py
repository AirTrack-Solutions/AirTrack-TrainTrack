# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# app.py

from version import FULL_VERSION, DISPLAY_VERSION

from utils.country_flags import get_country_flag
from utils import jinja_filters, theme_scanner
from extensions import db

import logging
import os
import subprocess
import sys

from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import time

import pytz

from dotenv import load_dotenv

from flask import (
    Flask,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    has_app_context,
)

from flask_wtf.csrf import CSRFProtect, generate_csrf
from sqlalchemy import text

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=str(Path(__file__).with_name('templates')),
    static_folder=str(Path(__file__).with_name('static')),
)

# ---------------------------------------------------------------------------
# License load
# ---------------------------------------------------------------------------
try:
    if os.getenv("TRAINTRACK_ROLE") == "client":
        from config.license import load_license
        license_data = load_license()
        if license_data:
            print("✔ License loaded")
            print(f"Customer: {license_data.name}")
            print(f"Edition:  {license_data.edition}")
            print(f"License ID: {license_data.license_id}")
            print(f"Issued: {license_data.issued}")
        else:
            print("⚠ No license detected")
except Exception as e:
    print(f"⚠ License system not available: {e}")

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') or \
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
    f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['DEBUG'] = False
app.config['TESTING'] = False

app.secret_key = os.getenv("SECRET_KEY", "traintrack-fallback-key-change-me")

db.init_app(app)

# ---------------------------------------------------------------------------
# CSRF
# ---------------------------------------------------------------------------
csrf = CSRFProtect()
app.config.update(
    WTF_CSRF_TIME_LIMIT=None,
    WTF_CSRF_SSL_STRICT=False,
    WTF_CSRF_HEADERS=['X-CSRFToken'],
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False,
)
csrf.init_app(app)

# ---------------------------------------------------------------------------
# Jinja filters + globals
# ---------------------------------------------------------------------------
jinja_filters.register_filters(app)

app.jinja_env.globals['csrf_token'] = generate_csrf
app.jinja_env.globals['get_country_flag'] = get_country_flag
app.jinja_env.globals['time'] = time

# ---------------------------------------------------------------------------
# Context processors
# ---------------------------------------------------------------------------
@app.context_processor
def inject_traintrack_version():
    return {
        "TRAINTRACK_VERSION": FULL_VERSION,
        "TRAINTRACK_DISPLAY_VERSION": DISPLAY_VERSION,
    }


@app.context_processor
def inject_app_context():
    return {"current_app": current_app, "config": current_app.config}


@app.context_processor
def inject_time():
    return {"time": time}


@app.context_processor
def inject_env_vars():
    try:
        return {
            "TRAINTRACK_ROLE": os.getenv("TRAINTRACK_ROLE", "client"),
            "TRAINTRACK_SYNC_USER": os.getenv("TRAINTRACK_SYNC_USER", ""),
        }
    except Exception:
        return {}


@app.context_processor
def inject_settings():
    """Expose app_settings rows as `settings` in templates."""
    try:
        with db.engine.connect() as conn:
            rows = conn.execute(
                text("SELECT SettingKey, SettingValue FROM app_settings")
            ).fetchall()
            return {"settings": {row[0]: row[1] for row in rows}}
    except Exception:
        return {"settings": {}}


@app.context_processor
def inject_theme():
    """Inject current theme key for body class."""
    try:
        with db.engine.connect() as conn:
            row = conn.execute(
                text("SELECT SettingValue FROM app_settings WHERE SettingKey = 'Theme'")
            ).fetchone()
            theme = row[0] if row and row[0] else "default"
            return {"TRAINTRACK_THEME": theme}
    except Exception:
        return {"TRAINTRACK_THEME": "default"}


# ---------------------------------------------------------------------------
# Timezone helpers
# ---------------------------------------------------------------------------
def _safe_tz(name: str | None):
    try:
        return pytz.timezone(name) if name else pytz.utc
    except Exception:
        logging.warning("Invalid timezone '%s', defaulting to UTC", name)
        return pytz.utc


def get_app_timezone():
    try:
        if not has_app_context():
            return pytz.utc
        with db.engine.connect() as conn:
            row = conn.execute(
                text("SELECT SettingValue FROM app_settings WHERE SettingKey = 'timezone'")
            ).fetchone()
            return _safe_tz(row[0] if row else None)
    except Exception:
        return pytz.utc


def get_backup_dir() -> Path:
    base = Path("/app/backups")
    try:
        base.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"❌ Failed to create backup directory {base}: {e}")
    return base


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_DIR = Path(BASE_DIR) / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "traintrack.log"

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
file_handler.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, logging.StreamHandler()])


# ---------------------------------------------------------------------------
# Before request
# ---------------------------------------------------------------------------
@app.before_request
def _before():
    theme_scanner.scan_if_stale()


# ---------------------------------------------------------------------------
# Admin routes (inline — lightweight)
# ---------------------------------------------------------------------------
@app.route("/admin/backup_database", methods=["POST"])
def backup_database():
    try:
        backup_dir = get_backup_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = backup_dir / f"traintrack_backup_{timestamp}.sql"
        cmd = [
            "mysqldump",
            f"-h{os.getenv('DB_HOST', 'traintrack-db')}",
            f"-u{os.getenv('DB_USER', '')}",
            f"-p{os.getenv('DB_PASSWORD', '')}",
            os.getenv("DB_NAME", "traintrack"),
        ]
        with open(filename, "wb") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE)
        if result.returncode == 0:
            flash(f"Backup created: {filename.name}", "success")
        else:
            raise RuntimeError(result.stderr.decode())
    except Exception as e:
        logging.error("❌ Backup error: %s", e)
        flash("Backup failed.", "danger")
    return redirect(url_for("admin.admin_dashboard"))


@app.route("/admin/flush_logs", methods=["POST"])
def flush_logs():
    try:
        open(LOG_FILE, "w").close()
        flash("Logs flushed.", "success")
    except Exception:
        flash("Failed to flush logs.", "danger")
    return redirect(url_for("admin.admin_dashboard"))


@app.route("/admin/flush", methods=["POST"])
def flush_database():
    try:
        if request.form.get("confirm_flush") != "CONFIRM":
            flash("Flush aborted.", "danger")
            return redirect(url_for("admin.admin_dashboard"))
        with db.engine.begin() as conn:
            conn.execute(text("DELETE FROM sightings"))
            conn.execute(text("DELETE FROM formations"))
            conn.execute(text("DELETE FROM locomotives"))
        flash("Database flushed.", "success")
    except Exception as e:
        logging.error("❌ Flush error: %s", e)
        flash("Failed to flush database.", "danger")
    return redirect(url_for("admin.admin_dashboard"))


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------
from routes.main_routes import main_bp
from routes.locomotive_routes import locomotive_bp
from routes.sighting_routes import sighting_bp
from routes.formation_routes import formation_bp
from routes.operator_routes import operator_bp
from routes.location_routes import location_bp
from routes.reports_routes import reports_bp
from routes.admin_routes import admin_bp

try:
    from routes.admin_tools_routes import admin_tools_bp
    has_admin_tools = True
except ImportError:
    has_admin_tools = False

app.register_blueprint(main_bp)
logging.info("✅ Registered blueprint: main_bp (/)")

app.register_blueprint(locomotive_bp)
logging.info("✅ Registered blueprint: locomotive_bp (/locomotives)")

app.register_blueprint(sighting_bp)
logging.info("✅ Registered blueprint: sighting_bp (/sightings)")

app.register_blueprint(formation_bp)
logging.info("✅ Registered blueprint: formation_bp (/formations)")

app.register_blueprint(operator_bp)
logging.info("✅ Registered blueprint: operator_bp (/operators)")

app.register_blueprint(location_bp)
logging.info("✅ Registered blueprint: location_bp (/locations)")

app.register_blueprint(reports_bp)
logging.info("✅ Registered blueprint: reports_bp (/reports)")

app.register_blueprint(admin_bp)
csrf.exempt(admin_bp)
logging.info("✅ Registered blueprint: admin_bp (/admin)")

if has_admin_tools:
    app.register_blueprint(admin_tools_bp)
    csrf.exempt(admin_tools_bp)
    logging.info("✅ Registered blueprint: admin_tools_bp (/admin/tools)")

# ---------------------------------------------------------------------------
# Dev entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        print("\n--- Flask URL Map ---")
        print(app.url_map)
        print("----------------------\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,
        threaded=True,
    )
