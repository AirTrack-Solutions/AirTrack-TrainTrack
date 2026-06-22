# Railtram AU — Phase 2B Missing Class Enrichment Ledger
**Date:** 2026-06-22
**Author:** Aardvark (source notes) + Goblin (enrichment mapping)
**Scope:** The seven AU classes left NULL after Phase 2A (no Railtram page found at the slugs tried)
**Status:** TREVOR RULING APPLIED. Awaiting Prudence review + Iguana dry-run + Trevor apply approval.

---

## Why These Seven Were Missed in Phase 2A

Phase 2A tried simple slug patterns for each class (e.g. `/h-class`, `/p-class`, `/s-class`).
All returned 404. The classes page at `/locomotive-classes` was not consulted during Phase 2A.

The Phase 2B discovery: Railtram uses **operator-qualified slugs** for classes that appear
under the same letter across multiple unrelated locomotive lineages:
- `/h-class-sct-logistics` and `/h-class-various-operators` (two different H classes)
- `/p-class-aurizon` and `/p-class-various-operators` (two different P classes)
- `/s-class-aurizon` and `/s-class-various-operators` (two different S classes)
- `/dl-class-pacific-national` and `/dl-class-queensland-rail` (two different DL classes)
- `/1200-class-genesee-wyoming-australi` and `/1200-class-nrec` (two different 1200 classes)
- `/y-class-various-operators` (single Y class, operator-qualified slug)

The 2150 class has **no Railtram page** — absent from the `/locomotive-classes` index entirely.

---

## Critical Finding: Amalgamated Class Rows

Four of the seven DB class rows each contain locomotives from **two distinct, unrelated lineages**
sharing the same class letter. Railtram gives each lineage its own page. The TrainTrack DB has one
row per class letter.

| DB Class | Railtram pages | Loco numbers per lineage | Conflict fields |
|----------|---------------|--------------------------|----------------|
| 1200 | Aurizon (G12C, 1960, Clyde); NREC (GenSet, 2013, NREC) | 1203–4 / 1201–2 | manufacturer, introduced_year |
| H | SCT (EE SRKT, 1965, English Electric); Watco (EMD 645E, 1968, Clyde) | H2–H3,H5 / H1–H3,H5 | manufacturer, introduced_year |
| P | Aurizon (GE 7FDL, 1989, Goninan/GE); SSR (EMD 645E3, 1984, Clyde) | P2501–17 / P11–18,P21–23 | manufacturer, introduced_year |
| S | Aurizon (EMD 710G3B, 1998, Clyde Forrestfield); SSR (EMD 567C, 1957, Clyde Granville) | S3301–11 / S311,S312,S317 | manufacturer, introduced_year |

**type_id is NOT in conflict for any of these**: all components of all four classes are Diesel-electric.
All have diesel engines driving electric traction motors via generators.

**manufacturer and introduced_year ARE in conflict** — the two lineages within each class row
have different builders, different build dates, and different mechanical specifications.

**Goblin's recommendation**: Propose `type_id = Diesel-electric` for all four.
Hold `manufacturer` and `introduced_year` as unresolvable until Trevor decides whether to
split these class rows or accept a "lowest common denominator" value with a note.

---

## Trevor Ruling (2026-06-22)

**Amalgamated class rows (1200, H, P, S):**
Apply `type_id = Diesel-electric` only. Leave `manufacturer` and `introduced_year` NULL.
Reason: each DB class row combines multiple unrelated lineages. Setting manufacturer or
introduced_year would smuggle one lineage's values into a row that actually contains several,
making the data look more complete while quietly making it less truthful.

**Clean classes (DL, Y):**
Full enrichment approved — type_id, manufacturer, introduced_year from Railtram source.

**2150 class:**
Medium-confidence enrichment allowed from Wikipedia secondary source.
- type_id: Diesel-electric
- manufacturer: Clyde Engineering
- introduced_year: 1978
- Accepted because it aligns with known Queensland Rail 2150/2250 family context.
- Source note and confidence flag must remain in ledger.

**Scope constraint:** Do not restructure the DB in Phase 2B. Do not create new class rows.
Do not touch locomotives. The four amalgamated rows are flagged as a future modelling issue
(class name alone is not always a safe identity), but that is a Phase 3+ decision.

