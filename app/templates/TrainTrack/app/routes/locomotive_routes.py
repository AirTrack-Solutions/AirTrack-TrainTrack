# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/locomotive_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from sqlalchemy import text
from extensions import db

locomotive_bp = Blueprint("locomotive", __name__, url_prefix="/locomotives")


def _get_lookups():
    """Return classes, operators, depots, types, countries for form dropdowns."""
    with db.engine.connect() as conn:
        classes   = conn.execute(text("SELECT id, name FROM classes ORDER BY name")).mappings().all()
        operators = conn.execute(text("SELECT id, name FROM operators ORDER BY name")).mappings().all()
        depots    = conn.execute(text("SELECT id, name FROM depots ORDER BY name")).mappings().all()
        types     = conn.execute(text("SELECT id, name FROM types ORDER BY name")).mappings().all()
        countries = conn.execute(text("SELECT code, name FROM countries ORDER BY name")).mappings().all()
    return {
        "classes":   list(classes),
        "operators": list(operators),
        "depots":    list(depots),
        "types":     list(types),
        "countries": list(countries),
    }


@locomotive_bp.route("/")
def index():
    search   = request.args.get("q", "").strip()
    status   = request.args.get("status", "")
    type_id  = request.args.get("type_id", "")
    op_id    = request.args.get("operator_id", "")
    page     = max(1, int(request.args.get("page", 1)))
    per_page = 50

    where  = ["1=1"]
    params = {}

    if search:
        where.append("(l.number LIKE :q OR l.name LIKE :q OR c.name LIKE :q)")
        params["q"] = f"%{search}%"
    if status:
        where.append("l.status = :status")
        params["status"] = status
    if type_id:
        where.append("l.type_id = :type_id")
        params["type_id"] = type_id
    if op_id:
        where.append("l.operator_id = :op_id")
        params["op_id"] = op_id

    where_clause = " AND ".join(where)

    try:
        with db.engine.connect() as conn:
            total = conn.execute(
                text(f"""
                    SELECT COUNT(*) FROM locomotives l
                    LEFT JOIN classes c ON c.id = l.class_id
                    WHERE {where_clause}
                """), params
            ).scalar() or 0

            offset = (page - 1) * per_page
            params["limit"]  = per_page
            params["offset"] = offset

            locomotives = conn.execute(
                text(f"""
                    SELECT
                        l.id, l.number, l.name, l.status, l.livery, l.image,
                        c.name  AS class_name,
                        t.name  AS type_name,
                        o.name  AS operator_name,
                        co.name AS country_name,
                        (SELECT COUNT(*) FROM sightings s WHERE s.locomotive_id = l.id) AS sighting_count,
                        (SELECT COUNT(*) FROM sightings s WHERE s.locomotive_id = l.id AND s.is_cop = 1) AS is_copped
                    FROM locomotives l
                    LEFT JOIN classes   c  ON c.id   = l.class_id
                    LEFT JOIN types     t  ON t.id   = l.type_id
                    LEFT JOIN operators o  ON o.id   = l.operator_id
                    LEFT JOIN countries co ON co.code = l.country_code
                    WHERE {where_clause}
                    ORDER BY l.number
                    LIMIT :limit OFFSET :offset
                """), params
            ).mappings().all()

            lookups = _get_lookups()

        return render_template(
            "locomotives.html",
            locomotives=locomotives,
            total=total,
            page=page,
            per_page=per_page,
            pages=(total + per_page - 1) // per_page,
            search=search,
            status=status,
            type_id=type_id,
            op_id=op_id,
            **lookups,
        )
    except Exception as e:
        current_app.logger.exception("locomotive index error")
        flash("Error loading locomotives.", "danger")
        return render_template("locomotives.html", locomotives=[], total=0, page=1, pages=1,
                               classes=[], operators=[], depots=[], types=[], countries=[])


@locomotive_bp.route("/<int:loco_id>")
def detail(loco_id):
    try:
        with db.engine.connect() as conn:
            loco = conn.execute(
                text("""
                    SELECT
                        l.*,
                        c.name  AS class_name,
                        t.name  AS type_name,
                        o.name  AS operator_name,
                        d.name  AS depot_name,
                        co.name AS country_name
                    FROM locomotives l
                    LEFT JOIN classes   c  ON c.id   = l.class_id
                    LEFT JOIN types     t  ON t.id   = l.type_id
                    LEFT JOIN operators o  ON o.id   = l.operator_id
                    LEFT JOIN depots    d  ON d.id   = l.depot_id
                    LEFT JOIN countries co ON co.code = l.country_code
                    WHERE l.id = :id
                """), {"id": loco_id}
            ).mappings().first()

            if not loco:
                flash("Locomotive not found.", "warning")
                return redirect(url_for("locomotive.index"))

            sightings = conn.execute(
                text("""
                    SELECT
                        s.*,
                        loc.name  AS location_name,
                        l2.number AS hauled_by_number
                    FROM sightings s
                    LEFT JOIN locations   loc ON loc.id = s.location_id
                    LEFT JOIN locomotives l2  ON l2.id  = s.hauled_by
                    WHERE s.locomotive_id = :id
                    ORDER BY s.sighting_date DESC, s.sighting_time DESC
                """), {"id": loco_id}
            ).mappings().all()

        return render_template("locomotive_detail.html", loco=loco, sightings=sightings)

    except Exception:
        current_app.logger.exception("locomotive detail error")
        flash("Error loading locomotive.", "danger")
        return redirect(url_for("locomotive.index"))


