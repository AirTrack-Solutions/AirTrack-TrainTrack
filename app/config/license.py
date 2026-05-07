# TrainTrack 1.0.0 'Stephenson' — Release 1
# Copyright (c) 2025 Trevor ('Subhuti'). All rights reserved.
# SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

# config/license.py
# Reads license.lic from app/config/ and exposes edition and license info.

import json

import logging

import os

from pathlib import Path

# Edition hierarchy — higher index = more features
EDITIONS = ['lite', 'TTP', 'TTF']

# Product code to friendly name
EDITION_NAMES = {
    'lite': 'Lite',
    'TTP': 'Personal',
    'TTF': 'Professional',
}

# Features available per edition
EDITION_FEATURES = {
    'lite': {
        'locomotive_log':       True,
        'sighting_history':     True,
        'basic_search':         True,
        'formations':           False,
        'reports':              False,
        'photo_logging':        False,
        'drivers_cab':          False,
        'maintenance_tools':    False,
        'export':               False,
    },
    'TTP': {
        'locomotive_log':       True,
        'sighting_history':     True,
        'basic_search':         True,
        'formations':           True,
        'reports':              True,
        'photo_logging':        True,
        'drivers_cab':          True,
        'maintenance_tools':    True,
        'export':               True,
    },
    'TTF': {
        'locomotive_log':       True,
        'sighting_history':     True,
        'basic_search':         True,
        'formations':           True,
        'reports':              True,
        'photo_logging':        True,
        'drivers_cab':          True,
        'maintenance_tools':    True,
        'export':               True,
    },
}

# Activations allowed per edition
EDITION_ACTIVATIONS = {
    'lite':  1,
    'TTP':   2,
    'TTF':  10,
}


class TrainTrackLicense:
    def __init__(self, edition='lite', license_id=None, name=None, issued=None):
        self.edition      = edition.lower() if edition else 'lite'
        self.license_id   = license_id or 'UNLICENSED'
        self.name         = name or 'Unknown'
        self.issued       = issued or ''
        self.features     = EDITION_FEATURES.get(self.edition, EDITION_FEATURES['lite'])
        self.activations  = EDITION_ACTIVATIONS.get(self.edition, 1)
        self.edition_name = EDITION_NAMES.get(self.edition, 'Lite')

    def has_feature(self, feature: str) -> bool:
        return bool(self.features.get(feature, False))

    def is_at_least(self, edition: str) -> bool:
        try:
            return EDITIONS.index(self.edition) >= EDITIONS.index(edition.lower())
        except ValueError:
            return False

    def __repr__(self):
        return f'<TrainTrackLicense {self.license_id} edition={self.edition}>'


def load_license() -> TrainTrackLicense:
    """
    Load license.lic from app/config/license.lic.
    Falls back to 'lite' if not found or invalid.
    TRAINTRACK_EDITION env var can override for development.
    """
    # Developer override via env (never shipped to users)
    env_edition = os.getenv('TRAINTRACK_EDITION', '').strip().lower()
    if env_edition in EDITIONS:
        logging.info(f'🔑 License: edition overridden by TRAINTRACK_EDITION={env_edition}')
        return TrainTrackLicense(edition=env_edition, license_id='ENV-OVERRIDE', name='Environment')

    # Look for license.lic relative to this file's location
    config_dir = Path(__file__).resolve().parent
    lic_path = config_dir / 'license.lic'

    if not lic_path.exists():
        logging.warning(f'⚠️  No license.lic found at {lic_path} — defaulting to lite edition.')
        return TrainTrackLicense()

    try:
        data = json.loads(lic_path.read_text(encoding='utf-8'))
        edition    = data.get('edition', 'lite')
        license_id = data.get('license_id', 'UNKNOWN')
        name       = data.get('name', 'Unknown')
        issued     = data.get('issued', '')

        if edition not in EDITIONS:
            logging.warning(f'⚠️  Unknown edition \'{edition}\' in license.lic — defaulting to lite.')
            edition = 'lite'

        lic = TrainTrackLicense(edition=edition, license_id=license_id, name=name, issued=issued)
        logging.info(f'🔑 License loaded: {lic}')
        return lic

    except Exception as e:
        logging.error(f'❌ Failed to load license.lic: {e} — defaulting to lite.')
        return TrainTrackLicense()
