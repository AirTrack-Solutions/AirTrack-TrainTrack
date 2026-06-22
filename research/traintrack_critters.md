# TrainTrack Critter Registry

Critters enter when a recurring job appears, has clear boundaries, produces evidence,
and will probably need automation later. They are named responsibility lanes first,
code and services later — only when the behaviour is proven.

This file records their roles and the evidence they have already produced.
Updated as new critters earn their place.

---

## Phase 2 — Fleet Enrichment: Critter Responsibilities

Before any Phase 2 enrichment work begins, the following ownership lanes are locked.
No critter acts outside its lane. No enrichment apply happens without Prudence's clearance.

| Critter | Phase 2 Lane | Apply gate? |
|---------|-------------|-------------|
| Ledger Goblin | Class/operator reconciliation, enrichment mapping, alias decisions | No apply without Goblin sign-off on mappings |
| Archival Aardvark | Source notes, URLs, access dates, provenance for every enrichment source | No apply without a dated Aardvark note |
| Prudence Porcupine | Overwrite risk, schema/data safety review before any apply | Hard gate — Prudence clears before Iguana applies |
| Import Iguana | Importer owner — dry-run/apply execution only | No apply without explicit Trevor approval |
| Slothful Seth | Standby — wakes only if rendered web capture is needed | Not active in Phase 2 unless a JS-rendered source is required |

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

**Phase 2 role:** Standby only.
Seth wakes if a Phase 2 enrichment source is JS-rendered and cannot be fetched statically.
He does NOT wake proactively. Aardvark identifies the source, then escalates to Seth if needed.
Seth is NOT responsible for deciding which sources to consult — that is Aardvark's lane.

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

**Phase 2 role:** Mandatory first step before any enrichment source is touched.
Every Phase 2 enrichment source must have an Aardvark note recording:
- Source URL
- Access date
- Scope (what it covers and what it does not)
- Field mapping to TrainTrack schema fields
- Known limitations or reliability concerns

No enrichment mapping (Goblin) and no enrichment apply (Iguana) proceeds without
a corresponding Aardvark note. This is a hard dependency, not a courtesy step.

Aardvark does NOT decide what gets imported — that is Goblin's lane.
Aardvark does NOT touch the database or the importer.

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

**Phase 2 role:** Hard gate before every enrichment apply.
Prudence reviews each proposed enrichment pass for:
- Overwrite risk — does the enrichment field already have user-entered data? If yes, block.
- Schema fit — does the enrichment value fit the column type, length, and constraints?
- Source reliability — is the Aardvark note present and complete before this apply runs?
- Null safety — will enriching this field produce NULLs, blanks, or placeholders that
  look like real data but aren't?

Prudence's clearance is required before Iguana runs `--apply` on any enrichment pass.
Prudence does NOT decide what gets imported — that is Goblin's lane.
Prudence does NOT fetch or evaluate sources — that is Aardvark's lane.
Prudence does NOT execute the apply — that is Iguana's lane.

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
- Phase 1 full apply complete: 2,633 locomotives, 40 operators, 168 classes loaded
- `railtram_import.py` built and committed with country pre-flight hard stop and idempotency

**Phase 2 role:** Importer owner — execution only, not decision-making.
Iguana runs dry-runs and applies on instruction. He does not decide what to enrich,
does not evaluate sources, and does not clear safety — those belong to Goblin, Aardvark,
and Prudence respectively.

No enrichment `--apply` without:
1. Aardvark note present for the source
2. Goblin sign-off on the field mappings
3. Prudence clearance on overwrite/safety risk
4. Explicit Trevor approval

Iguana is NOT on standby to absorb every new source file that appears. Each enrichment
pass is a deliberate decision, not a routine run.

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

**Phase 2 role:** Class/operator enrichment mapping owner.
Before any Phase 2 enrichment source is mapped to schema fields, Goblin reconciles:
- Class name aliases: does "ES44ACi" in the new source match "ES44ACi" in the DB?
  Are there spelling variants, abbreviations, or legacy names that need resolving?
- Operator aliases: does "PN" in the source map cleanly to "Pacific National" in the DB?
- Duplicate/conflict detection: if two sources give different values for the same field
  on the same class, Goblin flags it rather than silently picking one.
- Enrichment mapping sign-off: Goblin produces a field mapping document before Iguana
  runs any enrichment apply. This is the "enrichment ledger" — a table of
  source_value → DB_field → DB_row for every field being populated.

Goblin does NOT touch the database directly.
Goblin does NOT fetch source data — that is Aardvark and Seth's lane.
Goblin does NOT execute the apply — that is Iguana's lane.
Goblin does NOT clear safety — that is Prudence's lane.

---

## Critter Rule (TrainTrack)

A critter enters when:
1. A recurring job appears
2. The job has clear boundaries
3. The job produces evidence
4. The job will probably need automation later

Critters do NOT need dashboards, schedulers, or service wiring until their behaviour
is proven. The name and the job come first.
