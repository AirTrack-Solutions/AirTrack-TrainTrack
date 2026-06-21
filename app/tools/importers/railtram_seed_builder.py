#!/usr/bin/env python3
"""
railtram_seed_builder.py  —  Import Iguana Phase 1B
Converts Iguana's row-centric parser output into a unit-centric canonical
seed JSON suitable for future DB import.

No database connection. No writes. No side effects.

Usage:
    python3 railtram_seed_builder.py <input_file> [--accessed-at DATE]
    python3 railtram_seed_builder.py \\
        research/data_pack_samples/australia/railtram/railtram_number_index_2026-06-22.txt \\
        > research/data_pack_samples/australia/railtram/railtram_au_seed_2026-06-22.json

Input:  raw Railtram number index text (Chrome-rendered, saved as .txt)
Output: canonical seed JSON written to stdout
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Import parser from Phase 1A (same directory)
sys.path.insert(0, str(Path(__file__).parent))
from railtram_preview import parse_file, build_preview  # noqa: E402


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SOURCE_NAME    = "Railtram Locomotive Number Index"
SOURCE_URL     = "https://www.railtram.com.au/locomotive-number-indexes"
COUNTRY_CODE   = "AU"
REGION_PROFILE = "AU"

# Flags that propagate to individual unit records (all others stay in review_flags only)
_UNIT_LEVEL_FLAG_PREFIXES = (
    "CLASS NOT ON CLASSES PAGE",
    "UNKNOWN OPERATOR",
)

# Flags that indicate a row produced no usable expansion
_EXPANSION_FAILURE_PREFIXES = (
    "Cannot parse range start",
    "Cannot parse range end",
    "Prefix mismatch in range",
    "Suffix mismatch in range",
    "End < start in range",
    "UNRESOLVED ROW",
)


# ---------------------------------------------------------------------------
# Core builder
# ---------------------------------------------------------------------------

def build_seed(input_path: str, accessed_at: str | None = None) -> dict:
    """Parse the raw index text and produce the canonical seed structure."""

    if accessed_at is None:
        accessed_at = date.today().isoformat()

    text = Path(input_path).read_text(encoding="utf-8")
    numeric_rows, letter_rows = parse_file(text)
    preview = build_preview(numeric_rows, letter_rows, input_path)

    records: list[dict] = []
    review_flags: list[dict] = []
    seen_identities: set[tuple] = set()   # (country_code, operator_code, number)

    for row in preview["rows"]:
        op_code  = row["operator_code"]
        op_full  = row["operator_full"]
        cls      = row["class_name"]
        expr     = row["road_nums_expr"]
        section  = row["section"]
        row_idx  = row["row"]
        expanded = row["expanded"]
        flags    = row["flags"]

        # Collect all flags from this row into review_flags (with context)
        for flag in flags:
            review_flags.append({
                "source_row_index": row_idx,
                "section":          section,
                "operator_code":    op_code,
                "class_name":       cls,
                "road_nums_expr":   expr,
                "flag":             flag,
            })

        if not expanded:
            # Expansion produced nothing (parse failure or unresolved row) —
            # flags are already in review_flags; no records to emit.
            continue

        # Unit-level flags: only propagate flags that are meaningful per unit
        unit_flags = [
            f for f in flags
            if any(f.startswith(pfx) for pfx in _UNIT_LEVEL_FLAG_PREFIXES)
        ]

        for number in expanded:
            identity = (COUNTRY_CODE, op_code, number)

            if identity in seen_identities:
                # Deduplicate: note it, skip the second occurrence
                review_flags.append({
                    "source_row_index": row_idx,
                    "section":          section,
                    "operator_code":    op_code,
                    "class_name":       cls,
                    "road_nums_expr":   expr,
                    "flag":             (
                        f"DEDUPLICATED: '{number}' for operator '{op_code}' "
                        f"already emitted from an earlier source row — skipped"
                    ),
                })
                continue

            seen_identities.add(identity)
            records.append({
                "country_code":     COUNTRY_CODE,
                "operator_code":    op_code,
                "operator":         op_full,
                "class":            cls,
                "number":           number,
                "source_expression": expr,
                "source_row_index": row_idx,
                "status":           None,
                "flags":            unit_flags[:],   # copy so each record is independent
            })

    # Build summary (cross-op counts come from preview directly)
    summary = {
        "source_rows":                  preview["total_rows"],
        "records":                      len(records),
        "review_flags":                 len(review_flags),
        "cross_operator_shared_numbers": preview["cross_operator_shared_count"],
    }

    seed = {
        "source": {
            "name":          SOURCE_NAME,
            "url":           SOURCE_URL,
            "accessed_at":   accessed_at,
            "region_profile": REGION_PROFILE,
            "country_code":  COUNTRY_CODE,
            "generated_by":  "railtram_seed_builder.py",
        },
        "summary": summary,
        "records": records,
        "review_flags": review_flags,
    }

    return seed


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Railtram canonical seed builder — Import Iguana Phase 1B"
    )
    ap.add_argument("input_file", help="Path to extracted Railtram number index text")
    ap.add_argument(
        "--accessed-at",
        default=None,
        help="Override accessed_at date in seed (YYYY-MM-DD). Defaults to today.",
    )
    args = ap.parse_args()

    path = Path(args.input_file)
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    seed = build_seed(str(path), accessed_at=args.accessed_at)
    print(json.dumps(seed, indent=2))


if __name__ == "__main__":
    main()
