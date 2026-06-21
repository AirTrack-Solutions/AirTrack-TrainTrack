"""
region_profile.py — TrainTrack Railway Region Profile Loader

Loads region profile JSON files from app/data/region_profiles/.
Provides validated profile dicts for UI label rendering, import alias
resolution, and status mapping.

Usage:
    from utils.region_profile import load_profile, get_active_profile, list_profiles

    profile = get_active_profile()          # respects app_settings if in Flask context
    profile = load_profile("UK")            # explicit load by code
    codes   = list_profiles()               # ["AU", "CUSTOM", "DE", "FR", "NZ", "UK", "USA"]

Fallback chain:
    requested code → AU → CUSTOM → ProfileLoadError (only if all three fail)

Active profile source (in order of precedence):
    1. app_settings row  SettingKey='region_profile'  (if in Flask app context)
    2. DEFAULT_PROFILE_CODE ("AU")
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_PROFILE_CODE = "AU"
FALLBACK_PROFILE_CODE = "CUSTOM"
APP_SETTINGS_KEY = "region_profile"

REQUIRED_KEYS = {
    "region_code",
    "region_name",
    "version",
    "labels",
    "import_aliases",
    "status_map",
    "identity_strategy",
    "optional_fields",
    "cop_term",
    "dub_term",
    "notes",
}

# ---------------------------------------------------------------------------
# Profile directory resolution
# ---------------------------------------------------------------------------

def _profile_dir() -> Path:
    """
    Resolve the region_profiles directory regardless of working directory.

    Tries (in order):
      1. Path relative to this file:  <this_file>/../../data/region_profiles/
      2. Environment override:        TRAINTRACK_PROFILE_DIR
      3. Container default:           /app/data/region_profiles/
    """
    env_override = os.getenv("TRAINTRACK_PROFILE_DIR")
    if env_override:
        return Path(env_override)

    # Path relative to this file: app/utils/ → app/data/region_profiles/
    relative = Path(__file__).resolve().parent.parent / "data" / "region_profiles"
    if relative.is_dir():
        return relative

    # Container fallback
    return Path("/app/data/region_profiles")


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ProfileLoadError(Exception):
    """Raised only when both AU and CUSTOM fallback profiles are unavailable."""


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def list_profiles() -> list[str]:
    """
    Return sorted list of available profile codes (filenames without .json).
    Returns empty list rather than raising if the directory is missing.
    """
    profile_dir = _profile_dir()
    if not profile_dir.is_dir():
        log.warning("Region profile directory not found: %s", profile_dir)
        return []
    return sorted(p.stem for p in profile_dir.glob("*.json"))


def validate_profile(profile: dict) -> tuple[bool, list[str]]:
    """
    Check that a loaded profile dict contains all required top-level keys.

    Returns:
        (True, [])                    — profile is valid
        (False, [list of missing keys]) — profile is missing required keys
    """
    missing = [k for k in REQUIRED_KEYS if k not in profile]
    return (len(missing) == 0), missing


def load_profile(code: str) -> dict:
    """
    Load and validate the profile for the given region code.

    Falls back to AU, then CUSTOM if the requested profile is missing or invalid.
    Raises ProfileLoadError only if AU and CUSTOM are both unavailable.

    Args:
        code: Region code string, e.g. "AU", "UK", "DE". Case-insensitive.

    Returns:
        Validated profile dict.
    """
    code = code.upper().strip()
    profile_dir = _profile_dir()

    def _try_load(c: str) -> Optional[dict]:
        path = profile_dir / f"{c}.json"
        if not path.exists():
            log.warning("Profile file not found: %s", path)
            return None
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Could not read profile %s: %s", c, exc)
            return None
        valid, missing = validate_profile(data)
        if not valid:
            log.warning(
                "Profile %s is missing required keys: %s", c, missing
            )
            return None
        return data

    # 1. Try the requested code
    if code not in (DEFAULT_PROFILE_CODE, FALLBACK_PROFILE_CODE):
        result = _try_load(code)
        if result:
            return result
        log.warning(
            "Profile '%s' unavailable — falling back to %s",
            code, DEFAULT_PROFILE_CODE,
        )

    # 2. Try AU
    if code != FALLBACK_PROFILE_CODE:
        result = _try_load(DEFAULT_PROFILE_CODE)
        if result:
            if code != DEFAULT_PROFILE_CODE:
                result = dict(result)  # don't mutate cached copy
                result["_fallback_from"] = code
            return result
        log.warning(
            "Default profile %s unavailable — falling back to %s",
            DEFAULT_PROFILE_CODE, FALLBACK_PROFILE_CODE,
        )

    # 3. Try CUSTOM
    result = _try_load(FALLBACK_PROFILE_CODE)
    if result:
        result = dict(result)
        result["_fallback_from"] = code
        return result

    # 4. Give up
    raise ProfileLoadError(
        f"Cannot load profile '{code}' and neither fallback ({DEFAULT_PROFILE_CODE}, "
        f"{FALLBACK_PROFILE_CODE}) is available. Check {profile_dir}."
    )


def get_active_profile() -> dict:
    """
    Load the currently configured region profile.

    Resolution order:
      1. SettingKey='region_profile' in app_settings (if inside a Flask app context)
      2. DEFAULT_PROFILE_CODE ("AU")

    Never raises — falls back gracefully through load_profile()'s own fallback chain.
    """
    code = DEFAULT_PROFILE_CODE

    # Try to read from app_settings if we're inside a Flask request/app context.
    # Import lazily to avoid circular imports and to allow this module to be used
    # standalone (e.g. python3 -m app.utils.region_profile).
    try:
        from flask import has_app_context
        from sqlalchemy import text
        from extensions import db

        if has_app_context():
            with db.engine.connect() as conn:
                row = conn.execute(
                    text(
                        "SELECT SettingValue FROM app_settings "
                        "WHERE SettingKey = :key LIMIT 1"
                    ),
                    {"key": APP_SETTINGS_KEY},
                ).fetchone()
                if row and row[0]:
                    code = row[0].upper().strip()
    except Exception as exc:
        # DB unavailable, not in app context, or app_settings row absent —
        # all fine, just use the default.
        log.debug("get_active_profile: using default (%s). Reason: %s", code, exc)

    try:
        return load_profile(code)
    except ProfileLoadError:
        log.error(
            "get_active_profile: all fallbacks exhausted for code '%s'. "
            "Check app/data/region_profiles/.",
            code,
        )
        # Return a minimal safe dict so callers don't crash on missing keys.
        return _emergency_profile(code)


def _emergency_profile(code: str) -> dict:
    """
    Last-resort profile returned when even CUSTOM cannot be loaded.
    Contains bare-minimum structure so callers don't KeyError.
    This should never appear in normal operation.
    """
    log.critical(
        "Returning emergency profile — region_profiles directory may be missing or corrupt."
    )
    return {
        "region_code":       "EMERGENCY",
        "region_name":       "Emergency Fallback",
        "version":           0,
        "labels":            {
            "locomotive": "Unit", "number": "Number", "class": "Class",
            "operator": "Operator", "owner": "Owner", "depot": "Depot",
            "formation": "Formation", "carriage": "Carriage", "wagon": "Wagon",
            "multiple_unit": "Multiple Unit", "livery": "Livery",
            "builder": "Builder", "year_built": "Year Built", "status": "Status",
            "previous_number": "Previous Number", "reporting_mark": "Mark",
        },
        "import_aliases":    {},
        "status_map":        {},
        "identity_strategy": {"primary_key": "road_number", "secondary_key": None, "format_hint": ""},
        "optional_fields":   {},
        "cop_term":          "cop",
        "dub_term":          "dub",
        "notes":             f"Emergency fallback. Original code: {code}",
        "_emergency":        True,
    }


# ---------------------------------------------------------------------------
# Convenience helpers (reserved for Step 5 / Step 6 — stubs only)
# ---------------------------------------------------------------------------

# def resolve_import_header(header: str, profile: dict) -> Optional[str]:
#     """Map an import CSV column header to an internal field name."""
#     ...
#
# def map_status(value: str, profile: dict) -> str:
#     """Map a status string from import data to a TrainTrack ENUM value."""
#     ...


# ---------------------------------------------------------------------------
# Standalone test  (python3 -m app.utils.region_profile)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    codes = list_profiles()
    print(f"\nAvailable profiles ({len(codes)}): {codes}")

    print(f"\nDefault active profile (no DB context): {DEFAULT_PROFILE_CODE}")
    try:
        active = load_profile(DEFAULT_PROFILE_CODE)
        print(f"  → Loaded: {active['region_name']} (v{active['version']})")
    except ProfileLoadError as exc:
        print(f"  ✗ {exc}", file=sys.stderr)

    print("\nAll profiles:")
    errors = []
    for code in codes:
        try:
            p = load_profile(code)
            pk = p["identity_strategy"]["primary_key"]
            sk = p["identity_strategy"].get("secondary_key") or "—"
            status_count = len(p["status_map"])
            print(
                f"  {code:<8}  {p['region_name']:<35}  "
                f"pk={pk:<12}  sk={sk:<12}  {status_count:>2} status entries"
            )
        except ProfileLoadError as exc:
            errors.append((code, str(exc)))
            print(f"  {code:<8}  ✗ {exc}")

    if errors:
        print(f"\n✗ {len(errors)} profile(s) failed to load.", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\n✓ All {len(codes)} profiles loaded and validated.")
