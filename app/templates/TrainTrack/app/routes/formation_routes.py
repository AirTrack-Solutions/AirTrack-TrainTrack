# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/formation_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from sqlalchemy import text
from extensions import db

formation_bp = Blueprint("formation", __name__, url_prefix="/formations")


def _get_lookups():
    with db.engine.connect() as conn:
        classes   = conn.execute(text("SELECT id, name FROM classes ORDER BY name")).mappings().all()
        operators = conn.execute(text("SELECT id, name FROM operators ORDER BY name")).mappings().all()
    return {"classes": list(classes), "operators": list(operators)}


@formation_bp.route("/")
def index():
    search   = request.args.get("q", "").strip()
    page     = max(1, int(request.args.get("page", 1)))
    per_page = 50
    where    = ["1=1"]
    params   = {}

    if search:
        where.append("(f.set_number LIKE :q OR c.name LIKE :q OR o.name LIKE :q)")
        params["q"] = f"%{search}%"

    where_clause = " AND ".join(where)

    try:
        with db.engine.connect() as conn:
            total = conn.execute(
                text(f"""
                    SELECT COUNT(*) FROM formations f
                    LEFT JOIN classes   c ON c.id = f.class_id
                    LEFT JOIN operators o ON o.id = f.operator_id
                    WHERE {where_clause}
                """), params
            ).scalar() or 0

            offset = (page - 1) * per_page
            params["limit"]  = per_page
            params["offset"] = offset

            formations = conn.execute(
                text(f"""
                    SELECT
                        f.id, f.set_number, f.status,
                        c.name AS class_name,
                        o.name AS operator_name,
                        (SELECT COUNT(*) FROM sightings s WHERE s.formation_id = f.id) AS sighting_count,
                        (SELECT COUNT(*) FROM formation_vehicles fv WHERE fv.formation_id = f.id) AS vehicle_count
                    FROM formations f
                    LEFT JOIN classes   c ON c.id = f.class_id
                    LEFT JOIN operators o ON o.id = f.operator_id
                    WHERE {where_clause}
                    ORDER BY f.set_number
                    LIMIT :limit OFFSET :offset
                """), params
            ).mappings().all()

        return render_template(
            "formations.html",
            formations=formations,
            total=total, page=page, per_page=per_page,
            pages=(total + per_page - 1) // per_page,
            search=search,
        )
    except Exception:
        current_app.logger.exception("formations index error")
        flash("Error loading formations.", "danger")
        return render_template("formations.html", formations=[], total=0, page=1, pages=1, search="")


@formation_bp.route("/<int:formation_id>")
def detail(formation_id):
    try:
        with db.engine.connect() as conn:
            formation = conn.execute(
                text("""
                    SELECT f.*, c.name AS class_name, o.name AS operator_name
                    FROM formations f
                    LEFT JOIN classes   c ON c.id = f.class_id
                    LEFT JOIN operators o ON o.id = f.operator_id
                    WHERE f.id = :id
                """), {"id": formation_id}
            ).mappings().first()

            if not formation:
                flash("Formation not found.", "warning")
                return redirect(url_for("formation.index"))

            vehicles = conn.execute(
                text("""
                    SELECT * FROM formation_vehicles
                    WHERE formation_id = :id
                    ORDER BY position, vehicle_number
                """), {"id": formation_id}
            ).mappings().all()

            sightings = conn.execute(
                text("""
                    SELECT s.*, loc.name AS location_name
                    FROM sightings s
                    LEFT JOIN locations loc ON loc.id = s.location_id
                    WHERE s.formation_id = :id
                    ORDER BY s.sighting_date DESC
                """), {"id": formation_id}
            ).mappings().all()

        return render_template(
            "formation_detail.html",
            formation=formation,
            vehicles=vehicles,
            sightings=sightings,
        )
    except Exception:
        current_app.logger.exception("formation detail error")
        flash("Error loading formation.", "danger")
        return redirect(url_for("formation.index"))


@formation_bp.route("/add", methods=["GET", "POST"])
def add():
    lookups = _get_lookups()

    if request.method == "POST":
        set_number = request.form.get("set_number", "").strip()
        class_id   = request.form.get("class_id") or None
        op_id      = request.form.get("operator_id") or None
        status     = request.form.get("status", "active")
        notes      = request.form.get("notes", "").strip() or None

        # Vehicles — submitted as parallel arrays
        v_numbers  = request.form.getlist("vehicle_number[]")
        v_types    = request.form.getlist("vehicle_type[]")
        v_positions = request.form.getlist("vehicle_position[]")

        if not set_number:
            flash("Set number is required.", "danger")
            return render_template("formation_add.html", **lookups)

        try:
            with db.engine.begin() as conn:
                result = conn.execute(
                    text("""
                        INSERT INTO formations (set_number, class_id, operator_id, status, notes)
                        VALUES (:set_number, :class_id, :op_id, :status, :notes)
                    """),
                    {"set_number": set_number, "class_id": class_id, "op_id": op_id,
                     "status": status, "notes": notes}
                )
                formation_id = result.lastrowid

                for i, vnum in enumerate(v_numbers):
                    vnum = vnum.strip()
                    if not vnum:
                        continue
                    vtype = v_types[i].strip() if i < len(v_types) else ""
                    vpos  = v_positions[i] if i < len(v_positions) else None
                    conn.execute(
                        text("""
                            INSERT INTO formation_vehicles
                                (formation_id, vehicle_number, vehicle_type, position)
                            VALUES (:fid, :vnum, :vtype, :vpos)
                        """),
                        {"fid": formation_id, "vnum": vnum,
                         "vtype": vtype or None, "vpos": vpos or None}
                    )

            flash(f"Formation {set_number} added.", "success")
            return redirect(url_for("formation.detail", formation_id=formation_id))
        except Exception as e:
            current_app.logger.exception("add formation error")
            flash(f"Error adding formation: {e}", "danger")

    return render_template("formation_add.html", **lookups)


@formation_bp.route("/<int:formation_id>/delete", methods=["POST"])
def delete(formation_id):
    try:
        with db.engine.begin() as conn:
            f = conn.execute(
                text("SELECT set_number FROM formations WHERE id = :id"), {"id": formation_id}
            ).mappings().first()
            if f:
                conn.execute(text("DELETE FROM formations WHERE id = :id"), {"id": formation_id})
                flash(f"Formation {f['set_number']} deleted.", "success")
    except Exception:
        current_app.logger.exception("delete formation error")
        flash("Error deleting formation.", "danger")
    return redirect(url_for("formation.index"))
