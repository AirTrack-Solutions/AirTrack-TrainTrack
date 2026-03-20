# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/operator_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from sqlalchemy import text
from extensions import db

operator_bp = Blueprint("operator", __name__, url_prefix="/operators")


@operator_bp.route("/")
def index():
    try:
        with db.engine.connect() as conn:
            operators = conn.execute(
                text("""
                    SELECT o.*, co.name AS country_name,
                        (SELECT COUNT(*) FROM locomotives l WHERE l.operator_id = o.id) AS loco_count
                    FROM operators o
                    LEFT JOIN countries co ON co.code = o.country_code
                    ORDER BY o.name
                """)
            ).mappings().all()
        return render_template("operators.html", operators=operators)
    except Exception:
        current_app.logger.exception("operators index error")
        flash("Error loading operators.", "danger")
        return render_template("operators.html", operators=[])


@operator_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        code    = request.form.get("code", "").strip() or None
        country = request.form.get("country_code") or None
        otype   = request.form.get("type", "passenger")
        notes   = request.form.get("notes", "").strip() or None

        if not name:
            flash("Operator name is required.", "danger")
            return render_template("operator_add.html")

        try:
            with db.engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO operators (name, code, country_code, type, notes)
                        VALUES (:name, :code, :country, :type, :notes)
                    """),
                    {"name": name, "code": code, "country": country, "type": otype, "notes": notes}
                )
            flash(f"Operator {name} added.", "success")
            return redirect(url_for("operator.index"))
        except Exception as e:
            current_app.logger.exception("add operator error")
            flash(f"Error: {e}", "danger")

    with db.engine.connect() as conn:
        countries = conn.execute(text("SELECT code, name FROM countries ORDER BY name")).mappings().all()
    return render_template("operator_add.html", countries=list(countries))


@operator_bp.route("/<int:op_id>/delete", methods=["POST"])
def delete(op_id):
    try:
        with db.engine.begin() as conn:
            op = conn.execute(
                text("SELECT name FROM operators WHERE id = :id"), {"id": op_id}
            ).mappings().first()
            if op:
                conn.execute(text("DELETE FROM operators WHERE id = :id"), {"id": op_id})
                flash(f"Operator {op['name']} deleted.", "success")
    except Exception:
        flash("Error deleting operator.", "danger")
    return redirect(url_for("operator.index"))
