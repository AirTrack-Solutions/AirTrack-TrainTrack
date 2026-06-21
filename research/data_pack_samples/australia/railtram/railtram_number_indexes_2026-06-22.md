# Research Note: Railtram.com.au — Locomotive Number Indexes Page

**Source:** https://www.railtram.com.au/locomotive-number-indexes  
**Access date:** 2026-06-22  
**Fetched via:** Claude in Chrome (JS-rendered). Static curl returns a shell only — this page requires browser rendering.  
**Status:** Complete — full page extracted.

---

## Page Purpose and Scope

The Locomotive Number Indexes page is a consolidated cross-reference listing all Australian locomotives from the Locomotive Classes dataset, sorted by road number (numeric first, then alphabetic). Its stated purpose is to allow an observer who has noted a locomotive's road number and operator to identify its class.

> "An observer seeing a locomotive of an unknown class can note the locomotive number and owner/operator, and then use the Locomotive Number Indexes to determine its class."

The scope is identical to the classes page: locomotives currently owned and in operation with Australian passenger and freight operators. Heritage/preservation-only units excluded unless hired to freight operators.

---

## Column Structure

Three columns, no status column:

| Road Numbers | Operator | Class |
|---|---|---|
| (range or group) | (abbreviated code) | (class name) |

Road numbers are **NOT listed individually**. Each row is a range or comma-separated group sharing the same operator and class. A single operator may appear in multiple rows for the same class if their fleet is split across non-contiguous number blocks.

**Road number suffixes observed:** D, H, F, A, L — likely denote sub-variants or build batches (e.g. 2300D vs 2300, 2470H vs 2470D). Not explained on the page.

---

## Operator Abbreviation Table

The page includes a full operator lookup table (42 entries):

| Index Name | Full Operator Name |
|---|---|
| Aurizon | Aurizon |
| BHP | BHP |
| BMACC | BHP Mitsubishi Alliance |
| BlueScope | BlueScope Steel |
| Bowen | Bowen Rail Company |
| CBH | CBH Group |
| Centennial | Centennial Coal |
| Cockburn | Cockburn Cement |
| Crawfords | Crawfords Freightlines |
| Downer | Downer Rail |
| Ettamogah | Ettamogah Rail Hub |
| FIE | Fletcher International Exports |
| FMG | Fortescue Metals Group |
| Gemco | Gemco Rail |
| GrainCorp | GrainCorp |
| Greentrains | Greentrains |
| JRW | Junee Railway Workshop |
| Manildra | Manildra Group |
| MRG | Magnetic Rail Group |
| MTS | Metro Trains Sydney |
| NREC | National Railway Equipment Company |
| ORA | One Rail Australia |
| PN | Pacific National |
| Progress | Progress Rail |
| Qube | Qube Logistics |
| QR | Queensland Rail |
| RP | RailPower |
| Rail First | Rail First Asset Management |
| RTA | Rio Tinto Aluminium |
| RTIO | Rio Tinto Iron Ore |
| RHA | Roy Hill Australia |
| SCT | SCT Logistics |
| SMR | South Maitland Railways |
| SSR | Southern Shorthaul Railroad |
| ST | Sydney Trains |
| Swift | Swift Transport |
| TasRail | TasRail |
| Transperth | Transperth |
| UGL | UGL |
| V/Line | V/Line Passenger |
| Watco | Watco Australia |
| Whitehaven | Whitehaven Coal |

Note: "CT" appears as operator for CSR001–CSR024 but is **not in this table** — likely an error or unlisted abbreviation.

---

## Row Counts

- Numeric index (numbers): ~141 rows
- Alphabetic index (letters): ~180+ rows
- **Total: ~320+ rows** across both sections

Well over 100 rows — the full page was extracted.

---

## Sample Rows (first 20 from numeric index)

| Road Numbers | Operator | Class |
|---|---|---|
| 001–002, 004–005, 007–018 | FMG | C44-9W |
| 32, 33 | Aurizon | 32 |
| 49–50 | Cockburn | GE L80T |
| 53 | Rail First | 500 |
| 55, 57 | JRW | GE L80T |
| 101–128 | FMG | AC44C6M |
| 602–603 | SSR | 600 |
| 701–721 | FMG | SD70ACe/LC |
| 722–731 | FMG | SD70ACe-P6 |
| 851 | Aurizon | 830 |
| 852 | JRW | 830 |
| 859 | Aurizon | 830 |
| 864 | Qube | 830 |
| 869 | SSR | 830 |
| 872 | Qube | 830 |
| 873 | Aurizon | 830 |
| 901–902, 907–909 | FMG | SD90MAC-H Phase II |
| 901–907 | Aurizon | 900 |
| 1101–1108 | Qube | 1100 |
| 1104 | Downer | 11 |

