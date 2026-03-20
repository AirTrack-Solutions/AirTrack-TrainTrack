# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/admin_routes.py

from flask import Blueprint, render_template, request, jsonify, current_app
from sqlalchemy import text
from extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _get_stats():
    try:
        with db.engine.connect() as conn:
            return {
                "locomotives": conn.execute(text("SELECT COUNT(*) FROM locomotives")).scalar() or 0,
                "formations":  conn.execute(text("SELECT COUNT(*) FROM formations")).scalar() or 0,
                "sightings":   conn.execute(text("SELECT COUNT(*) FROM sightings")).scalar() or 0,
                "cops":        conn.execute(text("SELECT COUNT(*) FROM sightings WHERE is_cop = 1")).scalar() or 0,
                "dubs":        (conn.execute(text("SELECT COUNT(*) FROM sightings")).scalar() or 0) -
                               (conn.execute(text("SELECT COUNT(*) FROM sightings WHERE is_cop = 1")).scalar() or 0),
                "operators":   conn.execute(text("SELECT COUNT(*) FROM operators")).scalar() or 0,
                "locations":   conn.execute(text("SELECT COUNT(*) FROM locations")).scalar() or 0,
            }
    except Exception:
        return {"locomotives":0,"formations":0,"sightings":0,"cops":0,"dubs":0,"operators":0,"locations":0}


@admin_bp.route("/")
def admin_dashboard():
    stats = _get_stats()
    return render_template("admin.html", stats=stats)


@admin_bp.route("/cockpit")
def cockpit():
    stats = _get_stats()
    try:
        with db.engine.connect() as conn:
            recent_cops = conn.execute(
                text("""
                    SELECT s.cop_date, l.number AS loco_number, loc.name AS location_name
                    FROM sightings s
                    JOIN locomotives l ON l.id = s.locomotive_id
                    LEFT JOIN locations loc ON loc.id = s.location_id
                    WHERE s.is_cop = 1
                    ORDER BY s.cop_date DESC LIMIT 10
                """)
            ).mappings().all()
    except Exception:
        recent_cops = []
    return render_template("admin_cockpit.html", stats=stats, recent_cops=recent_cops)


@admin_bp.route("/settings", methods=["GET"])
def admin_settings():
    rows = db.session.execute(
        text("SELECT SettingKey, SettingValue FROM app_settings "
             "WHERE SettingKey IN ('FirstName','LastName','Callsign','Theme')")
    ).mappings().all()
    settings = {row["SettingKey"]: row["SettingValue"] for row in rows}

    # Load available themes
    try:
        from utils.theme_scanner import THEMES_JSON
        import json
        themes = json.loads(THEMES_JSON.read_text()) if THEMES_JSON.exists() else []
    except Exception:
        themes = []

    return render_template("admin_settings.html", settings=settings, themes=themes)


@admin_bp.route("/update_theme", methods=["POST"])
def update_theme():
    try:
        theme = request.form.get("theme", "default").strip()
        with db.engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO app_settings (SettingKey, SettingValue)
                    VALUES ('Theme', :theme)
                    ON DUPLICATE KEY UPDATE SettingValue = VALUES(SettingValue)
                """),
                {"theme": theme}
            )
        flash(f"Theme changed to {theme}.", "success")
    except Exception as e:
        current_app.logger.exception("update_theme failed")
        flash(f"Error: {e}", "danger")
    return redirect(url_for("admin.admin_settings"))
def save_settings():
    try:
        data = request.get_json(silent=True)
        if data is None:
            data = {
                "first_name": request.form.get("first_name", ""),
                "last_name":  request.form.get("last_name",  ""),
                "callsign":   request.form.get("callsign",   ""),
            }
        key_map = {
            "first_name": "FirstName",
            "last_name":  "LastName",
            "callsign":   "Callsign",
        }
        with db.engine.begin() as conn:
            for field, db_key in key_map.items():
                value = (data.get(field) or "").strip()
                conn.execute(
                    text("""
                        INSERT INTO app_settings (SettingKey, SettingValue)
                        VALUES (:key, :value)
                        ON DUPLICATE KEY UPDATE SettingValue = VALUES(SettingValue)
                    """),
                    {"key": db_key, "value": value},
                )
        return jsonify({"success": True})
    except Exception as e:
        current_app.logger.exception("save_settings failed")
        return jsonify({"success": False, "error": str(e)}), 500
