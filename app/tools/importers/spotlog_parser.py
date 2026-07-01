"""
SpotLog UK Locomotive Parser
============================
Reads SpotLog HTML class page snapshots and loads staging records into TrainTrack DB.

Usage (dry-run — default):
    python3 spotlog_parser.py --snapshot /path/to/GB_spotlog_class_66_20260627.html --class 66

Usage (apply to DB):
    python3 spotlog_parser.py --snapshot /path/to/GB_spotlog_class_66_20260627.html --class 66 --apply

Usage (multiple snapshots):
    python3 spotlog_parser.py --apply \
        --snapshot GB_spotlog_class_66_20260627.html --class 66 \
        --snapshot GB_spotlog_class_37_20260627.html --class 37

Flags:
    --apply             Write to DB (default: dry-run, prints summary only)
    --verbose           Print every row parsed
    --report            Write JSON reports to ./staging_reports/
    --report-dir DIR    Override report output directory

Rules:
    - No canonical promotion (promoted=0 always)
    - status_text, operator_name, depot_name always NULL (unresolved)
    - raw_source_payload stored for every row
    - Duplicate staging_id: UPDATE only if row hash changed, skip if identical
"""

import argparse
import hashlib
import html
import json
import os
import re
import sys
from datetime import datetime, timezone

try:
    import pymysql
except ImportError:
    print("ERROR: pymysql not installed. Run: pip install pymysql")
    sys.exit(1)

# ─── Constants ────────────────────────────────────────────────────────────────

SOURCE_NAME  = "spotlog"
COUNTRY_CODE = "GB"
CONFIDENCE   = "enthusiast"
BASE_URL     = "https://spotlog.org/locolist/class/UK/{class_name}"

# ─── Lookup tables ───────────────────────────────────────────────────────────

LOOKUPS_DIR = os.path.join(os.path.dirname(__file__), "lookups")

def _load_lookup(filename):
    """Load a lookup JSON from the lookups directory. Returns {} on failure."""
    path = os.path.join(LOOKUPS_DIR, filename)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def _lookup_version(data):
    """Extract version string from a lookup's _meta section."""
    meta = data.get("_meta", {})
    return meta.get("version", "unknown")

def load_pool_lookup():
    data = _load_lookup("pool_codes.json")
    codes = {k: v for k, v in data.items() if isinstance(v, dict) and k != "_meta"}
    return codes, _lookup_version(data)

def load_depot_lookup():
    data = _load_lookup("depot_codes.json")
    return data.get("codes", {}), _lookup_version(data)

def load_status_lookup():
    data = _load_lookup("status_codes.json")
    return data.get("codes", {}), _lookup_version(data)

def resolve_status(status_code, status_lookup, status_ver="unknown", mode="safe"):
    """Return (status_text, source, version, confidence) tuple."""
    key = status_code if status_code else "(blank)"
    if key not in status_lookup:
        return None, None, None, None
    entry = status_lookup[key]
    confidence = entry.get("confidence", "unresolved")
    is_confirmed = confidence == "confirmed"
    is_inferred  = confidence == "inferred"
    if is_confirmed:
        return entry.get("status_text"), "status_lookup", status_ver, "confirmed"
    if is_inferred and mode == "review":
        val = entry.get("status_text")
        return (f"{val} [inferred]" if val else None), "status_lookup", status_ver, "inferred"
    return None, None, None, None

def resolve_pool(pool_code, pool_lookup, pool_ver="unknown", mode="safe"):
    """Return (operator_name, source, version, confidence) tuple."""
    if not pool_code or pool_code not in pool_lookup:
        return None, None, None, None
    entry = pool_lookup[pool_code]
    confidence = entry.get("confidence", "unresolved")
    is_confirmed = confidence in ("confirmed", "rcts_confirmed")
    is_inferred  = confidence == "inferred"
    if is_confirmed:
        val = entry.get("operator_canonical") or entry.get("operator_name") or entry.get("operator") or None
        return val, "pool_lookup", pool_ver, "confirmed"
    if is_inferred and mode == "review":
        val = entry.get("operator_canonical") or entry.get("operator_name") or entry.get("operator") or None
        return (f"{val} [inferred]" if val else None), "pool_lookup", pool_ver, "inferred"
    return None, None, None, None

