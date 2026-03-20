# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/reports_routes.py

from flask import Blueprint, render_template, current_app
from sqlalchemy import text
from extensions import db

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/")
def index():
    try:
        with db.engine.connect() as conn:
            # Overall stats
            total_locos     = conn.execute(text("SELECT COUNT(*) FROM locomotives")).scalar() or 0
            total_sightings = conn.execute(text("SELECT COUNT(*) FROM sightings")).scalar() or 0
            total_cops      = conn.execute(text("SELECT COUNT(*) FROM sightings WHERE is_cop = 1")).scalar() or 0
            total_dubs      = total_sightings - total_cops
            total_formations = conn.execute(text("SELECT COUNT(*) FROM formations")).scalar() or 0

            # Cops list — first sighting of each loco
            cops = conn.execute(
                text("""
                    SELECT
                        s.cop_date,
                        l.number AS loco_number,
                        l.name   AS loco_name,
                        c.name   AS class_name,
                        loc.name AS location_name
                    FROM sightings s
                    JOIN locomotives l ON l.id = s.locomotive_id
                    LEFT JOIN classes   c   ON c.id   = l.class_id
                    LEFT JOIN locations loc ON loc.id = s.location_id
                    WHERE s.is_cop = 1
                    ORDER BY s.cop_date DESC
                    LIMIT 20
                """)
            ).mappings().all()

            # Most seen locations
            top_locations = conn.execute(
                text("""
                    SELECT loc.name, COUNT(*) AS cnt
                    FROM sightings s
                    JOIN locations loc ON loc.id = s.location_id
                    GROUP BY loc.id, loc.name
                    ORDER BY cnt DESC
                    LIMIT 10
                """)
            ).mappings().all()

            # Most seen operators
            top_operators = conn.execute(
                text("""
                    SELECT o.name, COUNT(*) AS cnt
                    FROM sightings s
                    JOIN locomotives l ON l.id = s.locomotive_id
                    JOIN operators   o ON o.id = l.operator_id
                    GROUP BY o.id, o.name
                    ORDER BY cnt DESC
                    LIMIT 10
                """)
            ).mappings().all()

            # Sightings by type
            by_type = conn.execute(
                text("""
                    SELECT t.name, COUNT(*) AS cnt
                    FROM sightings s
                    JOIN locomotives l ON l.id = s.locomotive_id
                    JOIN types       t ON t.id = l.type_id
                    GROUP BY t.id, t.name
                    ORDER BY cnt DESC
                """)
            ).mappings().all()

            # Sightings by month (last 12 months)
            by_month = conn.execute(
                text("""
                    SELECT DATE_FORMAT(sighting_date, '%Y-%m') AS month, COUNT(*) AS cnt
                    FROM sightings
                    WHERE sighting_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
                    GROUP BY month
                    ORDER BY month ASC
                """)
            ).mappings().all()

        return render_template(
            "reports.html",
            total_locos=total_locos,
            total_sightings=total_sightings,
            total_cops=total_cops,
            total_dubs=total_dubs,
            total_formations=total_formations,
            cops=cops,
            top_locations=top_locations,
            top_operators=top_operators,
            by_type=by_type,
            by_month=by_month,
        )
    except Exception:
        current_app.logger.exception("reports error")
        return render_template("reports.html",
                               total_locos=0, total_sightings=0, total_cops=0,
                               total_dubs=0, total_formations=0,
                               cops=[], top_locations=[], top_operators=[],
                               by_type=[], by_month=[])


@reports_bp.route("/cops")
def cops_list():
    """Full cops list."""
    try:
        with db.engine.connect() as conn:
            cops = conn.execute(
                text("""
                    SELECT
                        s.cop_date, s.sighting_date,
                        l.number AS loco_number,
                        l.name   AS loco_name,
                        c.name   AS class_name,
                        t.name   AS type_name,
                        o.name   AS operator_name,
                        loc.name AS location_name
                    FROM sightings s
                    JOIN locomotives l ON l.id = s.locomotive_id
                    LEFT JOIN classes   c   ON c.id   = l.class_id
                    LEFT JOIN types     t   ON t.id   = l.type_id
                    LEFT JOIN operators o   ON o.id   = l.operator_id
                    LEFT JOIN locations loc ON loc.id = s.location_id
                    WHERE s.is_cop = 1
                    ORDER BY s.cop_date DESC
                """)
            ).mappings().all()
        return render_template("cops_list.html", cops=cops)
    except Exception:
        current_app.logger.exception("cops list error")
        return render_template("cops_list.html", cops=[])


@reports_bp.route("/needscops")
def needs_cops():
    """Locomotives never seen — the wanted list."""
    try:
        with db.engine.connect() as conn:
            unseen = conn.execute(
                text("""
                    SELECT
                        l.id, l.number, l.name, l.status,
                        c.name AS class_name,
                        t.name AS type_name,
                        o.name AS operator_name
                    FROM locomotives l
                    LEFT JOIN classes   c ON c.id = l.class_id
                    LEFT JOIN types     t ON t.id = l.type_id
                    LEFT JOIN operators o ON o.id = l.operator_id
                    WHERE l.id NOT IN (
                        SELECT DISTINCT locomotive_id FROM sightings
                        WHERE locomotive_id IS NOT NULL
                    )
                    ORDER BY l.number
                """)
            ).mappings().all()
        return render_template("needs_cops.html", unseen=unseen)
    except Exception:
        current_app.logger.exception("needs cops error")
        return render_template("needs_cops.html", unseen=[])
