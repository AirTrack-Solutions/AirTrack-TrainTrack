# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC
# routes/depot_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from sqlalchemy import text
from extensions import db

depot_bp = Blueprint("depot", __name__, url_prefix="/depots")


@depot_bp.route("/")
def index():
    try:
        with db.engine.connect() as conn:
            depots = conn.execute(
                text("""
                    SELECT d.*, o.name AS operator_name, co.name AS country_name,
                        (SELECT COUNT(*) FROM locomotives l WHERE l.depot_id = d.id) AS loco_count
                    FROM depots d
                    LEFT JOIN operators o ON o.id = d.operator_id
                    LEFT JOIN countries co ON co.code = d.country_code
                    ORDER BY d.name
                """)
            ).mappings().all()
        return render_template("depots.html", depots=depots)
    except Exception:
        current_app.logger.exception("depots index error")
        flash("Error loading depots.", "danger")
        return render_template("depots.html", depots=[])


@depot_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        code        = request.form.get("code", "").strip() or None
        operator_id = request.form.get("operator_id") or None
        country     = request.form.get("country_code") or None
        notes       = request.form.get("notes", "").strip() or None

        if not name:
            flash("Depot name is required.", "danger")
            return _render_add_form()

        try:
            with db.engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO depots (name, code, operator_id, country_code, notes)
                        VALUES (:name, :code, :operator_id, :country, :notes)
                    """),
                    {
                        "name": name, "code": code, "operator_id": operator_id,
                        "country": country, "notes": notes,
                    }
                )
            flash(f"Depot {name} added.", "success")
            return redirect(url_for("depot.index"))
        except Exception as e:
            current_app.logger.exception("add depot error")
            flash(f"Error: {e}", "danger")

    return _render_add_form()


def _render_add_form():
    with db.engine.connect() as conn:
        operators = conn.execute(text("SELECT id, name FROM operators ORDER BY name")).mappings().all()
        countries = conn.execute(text("SELECT code, name FROM countries ORDER BY name")).mappings().all()
    return render_template("depot_add.html", operators=list(operators), countries=list(countries))


@depot_bp.route("/<int:depot_id>/delete", methods=["POST"])
def delete(depot_id):
    try:
        with db.engine.begin() as conn:
            dep = conn.execute(
                text("SELECT name FROM depots WHERE id = :id"), {"id": depot_id}
            ).mappings().first()
            if dep:
                conn.execute(text("DELETE FROM depots WHERE id = :id"), {"id": depot_id})
                flash(f"Depot {dep['name']} deleted.", "success")
    except Exception:
        flash("Error deleting depot.", "danger")
    return redirect(url_for("depot.index"))
