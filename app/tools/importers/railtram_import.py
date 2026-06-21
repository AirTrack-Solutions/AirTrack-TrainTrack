#!/usr/bin/env python3
"""
railtram_import.py  —  Import Iguana Phase 1C
Reads a canonical Railtram AU seed JSON and safely imports records into TrainTrack.

Default mode is dry-run.  Pass --apply to write to the database.

Usage (inside container):
    python3 /app/tools/importers/railtram_import.py \
        --seed /app/research/data_pack_samples/australia/railtram/railtram_au_seed_2026-06-22.json \
        [--apply] [--include-flagged] [--limit N] [--verbose]

Rules:
    - No deletes.
    - No overwriting user-entered fields: notes, image, livery, status, depot_id.
    - Locomotives existing in DB: only class_id updated, and only if currently NULL.
    - Operators/classes created on demand (--apply) or reported (dry-run).
    - Flagged records skipped by default; pass --include-flagged to process them.
    - Parse-failure records in seed are never imported (flagged at seed-build time).

DB connection:
    Reads DB_USER, DB_PASSWORD, DB_HOST, DB_NAME from environment.
    Defaults: host=traintrack-db, name=traintrack.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    import pymysql
    import pymysql.cursors
except ImportError:
    print("ERROR: pymysql not installed. Run: pip install pymysql", file=sys.stderr)
    sys.exit(2)

# ---------------------------------------------------------------------------
# Reuse validator (same directory)
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from railtram_seed_validate import validate as _validate_seed  # noqa: E402


# ---------------------------------------------------------------------------
# DB connection
# ---------------------------------------------------------------------------

def _connect() -> pymysql.Connection:
    host   = os.getenv("DB_HOST", "traintrack-db")
    user   = os.getenv("DB_USER", "")
    passwd = os.getenv("DB_PASSWORD", "")
    name   = os.getenv("DB_NAME", "traintrack")
    if not user or not passwd:
        print(
            "ERROR: DB_USER and DB_PASSWORD environment variables must be set.",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=passwd,
            database=name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
        return conn
    except pymysql.Error as exc:
        print(f"ERROR: Cannot connect to database ({host}/{name}): {exc}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# Operator helpers
# ---------------------------------------------------------------------------

def _load_operators(cur) -> dict[str, int]:
    """Return {code: id} for all operators with a non-null code."""
    cur.execute("SELECT id, code FROM operators WHERE code IS NOT NULL")
    return {row["code"]: row["id"] for row in cur.fetchall()}


def _create_operator(cur, name: str, code: str, country_code: str) -> int:
    cur.execute(
        "INSERT INTO operators (name, code, country_code, type) VALUES (%s, %s, %s, 'other')",
        (name, code, country_code),
    )
    return cur.lastrowid


# ---------------------------------------------------------------------------
# Class helpers
# ---------------------------------------------------------------------------

def _load_classes(cur) -> dict[str, int]:
    """Return {name_lower: id} for all classes."""
    cur.execute("SELECT id, name FROM classes")
    return {row["name"].lower(): row["id"] for row in cur.fetchall()}


def _create_class(cur, name: str, country_code: str) -> int:
    cur.execute(
        "INSERT INTO classes (name, country_code) VALUES (%s, %s)",
        (name, country_code),
    )
    return cur.lastrowid


# ---------------------------------------------------------------------------
# Locomotive helpers
# ---------------------------------------------------------------------------

def _load_locos(cur, country_code: str) -> dict[tuple, dict]:
    """
    Return {(country_code, operator_id, number): row_dict} for the target country.
    Fetches only the fields we care about for conflict detection.
    """
    cur.execute(
        """
        SELECT id, number, operator_id, class_id, country_code,
               notes, image, livery, status, depot_id
        FROM   locomotives
        WHERE  country_code = %s
        """,
        (country_code,),
    )
    return {
        (row["country_code"], row["operator_id"], row["number"]): row
        for row in cur.fetchall()
    }


def _create_loco(cur, number: str, operator_id: int, class_id, country_code: str) -> int:
    cur.execute(
        """
        INSERT INTO locomotives (number, operator_id, class_id, country_code, status)
        VALUES (%s, %s, %s, %s, 'active')
        """,
        (number, operator_id, class_id, country_code),
    )
    return cur.lastrowid


def _update_loco_class(cur, loco_id: int, class_id: int) -> None:
    """Set class_id only when it is currently NULL."""
    cur.execute(
        "UPDATE locomotives SET class_id = %s WHERE id = %s AND class_id IS NULL",
        (class_id, loco_id),
    )


# ---------------------------------------------------------------------------
# Main import logic
# ---------------------------------------------------------------------------

def run_import(
    seed_path: str,
    apply: bool,
    include_flagged: bool,
    limit,
    verbose: bool,
) -> int:
    """
    Execute the import (or dry-run).
    Returns exit code: 0 = success/clean dry-run, 1 = errors encountered.
    """
    W = 72

    # ------------------------------------------------------------------
    # 1. Validate seed
    # ------------------------------------------------------------------
    errors, warnings, info = _validate_seed(seed_path)
    print("=" * W)
    print(" Railtram AU Seed Importer  (Import Iguana Phase 1C)")
    mode_label = "APPLY" if apply else "DRY-RUN"
    print(f" Mode: {mode_label}")
    print("=" * W)
    print(f"  Seed file :  {seed_path}")
    print(f"  Source    :  {info.get('source_name', '?')}")
    print(f"  Accessed  :  {info.get('accessed_at', '?')}")
    print(f"  Records   :  {info.get('record_count', '?')}")
    print(f"  Rev flags :  {info.get('review_flag_count', '?')}")
    print()

    if errors:
        print("SEED VALIDATION FAILED " + "─" * (W - 24))
        for e in errors:
            print(f"  x  {e}")
        print()
        print("Aborting -- fix seed errors before importing.")
        return 1

    if warnings:
        for w in warnings:
            print(f"  !  {w}")
        print()

    # ------------------------------------------------------------------
    # 2. Load seed
    # ------------------------------------------------------------------
    seed      = json.loads(Path(seed_path).read_text(encoding="utf-8"))
    records   = seed.get("records", [])
    rev_flags = seed.get("review_flags", [])

    if limit is not None:
        records = records[:limit]
        print(f"  Limit: processing first {limit} records only.")
        print()

    # Partition flagged vs clean
    flagged_recs = [r for r in records if r.get("flags")]
    clean_recs   = [r for r in records if not r.get("flags")]

    work_recs = records if include_flagged else clean_recs

    print(f"  Clean records    : {len(clean_recs)}")
    print(f"  Flagged records  : {len(flagged_recs)}"
          + (" (will be processed -- --include-flagged)" if include_flagged else " (skipping)"))
    print(f"  Working set      : {len(work_recs)}")
    print()

    # ------------------------------------------------------------------
    # 3. Connect to DB
    # ------------------------------------------------------------------
    conn = _connect()
    cur  = conn.cursor()

    # ------------------------------------------------------------------
    # 4. Pre-flight: verify country code exists in DB
    # ------------------------------------------------------------------
    seed_cc = seed.get("source", {}).get("country_code", "AU")
    cur.execute("SELECT code FROM countries WHERE code = %s", (seed_cc,))
    cc_in_db = cur.fetchone() is not None
    if not cc_in_db:
        if apply:
            # Hard stop — do not write with NULL country_code; idempotency breaks.
            conn.close()
            print(f"ERROR: country_code '{seed_cc}' is not present in the countries table.")
            print(f"       Seed the country before applying the import:")
            print(f"         INSERT INTO countries (code, name) VALUES ('{seed_cc}', '<name>');")
            print(f"       Then re-run with --apply.")
            print()
            return 1
        else:
            print(f"  WARNING: country code '{seed_cc}' not found in countries table.")
            print(f"           In --apply mode this would be a hard stop.")
            print(f"           Add '{seed_cc}' to countries before running --apply.")
            print()
    resolved_cc = seed_cc if cc_in_db else None

    # ------------------------------------------------------------------
    # 5. Load current DB state
    # ------------------------------------------------------------------
    op_map    = _load_operators(cur)    # code -> id
    class_map = _load_classes(cur)      # name.lower() -> id
    loco_map  = _load_locos(cur, "AU")  # (cc, op_id, num) -> row

    # ------------------------------------------------------------------
    # 5. Plan pass
    # ------------------------------------------------------------------
    ops_found     = {}   # code -> existing_id
    ops_to_create = {}   # code -> (name, code, cc)
    cls_found     = {}   # name.lower() -> existing_id
    cls_to_create = {}   # name.lower() -> name

    locos_existing  = []  # exist in DB, no change
    locos_to_create = []  # new
    locos_to_update = []  # class_id fill-in
    locos_skipped   = []  # exist, no update needed
    row_errors      = []

    for rec in work_recs:
        op_code  = rec.get("operator_code", "")
        op_name  = rec.get("operator", "")
        cls_name = rec.get("class", "")
        number   = rec.get("number", "")
        cc       = rec.get("country_code", "AU")

        # --- operator ---
        if op_code in op_map:
            ops_found[op_code] = op_map[op_code]
            resolved_op_id = op_map[op_code]
        elif op_code in ops_to_create:
            resolved_op_id = -1  # new, real id unknown at plan time
        else:
            ops_to_create[op_code] = (op_name, op_code, cc)  # cc resolved at apply time
            resolved_op_id = -1

        # --- class ---
        cls_key = cls_name.lower()
        if cls_key in class_map:
            cls_found[cls_key] = class_map[cls_key]
            resolved_cls_id = class_map[cls_key]
        elif cls_key in cls_to_create:
            resolved_cls_id = -1
        else:
            cls_to_create[cls_key] = cls_name
            resolved_cls_id = -1

        # --- locomotive ---
        if resolved_op_id != -1:
            loco_key = (cc, resolved_op_id, number)
            existing = loco_map.get(loco_key)
            if existing:
                if existing["class_id"] is None and resolved_cls_id not in (-1, None):
                    locos_to_update.append({
                        "id":       existing["id"],
                        "number":   number,
                        "op_code":  op_code,
                        "cls_name": cls_name,
                        "cc":       cc,
                        "cls_id":   resolved_cls_id,
                    })
                else:
                    locos_skipped.append({
                        "number":   number,
                        "op_code":  op_code,
                        "cls_name": cls_name,
                        "reason":   "already exists, no update needed",
                    })
            else:
                locos_to_create.append({
                    "number":   number,
                    "op_code":  op_code,
                    "op_name":  op_name,
                    "cls_name": cls_name,
                    "cc":       cc,
                    "cls_id":   resolved_cls_id,
                })
        else:
            # Operator is new -> loco is definitely new
            locos_to_create.append({
                "number":   number,
                "op_code":  op_code,
                "op_name":  op_name,
                "cls_name": cls_name,
                "cc":       cc,
                "cls_id":   resolved_cls_id,
            })

    # ------------------------------------------------------------------
    # 6. Print plan
    # ------------------------------------------------------------------
    print("OPERATORS " + "-" * (W - 11))
    print(f"  Found in DB       : {len(ops_found)}")
    print(f"  To create         : {len(ops_to_create)}")
    if ops_to_create:
        for code, (name, _, _) in sorted(ops_to_create.items()):
            print(f"    + [{code}] {name}")
    print()

    print("CLASSES " + "-" * (W - 9))
    print(f"  Found in DB       : {len(cls_found)}")
    print(f"  To create         : {len(cls_to_create)}")
    if cls_to_create:
        sample = list(cls_to_create.values())
        if verbose:
            for cn in sorted(sample):
                print(f"    + {cn}")
        else:
            shown = sample[:5]
            print("    (first {}): {}{}".format(
                min(5, len(shown)), ", ".join(shown),
                "  ..." if len(cls_to_create) > 5 else ""
            ))
    print()

    print("LOCOMOTIVES " + "-" * (W - 13))
    print(f"  Existing (no change)  : {len(locos_skipped)}")
    print(f"  Existing (class fill) : {len(locos_to_update)}")
    print(f"  To create             : {len(locos_to_create)}")
    print(f"  Errors                : {len(row_errors)}")

    if verbose and locos_to_update:
        print()
        print("  Class fill-in candidates:")
        for lu in locos_to_update[:20]:
            print(f"    id={lu['id']} [{lu['op_code']}] {lu['number']} -> class={lu['cls_name']}")
        if len(locos_to_update) > 20:
            print(f"    ... and {len(locos_to_update) - 20} more")

    if verbose and locos_to_create:
        print()
        print("  New locomotives (first 20):")
        for lc in locos_to_create[:20]:
            print(f"    [{lc['op_code']}] {lc['number']} | class={lc['cls_name']}")
        if len(locos_to_create) > 20:
            print(f"    ... and {len(locos_to_create) - 20} more")
    print()

    if flagged_recs and not include_flagged:
        print("FLAGGED (SKIPPED) " + "-" * (W - 19))
        print(f"  {len(flagged_recs)} record(s) skipped due to flags:")
        for fr in flagged_recs[:10]:
            print(f"    [{fr['operator_code']}] {fr['number']} -- {fr['flags']}")
        if len(flagged_recs) > 10:
            print(f"    ... and {len(flagged_recs) - 10} more")
        print()

    if rev_flags:
        print("SEED REVIEW FLAGS " + "-" * (W - 19))
        for rf in rev_flags[:5]:
            print("  ! row {} [{}] {} -- {}".format(
                rf.get("source_row_index", "?"),
                rf.get("operator_code", "?"),
                rf.get("class_name", "?"),
                rf.get("flag", "?"),
            ))
        if len(rev_flags) > 5:
            print(f"  ... and {len(rev_flags) - 5} more")
        print()

    if row_errors:
        print("ERRORS " + "-" * (W - 8))
        for e in row_errors:
            print(f"  x  {e}")
        print()

    # ------------------------------------------------------------------
    # 7. Dry-run exit
    # ------------------------------------------------------------------
    if not apply:
        print("-" * W)
        print(" DRY-RUN COMPLETE -- no changes written.")
        print(" Run with --apply to execute the import.")
        print("-" * W)
        conn.close()
        return 0

    # ------------------------------------------------------------------
    # 8. Apply -- operators first
    # ------------------------------------------------------------------
    print("APPLYING " + "-" * (W - 10))
    created_ops   = {}
    created_cls   = {}
    created_locos = 0
    updated_locos = 0
    apply_errors  = []

    for code, (name, _, cc) in ops_to_create.items():
        try:
            new_id = _create_operator(cur, name, code, resolved_cc)
            created_ops[code] = new_id
            op_map[code] = new_id
            if verbose:
                print(f"  + Operator [{code}] {name}  -> id={new_id}")
        except pymysql.Error as exc:
            apply_errors.append(f"Operator [{code}] create failed: {exc}")

    # ------------------------------------------------------------------
    # 9. Apply -- classes
    # ------------------------------------------------------------------
    for cls_key, cls_name in cls_to_create.items():
        try:
            new_id = _create_class(cur, cls_name, resolved_cc)
            created_cls[cls_key] = new_id
            class_map[cls_key] = new_id
            if verbose:
                print(f"  + Class {cls_name}  -> id={new_id}")
        except pymysql.Error as exc:
            apply_errors.append(f"Class [{cls_name}] create failed: {exc}")

    # ------------------------------------------------------------------
    # 10. Apply -- class fill-ins on existing locos
    # ------------------------------------------------------------------
    for lu in locos_to_update:
        try:
            _update_loco_class(cur, lu["id"], lu["cls_id"])
            updated_locos += 1
            if verbose:
                print(f"  ~ Loco id={lu['id']} [{lu['op_code']}] {lu['number']}"
                      f" class_id -> {lu['cls_id']}")
        except pymysql.Error as exc:
            apply_errors.append(
                f"Loco update id={lu['id']} [{lu['op_code']}] {lu['number']}: {exc}"
            )

    # ------------------------------------------------------------------
    # 11. Apply -- new locomotives
    # ------------------------------------------------------------------
    for lc in locos_to_create:
        op_code  = lc["op_code"]
        cls_name = lc["cls_name"]
        number   = lc["number"]
        cc       = lc["cc"]

        op_id = op_map.get(op_code)
        if op_id is None:
            apply_errors.append(
                f"Loco [{op_code}] {number}: operator not in DB after create -- skipping"
            )
            continue

        cls_key = cls_name.lower()
        cls_id  = class_map.get(cls_key)  # None is fine

        try:
            _create_loco(cur, number, op_id, cls_id, resolved_cc)
            created_locos += 1
            if verbose:
                print(f"  + Loco [{op_code}] {number} (class={cls_name})")
        except pymysql.Error as exc:
            if exc.args[0] == 1062:
                if verbose:
                    print(f"  ~ Loco [{op_code}] {number} already exists (dup) -- skipped")
            else:
                apply_errors.append(f"Loco [{op_code}] {number}: {exc}")

    # ------------------------------------------------------------------
    # 12. Commit or rollback
    # ------------------------------------------------------------------
    if apply_errors:
        conn.rollback()
        print()
        print("ERRORS DURING APPLY -- ROLLED BACK " + "-" * (W - 36))
        for e in apply_errors:
            print(f"  x  {e}")
        print()
        conn.close()
        return 1

    conn.commit()
    conn.close()

    # ------------------------------------------------------------------
    # 13. Apply summary
    # ------------------------------------------------------------------
    print()
    print("APPLY SUMMARY " + "-" * (W - 15))
    print(f"  Operators created    : {len(created_ops)}")
    print(f"  Classes created      : {len(created_cls)}")
    print(f"  Locomotives created  : {created_locos}")
    print(f"  Locomotives updated  : {updated_locos}  (class_id fill-in)")
    print(f"  Locomotives skipped  : {len(locos_skipped)}")
    print()
    print("  OK  Import complete. All changes committed.")
    print()
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _default_seed() -> str:
    return (
        "/app/research/data_pack_samples/australia/railtram/"
        "railtram_au_seed_2026-06-22.json"
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Railtram AU seed DB importer -- Import Iguana Phase 1C",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Default mode is DRY-RUN.  Pass --apply to write to the database.\n"
            "Always review dry-run output before applying."
        ),
    )
    ap.add_argument(
        "--seed", default=_default_seed(),
        help="Path to railtram_au_seed_*.json",
    )
    ap.add_argument(
        "--apply", action="store_true",
        help="Write to the database (default: dry-run only)",
    )
    ap.add_argument(
        "--dry-run", action="store_true", default=True,
        help="Dry-run (default). Explicit flag for clarity.",
    )
    ap.add_argument(
        "--include-flagged", action="store_true",
        help="Process records with seed flags (default: skip them)",
    )
    ap.add_argument(
        "--limit", type=int, default=None, metavar="N",
        help="Process only the first N records",
    )
    ap.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show per-record detail",
    )
    args = ap.parse_args()

    sys.exit(
        run_import(
            seed_path=args.seed,
            apply=args.apply,
            include_flagged=args.include_flagged,
            limit=args.limit,
            verbose=args.verbose,
        )
    )


if __name__ == "__main__":
    main()