---

## Aardvark Source Notes

### Source A — Railtram.com.au (Operator-qualified class pages)
**Accessed:** 2026-06-22
**URLs:**
- `https://www.railtram.com.au/1200-class-genesee-wyoming-australi` — 1200 class, Aurizon (1203–4)
- `https://www.railtram.com.au/1200-class-nrec` — 1200 class, NREC/Watco (1201–2)
- `https://www.railtram.com.au/dl-class-pacific-national` — DL class, Pacific National (DL38–50)
- `https://www.railtram.com.au/h-class-sct-logistics` — H class, SCT Logistics (H2–3, H5)
- `https://www.railtram.com.au/h-class-various-operators` — H class, Watco Australia (H1–3, H5)
- `https://www.railtram.com.au/p-class-aurizon` — P class, Aurizon (P2501–17)
- `https://www.railtram.com.au/p-class-various-operators` — P class, SSR/various (P11–23)
- `https://www.railtram.com.au/s-class-aurizon` — S class, Aurizon (S3301–11)
- `https://www.railtram.com.au/s-class-various-operators` — S class, SSR/various (S302+)
- `https://www.railtram.com.au/y-class-various-operators` — Y class (Y115–Y174)

**Scope:** Each page covers one operator's fleet of a named class. Fields: road numbers, operator,
gauge, year of entry into service, number built, model, manufacturer, manufacturing location,
engine, traction power, wheel arrangement, weight, length. Reliability: high — Railtram is the
primary Aardvark-approved source for AU class enrichment (established in Phase 2A).
**Limitation:** Wix-rendered; static fetch used (raw HTML), confirmed to work for these pages.

### Source B — Wikipedia (Queensland Railways 2150 class)
**Accessed:** 2026-06-22
**URL:** `https://en.wikipedia.org/wiki/Queensland_Railways_2150_class`
**Scope:** Covers QR 2150 class — manufacturer, year, engine, type.
**Reliability:** Medium. Wikipedia is supporting evidence only. Consistent with known QR EMD-era
fleet pattern (Clyde Engineering Eagle Farm, 1978–79). No Railtram page available for cross-check.
**Limitation:** Single-source; no Railtram page exists for 2150 class.

---

## Summary

| Class | id | Locos | Railtram pages found | type_id resolvable | mfr resolvable | year resolvable | Overall |
|-------|----|-------|---------------------|--------------------|----------------|-----------------|---------|
| 1200  | 16 | 4 | 2 (conflicting lineages) | ✅ Diesel-electric | ❌ CONFLICT | ❌ CONFLICT | Partial |
| DL    | 98 | 13 | 1 (clean match) | ✅ Diesel-electric | ✅ Clyde Engineering | ✅ 1988 | Full |
| H     | 115 | 7 | 2 (conflicting lineages) | ✅ Diesel-electric | ❌ CONFLICT | ❌ CONFLICT | Partial |
| P     | 131 | 27 | 2 (conflicting lineages) | ✅ Diesel-electric | ❌ CONFLICT | ❌ CONFLICT | Partial |
| S     | 147 | 14 | 2 (conflicting lineages) | ✅ Diesel-electric | ❌ CONFLICT | ❌ CONFLICT | Partial |
| Y     | 169 | 17 | 1 (clean match) | ✅ Diesel-electric | ✅ Clyde Engineering | ✅ 1963 | Full |
| 2150  | 171 | 1 | 0 (Wikipedia only) | ✅ Diesel-electric | ⚠️ Medium | ⚠️ Medium | Partial |

**Fully resolvable (all 3 fields):** DL, Y — 2 classes
**type_id only (manufacturer/year conflict):** 1200, H, P, S — 4 classes
**Partial via Wikipedia (type + mfr + year, medium confidence):** 2150 — 1 class

---

## Class Entries

---

### 1200 class (id=16)

**DB road numbers:** 1201, 1202, 1203, 1204
**DB operators:** Aurizon (1203–4), Watco Australia (1201–2)

