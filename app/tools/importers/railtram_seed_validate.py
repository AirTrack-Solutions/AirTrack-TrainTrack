#!/usr/bin/env python3
"""
railtram_seed_validate.py  —  Import Iguana Phase 1B
Validates a canonical Railtram seed JSON file produced by railtram_seed_builder.py.

No database connection. No writes. No side effects.

Usage:
    python3 railtram_seed_validate.py <seed_file>

Exit codes:
    0  — validation passed (warnings are informational only)
    1  — validation failed (errors found)
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# Required fields on every record
# ---------------------------------------------------------------------------

REQUIRED_RECORD_FIELDS = {
    "country_code",
    "operator_code",
    "operator",
    "class",
    "number",
    "source_expression",
    "source_row_index",
    "status",
    "flags",
}


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

def validate(seed_path: str) -> tuple[list[str], list[str], dict]:
    """Validate the seed file.

    Returns (errors, warnings, info_dict).
    errors   — hard failures that must be fixed before import
    warnings — informational, do not block import
    info_dict — summary counts for display
    """
    errors: list[str] = []
    warnings: list[str] = []

    # --- 1. File readable and valid JSON ---
    path = Path(seed_path)
    if not path.exists():
        return [f"File not found: {seed_path}"], [], {}

    try:
        seed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON parse error: {exc}"], [], {}

    if not isinstance(seed, dict):
        return ["Seed root is not a JSON object"], [], {}

    # --- 2. source block exists and has required keys ---
    source = seed.get("source")
    if not source or not isinstance(source, dict):
        errors.append("Missing or invalid 'source' block")
    else:
        for key in ("name", "url", "accessed_at", "region_profile",
                    "country_code", "generated_by"):
            if key not in source:
                errors.append(f"source block missing field: '{key}'")

    # --- 3. summary block exists ---
    summary = seed.get("summary")
    if not summary or not isinstance(summary, dict):
        errors.append("Missing or invalid 'summary' block")

    # --- 4. records array exists and is non-empty ---
    records = seed.get("records")
    if records is None:
        errors.append("Missing 'records' array")
        records = []
    elif not isinstance(records, list):
        errors.append("'records' is not an array")
        records = []
    elif len(records) == 0:
        errors.append("'records' array is empty")

    # --- 5. review_flags array exists ---
    review_flags = seed.get("review_flags")
    if review_flags is None:
        errors.append("Missing 'review_flags' array")
        review_flags = []
    elif not isinstance(review_flags, list):
        errors.append("'review_flags' is not an array")
        review_flags = []

    # --- 6. Per-record field validation ---
    missing_fields_count = 0
    null_required_count  = 0
    field_errors_sample: list[str] = []

    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            errors.append(f"Record {i} is not a JSON object")
            continue
        for field in REQUIRED_RECORD_FIELDS:
            if field not in rec:
                missing_fields_count += 1
                if len(field_errors_sample) < 5:
                    field_errors_sample.append(
                        f"Record {i} missing field '{field}' "
                        f"(number={rec.get('number', '?')}, op={rec.get('operator_code', '?')})"
                    )
        # status may be null — that is valid
        # number must be a non-empty string
        n = rec.get("number")
        if not n or not isinstance(n, str):
            null_required_count += 1
            if len(field_errors_sample) < 5:
                field_errors_sample.append(
                    f"Record {i} has null/empty 'number' field"
                )

    if missing_fields_count:
        errors.append(
            f"{missing_fields_count} missing required field(s) across records"
        )
        errors.extend(field_errors_sample)

    if null_required_count:
        errors.append(
            f"{null_required_count} record(s) with null/empty 'number' field"
        )

    # --- 7. Duplicate identity check within same operator ---
    identity_count: dict[tuple, int] = defaultdict(int)
    for rec in records:
        cc  = rec.get("country_code", "")
        op  = rec.get("operator_code", "")
        num = rec.get("number", "")
        if cc and op and num:
            identity_count[(cc, op, num)] += 1

    dup_identities = {k: v for k, v in identity_count.items() if v > 1}
    if dup_identities:
        errors.append(
            f"{len(dup_identities)} duplicate identity/identities found "
            f"(country_code + operator_code + number must be unique within a seed)"
        )
        for (cc, op, num), count in list(dup_identities.items())[:5]:
            errors.append(
                f"  Duplicate: {cc} / {op} / {num}  ({count}×)"
            )

    # --- 8. Cross-operator shared numbers (informational) ---
    number_to_ops: dict[str, set] = defaultdict(set)
    for rec in records:
        num = rec.get("number")
        op  = rec.get("operator_code")
        if num and op:
            number_to_ops[num].add(op)

    cross_op = {n: sorted(ops) for n, ops in number_to_ops.items()
                if len(ops) > 1}
    if cross_op:
        warnings.append(
            f"{len(cross_op)} number(s) shared across operators "
            f"(allowed by schema — informational)"
        )

    # --- 9. Record count matches summary ---
    if summary and isinstance(summary, dict):
        declared_count = summary.get("records")
        if declared_count is not None and declared_count != len(records):
            errors.append(
                f"summary.records={declared_count} but actual record count={len(records)}"
            )

    # --- 10. Source row count matches summary ---
    if summary and isinstance(summary, dict):
        declared_rows = summary.get("source_rows")
        if declared_rows is not None:
            # We can't re-run the parser here, so trust the declared count
            # but check it is a positive integer
            if not isinstance(declared_rows, int) or declared_rows <= 0:
                errors.append(
                    f"summary.source_rows is not a positive integer: {declared_rows!r}"
                )

    # Build info dict for display
    info = {
        "file":                 seed_path,
        "source_name":          (source or {}).get("name", "?"),
        "accessed_at":          (source or {}).get("accessed_at", "?"),
        "country_code":         (source or {}).get("country_code", "?"),
        "source_rows":          (summary or {}).get("source_rows", "?"),
        "record_count":         len(records),
        "review_flag_count":    len(review_flags),
        "cross_op_shared":      len(cross_op),
        "errors":               len(errors),
        "warnings":             len(warnings),
    }

    return errors, warnings, info


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Railtram seed validator — Import Iguana Phase 1B"
    )
    ap.add_argument("seed_file", help="Path to railtram_au_seed_*.json")
    ap.add_argument(
        "--first-records", type=int, default=5,
        help="Number of records to show in output (default: 5)"
    )
    args = ap.parse_args()

    errors, warnings, info = validate(args.seed_file)

    W = 72
    print("=" * W)
    print(" Railtram Seed Validator  (Import Iguana Phase 1B)")
    print("=" * W)
    print(f"  File:          {info.get('file', '?')}")
    print(f"  Source:        {info.get('source_name', '?')}")
    print(f"  Accessed:      {info.get('accessed_at', '?')}")
    print(f"  Country:       {info.get('country_code', '?')}")
    print()
    print(f"  Source rows:   {info.get('source_rows', '?')}")
    print(f"  Records:       {info.get('record_count', '?')}")
    print(f"  Review flags:  {info.get('review_flag_count', '?')}")
    print(f"  Cross-op nums: {info.get('cross_op_shared', '?')}  (informational)")
    print()

    if warnings:
        print("WARNINGS " + "─" * (W - 10))
        for w in warnings:
            print(f"  ⚠  {w}")
        print()

    if errors:
        print("ERRORS " + "─" * (W - 8))
        for e in errors:
            print(f"  ✗  {e}")
        print()

    # Show sample records
    if not errors:
        try:
            seed = json.loads(Path(args.seed_file).read_text(encoding="utf-8"))
            records = seed.get("records", [])
            n = min(args.first_records, len(records))
            if n > 0:
                print(f"FIRST {n} RECORDS " + "─" * (W - len(f"FIRST {n} RECORDS ") - 1))
                for rec in records[:n]:
                    flag_str = f"  flags={rec['flags']}" if rec.get("flags") else ""
                    print(
                        f"  [{rec['country_code']}|{rec['operator_code']:<10}|{rec['class']:<22}]"
                        f"  {rec['number']:<16} row={rec['source_row_index']}{flag_str}"
                    )
                print()
        except Exception:
            pass  # display is best-effort

    # Verdict
    print("VERDICT " + "─" * (W - 9))
    if errors:
        n_err = info.get("errors", len(errors))
        print(f"  ✗  FAILED — {n_err} error(s).  Seed is not import-ready.")
        sys.exit(1)
    else:
        print("  ✓  PASSED — seed is structurally valid and import-ready.")
    print()


if __name__ == "__main__":
    main()
