# TrainTrack 1.0.0
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# routes/main_routes.py

from flask import Blueprint, render_template
from sqlalchemy import text
from extensions import db

main_bp = Blueprint("main", __name__)


def _get_stats() -> dict:
    try:
        with db.engine.connect() as conn:
            locomotives    = conn.execute(text("SELECT COUNT(*) FROM locomotives")).scalar() or 0
            sightings      = conn.execute(text("SELECT COUNT(*) FROM sightings")).scalar() or 0
            cops           = conn.execute(text("SELECT COUNT(*) FROM sightings WHERE is_cop = 1")).scalar() or 0
            formations     = conn.execute(text("SELECT COUNT(*) FROM formations")).scalar() or 0
            operators      = conn.execute(text("SELECT COUNT(*) FROM operators")).scalar() or 0
            locations      = conn.execute(text("SELECT COUNT(*) FROM locations")).scalar() or 0
            return {
                "locomotives": locomotives,
                "sightings":   sightings,
                "cops":        cops,
                "dubs":        sightings - cops,
                "formations":  formations,
                "operators":   operators,
                "locations":   locations,
            }
    except Exception:
        return {
            "locomotives": 0, "sightings": 0, "cops": 0,
            "dubs": 0, "formations": 0, "operators": 0, "locations": 0,
        }


@main_bp.route("/")
def dashboard():
    stats = _get_stats()
    return render_template("dashboard.html", stats=stats)