#### Lineage A — Aurizon 1200 class (1203–4)
- **Source:** `https://www.railtram.com.au/1200-class-genesee-wyoming-australi`
- **Origin:** Ex-WAGR A class, renumbered 1200 in private use
- **Manufacturer:** Clyde Engineering
- **Manufacturing location:** Granville, NSW
- **Model:** G12C
- **Engine:** EMD 567C
- **Wheel arrangement:** Co-Co
- **Year of entry into service:** 1960 (class first built; these 2 units entered service as A class 1965)
- **Type:** Diesel-electric

#### Lineage B — NREC 1200 class (1201–2)
- **Source:** `https://www.railtram.com.au/1200-class-nrec`
- **Origin:** NREC GenSet demonstration units, acquired by Watco Australia
- **Manufacturer:** National Railway Equipment Company
- **Manufacturing location:** Mt Vernon, Illinois, USA
- **Model:** 3GS24C-DE-AU
- **Engine:** Three Cummins QSK19C (GenSet)
- **Wheel arrangement:** Co-Co
- **Year of entry into service:** 2013
- **Type:** Diesel-electric

#### Goblin assessment
- **type_id proposed:** Diesel-electric (type_id=9) — both lineages are diesel-electric ✅
- **manufacturer proposed:** ❌ HOLD — Clyde Engineering vs National Railway Equipment Company. Irreconcilable in a single class row.
- **introduced_year proposed:** ❌ HOLD — 1960 vs 2013. A 53-year gap. Irreconcilable.
- **Confidence (type only):** High
- **Safe for Prudence (type_id only):** Yes
- **Unresolved:** manufacturer, introduced_year pending DB restructure decision

---

### DL class (id=98)

**DB road numbers:** DL38, DL39, DL40, DL41, DL42, DL43, DL44, DL45, DL46, DL47, DL49, DL50
**DB operators:** Pacific National, Queensland Rail

#### Source
- **URL:** `https://www.railtram.com.au/dl-class-pacific-national`
- **Railtram road numbers:** DL38–DL47, DL49–50 — **exact match to DB**
- **Operator:** Pacific National (transferred from Australian National via National Rail)
- **Manufacturer:** Clyde Engineering
- **Manufacturing location:** Kelso, NSW
- **Model:** AT42C
- **Engine:** EMD 710G3
- **Wheel arrangement:** Co-Co
- **Year of entry into service:** 1988
- **Type:** Diesel-electric

**Note on QR operator:** QR appears as an operator in the DB. The Railtram page lists Pacific National only. Road numbers DL38–50 are the Australian National/National Rail/Pacific National fleet. The QR DL class (DL1–4, Walkers, Gardner engine, 1939) has entirely different numbering — the QR listing against DL38+ is likely a data anomaly from the Phase 1 import. No action needed for class enrichment; flag for Phase 2 data review separately.

#### Goblin assessment
- **type_id proposed:** Diesel-electric (type_id=9) ✅
- **manufacturer proposed:** Clyde Engineering ✅
- **introduced_year proposed:** 1988 ✅
- **Confidence:** High — road numbers match exactly, single clear source
- **Safe for Prudence:** Yes
- **Unresolved:** None

---

### H class (id=115)

**DB road numbers:** H1, H2, H2, H3, H3, H5, H5 *(note: duplicate numbers — data anomaly)*
**DB operators:** SCT Logistics, Watco Australia

#### Lineage A — SCT Logistics H class (WA origin)
- **Source:** `https://www.railtram.com.au/h-class-sct-logistics`
- **Road numbers:** H2–3, H5 (standard gauge, Western Australia)
- **Origin:** First standard gauge diesels for WAGR; purchased by SCT for shunting; now stored
- **Manufacturer:** English Electric
- **Manufacturing location:** Rocklea, Qld
- **Model:** Unknown
- **Engine:** EE SRKT
- **Wheel arrangement:** Bo-Bo
- **Year of entry into service:** 1965
- **Type:** Diesel-electric

