# Railtram Importer — Plain-English Design

**Status:** Design only. No code written. Not approved for implementation.  
**Date:** 2026-06-22  
**Based on:** railtram_classes_2026-06-22.md + railtram_number_indexes_2026-06-22.md

---

## Pipeline Overview

```
Railtram number index (source)
  → Step 1: Parse operator abbreviation table
  → Step 2: Parse index rows into raw tokens
  → Step 3: Expand road-number ranges/groups into individual units
  → Step 4: Resolve operator abbreviation → operators.id
  → Step 5: Resolve/create class → classes.id
  → Step 6: Preview (dry run — show what would be inserted/updated)
  → Step 7: Insert/update locomotives by (country_code, operator_id, number)

ARTC PDF (separate, optional, later)
  → Class/spec enrichment only
  → Not a roster source
```

The importer reads from the Railtram number index page (either a saved/fetched copy or live). The operator abbreviation table on the same page is the key to resolving abbreviated operator names.

---

## Step 1: Parse the Operator Abbreviation Table

The page includes a two-column table mapping short codes to full names (e.g. `FMG → Fortescue Metals Group`). This must be parsed first — it is the lookup dictionary for all subsequent rows.

All 42 known entries are already documented in the research note. The importer should use this table, not hardcode the mapping — the page may update as operators merge or are renamed.

One anomaly: `CT` appears as operator for `CSR001–CSR024` but is not in the abbreviation table. The importer should flag any unresolved abbreviation as a review item rather than failing or silently dropping the row.

---

## Step 2: Parse Index Rows

Each row has three fields: `Road Numbers | Operator | Class`.

The raw road number field is a string that may span multiple lines on the page (long groups are word-wrapped in the Wix table). The browser-rendered text has already joined these — but if scraping live, the cell content must be fully joined before parsing.

After joining, the row is a single string like:
```
2475D–2477D, 2478H, 2479D, 2480E, 2481D–2483D, 2484H
```

---

## Step 3: Expand Road-Number Ranges

This is the hard step. The road number field uses several formats, and the gremlins are real. Here is every pattern found in the actual data:

### 3a. Simple range
```
701–721
```
Expand to 701, 702, 703, ... 721. The separator is an **en-dash** (–, Unicode U+2013), not a hyphen. The importer must handle both, since copy-paste or encoding changes can introduce hyphens.

### 3b. Simple list
```
32, 33
```
Split on comma. Each token is a single number.

### 3c. Mixed range and list
```
001–002, 004–005, 007–018
```
Split on comma first, then process each token. Some tokens are ranges, some are singletons.

### 3d. Abbreviated end of range
```
4601–16       →  4601–4616
7053–92       →  7053–7092
7094–98       →  7094–7098
2901–6        →  2901–2906
```
When the end number has fewer digits than the start number, it is an abbreviation. Reconstruction rule: take the leading digits of the start number (up to `len(start) - len(end)` digits) and prepend them to the end. This is the most common non-obvious format on the page.

### 3e. Suffix codes on road numbers
Some road numbers carry a trailing letter suffix that is part of the number, not a range indicator:
```
1724D     →  single unit, number is "1724D"
2302D     →  single unit, number is "2302D"
```
Suffixes seen in data: **D, H, F, A, E, L**. Their meaning is not defined on the page (likely build batch or variant codes).

### 3f. Suffix ranges
```
2302D–2315D   →  2302D, 2303D, 2304D, ... 2315D
2475D–2477D   →  2475D, 2476D, 2477D
```
When both start and end of a range carry the same suffix, strip the suffix, expand the numeric portion, reattach the suffix to each result. The suffix must match on both ends — if they don't match, treat as two separate singleton tokens and flag for review.

### 3g. Mixed suffix within a group
```
2475D–2477D, 2478H, 2479D, 2480E, 2481D–2483D, 2484H
```
Each comma-separated token may carry a different suffix. Process each token independently. Do not assume the suffix carries across the whole group.

### 3h. Leading zeros
```
001–018   →  001, 002, 003, ... 018
```
Preserve leading zeros. The expanded numbers must be zero-padded to the same width as the start of the range. `001` stays `001`, not `1`.

### 3i. Alphanumeric prefix embedded in number
```
AC4301–AC4308   →  AC4301, AC4302, ... AC4308
ACB4401–ACB4406 →  ACB4401, ACB4402, ... ACB4406
AN1–AN9, AN11   →  AN1, AN2, ... AN9, AN11
```
The alphabetic prefix is part of the road number string. To expand a range, detect the shared prefix, expand only the numeric suffix portion, then reconstruct with the prefix. If the two ends of a range have different prefixes, flag and skip.

### 3j. Known typos in source data
These were found in the actual page and should be handled explicitly rather than causing parse failures:

