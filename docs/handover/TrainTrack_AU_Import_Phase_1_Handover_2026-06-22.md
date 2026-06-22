# TrainTrack AU Import — Phase 1 Handover
**Date closed:** 2026-06-22
**Status:** COMPLETE ✅

---

## What Was Done

Phase 1 established the full Australian locomotive roster in TrainTrack from the canonical Railtram AU seed dataset. The work covered everything from zero — no importer existed, no Australian data existed in the DB — to a fully loaded, verified, UI-confirmed fleet.

### Phase 1A — Infrastructure
- Added two mounts to `docker-compose.yml` to make importer tools and research data accessible inside the TrainTrack container: `app/tools/importers/` and `research/data_pack_samples/`.

### Phase 1B — Importer
- Built `railtram_import.py` from scratch: a standalone Python importer that reads the Railtram AU seed JSON and creates operators, classes, and locomotives in the correct dependency order.
- Dry-run mode by default; `--apply` required to write anything.
- `--limit N` for staged testing.
- `--verbose` for per-record output.
- `--include-flagged` gate to keep flagged records out unless explicitly requested.
- Pre-flight country check: hard stop on `--apply` if the seed's country code is not present in the `countries` table. Prevents silent NULL country codes — a class of bug discovered during the first 20-record test apply.
- Idempotent: second apply detects existing records and creates nothing.
- User fields (notes, livery, etc.) are never overwritten on re-apply.

### Phase 1C — Data Load
- Inserted `AU / Australia` into the `countries` table (was empty on fresh install).
- Applied `--apply --limit 20` to prove the pipeline end-to-end.
- Hit and resolved the FK constraint bug (NULL country_code cascade failure) — repaired 20 NULL rows, patched importer with hard stop, re-ran to confirm idempotency.
- Ran full apply (no `--include-flagged`) — 2,627 net new records.
- Reviewed the flagged records/groups that remained after the clean import. Decision:
  - FMG SD70ACe-P6 (3 records, 722–731): **held out** — unverified fleet composition.
  - Aurizon 2250 (5 records, 2260–2275): **accepted** via Wikipedia source.
  - QR 2150 (1 record, 2158): **accepted** via Wikipedia source.
- Created and applied a narrow approved override seed (`railtram_au_approved_overrides_2026-06-22.json`) for the 6 confirmed records only.
- Total after override apply: **2,633 locomotives**.

### Phase 1D — UI Sanity Pass
Full walk of the platform at the active TrainTrack web port, confirmed as `http://localhost:5002` during this pass. All pages green, no 500 errors.

---

## Final Counts

| Item | Count |
|------|-------|
| Locomotives | 2,633 |
| Operators | 40 |
| Classes | 168 |
| Country | AU (Australia) |
| NULL country codes | 0 |
| Duplicate identities | 0 |
| Flagged records imported | 0 |
| FMG SD70ACe-P6 excluded | 10 units (722–731) |

---

## Files and Scripts Added

| File | Purpose |
|------|---------|
| `app/tools/importers/railtram_import.py` | Main importer — dry-run + apply, limit, verbose, include-flagged, country pre-flight |
| `research/data_pack_samples/australia/railtram/railtram_au_approved_overrides_2026-06-22.json` | Narrow override seed — 6 confirmed flagged records (Aurizon 2250 × 5, QR 2150 × 1) |
| `docker-compose.yml` | Added importer tools and research data mounts |

The main Railtram AU seed file (`railtram_au_seed.json`, 2,643 records) was pre-existing research data. The importer reads it; it was not modified.

---

## Commits

| Hash | Message |
|------|---------|
| `80ef862` | Mount TrainTrack importer tools and research data |
| `61406fc` | Add Railtram AU dry-run DB importer |
| `aa5f09d` | Require seed country before Railtram apply |
| `3e4931f` | Add approved Railtram AU override seed |

All four commits are pushed.

---

## Known Hold: FMG SD70ACe-P6

Ten units held out pending external fleet verification:

- Road numbers 722–731
- Class: SD70ACe-P6
- Operator: Fortescue Metals Group
- Reason: fleet composition unconfirmed — source data reliability could not be established during Phase 1 review.

**Do not import these records until verified against an authoritative FMG fleet source.**
The `--include-flagged` flag on the importer will surface them; do not use it for AU until this hold is lifted.

---

## Backlog Item: Operator Name Search (UX Improvement)

**Not a bug. Low priority.**

Current behaviour: the locomotive text search field (`?q=`) matches road number, name, and class only. Operator filtering is handled by the dropdown.

Searching "Pacific National" or "Aurizon" as free text returns 0 results, which is confusing when the operator column is visible on the same page.

Preferred fix when the time comes: extend the `q` filter with a JOIN to `operators.name`.
Quick interim option: update the search placeholder from "Search number, name, class…" to "Search number, name or class (use dropdown for operator)".

---

## Next Recommended Phase

**Phase 2 — Fleet Enrichment**

The data is in. The next logical pass is enrichment:

- Assign loco types (Diesel, Electric, etc.) to classes — currently all blank.
- Assign traction types, manufacturer, and year introduced to classes where known.
- Assign depot, livery, and year built to individual locos where data exists.
- Assess whether a second Railtram seed or supplementary source covers these fields, or whether it's a manual/research task.

This is lower urgency than getting data in — the platform works, searches work, sightings can be logged now. Enrichment is cosmetic and operational, not structural.

**Also in scope before Phase 2:** confirm the FMG hold is the only outstanding flagged group, or review the Railtram seed for any other records that were borderline.

---

*Handover written 2026-06-22. Platform confirmed green by UI sanity pass same date.*
*Next session: read this file before touching TrainTrack data or the importer.*
