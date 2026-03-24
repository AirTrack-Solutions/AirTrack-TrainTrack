# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC
# routes/class_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from sqlalchemy import text
from extensions import db

class_bp = Blueprint("loco_class", __name__, url_prefix="/classes")


@class_bp.route("/")
def index():
    try:
        with db.engine.connect() as conn:
            classes = conn.execute(
                text("""
                    SELECT cl.*, t.name AS type_name, co.name AS country_name,
                        (SELECT COUNT(*) FROM locomotives l WHERE l.class_id = cl.id) AS loco_count
                    FROM classes cl
                    LEFT JOIN types t ON t.id = cl.type_id
                    LEFT JOIN countries co ON co.code = cl.country_code
                    ORDER BY cl.name
                """)
            ).mappings().all()
        return render_template("classes.html", classes=classes)
    except Exception:
        current_app.logger.exception("classes index error")
        flash("Error loading classes.", "danger")
        return render_template("classes.html", classes=[])


@class_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name         = request.form.get("name", "").strip()
        type_id      = request.form.get("type_id") or None
        manufacturer = request.form.get("manufacturer", "").strip() or None
        intro_year   = request.form.get("introduced_year", "").strip() or None
        country      = request.form.get("country_code") or None
        description  = request.form.get("description", "").strip() or None

        if not name:
            flash("Class name is required.", "danger")
            return _render_add_form()

        try:
            with db.engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO classes
                            (name, type_id, manufacturer, introduced_year, country_code, description)
                        VALUES
                            (:name, :type_id, :manufacturer, :intro_year, :country, :description)
                    """),
                    {
                        "name": name, "type_id": type_id, "manufacturer": manufacturer,
                        "intro_year": intro_year, "country": country, "description": description,
                    }
                )
            flash(f"Class {name} added.", "success")
            return redirect(url_for("loco_class.index"))
        except Exception as e:
            current_app.logger.exception("add class error")
            flash(f"Error: {e}", "danger")

    return _render_add_form()


def _render_add_form():
    with db.engine.connect() as conn:
        types     = conn.execute(text("SELECT id, name FROM types ORDER BY name")).mappings().all()
        countries = conn.execute(text("SELECT code, name FROM countries ORDER BY name")).mappings().all()
    return render_template("class_add.html", types=list(types), countries=list(countries))


@class_bp.route("/<int:class_id>/delete", methods=["POST"])
def delete(class_id):
    try:
        with db.engine.begin() as conn:
            cl = conn.execute(
                text("SELECT name FROM classes WHERE id = :id"), {"id": class_id}
            ).mappings().first()
            if cl:
                conn.execute(text("DELETE FROM classes WHERE id = :id"), {"id": class_id})
                flash(f"Class {cl['name']} deleted.", "success")
    except Exception:
        flash("Error deleting class.", "danger")
    return redirect(url_for("loco_class.index"))