def resolve_depot(depot_code, depot_lookup, depot_ver="unknown", mode="safe"):
    """Return (depot_name, source, version, confidence) tuple."""
    if not depot_code or depot_code not in depot_lookup:
        return None, None, None, None
    entry = depot_lookup[depot_code]
    confidence = entry.get("confidence", "unresolved")
    is_confirmed = confidence in ("confirmed", "rcts_confirmed")
    is_inferred  = confidence == "inferred"
    if is_confirmed:
        val = entry.get("depot_name") or None
        return val, "depot_lookup", depot_ver, "confirmed"
    if is_inferred and mode == "review":
        val = entry.get("depot_name") or None
        return (f"{val} [inferred]" if val else None), "depot_lookup", depot_ver, "inferred"
    return None, None, None, None

# ─── DB connection ────────────────────────────────────────────────────────────

def get_db():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "traintrack-db"),
        user=os.environ.get("DB_USER", "traintrack"),
        password=os.environ.get("DB_PASSWORD", "ofTrainTrack"),
        database=os.environ.get("DB_NAME", "traintrack"),
        charset="utf8mb4",
        autocommit=False,
    )

# ─── Helpers ─────────────────────────────────────────────────────────────────

def clean(text):
    return html.unescape(text).strip()

def row_hash(raw_tr):
    normalised = re.sub(r'\s+', ' ', raw_tr).strip()
    return hashlib.sha256(normalised.encode()).hexdigest()[:16]

def cells_from_row(tr_html):
    raw_cells = re.findall(r'<td[^>]*>(.*?)</td>', tr_html, re.DOTALL)
    return [clean(re.sub(r'<[^>]+>', '', c)) for c in raw_cells]

def resolve_number(vehicle_number):
    if re.match(r'^\d{5,6}$', vehicle_number):
        return vehicle_number, "obvious"
    if vehicle_number.startswith('D') or re.match(r'^\d{1,4}$', vehicle_number):
        return None, "ambiguous"
    return None, "unresolved"

def class_sid(class_name):
    return f"{COUNTRY_CODE}:{SOURCE_NAME}:{class_name}"

def vehicle_sid(class_name, vehicle_number):
    return f"{COUNTRY_CODE}:{SOURCE_NAME}:{class_name}:{vehicle_number}"

# ─── Parse one class page ────────────────────────────────────────────────────