#### Lineage B — Watco Australia H class (VIC origin)
- **Source:** `https://www.railtram.com.au/h-class-various-operators`
- **Road numbers:** H1–H3, H5 (broad gauge, Victoria; ex-Victorian Railways hump yard shunters)
- **Origin:** Built as heavier version of T class for Melbourne hump yard; acquired by Watco 2023
- **Manufacturer:** Clyde Engineering
- **Manufacturing location:** Granville, NSW
- **Model:** G18B
- **Engine:** EMD 645E
- **Wheel arrangement:** Bo-Bo
- **Year of entry into service:** 1968
- **Type:** Diesel-electric

**Note on duplicate numbers:** The DB has H2, H2, H3, H3, H5, H5 — same numbers appear twice. This is consistent with two different locomotives (WA and VIC origin) carrying identical numbers. DB uniqueness constraint is `(country_code, operator_id, number)` — different operators would allow this. Not a class enrichment issue but worth flagging.

#### Goblin assessment
- **type_id proposed:** Diesel-electric (type_id=9) — both lineages are diesel-electric ✅
- **manufacturer proposed:** ❌ HOLD — English Electric vs Clyde Engineering. Irreconcilable.
- **introduced_year proposed:** ❌ HOLD — 1965 vs 1968. Gap is small but manufacturers differ so a blended year is misleading.
- **Confidence (type only):** High
- **Safe for Prudence (type_id only):** Yes
- **Unresolved:** manufacturer, introduced_year; also flag duplicate road numbers for data review

---

### P class (id=131)

**DB road numbers:** P11, P12, P14–P18, P21–P23 (SSR); P2501–P2517 (Aurizon)
**DB operators:** Aurizon, Southern Shorthaul Railroad

#### Lineage A — Aurizon P class (WA)
- **Source:** `https://www.railtram.com.au/p-class-aurizon`
- **Road numbers:** P2501–P2517
- **Origin:** First GE locomotive class in WA; mineral and grain traffic
- **Manufacturer:** Goninan/General Electric
- **Manufacturing location:** Bassendean, WA
- **Model:** CM25-8
- **Engine:** GE 7FDL
- **Wheel arrangement:** Co-Co
- **Year of entry into service:** 1989
- **Type:** Diesel-electric

#### Lineage B — V/Line P class / SSR (VIC)
- **Source:** `https://www.railtram.com.au/p-class-various-operators`
- **Road numbers:** P11–12, P14–18, P21–23
- **Origin:** Rebuilt from Victorian T class for V/Line passenger work 1984; later freight; acquired by SSR
- **Manufacturer:** Clyde Engineering
- **Manufacturing location:** Somerton, Vic.
- **Model:** G18HB-R
- **Engine:** EMD 645E3
- **Wheel arrangement:** Bo-Bo
- **Year of entry into service:** 1984
- **Type:** Diesel-electric

#### Goblin assessment
- **type_id proposed:** Diesel-electric (type_id=9) — both lineages are diesel-electric ✅
- **manufacturer proposed:** ❌ HOLD — Goninan/General Electric vs Clyde Engineering. Irreconcilable.
- **introduced_year proposed:** ❌ HOLD — 1989 vs 1984. Neither value is valid for both lineages.
- **Confidence (type only):** High
- **Safe for Prudence (type_id only):** Yes
- **Unresolved:** manufacturer, introduced_year pending DB restructure decision

---

### S class (id=147)

**DB road numbers:** S311, S312, S317 (Victorian Railways S class, SSR); S3301–S3311 (Aurizon WA)
**DB operators:** Aurizon, Southern Shorthaul Railroad

#### Lineage A — Aurizon S class (WA, narrow gauge)
- **Source:** `https://www.railtram.com.au/s-class-aurizon`
- **Road numbers:** S3301–S3311
- **Origin:** 1998 WA narrow gauge modernisation; mineral traffic Kwinana/Collie/Bunbury
- **Manufacturer:** Clyde Engineering
- **Manufacturing location:** Forrestfield, WA
- **Model:** JT42C
- **Engine:** EMD 710G3B
- **Wheel arrangement:** Co-Co
- **Year of entry into service:** 1998
- **Type:** Diesel-electric

