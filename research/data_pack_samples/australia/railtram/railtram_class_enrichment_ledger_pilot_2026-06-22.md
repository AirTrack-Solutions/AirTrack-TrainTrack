# Railtram AU — Goblin Prototype Enrichment Ledger (Pilot)
**Date:** 2026-06-22
**Author:** Goblin (Phase 2A Step 2)
**Status:** PILOT — 5 classes only. Not applied to DB. Awaiting Prudence clearance + Trevor approval.

---

## Purpose

This ledger captures Goblin's findings from the pilot fetch of 5 class sub-pages on railtram.com.au.
It documents the source data, the engine → type inference rules derived from it, the proposed DB updates,
and all flags requiring resolution before anything is applied.

The 5 pilot classes are: NR, 48, 81, C44-9W, 2250.
These were chosen to cover enough variety to surface alias weirdness and type inference edge cases
without consuming all 168 classes in one unverified pass.

---

## Engine → Type Inference Rules

Railtram class sub-pages do not have a "Traction Type" field. Type must be inferred from the Engine field.
Goblin's working mapping table (expand as new classes are fetched):

| Engine string (on sub-page) | Inferred type | DB type_id |
|-----------------------------|---------------|------------|
| GE 7FDL                     | Diesel        | 2          |
| Alco 251B                   | Diesel        | 2          |
| EMD 645E3B                  | Diesel        | 2          |
| EMD 645E3C                  | Diesel        | 2          |
| EMD 12-710G3B-T2            | Diesel        | 2          |

All pilot classes map to Diesel. No Electric, Steam, or DMU/EMU cases encountered in this pilot set.
A broader pass over the full 168 classes will be needed to build out the full mapping table.

**Rule for unknowns:** If Goblin encounters an Engine string not in this table, it raises a flag and does
NOT attempt to infer a type. Inference proceeds only for confirmed mappings.

---

## Pilot Class Data

### NR Class

| Field             | Source value                       | Proposed DB value |
|-------------------|------------------------------------|-------------------|
| DB class name     | NR                                 | —                 |
| DB class id       | 128                                | —                 |
| Railtram URL      | /nr-class                          | —                 |
| Introduced        | 1996                               | 1996              |
| Manufacturer      | Goninan/General Electric           | Goninan/General Electric |
| Engine            | GE 7FDL                            | —                 |
| Inferred type     | Diesel                             | type_id = 2       |

**Goblin flags:** None. Clean entry. URL slug matches class name directly.

---

### 48 Class

| Field             | Source value                       | Proposed DB value |
|-------------------|------------------------------------|-------------------|
| DB class name     | 48                                 | —                 |
| DB class id       | 46                                 | —                 |
| Railtram URL      | /48-class                          | —                 |
| Introduced        | 1959                               | 1959              |
| Manufacturer      | AE Goodwin                         | AE Goodwin        |
| Engine            | Alco 251B                          | —                 |
| Inferred type     | Diesel                             | type_id = 2       |

**Goblin flags:**
- **PARSING ARTIFACT — Operator field:** When extracting structured label/value pairs from the 48 Class
  sub-page, the Operator field returned "1435 mm" (the Gauge value) instead of the actual operator name.
  This is an off-by-one in the label/value extraction — the 48 Class page layout differs slightly from
  NR Class. The real operator is GrainCorp (visible in the page image caption).
  This does not affect the three enrichment fields (introduced_year, manufacturer, type_id) which were
  read correctly. However, it signals that the batch parser will need per-page structure validation
  before scaling to all 168 classes.

---

### 81 Class

| Field             | Source value                       | Proposed DB value |
|-------------------|------------------------------------|-------------------|
| DB class name     | 81                                 | —                 |
| DB class id       | 57                                 | —                 |
| Railtram URL      | /81-class                          | —                 |
| Introduced        | 1982                               | 1982              |
| Manufacturer      | Clyde Engineering                  | Clyde Engineering |
| Engine            | EMD 645E3B                         | —                 |
| Inferred type     | Diesel                             | type_id = 2       |

**Goblin flags:** None. Clean entry.

---

### C44-9W Class — ⚠ ALIAS CONFLICT — REQUIRES RESOLUTION

| Field             | Source value (FMG)                  | Source value (RTIO)                  | Proposed DB value |
|-------------------|------------------------------------|--------------------------------------|-------------------|
| DB class name     | C44-9W                             | C44-9W                               | —                 |
| DB class id       | 4                                  | 4                                    | —                 |
| Railtram URL (FMG)| /c44-9w-class-fortescue-metals-group | —                                  | —                 |
| Railtram URL (RTIO)| —                                 | /c44-9w-class-rio-tinto-iron-ore    | —                 |
| Introduced (FMG)  | 2007                               | —                                    | (not used — see note) |
| Introduced (RTIO) | —                                  | 1995                                 | 1995 ✅            |
| Manufacturer      | General Electric                   | General Electric                     | General Electric  |
| Engine            | GE 7FDL                            | GE 7FDL                              | —                 |
| Inferred type     | Diesel                             | Diesel                               | type_id = 2       |