def parse_page(class_name, filepath, source_url, pool_lookup=None, depot_lookup=None, status_lookup=None, pool_ver="unknown", depot_ver="unknown", status_ver="unknown", lookup_mode="safe"):
    with open(filepath, encoding='utf-8', errors='replace') as f:
        page_html = f.read()

    retrieved_at = datetime.fromtimestamp(
        os.path.getmtime(filepath), tz=timezone.utc
    ).strftime('%Y-%m-%d %H:%M:%S')

    tables = re.findall(r'<table.*?</table>', page_html, re.DOTALL)
    if len(tables) < 2:
        return None, [], {"error": f"Expected 2 tables, found {len(tables)}"}

    # Class spec
    spec_rows = re.findall(r'<tr>(.*?)</tr>', tables[0], re.DOTALL)
    spec_dict = {}
    for row in spec_rows:
        c = cells_from_row(row)
        if len(c) >= 2 and c[0]:
            spec_dict[c[0]] = c[1]

    staging_class = {
        "staging_class_id":  class_sid(class_name),
        "source_name":       SOURCE_NAME,
        "source_url":        source_url,
        "country_code":      COUNTRY_CODE,
        "class_name":        class_name,
        "builder":           spec_dict.get("Builder"),
        "max_speed":         spec_dict.get("Max Speed"),
        "introduced":        spec_dict.get("Introduced"),
        "spec_json":         json.dumps(spec_dict, ensure_ascii=False),
        "raw_row_hash":      hashlib.sha256(
                                 json.dumps(spec_dict, sort_keys=True).encode()
                             ).hexdigest()[:16],
        "raw_source_payload": tables[0],
        "retrieved_at":      retrieved_at,
    }

    # Vehicle rows
    all_rows  = re.findall(r'<tr>(.*?)</tr>', tables[1], re.DOTALL)
    data_rows = all_rows[1:]  # row 0 is blank header

    vehicles     = []
    duplicates   = []
    seen_ids     = {}
    warnings     = []
    pool_codes   = {}
    status_codes = {}
    depot_codes  = {}
    alt_report   = []
    name_report  = []

    for tr in data_rows:
        c = cells_from_row(tr)
        if not any(c):
            continue

        warning = None
        if len(c) != 7:
            warning = f"Expected 7 cells, got {len(c)}"
            c = (c + [''] * 7)[:7]

        vehicle_number = c[0]
        alt_number_raw = c[1] or None
        name_raw       = c[2] or None
        status_code    = c[3] or None
        pool_code      = c[4] or None
        depot_code     = c[5] or None
        notes          = c[6] or None

        if not vehicle_number:
            continue

        candidate, resolution = resolve_number(vehicle_number)
        this_hash = row_hash(tr)
        group_id = vehicle_sid(class_name, vehicle_number)
        row_id   = f"{group_id}:{this_hash[:8]}"
        sid = group_id  # staging_id kept as alias for staging_group_id

        sc_key = status_code if status_code else "(blank)"
        status_codes[sc_key] = status_codes.get(sc_key, 0) + 1
        if pool_code:
            pool_codes[pool_code] = pool_codes.get(pool_code, 0) + 1
        if depot_code:
            depot_codes[depot_code] = depot_codes.get(depot_code, 0) + 1

        if alt_number_raw:
            parsed = [a.strip() for a in alt_number_raw.split(',') if a.strip()]
            alt_report.append({
                "staging_id": sid, "vehicle_number_raw": vehicle_number,
                "alt_number_raw": alt_number_raw,
                "alt_number_count": len(parsed), "parsed_alt_numbers": parsed,
            })

        if name_raw and ('**' in name_raw or ',' in name_raw):
            parsed_names = [n.strip() for n in name_raw.split(',') if n.strip()]
            name_report.append({
                "staging_id": sid, "name_raw": name_raw,
                "contains_double_star": '**' in name_raw,
                "parsed_name_count": len(parsed_names),
            })

        if warning:
            warnings.append({"staging_id": sid, "warning": warning})

        if sid in seen_ids:
            duplicates.append({
                "staging_id":        sid,
                "vehicle_number_raw": vehicle_number,
                "class_name":        class_name,
                "source_url":        source_url,
                "occurrence":        seen_ids[sid]["count"] + 1,
                "hash_first":        seen_ids[sid]["hash"],
                "hash_this":         this_hash,
                "hashes_identical":  seen_ids[sid]["hash"] == this_hash,
            })
            seen_ids[sid]["count"] += 1
        else:
            seen_ids[sid] = {"hash": this_hash, "count": 1}

        vehicles.append({
            "staging_id":               group_id,
            "staging_row_id":           row_id,
            "staging_group_id":         group_id,
            "staging_class_id":         class_sid(class_name),
            "source_name":              SOURCE_NAME,
            "source_url":               source_url,
            "country_code":             COUNTRY_CODE,
            "class_name":               class_name,
            "vehicle_number_raw":           vehicle_number,
            "alt_numbers_raw":               alt_number_raw,
            "candidate_current_number": candidate,
            "number_resolution_status": resolution,
            "evn":                      None,
            "names_raw":                 name_raw,
            "status_code_raw":              status_code,
            "status_text":              (_st_res := resolve_status(status_code, status_lookup or {}, status_ver, lookup_mode))[0],
            "status_source":            _st_res[1],
            "status_lookup_version":    _st_res[2],
            "status_confidence":        _st_res[3],
            "pool_code_raw":                pool_code,
            "operator_name":            (_op_res := resolve_pool(pool_code, pool_lookup or {}, pool_ver, lookup_mode))[0],
            "operator_source":          _op_res[1],
            "operator_lookup_version":  _op_res[2],
            "operator_confidence":      _op_res[3],
            "depot_code_raw":               depot_code,
            "depot_name":               (_dp_res := resolve_depot(depot_code, depot_lookup or {}, depot_ver, lookup_mode))[0],
            "depot_source":             _dp_res[1],
            "depot_lookup_version":     _dp_res[2],
            "depot_confidence":         _dp_res[3],
            "notes_raw":                 notes,
            "source_confidence":        CONFIDENCE,
            "raw_row_hash":             row_hash(tr),
            "raw_source_payload":       tr.strip(),
            "parse_warning":            warning,
            "retrieved_at":             retrieved_at,
        })

    return staging_class, vehicles, {
        "pool_codes": dict(sorted(pool_codes.items(), key=lambda x: -x[1])),
        "status_codes": dict(sorted(status_codes.items(), key=lambda x: -x[1])),
        "depot_codes": dict(sorted(depot_codes.items(), key=lambda x: -x[1])),
        "alt_numbers": alt_report,
        "name_markers": name_report,
        "warnings": warnings,
        "duplicates": duplicates,
        "vehicles": vehicles,
    }

