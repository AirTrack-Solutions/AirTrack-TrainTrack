# Research Note: Railtram.com.au — Locomotive Class Sub-pages

**Critter:** Archival Aardvark
**Source:** https://www.railtram.com.au/ (individual class sub-pages)
**URL pattern:** `https://www.railtram.com.au/{classname-slug}` — e.g. `/nr-class`, `/48-class`, `/c44-9w-class`
**Access date:** 2026-06-22
**Fetched via:** Static HTTP. Pages are Wix-hosted but sub-page body content renders in static HTML. No browser/JS execution required. (NB: The *number index* page at `/locomotive-number-indexes` is JS-rendered and requires Chrome — these class sub-pages are different and do not.)
**Status:** Sample confirmed — NR Class sub-page fetched and documented. Full batch not yet approved.

---

## Purpose

This source is to be used for **class-level enrichment only** in Phase 2A:

- `classes.type_id` (traction type — Diesel / Electric / Steam / etc.)
- `classes.manufacturer` (builder name as stated on page)
- `classes.introduced_year` (year of first entry into service)
- `classes.description` (narrative paragraph — Phase 2B only, style decisions needed first)

This source is **not** to be used for:

- Current operator assignments (`locomotives.operator_id`) — Railtram sub-pages list current operators but this is subject to change and is already captured in the Phase 1 roster seed. Do not overwrite.
- Current loco status (`locomotives.status`) — narrative describes stored/withdrawn units but not consistently enough to map to the status ENUM.
- Per-loco built year (`locomotives.built_year`) — pages give total fleet year, not per-unit build dates.
- Per-loco livery (`locomotives.livery`) — user field, not in source.
- Per-loco depot (`locomotives.depot_id`) — not in source.
- FMG SD70ACe-P6 records — hold remains in force. No SD70ACe-P6 sub-page to be fetched or used.

**Warning — two distinct Railtram sources, two distinct purposes:**
The Phase 1 roster seed came from the *number index* page — a consolidated roster cross-reference.
The Phase 2 enrichment source is the *individual class sub-pages* — spec and narrative per class.
These are different pages with different content and different reliability properties.
Do not confuse the two or assume consistency between them.

---

## Page Structure — Sample: NR Class

**URL fetched:** https://www.railtram.com.au/nr-class
**Fetched:** 2026-06-22, static HTTP

The sub-page returns structured labelled fields followed by a prose description. The label/value pattern is consistent and parseable.

### Fields present on NR Class page

| Page label | Value | Maps to |
|-----------|-------|---------|
| Road numbers | NR1–2, NR4–32, NR34–NR40, NR42–NR78, NR81–NR122 | Reference only — roster already imported |
| Operator | Pacific National | Reference only — already in DB |
| Gauge | 1435 mm | Not in TrainTrack schema currently |
| Year of entry into service | 1996 | `classes.introduced_year` ✅ |
| Number built | 120 | Not in TrainTrack schema currently |
| Model | Cv40-9i | Not in TrainTrack schema currently |
| Manufacturer | Goninan/General Electric | `classes.manufacturer` ✅ |
| Manufacturing location | Broadmeadow, NSW (NR1–60); Bassendean, WA (NR61–120) | Not in schema |
| Engine | GE 7FDL | Inferred → `classes.type_id` (see note below) |
| Traction power | 3000 kW | Not in TrainTrack schema currently |
| Wheel arrangement | Co-Co | Not in TrainTrack schema currently |
| Weight | 132.0 t | Not in TrainTrack schema currently |
| Length | 20.8 m | Not in TrainTrack schema currently |
| Description (prose) | Narrative paragraph | `classes.description` — Phase 2B only |

### Traction type note (important — Goblin task)

The sub-pages do **not** have a "Traction type: Diesel" field. Type must be **inferred** from the Engine field:
- `GE 7FDL` → diesel engine → `types.name = 'Diesel'`
- An electric class would have a different engine field (or no engine field, with an "Electrical system" field instead)
- Steam classes would show a steam-specific engine or boiler specification

Ledger Goblin must map each class's engine field (or class category) to the correct `types` row. This is not automatic — it requires judgment for ambiguous cases (e.g. diesel-electric vs electric, DMUs with diesel engines, dual-mode units).

### Data extracted from NR Class page (for reference)

```
introduced_year: 1996
manufacturer:    Goninan/General Electric
inferred_type:   Diesel
description:     The National Rail Corporation introduced the NR Class to service in
                 1996, with all 120 units in service by the end of 1997. NR3 was
                 damaged in an accident and later rebuilt as NR121, while NR80 was
                 involved in a collision and returned to service as NR122. NR33 was
                 scrapped following a collision. In addition to widespread freight
                 service on standard gauge tracks throughout mainland Australia, they
                 are also used in hauling the Indian Pacific, The Ghan, Great Southern
                 and The Overland passenger trains.
```

---

## Fetch Assessment

**Is static fetch sufficient?** Yes, for class sub-pages. Full content including all labelled fields and the prose description returned on static HTTP. Wix serves the body text server-side for these pages.

**Seth required?** No. Seth remains on standby. This entire Phase 2A enrichment batch can be executed with plain static fetches.

**Parseable?** Yes, with care. The label/value structure is consistent across the NR sample. Labels appear to be fixed across classes (same labels, different values). A parser that reads `{Label}:\n{Value}` pairs from the page body would cover most cases. Edge cases: some classes may omit fields (e.g. a steam class won't have an "Engine" field in the same sense). Goblin should flag any class where a field is absent unexpectedly.

**Rate limiting:** Not tested yet. Fetching 168 pages in rapid succession would be impolite. Batch fetch should be paced (e.g. 1–2 pages per second with a small delay). Seth's rate-limiting principles apply even though Seth himself is not needed.

---

## Scope Limitations

1. **Operator truth is snapshot-only.** Railtram updates its pages over time but the access date is our truth boundary. Any operator or status data on these pages reflects Railtram's view at 2026-06-22.

2. **Not all 168 DB classes may have a matching sub-page.** The DB was built from the number index, not the classes page. Some operator-specific classes (e.g. the "FIE" class for Fletcher International Exports) may not have a Railtram sub-page at all. Goblin should flag any class with no matching sub-page — do not assume the class is wrong, assume the sub-page doesn't exist.

3. **Duplicate class names.** Nine class names appear twice on Railtram (different operators — e.g. "P Class Aurizon" / "P Class Various"). In the DB these are single class rows. If two sub-pages give different manufacturer or year values for what appears to be the same class name, Goblin must flag for manual decision.

4. **DB class names may not match URL slugs exactly.** The DB has "C44-9W", "SD70ACe/LC", "GE L80T" etc. URL slug derivation needs care — spaces become hyphens, slashes may become hyphens or be omitted, capitalisation is lowercased. Goblin must maintain a class_name → URL slug mapping rather than auto-generating slugs.

5. **No per-loco build year on these pages.** Pages give total fleet size and entry-into-service year but not individual unit build dates.

---

## Next Step (Phase 2A Step 2 — pending Trevor approval)

Ledger Goblin builds the enrichment ledger for a pilot set of 5 classes: NR, 48, 81, C44-9W, 2250. For each:
- Confirm sub-page URL slug
- Fetch page
- Extract: introduced_year, manufacturer, inferred type
- Map type to `types.name` row
- Record any conflicts or absent fields

No apply. No import. Ledger only.

---

*Note written 2026-06-22 by Archival Aardvark. No database changes. No imports. Evidence gathering only.*
