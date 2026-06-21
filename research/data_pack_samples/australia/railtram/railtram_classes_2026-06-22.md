# Research Note: Railtram.com.au — Locomotive Classes Page

**Source:** https://www.railtram.com.au/locomotive-classes  
**Access date:** 2026-06-22  
**Fetched via:** static HTTP (curl-equivalent). Page is Wix-generated; body text and link list are in static HTML. Dynamic content (if any) was not needed for this page.  
**Status:** Complete — all class links extracted.

---

## Page Purpose and Scope

The Locomotive Classes page is an index of Australian locomotive classes currently in active ownership and operation. It is NOT a historical record or a heritage archive.

### Explicit scope statements (verbatim from page)

> "The listings provided on these pages describe the locomotives currently owned and in operation with the various passenger and freight rail operators throughout Australia on the three main gauges. Most of the locomotives listed are operational on a regular basis."

> "A small number are stored but are retained in the ownership of various operators. Some locomotives are stored temporarily and may return to service in the future. Others have been withdrawn from service and will eventually be scrapped. Stored locomotives are included because some will eventually return to service."

> "Not included are many locomotives used on local industrial railways, such as those that service the sugar cane railway networks in Queensland. Also not included are steam, diesel and electric locomotives retained solely for historical purposes."

> "Nevertheless, some units owned by preservation groups are hired at times to freight operators."

> "Road numbers listed refer to those locomotives currently in existence."

> "The year of entry into service refers to the year the first member of the class officially entered service."

### Gauges covered
Narrow (1067 mm), Standard (1435 mm), Broad (1600 mm).

### Excluded
- Industrial / sugar cane railway locomotives
- Heritage/preservation-only units (unless hired to freight operators)

---

## Class Entries Found

**Total class entries: 175** (some classes appear twice where the same designation is used by two operators — e.g. 1200 Class Aurizon / 1200 Class NREC, DC Class Aurizon / DC Class Bowen Rail, DL Class Pacific National / DL Class Queensland Rail, etc.)

### Sample — first 20 entries (in page order)

| # | Class Name | Page URL slug |
|---|------------|---------------|
| 1 | 11 Class | /11-class |
| 2 | 14 Class | /14-class |
| 3 | 22 Class | /22-class |
| 4 | 32 Class | /32-class |
| 5 | 44 Class | /44-class |
| 6 | 45 Class | /45-class |
| 7 | 48 Class | /48-class |
| 8 | 49 Class | /49-class |
| 9 | 71 Class | /71-class |
| 10 | 73 Class | /73-class |
| 11 | 80 Class | /80-class |
| 12 | 81 Class | /81-class |
| 13 | 82 Class | /82-class |
| 14 | 83 Class | /83-class |
| 15 | 88 Class | /88-class |
| 16 | 90 Class | /90-class |
| 17 | 92 Class | /92-class |
| 18 | 93 Class | /93-class |
| 19 | 94 Class | /94-class |
| 20 | 422 Class | /422-class |

### Full class list (all 175)

Numeric classes (54): 11, 14, 22, 32, 44, 45, 48, 49, 71, 73, 80, 81, 82, 83, 88, 90, 92, 93, 94, 422, 442, 500, 600, 830, 900, 1100, 1200 (Aurizon), 1200 (NREC), 1300, 1600, 1720, 1900, 2050, 2170, 2170F, 2300, 2300D, 2400, 2470, 2700, 2800, 2900, 3200, 3551, 3700, 3800, 4000, 4100, 4600, 5000, 5020, 6000, 6020.