# ─── DB writes ───────────────────────────────────────────────────────────────

UPSERT_CLASS = """
INSERT INTO staging_classes
    (staging_class_id, source_name, source_url, country_code, class_name,
     builder, max_speed, introduced, spec_json,
     raw_row_hash, raw_source_payload, retrieved_at)
VALUES
    (%(staging_class_id)s, %(source_name)s, %(source_url)s, %(country_code)s, %(class_name)s,
     %(builder)s, %(max_speed)s, %(introduced)s, %(spec_json)s,
     %(raw_row_hash)s, %(raw_source_payload)s, %(retrieved_at)s)
ON DUPLICATE KEY UPDATE
    raw_row_hash=VALUES(raw_row_hash), raw_source_payload=VALUES(raw_source_payload),
    spec_json=VALUES(spec_json), retrieved_at=VALUES(retrieved_at)
"""

UPSERT_VEHICLE = """
INSERT INTO staging_vehicles
    (staging_id, staging_row_id, staging_group_id, staging_class_id,
     source_name, source_url, country_code, class_name,
     vehicle_number_raw, alt_numbers_raw, candidate_current_number, number_resolution_status,
     evn, names_raw, status_code_raw, status_text,
     status_source, status_lookup_version, status_confidence,
     pool_code_raw, operator_name, operator_source, operator_lookup_version, operator_confidence,
     depot_code_raw, depot_name, depot_source, depot_lookup_version, depot_confidence,
     notes_raw, source_confidence,
     raw_row_hash, raw_source_payload, parse_warning, retrieved_at)
VALUES
    (%(staging_id)s, %(staging_row_id)s, %(staging_group_id)s, %(staging_class_id)s,
     %(source_name)s, %(source_url)s, %(country_code)s, %(class_name)s,
     %(vehicle_number_raw)s, %(alt_numbers_raw)s,
     %(candidate_current_number)s, %(number_resolution_status)s,
     %(evn)s, %(names_raw)s, %(status_code_raw)s, %(status_text)s,
     %(status_source)s, %(status_lookup_version)s, %(status_confidence)s,
     %(pool_code_raw)s, %(operator_name)s, %(operator_source)s, %(operator_lookup_version)s, %(operator_confidence)s,
     %(depot_code_raw)s, %(depot_name)s, %(depot_source)s, %(depot_lookup_version)s, %(depot_confidence)s,
     %(notes_raw)s, %(source_confidence)s,
     %(raw_row_hash)s, %(raw_source_payload)s, %(parse_warning)s, %(retrieved_at)s)
ON DUPLICATE KEY UPDATE
    raw_row_hash=VALUES(raw_row_hash),
    raw_source_payload=VALUES(raw_source_payload),
    retrieved_at=VALUES(retrieved_at),
    operator_name=VALUES(operator_name), operator_source=VALUES(operator_source),
    operator_lookup_version=VALUES(operator_lookup_version), operator_confidence=VALUES(operator_confidence),
    depot_name=VALUES(depot_name), depot_source=VALUES(depot_source),
    depot_lookup_version=VALUES(depot_lookup_version), depot_confidence=VALUES(depot_confidence),
    status_text=VALUES(status_text), status_source=VALUES(status_source),
    status_lookup_version=VALUES(status_lookup_version), status_confidence=VALUES(status_confidence),
    candidate_current_number=VALUES(candidate_current_number),
    number_resolution_status=VALUES(number_resolution_status)
"""