**Goblin flags:**
- **ALIAS CONFLICT — introduced_year: RESOLVED.** Two Railtram sub-pages exist for a single DB class
  row (C44-9W, id=4). The RTIO page gives 1995; the FMG page gives 2007. These are separate operator
  orders of the same class, hence different delivery dates.
  **Trevor's ruling (2026-06-22):** Use 1995 (RTIO). The DB has one shared C44-9W class row, so
  `introduced_year` represents the earliest known Australian entry into service for the class — not
  the later introduction date for one operator fleet. The FMG 2007 figure is preserved here as an
  operator-specific source note; it is not written to the class row and no operator-specific class
  variants are created in this phase.
- **URL slug edge case:** The /c44-9w-class URL returns 404. Correct slugs must be operator-qualified.
  The batch parser must handle this — it cannot assume slug = class name for all classes.
- **Manufacturer and type are unambiguous** — both sub-pages agree. All three enrichment fields
  (type_id, manufacturer, introduced_year) are now resolved and ready to write.

---

### 2250 Class

| Field             | Source value                            | Proposed DB value |
|-------------------|-----------------------------------------|-------------------|
| DB class name     | 2250                                    | —                 |
| DB class id       | 170                                     | —                 |
| Railtram URL      | /2250-class                             | —                 |
| Introduced        | 2004                                    | 2004              |
| Manufacturer      | Clyde Engineering / Queensland Rail     | Clyde Engineering / Queensland Rail |
| Engine            | EMD 645E3C                              | —                 |
| Inferred type     | Diesel                                  | type_id = 2       |

**Goblin flags:** None. Clean entry. Dual manufacturer attribution (Clyde/QR) is accurate per source.

---

## Proposed DB Updates — Pilot Classes

These updates are PROPOSED. They are not applied. They require Prudence clearance + explicit Trevor approval.

```sql
-- Phase 2A pilot: class-level enrichment (type_id, manufacturer, introduced_year)
-- 5 classes: NR, 48, 81, C44-9W, 2250
-- Generated by Goblin 2026-06-22
-- REQUIRES: Trevor approval + Prudence clearance before apply

UPDATE classes SET type_id = 2, manufacturer = 'Goninan/General Electric', introduced_year = 1996
WHERE id = 128 AND name = 'NR';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin', introduced_year = 1959
WHERE id = 46 AND name = '48';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1982
WHERE id = 57 AND name = '81';

-- C44-9W: all three fields — introduced_year = 1995 (RTIO, earliest AU introduction)
-- FMG operator-specific introduction year (2007) is documented in ledger; not written to class row
UPDATE classes SET type_id = 2, manufacturer = 'General Electric', introduced_year = 1995
WHERE id = 4 AND name = 'C44-9W';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering / Queensland Rail', introduced_year = 2004
WHERE id = 170 AND name = '2250';
```

**Note on C44-9W:** introduced_year = 1995 (RTIO). Trevor's ruling: the shared class row
should reflect the earliest known Australian introduction. The FMG 2007 figure is an operator-specific
delivery date, documented in this ledger as a source note only. No operator-specific class rows created.

---

## Summary of Goblin Flags

| Class  | Flag                                              | Blocking? |
|--------|---------------------------------------------------|-----------|
| 48     | Operator field parse artifact (Gauge value returned) | No — does not affect enrichment fields |
| C44-9W | Two sub-pages, conflicting introduced_year (2007 vs 1995) | **RESOLVED** — 1995 (RTIO) used; 2007 (FMG) documented as operator-specific note |
| C44-9W | URL slug requires operator qualifier (/c44-9w-class returns 404) | Noted — batch parser must handle |
| All    | All pilot classes are Diesel — type diversity not tested | Noted — not a bug, limitation of pilot set |

---

## Pilot Outcome

- 5 classes fetched from Railtram class sub-pages
- All 5 map cleanly to Diesel (type_id = 2)
- 4 of 5 classes have clean, unambiguous enrichment data ready to write
- C44-9W introduced_year conflict resolved: 1995 (RTIO) written to class row; 2007 (FMG) documented as operator-specific note
- 1 parsing quirk found (48 Class operator field) — does not affect this phase's target fields
- Engine → type mapping table seeded with 5 confirmed entries

**Goblin's verdict:** The pipeline works. The data is good enough to proceed with the clean 4 once
the C44-9W introduced_year question is answered. Recommend Trevor decide on C44-9W and then green-light
the full pilot apply.

---

## Before Any Apply

All four gates must be passed:
1. Aardvark source note on file — ✅ `railtram_class_subpages_2026-06-22.md`
2. Goblin ledger on file — ✅ this document
3. Prudence clearance — ⬜ not yet run
4. Explicit Trevor approval — ⬜ not yet given

Do not run UPDATE statements until all four gates are green.

---

*Ledger written 2026-06-22. Pilot phase only — 5 of 168 classes.*
*C44-9W introduced_year resolved 2026-06-22 (Trevor). Next step: Prudence review + Trevor approval to apply.*