Alpha/model classes (121): A, AB, AC, AC44C6M, ACB, ACC, ACD, ACN, ALF, AN, B, BEL, BL, BMACC, BRM, C, C36-7M, C44-9W (Fortescue Metals Group), C44-9W (Rio Tinto Iron Ore), CD, CEY, CF, CK, CLF, CLP, CM, Comalco GT26C, CS, CSR, DAZ, DBZ, DC (Aurizon), DC (Bowen Rail Company), DFZ, DH, DL (Pacific National), DL (Queensland Rail), DQ, DR, EL, ES44ACi, ES44DCi, FIE, FJ, FL, FQ, G, GE L80T, GL, GM1, GM12, GML, GPU, GWA, GWB, GWN, GWU, H (SCT Logistics), H (Watco Australia), HL, J, JT42C, K, KA, L, LDP, MAN, MM, MP27CN, MP33C, MP33CN, MRL, N, NR, ORN, ORQ, P (Aurizon), P (Various operators), PA, PB, PH, PHC, PL, PN, PRL, PRQ, Q, QBX, QE, QL, RHA, RL, RT, S (Aurizon), S (Southern Shorthaul Railroad), SCT, SD70ACe, SD70ACe/LC, SD70ACe/LCi, SD90MAC-H Phase II, SSR, T, TA, TL, TR, TT, TT2, UM20C, V, VL, WH, WRA, WRB, WRC, WRD, WRE, X, X200, XR, XRB, XRN, Y.

---

## Visible Fields on This Page

The index page itself provides **class name only** (hyperlinked). No additional fields are present here. All further data (manufacturer, year introduced, traction type, operator, road numbers, specifications) is on each individual class sub-page (e.g. `/11-class`, `/a-class`, etc.).

---

## Mapping to TrainTrack Schema

| Railtram field | TrainTrack table/column | Notes |
|----------------|------------------------|-------|
| Class name | `classes.name` | Direct. Where same class name is shared by two operators, the operator name is disambiguated in parentheses on Railtram — e.g. "P Class (Aurizon)" vs "P Class (Various operators)". |
| Traction type (on sub-page) | `types.name` | Will require lookup against `types` table (Diesel, Electric, etc.) |
| Year of entry into service (on sub-page) | `classes.introduced_year` | Railtram uses year of first member entering service — matches `introduced_year` semantics. |
| Manufacturer (on sub-page) | `classes.manufacturer` | Explicitly stated on sub-pages. |
| Description / spec text (on sub-page) | `classes.description` | Free text — sub-pages contain detailed narrative. |
| Country | `classes.country_code` | Always AU for this dataset. |
| Operator(s) (on sub-page) | `operators.name` / `operators.id` | Sub-pages list current operators. Operator must exist in `operators` table first. |
| Road numbers (on sub-page) | `locomotives.number` | Listed per-class on sub-pages. This is the key data for the number index (separate page). |
| Status (on sub-page) | `locomotives.status` | Active/stored/withdrawn distinguishable from narrative. Exact status language varies. |

---

## Limitations

1. **This page is an index only.** No field data beyond class name is available here — all spec and roster data is on individual class sub-pages. A full import requires crawling all 175 sub-pages.

2. **No road numbers on this page.** The `/locomotive-number-indexes` page provides a consolidated number-to-class cross-reference. That page is JS-rendered (Wix dynamic) and requires a real browser to extract. Static fetch returns only a shell.

3. **Duplicate class names.** At least 9 class names appear twice (for different operators). TrainTrack's `classes` table has no operator linkage — the disambiguation parenthetical would need to be included in `classes.name` or a separate `operator_id` added to the class at import time.

4. **No status field at class level.** Railtram does not give a class-level status — only the narrative on each sub-page distinguishes active from stored units. Status belongs on individual `locomotives` rows, not `classes`.

5. **Heritage units occasionally included.** Railtram notes that some preservation units are included if they work freight. These may map to `status='preserved'` in TrainTrack but will appear alongside active/stored entries without a clear flag.

6. **No year-withdrawn or scrapped date.** Railtram does not provide withdrawal dates — only mentions that some are stored or will be scrapped.

7. **Sub-page structure not yet confirmed.** The field structure (column layout, table vs prose) on individual class sub-pages has not been examined. This is required before any importer can be designed.

---

## Proposed Next Steps (for discussion — not approved)

- Fetch and document one sample class sub-page (e.g. `/nr-class` — NR Class, large fleet, well-known) to confirm field structure.
- Fetch `/locomotive-number-indexes` via browser (Chrome extension) to confirm column layout and assess per-row vs per-range format.
- Once sub-page structure is confirmed, design class and locomotive import schemas.

---

## Copyright Notice

Railtram.com.au is a privately maintained reference site. No explicit copyright notice was visible in the static page content retrieved. Standard copyright applies. Data should be used for personal/research reference only; bulk automated scraping should be approached with care.

