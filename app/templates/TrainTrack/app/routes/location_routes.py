# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/location_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from sqlalchemy import text
from extensions import db

location_bp = Blueprint("location", __name__, url_prefix="/locations")


@location_bp.route("/")
def index():
    search = request.args.get("q", "").strip()
    where  = ["1=1"]
    params = {}

    if search:
        where.append("(l.name LIKE :q OR l.station_code LIKE :q OR l.line LIKE :q)")
        params["q"] = f"%{search}%"

    try:
        with db.engine.connect() as conn:
            locations = conn.execute(
                text(f"""
                    SELECT l.*, co.name AS country_name,
                        (SELECT COUNT(*) FROM sightings s WHERE s.location_id = l.id) AS sighting_count
                    FROM locations l
                    LEFT JOIN countries co ON co.code = l.country_code
                    WHERE {" AND ".join(where)}
                    ORDER BY l.name
                """), params
            ).mappings().all()
        return render_template("locations.html", locations=locations, search=search)
    except Exception:
        current_app.logger.exception("locations index error")
        flash("Error loading locations.", "danger")
        return render_template("locations.html", locations=[], search="")


@location_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        code    = request.form.get("station_code", "").strip() or None
        line    = request.form.get("line", "").strip() or None
        country = request.form.get("country_code") or None
        lat     = request.form.get("lat") or None
        lng     = request.form.get("lng") or None
        notes   = request.form.get("notes", "").strip() or None

        if not name:
            flash("Location name is required.", "danger")
            return render_template("location_add.html")

        try:
            with db.engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO locations (name, station_code, line, country_code, lat, lng, notes)
                        VALUES (:name, :code, :line, :country, :lat, :lng, :notes)
                    """),
                    {"name": name, "code": code, "line": line, "country": country,
                     "lat": lat, "lng": lng, "notes": notes}
                )
            flash(f"{name} added.", "success")
            return redirect(url_for("location.index"))
        except Exception as e:
            current_app.logger.exception("add location error")
            flash(f"Error: {e}", "danger")

    with db.engine.connect() as conn:
        countries = conn.execute(text("SELECT code, name FROM countries ORDER BY name")).mappings().all()
    return render_template("location_add.html", countries=list(countries))


@location_bp.route("/<int:loc_id>/delete", methods=["POST"])
def delete(loc_id):
    try:
        with db.engine.begin() as conn:
            loc = conn.execute(
                text("SELECT name FROM locations WHERE id = :id"), {"id": loc_id}
            ).mappings().first()
            if loc:
                conn.execute(text("DELETE FROM locations WHERE id = :id"), {"id": loc_id})
                flash(f"{loc['name']} deleted.", "success")
    except Exception:
        flash("Error deleting location.", "danger")
    return redirect(url_for("location.index"))