@locomotive_bp.route("/add", methods=["GET", "POST"])
def add():
    lookups = _get_lookups()

    if request.method == "POST":
        number   = request.form.get("number", "").strip()
        name     = request.form.get("name", "").strip() or None
        class_id = request.form.get("class_id") or None
        type_id  = request.form.get("type_id") or None
        op_id    = request.form.get("operator_id") or None
        depot_id = request.form.get("depot_id") or None
        livery   = request.form.get("livery", "").strip() or None
        built    = request.form.get("built_year") or None
        status   = request.form.get("status", "active")
        country  = request.form.get("country_code") or None
        notes    = request.form.get("notes", "").strip() or None

        if not number:
            flash("Locomotive number is required.", "danger")
            return render_template("locomotive_add.html", **lookups)

        try:
            with db.engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO locomotives
                            (number, name, class_id, type_id, operator_id, depot_id,
                             livery, built_year, status, country_code, notes)
                        VALUES
                            (:number, :name, :class_id, :type_id, :op_id, :depot_id,
                             :livery, :built, :status, :country, :notes)
                    """),
                    {
                        "number": number, "name": name, "class_id": class_id,
                        "type_id": type_id, "op_id": op_id, "depot_id": depot_id,
                        "livery": livery, "built": built, "status": status,
                        "country": country, "notes": notes,
                    }
                )
            flash(f"Locomotive {number} added.", "success")
            return redirect(url_for("locomotive.index"))
        except Exception as e:
            current_app.logger.exception("add locomotive error")
            flash(f"Error adding locomotive: {e}", "danger")

    return render_template("locomotive_add.html", **lookups)


@locomotive_bp.route("/<int:loco_id>/edit", methods=["GET", "POST"])
def edit(loco_id):
    lookups = _get_lookups()

    try:
        with db.engine.connect() as conn:
            loco = conn.execute(
                text("SELECT * FROM locomotives WHERE id = :id"), {"id": loco_id}
            ).mappings().first()

        if not loco:
            flash("Locomotive not found.", "warning")
            return redirect(url_for("locomotive.index"))

        if request.method == "POST":
            number   = request.form.get("number", "").strip()
            name     = request.form.get("name", "").strip() or None
            class_id = request.form.get("class_id") or None
            type_id  = request.form.get("type_id") or None
            op_id    = request.form.get("operator_id") or None
            depot_id = request.form.get("depot_id") or None
            livery   = request.form.get("livery", "").strip() or None
            built    = request.form.get("built_year") or None
            status   = request.form.get("status", "active")
            country  = request.form.get("country_code") or None
            notes    = request.form.get("notes", "").strip() or None

            if not number:
                flash("Locomotive number is required.", "danger")
                return render_template("locomotive_edit.html", loco=loco, **lookups)

            with db.engine.begin() as conn:
                conn.execute(
                    text("""
                        UPDATE locomotives SET
                            number=:number, name=:name, class_id=:class_id,
                            type_id=:type_id, operator_id=:op_id, depot_id=:depot_id,
                            livery=:livery, built_year=:built, status=:status,
                            country_code=:country, notes=:notes
                        WHERE id=:id
                    """),
                    {
                        "number": number, "name": name, "class_id": class_id,
                        "type_id": type_id, "op_id": op_id, "depot_id": depot_id,
                        "livery": livery, "built": built, "status": status,
                        "country": country, "notes": notes, "id": loco_id,
                    }
                )
            flash(f"Locomotive {number} updated.", "success")
            return redirect(url_for("locomotive.detail", loco_id=loco_id))

        return render_template("locomotive_edit.html", loco=loco, **lookups)

    except Exception:
        current_app.logger.exception("edit locomotive error")
        flash("Error updating locomotive.", "danger")
        return redirect(url_for("locomotive.index"))


@locomotive_bp.route("/<int:loco_id>/delete", methods=["POST"])
def delete(loco_id):
    try:
        with db.engine.begin() as conn:
            loco = conn.execute(
                text("SELECT number FROM locomotives WHERE id = :id"), {"id": loco_id}
            ).mappings().first()
            if loco:
                conn.execute(text("DELETE FROM locomotives WHERE id = :id"), {"id": loco_id})
                flash(f"Locomotive {loco['number']} deleted.", "success")
    except Exception:
        current_app.logger.exception("delete locomotive error")
        flash("Error deleting locomotive.", "danger")
    return redirect(url_for("locomotive.index"))


@locomotive_bp.route("/search_json")
def search_json():
    """JSON endpoint for autocomplete."""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    try:
        with db.engine.connect() as conn:
            rows = conn.execute(
                text("""
                    SELECT id, number, name, status
                    FROM locomotives
                    WHERE number LIKE :q OR name LIKE :q
                    ORDER BY number LIMIT 20
                """), {"q": f"%{q}%"}
            ).mappings().all()
        return jsonify([dict(r) for r in rows])
    except Exception:
        return jsonify([])
