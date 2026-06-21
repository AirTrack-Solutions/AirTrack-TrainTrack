# TrainTrack Critter Registry

Critters enter when a recurring job appears, has clear boundaries, produces evidence,
and will probably need automation later. They are named responsibility lanes first,
code and services later — only when the behaviour is proven.

This file records their roles and the evidence they have already produced.
Updated as new critters earn their place.

---

## Slothful Seth
**Role:** Rendered web source gathering — patient, careful retrieval of JS-rendered pages
(Wix, React, SPAs) that static curl cannot reach.

**Motto:** Slow is smooth. Smooth is safe. Safe avoids angry website admins.

**TrainTrack territory:** Railtram.com.au and any other JS-rendered railway reference source.

**Evidence already produced (2026-06-22):**
- Navigated to `https://www.railtram.com.au/locomotive-number-indexes` via Chrome
- Confirmed the page is Wix/JS-rendered — static fetch returns a shell only
- Extracted full rendered page text: 42-operator abbreviation table + ~320 index rows
- Confirmed column structure: Road Numbers | Operator | Class (3 columns, no status)
- Recorded in: `research/data_pack_samples/australia/railtram/railtram_number_indexes_2026-06-22.md`

**Also contributed to:** Classes page static fetch (that one came back on plain HTTP —
Seth approves of sources that don't make him work too hard).

---

## Archival Aardvark
**Role:** Research notes, source preservation, access dates, evidence trails.
Keeps the paper trail so the importer knows where its data came from.

**Motto:** If it has no date and no URL, it never happened.

**TrainTrack territory:** All source research notes. Every data source gets a dated note
before any importer touches it.

**Evidence already produced (2026-06-22):**
- `research/data_pack_samples/australia/railtram/railtram_classes_2026-06-22.md`
  — 175 class entries, scope statements, field mapping, limitations
- `research/data_pack_samples/australia/railtram/railtram_number_indexes_2026-06-22.md`
  — full operator table, ~320 index rows, anomalies, schema blocker identified
- `research/data_pack_samples/australia/railtram/railtram_importer_design_2026-06-22.md`
  — plain-English importer design with range expansion rules

**Still to do:** ARTC PDF research note (class/spec reference, not roster). Aardvark
should produce this before any class enrichment work begins.

---

## Prudence Porcupine
**Role:** Schema and data safety. Catches dangerous assumptions before they become
production bugs. Raises the flag before code gets written, not after data gets corrupted.

**Motto:** A constraint is cheaper than a rollback.

**TrainTrack territory:** Schema review at each design decision point. Runs before any
importer phase begins. Checks that the DB can actually hold what the source is sending.

**Evidence already produced (2026-06-22):**
- Identified that `UNIQUE KEY uq_loco_number (number)` assumes globally unique road
  numbers — an aircraft assumption that breaks on national railway data
- Confirmed the assumption is wrong: FMG 901 and Aurizon 901 can coexist
- Recommended `UNIQUE KEY uq_loco_identity (country_code, operator_id, number)`
- Flagged the nullable `operator_id` interaction with the compound key
- Recommended `NOT NULL DEFAULT 1` + Unknown operator seed as the clean fix
- Schema change applied, dev DB rebuilt and verified (2026-06-22, commit 09251db)

**Watch list (items Prudence is keeping an eye on):**
- `formations` table still has `UNIQUE KEY uq_set_number (set_number)` — same
  potential problem if multi-operator formation sets ever share numbers. Not confirmed
  yet, but worth remembering.
- `operator_id=1` (Unknown) as a landing zone — Prudence says this is a review flag,
  not a comfortable home. Any import row landing on Unknown must be surfaced.

---

## Import Iguana
**Role:** Careful data intake. Dry-run first, always. Parses sources, expands ranges,
resolves references, stages rows for review before anything touches a live table.

**Motto:** Preview before you commit. Stage before you insert. Never dump into live.

**TrainTrack territory:** All locomotive/formation import pipelines. The number index
importer is Iguana's first real job.

**Evidence already produced (2026-06-22):**
- Importer design document written covering all 7 pipeline steps
- Range expansion rules catalogued from real data (10 distinct patterns found)
- Anomalies documented: abbreviated end-of-range, suffix codes, mixed suffix groups,
  leading zeros, embedded alphanumeric prefixes, known source typos
- 4 open questions identified that must be answered before any code is written
- Recorded in: `research/data_pack_samples/australia/railtram/railtram_importer_design_2026-06-22.md`

**Not yet built.** Iguana's first code will be the dry-run range expander —
whenever that gets approved.

---

## Ledger Goblin
**Role:** Reconciliation of classes, operators, numbers, and names. Finds duplicates,
resolves ambiguous codes, flags things that don't match cleanly.
Grumpy about inconsistency. Precise about ledgers.

**Motto:** If the same thing has two names, one of them is wrong. Possibly both.

**TrainTrack territory:** Operator abbreviation resolution, class name deduplication,
the messy corners where source data doesn't map cleanly to schema rows.

**Evidence already produced (2026-06-22):**
- Identified 9 class names that appear twice in Railtram with different operators
  (P Class Aurizon / P Class Various, H Class SCT / H Class Watco, etc.)
- Identified 3 class names in the number index with no matching classes page entry
  (2250, SD70ACe-P6, 2150) — create-or-flag decision documented
- Identified `CT` operator abbreviation appearing in index but missing from the
  42-entry abbreviation table — unresolved operator, must be flagged not silently dropped
- Recorded in: `research/data_pack_samples/australia/railtram/railtram_number_indexes_2026-06-22.md`

**Not yet built.** Ledger Goblin's first active role will be during the importer
dry-run — the reconciliation report is his output.

---

## Critter Rule (TrainTrack)

A critter enters when:
1. A recurring job appears
2. The job has clear boundaries
3. The job produces evidence
4. The job will probably need automation later

Critters do NOT need dashboards, schedulers, or service wiring until their behaviour
is proven. The name and the job come first.