#### Lineage B — Victorian Railways S class / SSR (VIC, standard gauge)
- **Source:** `https://www.railtram.com.au/s-class-various-operators`
- **Road numbers:** S302+; surviving units S311, S312, S317 now with SSR
- **Origin:** Victorian Railways Co-Co passenger/freight locos 1957–61; standard gauge Melbourne–Albury
- **Manufacturer:** Clyde Engineering
- **Manufacturing location:** Granville, NSW
- **Model:** 16C
- **Engine:** EMD 567C
- **Wheel arrangement:** Co-Co
- **Year of entry into service:** 1957
- **Type:** Diesel-electric

**Note:** Both lineages use Clyde Engineering as manufacturer — but different plants (Forrestfield WA vs Granville NSW), 41 years apart, with fundamentally different engines and traction power. Setting manufacturer to "Clyde Engineering" would be technically accurate but would mask the 1957 vs 1998 conflict. Year is irreconcilable.

#### Goblin assessment
- **type_id proposed:** Diesel-electric (type_id=9) — both lineages are diesel-electric ✅
- **manufacturer proposed:** ❌ HOLD — Both are Clyde Engineering but different plants/eras. The shared name is misleading without the year context. Hold pending DB split decision.
- **introduced_year proposed:** ❌ HOLD — 1957 vs 1998. A 41-year gap. Irreconcilable in a single field.
- **Confidence (type only):** High
- **Safe for Prudence (type_id only):** Yes
- **Unresolved:** manufacturer, introduced_year pending DB restructure decision

---

### Y class (id=169)

**DB road numbers:** Y115, Y119, Y124, Y129, Y134, Y142, Y147, Y148, Y151, Y152, Y156, Y157, Y161, Y163, Y169, Y171, Y174
**DB operators:** BlueScope Steel, Downer Rail, Ettamogah Rail Hub, Southern Shorthaul Railroad, V/Line Passenger

#### Source
- **URL:** `https://www.railtram.com.au/y-class-various-operators`
- **Railtram road numbers:** Y115, Y119, Y124, Y129, Y134, Y142, Y147–8, Y151–2, Y156–7, Y161, Y163, Y169, Y171, Y174 — **exact match to DB**
- **Manufacturer:** Clyde Engineering
- **Manufacturing location:** Granville, NSW
- **Model:** G6B
- **Engine:** EMD 567C (Y101–50); EMD 645E (Y151–75)
- **Wheel arrangement:** Bo-Bo
- **Year of entry into service:** 1963
- **Type:** Diesel-electric

#### Goblin assessment
- **type_id proposed:** Diesel-electric (type_id=9) ✅
- **manufacturer proposed:** Clyde Engineering ✅
- **introduced_year proposed:** 1963 ✅
- **Confidence:** High — road numbers match exactly, single clear source, 75-unit class well documented
- **Safe for Prudence:** Yes
- **Unresolved:** None

---

### 2150 class (id=171)

**DB road numbers:** 2158
**DB operators:** Queensland Rail

#### Source
- **No Railtram page found.** Class absent from Railtram `/locomotive-classes` index.
- **Wikipedia:** `https://en.wikipedia.org/wiki/Queensland_Railways_2150_class`
  - Manufacturer: Clyde Engineering
  - Manufacturing location: Eagle Farm, Qld
  - Year: 1978–1979
  - Type: Diesel-electric (EMD-powered, QR standard of the era)
- **Wikipedia reliability:** Medium — supporting source only. Consistent with QR fleet pattern of the late 1970s (same era as 2250 class: Clyde Engineering, Eagle Farm, EMD-powered).

#### Goblin assessment
- **type_id proposed:** Diesel-electric (type_id=9) — high confidence (QR EMD-era fleet, consistent with 2250 pilot class)
- **manufacturer proposed:** Clyde Engineering — medium confidence (Wikipedia; consistent with era)
- **introduced_year proposed:** 1978 — medium confidence (Wikipedia; single-source)
- **Confidence:** Medium (Wikipedia only, no Railtram page available)
- **Safe for Prudence:** Yes, with medium-confidence flag on manufacturer and introduced_year
- **Unresolved:** No Railtram page. If higher confidence is required, leave manufacturer/year NULL.

---

## Proposed Updates (Goblin sign-off)

### Full enrichment (type + manufacturer + introduced_year):