---

## Mapping to TrainTrack Schema

| Railtram field | TrainTrack table/column | Notes |
|---|---|---|
| Road Numbers (individual, expanded from ranges) | `locomotives.number` | Ranges must be expanded during import. Each individual unit gets its own row. |
| Operator (abbreviated) | `operators.id` | Abbreviation must be resolved via the operator table above before import. Operator must pre-exist in `operators` table. |
| Class | `classes.id` | Class name must match an existing `classes` row. |
| (status) | `locomotives.status` | No status column on this page — all listed units are implied active or stored. Default to `active`; individual unit status requires sub-page data or manual assignment. |
| (type) | `locomotives.type_id` | Not present here — comes from the class sub-page. |
| (country) | `locomotives.country_code` | Always AU for this dataset. |

---

## Notable Observations and Anomalies

1. **2250 Class appears in number index but not on the classes page.** Three units: 2260–2262, 2269, 2275 (Aurizon). The classes page has 2170, 2170F, 2300, 2300D but no 2250. This suggests the number index may be more current than the classes index, or it's a data discrepancy on Railtram's end.

2. **SD70ACe-P6 variant appears but is not in the classes list.** Rows for FMG 722–731 reference this class — the classes page lists SD70ACe, SD70ACe/LC, and SD70ACe/LCi but not "SD70ACe-P6". Likely an unlinked sub-variant.

3. **2150 Class referenced but not on classes page.** Entry: 2158 QR 2150. Only 2170/2170F appear on classes page.

4. **Rows not in the classes page require a TrainTrack class entry before import** — either create the class row or skip the affected units. A pre-import gap check is essential.

5. **Apparent page typos observed:**
   - `2822– 850` — should read `2822–2850` (Aurizon 2800 class)
   - `48s33` and `48s36` — likely `4833` and `4836` (SSR 48 Class; lowercase 's' appears to be a rendering artefact)
   - `48211–4828` (GrainCorp 48) — appears truncated, likely `48211–48280` or similar
   - `2332D–3D` — likely `2332D–2333D` (Aurizon 2300D)
   - `4601–16` (Bowen 4600) — likely `4601–4616`

6. **Same road numbers used by multiple operators.** The page explicitly notes this (e.g. FMG 901–909 and Aurizon 901–907 overlap). Operator is the disambiguating key. TrainTrack's `UNIQUE KEY uq_loco_number (number)` on the `locomotives` table will **reject duplicates** — this constraint will need revisiting before any AU import that mixes operators with overlapping number ranges.

7. **No status column.** All listed units are current (as per the classes page scope). No withdrawn/scrapped units appear here.

8. **No copyright notice** was visible on the rendered page.

---

## Critical Schema Issue for Import Design

TrainTrack's `locomotives` table enforces `UNIQUE KEY uq_loco_number (number)`. The AU dataset has confirmed overlapping road numbers across operators (e.g. 901 appears for both FMG and Aurizon). This uniqueness constraint makes sense for a single-operator install but **breaks multi-operator AU imports**. Resolution options to discuss:

- Make the unique key composite: `(number, operator_id)` or `(number, country_code)`  
- Prefix road numbers with operator code at import (e.g. `FMG-901`, `AUR-901`)  
- Accept the constraint and require manual deconfliction  
- Document as a known ticket for discussion before any import begins

---

## Limitations

1. Road numbers are ranges/groups per row — expansion logic required for individual unit import.
2. No traction type, manufacturer, year, or specification data on this page — comes from class sub-pages.
3. No status per unit — implied current from page scope.
4. Operator abbreviations require resolution via the lookup table above before import.
5. At least 3 class names in the number index have no corresponding class page (2250, SD70ACe-P6, 2150).
6. Several apparent typos in road number ranges require manual review before import.
7. The unique road number constraint in TrainTrack schema is incompatible with the AU multi-operator dataset as-is.

---

## Proposed Next Steps (for discussion — not approved)

- Cross-check the 3 missing classes (2250, SD70ACe-P6, 2150) against one or more class sub-pages to confirm they exist.
- Design decision on the `uq_loco_number` constraint before any importer work begins.
- Fetch one sample class sub-page (e.g. NR Class — large PN fleet, well-documented) to confirm sub-page field structure.
- With both research notes committed, the source shape is now documented well enough to begin importer design discussion.

