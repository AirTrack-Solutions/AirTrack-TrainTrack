# TrainTrack 1.0.0 "Stephenson" — Release 1
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# wsgi.py — gunicorn entry point
from app import app

if __name__ == "__main__":
    app.run()