| id | name | type_id | type_name | manufacturer | introduced_year | confidence |
|----|------|---------|-----------|--------------|-----------------|------------|
| 98 | DL | 9 | Diesel-electric | Clyde Engineering | 1988 | High |
| 169 | Y | 9 | Diesel-electric | Clyde Engineering | 1963 | High |

### type_id only (manufacturer + year held — lineage conflict):

| id | name | type_id | type_name | manufacturer | introduced_year | note |
|----|------|---------|-----------|--------------|-----------------|------|
| 16 | 1200 | 9 | Diesel-electric | NULL (hold) | NULL (hold) | Two lineages: Clyde G12C 1960 + NREC GenSet 2013 |
| 115 | H | 9 | Diesel-electric | NULL (hold) | NULL (hold) | Two lineages: English Electric 1965 + Clyde 1968 |
| 131 | P | 9 | Diesel-electric | NULL (hold) | NULL (hold) | Two lineages: Goninan/GE 1989 + Clyde 1984 |
| 147 | S | 9 | Diesel-electric | NULL (hold) | NULL (hold) | Two lineages: Clyde Forrestfield 1998 + Clyde Granville 1957 |

### Partial enrichment (Wikipedia, medium confidence):

| id | name | type_id | type_name | manufacturer | introduced_year | confidence |
|----|------|---------|-----------|--------------|-----------------|------------|
| 171 | 2150 | 9 | Diesel-electric | Clyde Engineering | 1978 | Medium |

---

## Preview SQL (PREVIEW ONLY — do not execute)

```sql
-- PREVIEW ONLY. Not for execution. Awaiting Prudence review + Trevor approval.
-- Trevor ruling applied 2026-06-22.

-- Full enrichment (Railtram source, high confidence)
UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1988
WHERE id = 98 AND name = 'DL';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1963
WHERE id = 169 AND name = 'Y';

-- type_id ONLY (Trevor ruling: manufacturer + year held — amalgamated lineages)
-- 1200: Clyde G12C 1960 vs NREC GenSet 2013 — irreconcilable
UPDATE classes SET type_id = 9
WHERE id = 16 AND name = '1200';

-- H: English Electric 1965 vs Clyde 1968 — irreconcilable
UPDATE classes SET type_id = 9
WHERE id = 115 AND name = 'H';

-- P: Goninan/GE 1989 vs Clyde 1984 — irreconcilable
UPDATE classes SET type_id = 9
WHERE id = 131 AND name = 'P';

-- S: Clyde Forrestfield 1998 vs Clyde Granville 1957 — irreconcilable
UPDATE classes SET type_id = 9
WHERE id = 147 AND name = 'S';

-- Medium confidence (Wikipedia secondary source — Trevor accepted, note retained)
UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1978
WHERE id = 171 AND name = '2150';
```

---

## Risks and Warnings

1. **Amalgamated class rows (1200, H, P, S):** The DB has one class row per letter, but each of these corresponds to two distinct locomotive lineages with different manufacturers, build dates, and specifications. Setting manufacturer and introduced_year would require choosing one lineage over the other, which is misleading. Trevor should decide whether to split these class rows before Phase 2B apply.

2. **Duplicate road numbers in H class:** H2, H3, H5 appear twice in the DB (one per operator lineage). This is consistent with the two-lineage situation but may warrant investigation.

3. **DL class / QR operator anomaly:** The DB shows QR as an operator of DL38–50. The QR DL class (DL1–4, 1939, Walkers, Gardner engine) has entirely different numbers and specifications. The QR entries against DL38–50 are likely a Phase 1 import artefact.

4. **2150 class / single unit:** Only one unit (2158) exists. Single-unit class rows are unusual. The 2150 class had multiple units built (Railtram lists 2170 class as current QR narrow gauge); 2158 being the sole survivor is consistent with most being withdrawn.

5. **No Railtram page for 2150:** Wikipedia is the only available source. If higher confidence is required, leave manufacturer and introduced_year NULL until a better source is found.

---

## Unresolved Classes

None are unresolvable for type_id — all seven classes are Diesel-electric.
Four classes (1200, H, P, S) require a DB restructure decision before manufacturer/year can be set.
One class (2150) has medium-confidence manufacturer/year via Wikipedia.
