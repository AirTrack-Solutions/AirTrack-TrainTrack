# TrainTrack Phase 2A — Pilot Enrichment Result
**Date:** 2026-06-22
**Status:** COMPLETE ✅

---

## What Was Applied

Five class rows updated in the live TrainTrack DB. No locomotive rows touched directly.
No new rows created. No code changes. No commit required (DB-only apply).

| Class  | type_id | manufacturer                        | introduced_year |
|--------|---------|-------------------------------------|----------------|
| 2250   | 2       | Clyde Engineering / Queensland Rail | 2004           |
| 48     | 2       | AE Goodwin                          | 1959           |
| 81     | 2       | Clyde Engineering                   | 1982           |
| C44-9W | 2       | General Electric                    | 1995           |
| NR     | 2       | Goninan/General Electric            | 1996           |

All five updated via: `UPDATE classes SET type_id=2, manufacturer=..., introduced_year=... WHERE id=N AND name='X'`

`type_id = 2` = Diesel in the `types` table. FK constraint confirmed before apply.

---

## Verification Checks (post-apply)

| Check | Result |
|-------|--------|
| Rows affected (5 UPDATEs) | 1 each — 5 total |
| All five class rows show correct values | ✅ |
| Type inheritance: NR locos (sample NR113, NR81, NR47) | ✅ Diesel via class JOIN |
| Type inheritance: Aurizon 2260 → class 2250 | ✅ Diesel |
| QR 2158 → class 2150 type | NULL — expected (2150 not in pilot scope) |
| Total locomotives | 2,633 ✅ unchanged |
| Total classes | 168 ✅ unchanged |
| FMG SD70ACe-P6 (722–731) | 0 rows ✅ hold intact |
| Git working tree | clean ✅ |

---

## Notes

**QR 2158 / class 2150 NULL type:** This is a correct and expected result. Class 2150 was not in the
pilot scope. Its type_id remains NULL until a subsequent enrichment pass covers it. The NULL confirms
the pilot stayed inside its painted lines — no out-of-scope classes were touched.

**C44-9W introduced_year:** 1995 written to the shared class row per Trevor's ruling (2026-06-22).
Rationale: introduced_year on a shared class row represents the earliest known Australian entry into
service for the class. RTIO received the first C44-9W units in 1995; FMG's order followed in 2007.
The 2007 figure is documented in the Goblin ledger as an operator-specific source note only.

**Engine → type inference:** All five pilot classes used the GE/Alco/EMD engine strings confirmed in
the Goblin ledger. Type was inferred from engine field (no explicit traction type field on Railtram
sub-pages). Mapping table seeded with 5 confirmed entries — to be expanded during full batch.

---

## Gate Record

| Gate              | Status |
|-------------------|--------|
| Aardvark source note | ✅ `railtram_class_subpages_2026-06-22.md` |
| Goblin pilot ledger  | ✅ `railtram_class_enrichment_ledger_pilot_2026-06-22.md` |
| Prudence review      | ✅ All 7 safety checks passed |
| Iguana dry-run       | ✅ All 8 dry-run checks passed, zero writes |
| Trevor apply approval| ✅ Explicit approval given 2026-06-22 |
| Post-apply verification | ✅ All checks passed |

---

## Next Step: Full Class Enrichment Ledger

The pilot proved the pipeline. Next move is Goblin building the full ledger for all remaining classes
(163 classes, excluding the 5 already enriched).

Before that happens:
- Same four gates apply: Aardvark → Goblin → Prudence → Iguana dry-run → Trevor approval
- Goblin should expand the engine → type mapping table as new engine strings are encountered
- Goblin should flag any further URL slug edge cases (operator-qualified slugs, 404s, etc.)
- Do not batch-apply until the full ledger is reviewed

Do not touch FMG SD70ACe-P6 (722–731) until external fleet verification is complete.

---

*Result documented 2026-06-22. Pilot phase closed.*