def apply_to_db(staging_class, vehicles, verbose=False):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(UPSERT_CLASS, staging_class)
            ins = upd = skp = 0
            for v in vehicles:
                cur.execute(UPSERT_VEHICLE, v)
                rc = cur.rowcount
                if rc == 1:   ins += 1
                elif rc == 2: upd += 1
                else:         skp += 1
                if verbose:
                    tag = "INS" if rc==1 else ("UPD" if rc==2 else "SKP")
                    print(f"  [{tag}] {v['staging_id']}")
        db.commit()
        return ins, upd, skp
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# ─── Report writer ───────────────────────────────────────────────────────────

# Field population spec: (field_name, kind, blocking_level)
FIELD_SPEC = [
    ("vehicle_number_raw",          "source-verbatim",  "required"),
    ("candidate_current_number",    "derived",          "review"),
    ("alt_numbers_raw",             "source-verbatim",  "optional"),
    ("names_raw",                   "source-verbatim",  "optional"),
    ("status_code_raw",             "source-verbatim",  "review"),
    ("status_text",                 "derived",          "promotion-blocking"),
    ("pool_code_raw",               "source-verbatim",  "review"),
    ("operator_name",               "derived",          "promotion-blocking"),
    ("depot_code_raw",              "source-verbatim",  "review"),
    ("depot_name",                  "derived",          "promotion-blocking"),
    ("notes_raw",                   "source-verbatim",  "optional"),
    ("evn",                         "source-verbatim",  "optional"),
    ("raw_source_payload",          "source-verbatim",  "required"),
    ("parse_warning",               "derived",          "review"),
]

def write_reports(all_reports, report_dir, pool_lookup_version="unknown", depot_lookup_version="unknown", lookup_mode="safe"):
    os.makedirs(report_dir, exist_ok=True)
    pool = {}; status = {}; depot = {}; alts = []; names = []; warns = []; dups = []
    all_vehicles = []
    for r in all_reports:
        for k, v in r["pool_codes"].items():   pool[k]   = pool.get(k, 0)   + v
        for k, v in r["status_codes"].items(): status[k] = status.get(k, 0) + v
        for k, v in r["depot_codes"].items():  depot[k]  = depot.get(k, 0)  + v
        alts.extend(r["alt_numbers"])
        names.extend(r["name_markers"])
        warns.extend(r["warnings"])
        dups.extend(r.get("duplicates", []))
        all_vehicles.extend(r.get("vehicles", []))

    total = len(all_vehicles)

    def wj(name, data):
        path = os.path.join(report_dir, name)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        n = len(data) if isinstance(data, (list, dict)) else 0
        print(f"  {name}: {n} entries")

    # Field population report
    pop_report = []
    for field, kind, blocking in FIELD_SPEC:
        populated = sum(
            1 for v in all_vehicles
            if v.get(field) is not None and v.get(field) != ""
        )
        pop_report.append({
            "field":          field,
            "populated":      populated,
            "total":          total,
            "pct":            round(100 * populated / total, 1) if total else 0,
            "kind":           kind,
            "blocking_level": blocking,
        })

    wj("pool_codes_seen.json",        sorted(pool.items(),   key=lambda x: -x[1]))
    wj("status_codes_seen.json",      sorted(status.items(), key=lambda x: -x[1]))
    wj("depot_codes_seen.json",       sorted(depot.items(),  key=lambda x: -x[1]))
    wj("alt_numbers_seen.json",       alts)
    wj("name_markers_seen.json",      names)
    wj("parse_warnings.json",         warns)
    wj("duplicate_source_rows.json",  dups)
    wj("field_population_report.json", pop_report)

    # parse_summary.json — lookup versions + aggregate counts
    from datetime import datetime, timezone as tz
    summary = {
        "generated_at":          datetime.now(tz.utc).isoformat(),
        "source_name":           "spotlog",
        "country_code":          "GB",
        "lookup_mode":           lookup_mode,
        "pool_lookup_version":   pool_lookup_version,
        "depot_lookup_version":  depot_lookup_version,
        "status_lookup_version": status_ver,
        "total_vehicles":        total,
        "total_classes":         len(all_reports),
        "parse_warnings":        len(warns),
        "duplicate_source_rows": len(dups),
        "promoted":              0,
    }
    wj("parse_summary.json", summary)

# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="SpotLog UK locomotive staging importer")
    p.add_argument("--snapshot",   action="append", required=True)
    p.add_argument("--class",      action="append", dest="classes", required=True)
    p.add_argument("--apply",      action="store_true")
    p.add_argument("--verbose",    action="store_true")
    p.add_argument("--report",     action="store_true")
    p.add_argument("--report-dir",   default="./staging_reports")
    p.add_argument("--lookup-mode", dest="lookup_mode", default="safe", choices=["safe","review"],
                   help="safe=confirmed-only (default); review=confirmed+inferred with annotation")
    args = p.parse_args()

    if len(args.snapshot) != len(args.classes):
        print("ERROR: --snapshot and --class counts must match")
        sys.exit(1)

    print(f"\nSpotLog Parser — {'APPLY' if args.apply else 'DRY-RUN'} (lookup-mode: {args.lookup_mode})")

    pool_lookup,   pool_ver   = load_pool_lookup()
    depot_lookup,  depot_ver  = load_depot_lookup()
    status_lookup, status_ver = load_status_lookup()
    if pool_lookup:   print(f"  Pool lookup:   {len(pool_lookup)} codes loaded (v{pool_ver})")
    if depot_lookup:  print(f"  Depot lookup:  {len(depot_lookup)} codes loaded (v{depot_ver})")
    if status_lookup: print(f"  Status lookup: {len(status_lookup)} codes loaded (v{status_ver})")

    all_reports = []
    total_ins = total_upd = total_skp = 0

    for filepath, class_name in zip(args.snapshot, args.classes):
        source_url = BASE_URL.format(class_name=class_name)
        print(f"\nClass {class_name} — {os.path.basename(filepath)}")

        staging_class, vehicles, reports = parse_page(
            class_name, filepath, source_url,
            pool_lookup=pool_lookup, depot_lookup=depot_lookup, status_lookup=status_lookup,
            pool_ver=pool_ver, depot_ver=depot_ver, status_ver=status_ver, lookup_mode=args.lookup_mode
        )
        all_reports.append(reports)

        obvious   = sum(1 for v in vehicles if v["number_resolution_status"] == "obvious")
        ambiguous = sum(1 for v in vehicles if v["number_resolution_status"] == "ambiguous")

        print(f"  Rows:          {len(vehicles)}")
        print(f"  Obvious nums:  {obvious}  Ambiguous: {ambiguous}")
        print(f"  Pool/Status/Depot codes: "
              f"{len(reports['pool_codes'])} / {len(reports['status_codes'])} / {len(reports['depot_codes'])}")
        op_resolved = sum(1 for v in vehicles if v.get("operator_name"))
        dp_resolved = sum(1 for v in vehicles if v.get("depot_name"))
        if pool_lookup or depot_lookup:
            print(f"  Lookup resolved: {op_resolved} operators, {dp_resolved} depots")
        if reports["warnings"]:
            for w in reports["warnings"]:
                print(f"  WARNING: {w}")

        if args.apply:
            ins, upd, skp = apply_to_db(staging_class, vehicles, verbose=args.verbose)
            total_ins += ins; total_upd += upd; total_skp += skp
            print(f"  DB: {ins} inserted, {upd} updated, {skp} skipped")
        else:
            print(f"  (dry-run — no DB writes)")

    if args.report:
        print("\nWriting reports ...")
        write_reports(all_reports, args.report_dir,
                      pool_lookup_version=pool_ver, depot_lookup_version=depot_ver,
                      lookup_mode=args.lookup_mode)

    if args.apply:
        print(f"\nTotal: {total_ins} inserted, {total_upd} updated, {total_skp} skipped")

    print("\nNo canonical promotion. promoted=0 for all rows.")

if __name__ == "__main__":
    main()
