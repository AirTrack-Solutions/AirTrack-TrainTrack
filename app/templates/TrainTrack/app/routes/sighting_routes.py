# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/sighting_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from sqlalchemy import text
from extensions import db
from datetime import date

sighting_bp = Blueprint("sighting", __name__, url_prefix="/sightings")


def _get_lookups():
    with db.engine.connect() as conn:
        locomotives = conn.execute(
            text("SELECT id, number, name FROM locomotives ORDER BY number")
        ).mappings().all()
        formations = conn.execute(
            text("SELECT id, set_number FROM formations ORDER BY set_number")
        ).mappings().all()
        locations = conn.execute(
            text("SELECT id, name FROM locations ORDER BY name")
        ).mappings().all()
    return {
        "locomotives": list(locomotives),
        "formations":  list(formations),
        "locations":   list(locations),
    }


def _is_cop(conn, locomotive_id=None, formation_id=None) -> tuple[bool, str | None]:
    """
    Check if this is the first ever sighting of a locomotive or formation.
    Returns (is_cop: bool, cop_date: str | None)
    """
    if locomotive_id:
        existing = conn.execute(
            text("SELECT sighting_date FROM sightings WHERE locomotive_id = :id AND is_cop = 1 LIMIT 1"),
            {"id": locomotive_id}
        ).fetchone()
    elif formation_id:
        existing = conn.execute(
            text("SELECT sighting_date FROM sightings WHERE formation_id = :id AND is_cop = 1 LIMIT 1"),
            {"id": formation_id}
        ).fetchone()
    else:
        return False, None

    if existing:
        # Already copped — this is a dub
        return False, str(existing[0])
    else:
        # First ever sighting — it's a cop
        return True, str(date.today())


@sighting_bp.route("/")
def index():
    page     = max(1, int(request.args.get("page", 1)))
    per_page = 50
    cops_only = request.args.get("cops", "") == "1"
    search   = request.args.get("q", "").strip()

    where  = ["1=1"]
    params = {}

    if cops_only:
        where.append("s.is_cop = 1")
    if search:
        where.append("(l.number LIKE :q OR f.set_number LIKE :q OR loc.name LIKE :q)")
        params["q"] = f"%{search}%"

    where_clause = " AND ".join(where)

    try:
        with db.engine.connect() as conn:
            total = conn.execute(
                text(f"""
                    SELECT COUNT(*) FROM sightings s
                    LEFT JOIN locomotives l   ON l.id   = s.locomotive_id
                    LEFT JOIN formations  f   ON f.id   = s.formation_id
                    LEFT JOIN locations   loc ON loc.id = s.location_id
                    WHERE {where_clause}
                """), params
            ).scalar() or 0

            offset = (page - 1) * per_page
            params["limit"]  = per_page
            params["offset"] = offset

            sightings = conn.execute(
                text(f"""
                    SELECT
                        s.id, s.sighting_date, s.sighting_time,
                        s.working, s.direction, s.is_cop, s.notes,
                        l.number    AS loco_number,
                        l.name      AS loco_name,
                        f.set_number AS formation_number,
                        loc.name    AS location_name
                    FROM sightings s
                    LEFT JOIN locomotives l   ON l.id   = s.locomotive_id
                    LEFT JOIN formations  f   ON f.id   = s.formation_id
                    LEFT JOIN locations   loc ON loc.id = s.location_id
                    WHERE {where_clause}
                    ORDER BY s.sighting_date DESC, s.sighting_time DESC
                    LIMIT :limit OFFSET :offset
                """), params
            ).mappings().all()

        return render_template(
            "sightings.html",
            sightings=sightings,
            total=total,
            page=page,
            per_page=per_page,
            pages=(total + per_page - 1) // per_page,
            cops_only=cops_only,
            search=search,
        )
    except Exception:
        current_app.logger.exception("sightings index error")
        flash("Error loading sightings.", "danger")
        return render_template("sightings.html", sightings=[], total=0, page=1, pages=1,
                               cops_only=False, search="")


@sighting_bp.route("/log", methods=["GET", "POST"])
def log():
    """Log a new sighting."""
    lookups = _get_lookups()

    if request.method == "POST":
        subject    = request.form.get("subject_type", "locomotive")  # locomotive | formation
        loco_id    = request.form.get("locomotive_id") or None
        form_id    = request.form.get("formation_id") or None
        sight_date = request.form.get("sighting_date") or str(date.today())
        sight_time = request.form.get("sighting_time") or None
        loc_id     = request.form.get("location_id") or None
        working    = request.form.get("working", "").strip() or None
        direction  = request.form.get("direction", "").strip() or None
        hauled_by  = request.form.get("hauled_by") or None
        notes      = request.form.get("notes", "").strip() or None

        # Validate subject
        if subject == "locomotive" and not loco_id:
            flash("Select a locomotive.", "danger")
            return render_template("sighting_log.html", **lookups)
        if subject == "formation" and not form_id:
            flash("Select a formation.", "danger")
            return render_template("sighting_log.html", **lookups)

        # Clear the unused subject
        if subject == "locomotive":
            form_id = None
        else:
            loco_id = None

        try:
            with db.engine.begin() as conn:
                is_cop, cop_date = _is_cop(
                    conn,
                    locomotive_id=int(loco_id) if loco_id else None,
                    formation_id=int(form_id) if form_id else None,
                )

                conn.execute(
                    text("""
                        INSERT INTO sightings
                            (locomotive_id, formation_id, sighting_date, sighting_time,
                             location_id, working, direction, hauled_by, notes, is_cop, cop_date)
                        VALUES
                            (:loco_id, :form_id, :sight_date, :sight_time,
                             :loc_id, :working, :direction, :hauled_by, :notes, :is_cop, :cop_date)
                    """),
                    {
                        "loco_id": loco_id, "form_id": form_id,
                        "sight_date": sight_date, "sight_time": sight_time,
                        "loc_id": loc_id, "working": working, "direction": direction,
                        "hauled_by": hauled_by, "notes": notes,
                        "is_cop": 1 if is_cop else 0, "cop_date": cop_date,
                    }
                )

            result = "🚂 COP!" if is_cop else "Dub logged."
            flash(f"Sighting logged. {result}", "success")
            return redirect(url_for("sighting.index"))

        except Exception as e:
            current_app.logger.exception("log sighting error")
            flash(f"Error logging sighting: {e}", "danger")

    return render_template("sighting_log.html", **lookups)


@sighting_bp.route("/<int:sighting_id>/delete", methods=["POST"])
def delete(sighting_id):
    try:
        with db.engine.begin() as conn:
            conn.execute(text("DELETE FROM sightings WHERE id = :id"), {"id": sighting_id})
        flash("Sighting deleted.", "success")
    except Exception:
        current_app.logger.exception("delete sighting error")
        flash("Error deleting sighting.", "danger")
    return redirect(url_for("sighting.index"))
