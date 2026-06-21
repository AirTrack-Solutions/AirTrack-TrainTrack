#!/usr/bin/env python3
"""
railtram_preview.py  —  Import Iguana Phase 1A
Dry-run parser for the Railtram locomotive number index.

Reads extracted Railtram number index text, expands road-number ranges,
resolves operator abbreviations, and prints a structured dry-run preview.

No database connection. No writes. No side effects.

Usage:
    python3 railtram_preview.py <input_file> [--json]

"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# Operator abbreviation table  (Railtram page, 2026-06-22)
# ---------------------------------------------------------------------------
OPERATOR_TABLE = {
    "Aurizon":    "Aurizon",
    "BHP":        "BHP",
    "BMACC":      "BHP Mitsubishi Alliance",
    "BlueScope":  "BlueScope Steel",
    "Bowen":      "Bowen Rail Company",
    "CBH":        "CBH Group",
    "Centennial": "Centennial Coal",
    "Cockburn":   "Cockburn Cement",
    "Crawfords":  "Crawfords Freightlines",
    "Downer":     "Downer Rail",
    "Ettamogah":  "Ettamogah Rail Hub",
    "FIE":        "Fletcher International Exports",
    "FMG":        "Fortescue Metals Group",
    "Gemco":      "Gemco Rail",
    "GrainCorp":  "GrainCorp",
    "Greentrains":"Greentrains",
    "JRW":        "Junee Railway Workshop",
    "Manildra":   "Manildra Group",
    "MRG":        "Magnetic Rail Group",
    "MTS":        "Metro Trains Sydney",
    "NREC":       "National Railway Equipment Company",
    "ORA":        "One Rail Australia",
    "PN":         "Pacific National",
    "Progress":   "Progress Rail",
    "Qube":       "Qube Logistics",
    "QR":         "Queensland Rail",
    "RP":         "RailPower",
    "Rail First": "Rail First Asset Management",
    "RTA":        "Rio Tinto Aluminium",
    "RTIO":       "Rio Tinto Iron Ore",
    "RHA":        "Roy Hill Australia",
    "SCT":        "SCT Logistics",
    "SMR":        "South Maitland Railways",
    "SSR":        "Southern Shorthaul Railroad",
    "ST":         "Sydney Trains",
    "Swift":      "Swift Transport",
    "TasRail":    "TasRail",
    "Transperth": "Transperth",
    "UGL":        "UGL",
    "V/Line":     "V/Line Passenger",
    "Watco":      "Watco Australia",
    "Whitehaven": "Whitehaven Coal",
}

# ---------------------------------------------------------------------------
# Known classes from railtram_classes_2026-06-22.md (175 entries)
# Used only for flagging classes absent from the classes page.
# ---------------------------------------------------------------------------
KNOWN_CLASSES = {
    "11","14","22","32","44","45","48","49","71","73","80","81","82","83","88",
    "90","92","93","94","422","442","500","600","830","900","1100","1200","1300",
    "1600","1720","1900","2050","2170","2170F","2300","2300D","2400","2470",
    "2700","2800","2900","3200","3551","3700","3800","4000","4100","4600","5000",
    "5020","6000","6020",
    "A","AB","AC","AC44C6M","ACB","ACC","ACD","ACN","ALF","AN",
    "B","BEL","BL","BMACC","BRM",
    "C","C36-7M","C44-9W","CD","CEY","CF","CK","CLF","CLP","CM",
    "Comalco GT26C","CS","CSR",
    "DAZ","DBZ","DC","DFZ","DH","DL","DQ","DR",
    "EL","ES44ACi","ES44DCi",
    "FIE","FJ","FL","FQ",
    "G","GE L80T","GL","GM1","GM12","GML","GPU","GWA","GWB","GWN","GWU",
    "H","HL","J","JT42C","K","KA","L","LDP",
    "MAN","MM","MP27CN","MP33C","MP33CN","MRL",
    "N","NR","ORN","ORQ",
    "P","PA","PB","PH","PHC","PL","PN","PRL","PRQ",
    "Q","QBX","QE","QL",
    "RHA","RL","RT",
    "S","SCT","SD70ACe","SD70ACe/LC","SD70ACe/LCi","SD90MAC-H Phase II","SSR",
    "T","TL","TR","TT","TT2","UM20C","V","VL",
    "WH","WRA","WRB","WRC","WRD","WRE",
    "X","X200","XR","XRB","XRN","Y",
}


# ---------------------------------------------------------------------------
# Road number helpers
# ---------------------------------------------------------------------------

def preprocess_typos(expr: str) -> str:
    """Fix known Railtram source typos in a road number expression."""
    # Stray space after range separator: "2822– 850" → "2822–850"
    expr = re.sub(r'([–\-])\s+(\d)', r'\1\2', expr)
    # Lowercase-s rendering artefact between digits: "48s33" → "4833"
    expr = re.sub(r'(\d)s(\d)', r'\1\2', expr)
    return expr


def parse_road_number(s: str):
    """Split a road number string into (alpha_prefix, numeric_str, alpha_suffix).
    The numeric_str preserves leading zeros as a string.
    Returns (None, None, None) if s is not a parseable road number."""
    m = re.fullmatch(r'([A-Za-z]*)(\d+)([A-Za-z]*)', s.strip())
    if m:
        return m.group(1), m.group(2), m.group(3)
    return None, None, None


def expand_range(start_s: str, end_s: str):
    """Expand a single range token 'start_s–end_s' into individual road numbers.

    Handles:
    - Leading-zero preservation:  WH001–WH003 → WH001 WH002 WH003
    - Alpha prefix ranges:        NR1–NR9 → NR1..NR9
    - Suffix codes:               2302D–2315D → 2302D..2315D
    - Abbreviated ends:           4601–16 → 4601..4616  (end shorter than start)

    Returns (list[str], flag_str|None).
    """
    sp, sn, ss = parse_road_number(start_s)
    ep, en, es = parse_road_number(end_s)

    if sn is None:
        return [start_s, end_s], f"Cannot parse range start '{start_s}'"
    if en is None:
        return [start_s, end_s], f"Cannot parse range end '{end_s}'"

    # Abbreviated end: end has fewer digits than start and no alpha prefix
    # e.g. 4601–16 → en='16' (2 digits) < sn='4601' (4 digits), ep=''
    if len(en) < len(sn) and ep == '':
        n_missing = len(sn) - len(en)
        reconstructed = sn[:n_missing] + en
        if int(reconstructed) < int(sn):
            return [start_s, end_s], (
                f"Abbreviated end '{end_s}' reconstructs to '{reconstructed}' "
                f"which is < start '{sn}' — source data error, review manually"
            )
        en = reconstructed
        ep = sp
        if not es:
            es = ss

    # Inherit unset prefix/suffix from start
    if not ep and sp:
        ep = sp
    if not es and ss:
        es = ss

    # Validate consistency
    if sp != ep:
        return [start_s, end_s], f"Prefix mismatch in range '{start_s}'–'{end_s}'"
    if ss != es:
        return [start_s, end_s], f"Suffix mismatch in range '{start_s}'–'{end_s}'"

    s_int, e_int = int(sn), int(en)
    if e_int < s_int:
        return [start_s, end_s], f"End < start in range '{start_s}'–'{end_s}'"

    pad = len(sn)  # preserve original leading-zero width
    return [f"{sp}{str(n).zfill(pad)}{ss}" for n in range(s_int, e_int + 1)], None


def expand_expression(expr: str):
    """Expand a full road-number expression into individual unit strings.

    Handles comma-separated lists, en-dash ranges, hyphen ranges,
    and all documented pattern variants.

    Returns (list[str], list[str flags]).
    """
    expr = preprocess_typos(expr)
    expr = re.sub(r'\s+', ' ', expr).strip()

    tokens = [t.strip() for t in expr.split(',') if t.strip()]
    numbers = []
    flags = []

    for token in tokens:
        if not token:
            continue

        # --- En-dash range (preferred Railtram separator) ---
        if '–' in token:
            parts = token.split('–', 1)
            expanded, flag = expand_range(parts[0].strip(), parts[1].strip())
            numbers.extend(expanded)
            if flag:
                flags.append(flag)

        # --- Hyphen range: digit–hyphen–digit or digit–hyphen–alpha ---
        elif re.search(r'(?<=\d)-(?=[\dA-Za-z])', token):
            m = re.search(r'(?<=\d)-(?=[\dA-Za-z])', token)
            hp = m.start()  # position of the hyphen
            start_part = token[:hp].strip()
            end_part   = token[hp + 1:].strip()
            expanded, flag = expand_range(start_part, end_part)
            numbers.extend(expanded)
            if flag:
                flags.append(flag)

        # --- Single road number ---
        else:
            numbers.append(token)

    return numbers, flags


# ---------------------------------------------------------------------------
# Row parsing
# ---------------------------------------------------------------------------

def parse_row(line: str):
    """Parse a single index line into (road_nums_str, operator_code, class_name).

    Strategy: walk tokens right-to-left looking for a known operator code.
    This handles multi-word class names (the class is always last) and cases
    where the operator abbreviation also appears in road numbers (e.g. 'PN').

    Returns (None, None, None) if no operator found.
    """
    tokens = line.split()
    n = len(tokens)
    if n < 3:
        return None, None, None

    # Single-word operators (walk right-to-left, skip last token which is class)
    for i in range(n - 2, 0, -1):
        if tokens[i] in OPERATOR_TABLE:
            road_nums  = ' '.join(tokens[:i])
            class_name = ' '.join(tokens[i + 1:])
            if road_nums.strip() and class_name.strip():
                return road_nums.strip(), tokens[i], class_name.strip()

    # Two-word operators (e.g. "Rail First")
    for i in range(n - 3, 0, -1):
        two_word = tokens[i] + ' ' + tokens[i + 1]
        if two_word in OPERATOR_TABLE:
            road_nums  = ' '.join(tokens[:i])
            class_name = ' '.join(tokens[i + 2:])
            if road_nums.strip() and class_name.strip():
                return road_nums.strip(), two_word, class_name.strip()

    return None, None, None


def parse_section(text: str) -> list:
    """Parse one index section into a list of (road_nums_str, op_code, class_name).

    Handles multi-line entries where a blank line or line-break appears in the
    middle of a long road-number expression.
    """
    SKIP_EXACT = {
        'Road Numbers Operator Class',
        'Index By Number',
        'Index By Letter',
        '​',  # zero-width space (Wix artefact)
    }

    results = []
    buffer  = []  # accumulated partial road-number tokens from continuation lines

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line in SKIP_EXACT or line.startswith('Index By '):
            continue

        # Build candidate: join any buffered continuation + current line
        if buffer:
            combined_prefix = ', '.join(b.rstrip(',').strip() for b in buffer)
            candidate = combined_prefix + ', ' + line
        else:
            candidate = line

        road_nums, op, cls = parse_row(candidate)

        if op is not None:
            road_nums = road_nums.rstrip(',').strip()
            results.append((road_nums, op, cls))
            buffer = []
        else:
            # No operator found — this is a continuation of the previous road-number list
            buffer.append(line)

    # Flush any unparseable trailing content
    if buffer:
        results.append((' '.join(buffer), None, None))

    return results


def parse_file(text: str):
    """Split the full index text into numeric and letter sections, parse each.
    Returns (numeric_rows, letter_rows).
    """
    num_idx = text.find('Index By Number')
    let_idx = text.find('Index By Letter')

    if num_idx == -1 and let_idx == -1:
        return parse_section(text), []
    if num_idx != -1 and let_idx != -1:
        return parse_section(text[num_idx:let_idx]), parse_section(text[let_idx:])
    if num_idx != -1:
        return parse_section(text[num_idx:]), []
    return [], parse_section(text[let_idx:])


# ---------------------------------------------------------------------------
# Preview generation
# ---------------------------------------------------------------------------

def build_preview(numeric_rows: list, letter_rows: list, source_path: str) -> dict:
    """Build the full structured dry-run preview."""
    all_rows      = []
    review_flags  = []
    op_seen       = defaultdict(set)      # op_code → set of expanded numbers
    number_to_ops = defaultdict(list)     # number  → [op_codes]

    for section, rows in [('numeric', numeric_rows), ('letter', letter_rows)]:
        for idx, (road_nums, op_code, class_name) in enumerate(rows, 1):
            flags = []

            # --- Unresolved row (no operator identified) ---
            if op_code is None:
                flags.append('UNRESOLVED ROW: operator not identified')
                all_rows.append({
                    'section': section, 'row': idx,
                    'road_nums_expr': road_nums,
                    'operator_code': None, 'operator_full': None,
                    'class_name': None, 'expanded': [], 'unit_count': 0,
                    'flags': flags,
                })
                review_flags.extend(flags)
                continue

            # --- Operator resolution ---
            op_full = OPERATOR_TABLE.get(op_code)
            if op_full is None:
                flags.append(f"UNKNOWN OPERATOR: '{op_code}' not in abbreviation table")

            # --- Class check ---
            if class_name and class_name not in KNOWN_CLASSES:
                flags.append(f"CLASS NOT ON CLASSES PAGE: '{class_name}'")

            # --- Road number expansion ---
            expanded, expand_flags = expand_expression(road_nums or '')
            flags.extend(expand_flags)

            # --- Within-operator duplicate check ---
            seen_here = op_seen[op_code]
            for n in expanded:
                if n in seen_here:
                    flags.append(f"DUPLICATE WITHIN OPERATOR: '{n}' (op={op_code})")
                else:
                    seen_here.add(n)

            # --- Cross-operator tracking (informational, not an error) ---
            for n in expanded:
                number_to_ops[n].append(op_code)

            all_rows.append({
                'section':       section,
                'row':           idx,
                'road_nums_expr': road_nums,
                'operator_code': op_code,
                'operator_full': op_full or f'UNKNOWN ({op_code})',
                'class_name':    class_name,
                'expanded':      expanded,
                'unit_count':    len(expanded),
                'flags':         flags,
            })
            review_flags.extend(flags)

    # Cross-operator shared numbers (informational)
    cross_op = {
        n: sorted(set(ops))
        for n, ops in number_to_ops.items()
        if len(set(ops)) > 1
    }

    return {
        'source':                        source_path,
        'country':                       'AU',
        'total_rows':                    len(all_rows),
        'total_units':                   sum(r['unit_count'] for r in all_rows),
        'rows':                          all_rows,
        'review_flag_count':             len(review_flags),
        'cross_operator_shared_numbers': cross_op,
        'cross_operator_shared_count':   len(cross_op),
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

_W = 72  # output width


def _wrap_numbers(numbers: list, indent: int = 15, width: int = 56) -> list:
    """Wrap a list of road numbers into display lines."""
    lines, current, cur_len = [], [], 0
    for n in numbers:
        if cur_len + len(n) + 1 > width and current:
            lines.append(' ' * indent + ' '.join(current))
            current, cur_len = [n], len(n)
        else:
            current.append(n)
            cur_len += len(n) + 1
    if current:
        lines.append(' ' * indent + ' '.join(current))
    return lines


def print_text(preview: dict) -> None:
    print('=' * _W)
    print(' Railtram Number Index — Dry-Run Preview  (Import Iguana Phase 1A)')
    print('=' * _W)
    print(f"  Source:  {preview['source']}")
    print(f"  Country: {preview['country']}")
    print()

    current_section = None
    for row in preview['rows']:
        if row['section'] != current_section:
            current_section = row['section']
            label = 'NUMERIC INDEX' if current_section == 'numeric' else 'LETTER INDEX'
            print(label + ' ' + '─' * (_W - len(label) - 1))
            print()

        op_str  = (f"{row['operator_code']} / {row['operator_full']}"
                   if row['operator_full'] else str(row['operator_code']))
        cls_str = row['class_name'] or '?'

        print(f"  Row {row['row']:>3}  [{op_str}]  class: {cls_str}")
        print(f"           expr: {row['road_nums_expr']}")

        if row['expanded']:
            unit_lines = _wrap_numbers(row['expanded'])
            print(f"           units [{row['unit_count']}]:")
            for ul in unit_lines:
                print(ul)
        elif row['unit_count'] == 0 and row['operator_code']:
            print('           units [0]: (none expanded)')

        for flag in row['flags']:
            print(f"           ⚑ {flag}")
        print()

    # Review flags
    if preview['review_flag_count']:
        print('REVIEW FLAGS ' + '─' * (_W - 14))
        print()
        for row in preview['rows']:
            for flag in row['flags']:
                op   = row['operator_code'] or '?'
                cls  = row['class_name']    or '?'
                print(f"  [row {row['row']:>3}|{op:<10}|{cls:<22}]  {flag}")
        print()

    # Cross-operator shared numbers
    if preview['cross_operator_shared_count']:
        label = 'CROSS-OPERATOR SHARED NUMBERS (informational — allowed by schema)'
        print(label + ' ' + '─' * max(0, _W - len(label) - 1))
        print()
        for number, ops in sorted(preview['cross_operator_shared_numbers'].items()):
            print(f"  {number:<14} {', '.join(ops)}")
        print()

    # Summary
    print('SUMMARY ' + '─' * (_W - 9))
    print(f"  Rows parsed:           {preview['total_rows']}")
    print(f"  Units expanded:        {preview['total_units']}")
    print(f"  Review flags:          {preview['review_flag_count']}")
    print(f"  Cross-op shared nums:  {preview['cross_operator_shared_count']}")
    print()
    if preview['review_flag_count'] == 0:
        print('  ✓  No flags — dry run clean.')
    else:
        print(f"  ⚑  {preview['review_flag_count']} flag(s) need review before import.")
    print()


def print_json_output(preview: dict) -> None:
    print(json.dumps(preview, indent=2))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description='Railtram number index dry-run parser — Import Iguana Phase 1A'
    )
    ap.add_argument('input_file', help='Path to extracted Railtram number index text')
    ap.add_argument('--json', action='store_true', help='Output JSON instead of text')
    args = ap.parse_args()

    path = Path(args.input_file)
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding='utf-8')
    numeric_rows, letter_rows = parse_file(text)
    preview = build_preview(numeric_rows, letter_rows, str(path))

    if args.json:
        print_json_output(preview)
    else:
        print_text(preview)


if __name__ == '__main__':
    main()