| Raw text | Correct interpretation | Action |
|---|---|---|
| `2822– 850` | `2822–2850` | Strip stray space before digit |
| `48s33`, `48s36` | `4833`, `4836` | Strip lowercase `s` (rendering artefact) |
| `48211–4828` (GrainCorp 48) | `48211–48280` or similar | Abbreviated end; truncation likely — flag for review |
| `2332D–3D` | `2332D–2333D` | Abbreviated end with suffix |
| `4601–16` | `4601–4616` | Abbreviated end (covered by rule 3d) |
| `CBH023–BH025` | `CBH023–CBH025` | Inconsistent prefix — strip non-alpha prefix from end and reconstruct |

The importer should not fail hard on these. It should apply best-effort parsing, flag the anomalous rows in the preview/review output, and let a human confirm before insert.

---

## Step 4: Resolve Operator

Each row has a short operator code (e.g. `FMG`, `PN`, `Aurizon`). Resolution:

1. Look up code in the parsed abbreviation table → get full name
2. Look up full name in `operators` table → get `operator_id`
3. If not found in `operators` table → create the operator row (with `country_code='AU'`, `type='freight'` as default) and flag as "created during import, verify details"
4. If abbreviation not in the lookup table (the `CT` case) → flag row as "unresolved operator, skipped" and continue

`Unknown` (id=1) is the last resort, not the first. Any row landing on Unknown should appear in a separate review list.

---

## Step 5: Resolve or Create Class

Each row has a class name (e.g. `C44-9W`, `NR`, `830`). Resolution:

1. Look up class name in `classes` table (case-insensitive, `country_code='AU'`)
2. If found → use `class_id`
3. If not found → create a minimal class row: `name`, `country_code='AU'`, and flag as "created from Railtram number index — needs spec enrichment from sub-page"

Three classes are known to be in the number index but missing from the classes page: `2250`, `SD70ACe-P6`, `2150`. These will be auto-created if this rule is followed. That's the correct behaviour.

---

## Step 6: Preview (Dry Run)

Before any insert, the importer should produce a preview report showing:

- Total rows parsed from source
- Total individual units after range expansion
- Breakdown by operator and class
- Rows that would be new inserts vs. updates (matched on `country_code + operator_id + number`)
- Review flags: unresolved operators, auto-created classes, Unknown operator fallbacks, parse anomalies
- Estimated row count for each category

The preview must be human-readable and short enough to actually read. No one reviews a 2,000-line diff — summarise by operator, list anomalies in full.

---

## Step 7: Insert / Update

Identity key for upsert: `(country_code, operator_id, number)` — matching the new unique key.

On match (existing row): update `class_id`, `status` (if the import has status data — it doesn't from the number index, so leave status alone on update). Do not overwrite manually-entered data.

On no match (new row): insert with `country_code='AU'`, resolved `operator_id`, resolved `class_id`, `status='active'` (default — number index implies current fleet).

`operator_id=1` (Unknown) rows: insert allowed but flagged separately. Do not silently accept.

---

## What the Number Index Does Not Provide

The importer will NOT be able to populate these fields from the number index alone. They require class sub-page scraping or manual entry:

- `locomotives.type_id` (traction type — diesel/electric etc.)
- `locomotives.built_year`
- `locomotives.name` (named locomotives)
- `locomotives.livery`
- `locomotives.depot_id`
- `classes.manufacturer`
- `classes.introduced_year`
- `classes.type_id`
- `classes.description`

These are enrichment tasks for a later phase, using individual class sub-pages.

---

## ARTC PDF — Separate, Later

The ARTC Rolling Stock PDF is a class/spec reference (2011-era) not a current roster. It maps to `classes` table enrichment: manufacturer, introduced year, traction type, description. It should not drive any `locomotives` rows. When ready, it can run as a separate enrichment pass after the number-index import has established the class rows.

---

## Open Questions Before Coding

1. **Input source**: Should the importer scrape Railtram live (requiring Chrome/browser rendering for the number index), or work from a saved copy of the extracted text? A saved copy is safer and reproducible. Recommendation: save the rendered text to a seed file in `research/`, import from that.

2. **Update strategy on re-run**: If the importer runs a second time (e.g. after Railtram updates its roster), should it update existing rows, skip them, or prompt? Recommendation: update `class_id` only if it changed; never overwrite user-entered fields (name, livery, notes, depot).

3. **Operator create vs prompt**: When an operator from Railtram doesn't exist in the DB, should the importer auto-create it or require it to be pre-seeded? Auto-create is faster; pre-seed is safer. Could be a flag.

4. **Status handling**: Number index implies current fleet = `active`. But Railtram includes stored/withdrawn units. Without a status column in the index, all imports would default to `active`. Accept this for now, fix per-unit in a later enrichment pass?

