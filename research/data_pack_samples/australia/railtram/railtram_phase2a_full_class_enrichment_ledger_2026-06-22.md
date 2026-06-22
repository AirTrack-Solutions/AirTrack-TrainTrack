# Railtram AU — Phase 2A Full Class Enrichment Ledger
**Date:** 2026-06-22
**Author:** Goblin (Phase 2A full batch)
**Status:** LEDGER ONLY. No DB changes. Awaiting Prudence review + Trevor approval.

---

## Summary

| Item | Count |
|------|-------|
| Total classes in DB (excl. pilot 5) | 163 |
| Pages found (slug matched) | 156 |
| Pages not found (404, all slugs tried) | 7 |
| Safe for Prudence review | 156 |
| Flagged (notes, review) | 1 |
| Manufacturer >100 chars | 0 |
| Type: Diesel | 150 |
| Type: Electric | 6 |
| Type: Steam | 0 |
| Pilot classes (already applied) | 5 |
| **Proposed updates (safe)** | **156** |

---

## Engine to Type Mapping Table

| Engine string / pattern | Inferred type | type_id | Confidence |
|-------------------------|---------------|---------|------------|
| GE 7FDL / 7FDL-16EFI | Diesel | 2 | High |
| GE GEVO / GEVO-12 | Diesel | 2 | High |
| GE V250 | Diesel | 2 | High |
| GE prefix (general) | Diesel | 2 | High |
| EMD 6xx / 7xx series | Diesel | 2 | High |
| Electro-Motive Diesel | Diesel | 2 | High |
| Alco 251 series | Diesel | 2 | High |
| English Electric / EE prefix | Diesel | 2 | High |
| Cummins (any series) | Diesel | 2 | High |
| MTU Friedrichshafen | Diesel | 2 | High |
| Deutz | Diesel | 2 | High |
| Rolls-Royce | Diesel | 2 | High |
| Volvo EU | Diesel | 2 | High |
| Fordson | Diesel | 2 | High |
| Cummins QSK series | Diesel | 2 | High |
| Wabtec (AC44C6M) | Diesel | 2 | Medium (engine blank; inferred from model + manufacturer) |
| electric (any) | Electric | 3 | High |
| steam (any) | Steam | 1 | High |

---

## Classes Not Found on Railtram (7)

No page found at simple slug or any operator-qualified variant.
These 7 classes are excluded from proposed updates.

| DB id | Class | Slugs tried | Action |
|-------|-------|-------------|--------|
| 16 | 1200 | 1200-class, 1200-class-fortescue-metals-group, 1200-class-rio-tinto, 1200-class-qr | Excluded — no source |
| 98 | DL | dl-class, dl-class-kiwirail, dl-class-nz | Excluded — no source |
| 115 | H | h-class, h-class-westrail, h-class-public-transport-authority | Excluded — no source |
| 131 | P | p-class, p-class-westrail, p-class-public-transport-authority | Excluded — no source |
| 147 | S | s-class, s-class-westrail, s-class-public-transport-authority, s-class-act | Excluded — no source |
| 169 | Y | y-class, y-class-westrail, y-class-v-line, y-class-queensland-rail | Excluded — no source |
| 171 | 2150 | 2150-class, 2150-class-queensland-rail, 2150-class-qr | Excluded — no source |

---

## Full Class Ledger (163 classes)

### 32 (id=5)
- **Source:** `https://www.railtram.com.au/32-class`
- **Raw engine:** `Deutz diesel A8L714`
- **type_id:** 2 (Diesel)
- **manufacturer:** Orenstein & Koppel
- **introduced_year:** 1963
- **Safe for Prudence:** Yes

### GE L80T (id=6)
- **Source:** `https://www.railtram.com.au/ge-l80t-class`
- **Raw engine:** `Rolls Royce C6TFL (49–50); Cummins NT855-L2 (55); Cummins NT855-L4 (57); Cummins NT380 (D2)`
- **type_id:** 2 (Diesel)
- **manufacturer:** Goninan
- **introduced_year:** 1960
- **Safe for Prudence:** Yes

### 500 (id=7)
- **Source:** `https://www.railtram.com.au/500-class`
- **Raw engine:** `EE SRKT`
- **type_id:** 2 (Diesel)
- **manufacturer:** English Electric/South Australian Railways
- **introduced_year:** 1964
- **Safe for Prudence:** Yes

### AC44C6M (id=8)
- **Source:** `https://www.railtram.com.au/ac44c6m-class`
- **Raw engine:** `(blank)`
- **type_id:** 2 (Diesel)
- **manufacturer:** Wabtec Corporation
- **introduced_year:** 2022
- **Safe for Prudence:** Yes
- **Flag:** ENGINE NOTE: engine field blank on Railtram page. Type=Diesel inferred from model name (AC44C6M = AC = AC traction diesel-electric, Wabtec/GE product line) and manufacturer (Wabtec Corporation). Flagged for Prudence review.

### 600 (id=9)
- **Source:** `https://www.railtram.com.au/600-class`
- **Raw engine:** `Alco 251B`
- **type_id:** 2 (Diesel)
- **manufacturer:** AE Goodwin
- **introduced_year:** 1965
- **Safe for Prudence:** Yes

### SD70ACe/LC (id=10)
- **Source:** `https://www.railtram.com.au/sd70ace-lc-class`
- **Raw engine:** `EMD 710G3C-T2`
- **type_id:** 2 (Diesel)
- **manufacturer:** Electro-Motive Diesel
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### 830 (id=11)
- **Source:** `https://www.railtram.com.au/830-class`
- **Raw engine:** `Alco 251B`
- **type_id:** 2 (Diesel)
- **manufacturer:** AE Goodwin
- **introduced_year:** 1959
- **Safe for Prudence:** Yes

### SD90MAC-H Phase II (id=12)
- **Source:** `https://www.railtram.com.au/sd90mac-h-phase-ii-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Electro-Motive Diesel
- **introduced_year:** 1999
- **Safe for Prudence:** Yes

### 900 (id=13)
- **Source:** `https://www.railtram.com.au/900-class`
- **Raw engine:** `Alco 251B`
- **type_id:** 2 (Diesel)
- **manufacturer:** AE Goodwin
- **introduced_year:** 1991
- **Safe for Prudence:** Yes

### 1100 (id=14)
- **Source:** `https://www.railtram.com.au/1100-class`
- **Raw engine:** `EMD 645E3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** National Railway Equipment Company
- **introduced_year:** 2011
- **Safe for Prudence:** Yes

### 11 (id=15)
- **Source:** `https://www.railtram.com.au/11-class`
- **Raw engine:** `Caterpillar D398 Series B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Walkers Ltd
- **introduced_year:** 1969
- **Safe for Prudence:** Yes

### 1200 (id=16)
- **Source:** MISSING
- **Proposed updates:** none
- **Safe for Prudence:** No

### 1300 (id=17)
- **Source:** `https://www.railtram.com.au/1300-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Morris Knudsen Australia
- **introduced_year:** 1993
- **Safe for Prudence:** Yes

### 14 (id=18)
- **Source:** `https://www.railtram.com.au/14-class`
- **Raw engine:** `EMD 645E3`
- **type_id:** 2 (Diesel)
- **manufacturer:** Nydqvist & Holm AB
- **introduced_year:** 2006
- **Safe for Prudence:** Yes

### 1600 (id=19)
- **Source:** `https://www.railtram.com.au/1600-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1971
- **Safe for Prudence:** Yes

### 1720 (id=20)
- **Source:** `https://www.railtram.com.au/1720-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Commonwealth Engineering/Clyde Engineering
- **introduced_year:** 1966
- **Safe for Prudence:** Yes

### 1900 (id=21)
- **Source:** `https://www.railtram.com.au/1900-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 2003
- **Safe for Prudence:** Yes

### DQ (id=22)
- **Source:** `https://www.railtram.com.au/dq-class`
- **Raw engine:** `EMD 645C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Hutt Railway Workshops
- **introduced_year:** 1998
- **Safe for Prudence:** Yes

### 2050 (id=23)
- **Source:** `https://www.railtram.com.au/2050-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Commonwealth Engineering
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### 2170F (id=24)
- **Source:** `https://www.railtram.com.au/2170f-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Commonwealth Engineering/Clyde Engineering
- **introduced_year:** 1982
- **Safe for Prudence:** Yes

### 2170 (id=25)
- **Source:** `https://www.railtram.com.au/2170-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Commonwealth Engineering/Clyde Engineering
- **introduced_year:** 1982
- **Safe for Prudence:** Yes

### 22 (id=26)
- **Source:** `https://www.railtram.com.au/22-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1969
- **Safe for Prudence:** Yes

### 2300 (id=27)
- **Source:** `https://www.railtram.com.au/2300-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering/Queensland Rail
- **introduced_year:** 1997
- **Safe for Prudence:** Yes

### 2300D (id=28)
- **Source:** `https://www.railtram.com.au/2300d-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering/Queensland Rail
- **introduced_year:** 1997
- **Safe for Prudence:** Yes

### 2400 (id=29)
- **Source:** `https://www.railtram.com.au/2400-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering/Commonwealth Engineering
- **introduced_year:** 1977
- **Safe for Prudence:** Yes

### 2470 (id=30)
- **Source:** `https://www.railtram.com.au/2470-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Commonwealth Engineering/Clyde Engineering
- **introduced_year:** 1980
- **Safe for Prudence:** Yes

### 2700 (id=31)
- **Source:** `https://www.railtram.com.au/2700-class`
- **Raw engine:** `EMD 710G`
- **type_id:** 2 (Diesel)
- **manufacturer:** Progress Rail
- **introduced_year:** 2019
- **Safe for Prudence:** Yes

### 2800 (id=32)
- **Source:** `https://www.railtram.com.au/2800-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** Goninan/General Electric
- **introduced_year:** 1995
- **Safe for Prudence:** Yes

### 2900 (id=33)
- **Source:** `https://www.railtram.com.au/2900-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Commonwealth Engineering; Aurizon
- **introduced_year:** 2022
- **Safe for Prudence:** Yes

### 3200 (id=34)
- **Source:** `https://www.railtram.com.au/3200-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** Goninan/General Electric
- **introduced_year:** 1995
- **Safe for Prudence:** Yes

### 3551 (id=35)
- **Source:** `https://www.railtram.com.au/3551-class`
- **Raw engine:** `25 kV electric`
- **type_id:** 3 (Electric)
- **manufacturer:** Walkers Limited
- **introduced_year:** 2003
- **Safe for Prudence:** Yes

### 45 (id=36)
- **Source:** `https://www.railtram.com.au/45-class`
- **Raw engine:** `Alco 251B`
- **type_id:** 2 (Diesel)
- **manufacturer:** AE Goodwin
- **introduced_year:** 1962
- **Safe for Prudence:** Yes

### 3700 (id=37)
- **Source:** `https://www.railtram.com.au/3700-class`
- **Raw engine:** `25 kV electric`
- **type_id:** 3 (Electric)
- **manufacturer:** United Group Rail/Siemens
- **introduced_year:** 2005
- **Safe for Prudence:** Yes

### 3800 (id=38)
- **Source:** `https://www.railtram.com.au/3800-class`
- **Raw engine:** `25 kV electric`
- **type_id:** 3 (Electric)
- **manufacturer:** Siemens Mobility
- **introduced_year:** 2008
- **Safe for Prudence:** Yes

### 4000 (id=39)
- **Source:** `https://www.railtram.com.au/4000-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **introduced_year:** 2000
- **Safe for Prudence:** Yes

### 4100 (id=40)
- **Source:** `https://www.railtram.com.au/4100-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **introduced_year:** 2007
- **Safe for Prudence:** Yes

### SD70ACe/LCi (id=41)
- **Source:** `https://www.railtram.com.au/sd70ace-lci-class`
- **Raw engine:** `EMD 710G3C-T2`
- **type_id:** 2 (Diesel)
- **manufacturer:** Electro-Motive Diesel (4314–23, 4334–46, 4356–39, 4441–71, 4473); Progress Rail (4374–4499)
- **introduced_year:** 2005
- **Safe for Prudence:** Yes

### SD70ACe (id=42)
- **Source:** `https://www.railtram.com.au/sd70ace-class`
- **Raw engine:** `EMD 710G3C-T2`
- **type_id:** 2 (Diesel)
- **manufacturer:** Electro-Motive Diesel
- **introduced_year:** 2008
- **Safe for Prudence:** Yes

### DC (id=43)
- **Source:** `https://www.railtram.com.au/dc-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 2001
- **Safe for Prudence:** Yes

### 44 (id=44)
- **Source:** `https://www.railtram.com.au/44-class`
- **Raw engine:** `Alco 251B`
- **type_id:** 2 (Diesel)
- **manufacturer:** AE Goodwin
- **introduced_year:** 1957
- **Safe for Prudence:** Yes

### 4600 (id=45)
- **Source:** `https://www.railtram.com.au/4600-class`
- **Raw engine:** `EMD 16-710G3C-T3`
- **type_id:** 2 (Diesel)
- **manufacturer:** Progress Rail
- **introduced_year:** 2021
- **Safe for Prudence:** Yes

### 49 (id=47)
- **Source:** `https://www.railtram.com.au/49-class`
- **Raw engine:** `EMD 567CR`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1960
- **Safe for Prudence:** Yes

### 5000 (id=48)
- **Source:** `https://www.railtram.com.au/5000-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** United Group Rail/General Electric
- **introduced_year:** 2005
- **Safe for Prudence:** Yes

### 5020 (id=49)
- **Source:** `https://www.railtram.com.au/5020-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2010
- **Safe for Prudence:** Yes

### C36-7M (id=50)
- **Source:** `https://www.railtram.com.au/c36-7m-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** Goninan/General Electric
- **introduced_year:** 1987
- **Safe for Prudence:** Yes

### 6000 (id=51)
- **Source:** `https://www.railtram.com.au/6000-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** United Group Rail
- **introduced_year:** 2009
- **Safe for Prudence:** Yes

### 6020 (id=52)
- **Source:** `https://www.railtram.com.au/6020-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### 71 (id=53)
- **Source:** `https://www.railtram.com.au/71-class`
- **Raw engine:** `25 kV electric`
- **type_id:** 3 (Electric)
- **manufacturer:** Siemens Mobility
- **introduced_year:** 2009
- **Safe for Prudence:** Yes

### 73 (id=54)
- **Source:** `https://www.railtram.com.au/73-class`
- **Raw engine:** `Caterpillar D379B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Walkers Limited
- **introduced_year:** 1970
- **Safe for Prudence:** Yes

### 80 (id=55)
- **Source:** `https://www.railtram.com.au/80-class`
- **Raw engine:** `Alco 251CE`
- **type_id:** 2 (Diesel)
- **manufacturer:** Commonwealth Engineering
- **introduced_year:** 1978
- **Safe for Prudence:** Yes

### ES44DCi (id=56)
- **Source:** `https://www.railtram.com.au/es44dci-class`
- **Raw engine:** `GE GEVO`
- **type_id:** 2 (Diesel)
- **manufacturer:** General Electric
- **introduced_year:** 2007
- **Safe for Prudence:** Yes

### 82 (id=58)
- **Source:** `https://www.railtram.com.au/82-class`
- **Raw engine:** `EMD 710G3A`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1994
- **Safe for Prudence:** Yes

### 83 (id=59)
- **Source:** `https://www.railtram.com.au/83-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2008
- **Safe for Prudence:** Yes

### 88 (id=60)
- **Source:** `https://www.railtram.com.au/88-class`
- **Raw engine:** `MTU Freidrichshafen 20V4000R43`
- **type_id:** 2 (Diesel)
- **manufacturer:** CSR Ziyang Locomotive Company
- **introduced_year:** 2014
- **Safe for Prudence:** Yes

### 90 (id=61)
- **Source:** `https://www.railtram.com.au/90-class`
- **Raw engine:** `EMD 710G3A`
- **type_id:** 2 (Diesel)
- **manufacturer:** Electro-Motive Diesel (9001–31); Downer EDI (9032–5)
- **introduced_year:** 1994
- **Safe for Prudence:** Yes

### ES44ACi (id=62)
- **Source:** `https://www.railtram.com.au/es44aci-class`
- **Raw engine:** `GE V250`
- **type_id:** 2 (Diesel)
- **manufacturer:** General Electric
- **introduced_year:** 2014
- **Safe for Prudence:** Yes

### 92 (id=63)
- **Source:** `https://www.railtram.com.au/92-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** United Group Rail
- **introduced_year:** 2008
- **Safe for Prudence:** Yes

### 93 (id=64)
- **Source:** `https://www.railtram.com.au/93-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### 94 (id=65)
- **Source:** `https://www.railtram.com.au/94-class`
- **Raw engine:** `GEVO-12`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2025
- **Safe for Prudence:** Yes

### 422 (id=66)
- **Source:** `https://www.railtram.com.au/422-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1969
- **Safe for Prudence:** Yes

### 442 (id=67)
- **Source:** `https://www.railtram.com.au/442-class`
- **Raw engine:** `Alco 251C`
- **type_id:** 2 (Diesel)
- **manufacturer:** AE Goodwin (44201–44234); Commonwealth Engineering (44235–44240)
- **introduced_year:** 1971
- **Safe for Prudence:** Yes

### A (id=68)
- **Source:** `https://www.railtram.com.au/a-class`
- **Raw engine:** `EMD 645E3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1984
- **Safe for Prudence:** Yes

### AB (id=69)
- **Source:** `https://www.railtram.com.au/ab-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1969
- **Safe for Prudence:** Yes

### AC (id=70)
- **Source:** `https://www.railtram.com.au/ac-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** United Group Rail
- **introduced_year:** 2009
- **Safe for Prudence:** Yes

### ACB (id=71)
- **Source:** `https://www.railtram.com.au/acb-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2011
- **Safe for Prudence:** Yes

### ACC (id=72)
- **Source:** `https://www.railtram.com.au/acc-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2013
- **Safe for Prudence:** Yes

### ACD (id=73)
- **Source:** `https://www.railtram.com.au/acd-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2022
- **Safe for Prudence:** Yes

### ACN (id=74)
- **Source:** `https://www.railtram.com.au/acn-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **introduced_year:** 2011
- **Safe for Prudence:** Yes

### ALF (id=75)
- **Source:** `https://www.railtram.com.au/alf-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Morris Knudsen Australia
- **introduced_year:** 1994
- **Safe for Prudence:** Yes

### AN (id=76)
- **Source:** `https://www.railtram.com.au/an-class`
- **Raw engine:** `EMD 710G3A`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1992
- **Safe for Prudence:** Yes

### B (id=77)
- **Source:** `https://www.railtram.com.au/b-class`
- **Raw engine:** `EMD 567B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1952
- **Safe for Prudence:** Yes

### BEL (id=78)
- **Source:** `https://www.railtram.com.au/bel-class`
- **Raw engine:** `1500 V electric/battery`
- **type_id:** 3 (Electric)
- **manufacturer:** CRRC ZhuZhou Locomotive Company
- **introduced_year:** 2018
- **Safe for Prudence:** Yes

### BL (id=79)
- **Source:** `https://www.railtram.com.au/bl-class`
- **Raw engine:** `EMD 645E3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1984
- **Safe for Prudence:** Yes

### BMACC (id=80)
- **Source:** `https://www.railtram.com.au/bmacc-class`
- **Raw engine:** `25 kV electric`
- **type_id:** 3 (Electric)
- **manufacturer:** Siemens Mobility
- **introduced_year:** 2013
- **Safe for Prudence:** Yes

### BRM (id=81)
- **Source:** `https://www.railtram.com.au/brm-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Southern Shorthaul Railroad
- **introduced_year:** 2013
- **Safe for Prudence:** Yes

### C (id=82)
- **Source:** `https://www.railtram.com.au/c-class`
- **Raw engine:** `EMD 645E3`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1977
- **Safe for Prudence:** Yes

### MP27CN (id=83)
- **Source:** `https://www.railtram.com.au/mp27cn-class`
- **Raw engine:** `Cummins QSK60`
- **type_id:** 2 (Diesel)
- **manufacturer:** Motive Power Inc.
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### MP33CN (id=84)
- **Source:** `https://www.railtram.com.au/mp33cn-class`
- **Raw engine:** `Cummins QSK78`
- **type_id:** 2 (Diesel)
- **manufacturer:** Motive Power Inc.
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### MP33C (id=85)
- **Source:** `https://www.railtram.com.au/mp33c-class`
- **Raw engine:** `Cummins QSK78`
- **type_id:** 2 (Diesel)
- **manufacturer:** Motive Power Inc.
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### CD (id=86)
- **Source:** `https://www.railtram.com.au/cd-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** Goninan/General Electric
- **introduced_year:** 1989
- **Safe for Prudence:** Yes

### CEY (id=87)
- **Source:** `https://www.railtram.com.au/cey-class`
- **Raw engine:** `GE 7FDL-16`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### CF (id=88)
- **Source:** `https://www.railtram.com.au/cf-class`
- **Raw engine:** `GE 7FDL-16`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2011
- **Safe for Prudence:** Yes

### CK (id=89)
- **Source:** `https://www.railtram.com.au/ck-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1994
- **Safe for Prudence:** Yes

### CLF (id=90)
- **Source:** `https://www.railtram.com.au/clf-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Morris Knudsen Australia
- **introduced_year:** 1993
- **Safe for Prudence:** Yes

### CLP (id=91)
- **Source:** `https://www.railtram.com.au/clp-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Morris Knudsen Australia
- **introduced_year:** 1993
- **Safe for Prudence:** Yes

### CM (id=92)
- **Source:** `https://www.railtram.com.au/cm-class`
- **Raw engine:** `Cummins QSK78`
- **type_id:** 2 (Diesel)
- **manufacturer:** Motive Power Inc.
- **introduced_year:** 2013
- **Safe for Prudence:** Yes

### CS (id=93)
- **Source:** `https://www.railtram.com.au/cs-class`
- **Raw engine:** `Volvo EU`
- **type_id:** 2 (Diesel)
- **manufacturer:** Windhoff
- **introduced_year:** 2002
- **Safe for Prudence:** Yes

### DAZ (id=94)
- **Source:** `https://www.railtram.com.au/daz-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1972
- **Safe for Prudence:** Yes

### DBZ (id=95)
- **Source:** `https://www.railtram.com.au/dbz-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1982
- **Safe for Prudence:** Yes

### DFZ (id=96)
- **Source:** `https://www.railtram.com.au/dfz-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering/Queensland Rail
- **introduced_year:** 2008
- **Safe for Prudence:** Yes

### DH (id=97)
- **Source:** `https://www.railtram.com.au/dh-class`
- **Raw engine:** `Caterpillar D353E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Walkers Limited
- **introduced_year:** 1966
- **Safe for Prudence:** Yes

### DL (id=98)
- **Source:** MISSING
- **Proposed updates:** none
- **Safe for Prudence:** No

### DR (id=99)
- **Source:** `https://www.railtram.com.au/dr-class`
- **Raw engine:** `EMD645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1971
- **Safe for Prudence:** Yes

### EL (id=100)
- **Source:** `https://www.railtram.com.au/el-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** Goninan/General Electric
- **introduced_year:** 1990
- **Safe for Prudence:** Yes

### FIE (id=101)
- **Source:** `https://www.railtram.com.au/fie-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2015
- **Safe for Prudence:** Yes

### FJ (id=102)
- **Source:** `https://www.railtram.com.au/fj-class`
- **Raw engine:** `EMD 567C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1966
- **Safe for Prudence:** Yes

### FL (id=103)
- **Source:** `https://www.railtram.com.au/fl-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1970
- **Safe for Prudence:** Yes

### FQ (id=104)
- **Source:** `https://www.railtram.com.au/fq-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2003
- **Safe for Prudence:** Yes

### G (id=105)
- **Source:** `https://www.railtram.com.au/g-class`
- **Raw engine:** `EMD 645E3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1984
- **Safe for Prudence:** Yes

### GL (id=106)
- **Source:** `https://www.railtram.com.au/gl-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** Goninan/General Electric
- **introduced_year:** 2003
- **Safe for Prudence:** Yes

### GM1 (id=107)
- **Source:** `https://www.railtram.com.au/gm1-class`
- **Raw engine:** `EMD 567B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1951
- **Safe for Prudence:** Yes

### GM12 (id=108)
- **Source:** `https://www.railtram.com.au/gm12-class`
- **Raw engine:** `EMD 567C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1955
- **Safe for Prudence:** Yes

### GML (id=109)
- **Source:** `https://www.railtram.com.au/gml-class`
- **Raw engine:** `EMD 710G3A`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1990
- **Safe for Prudence:** Yes

### GPU (id=110)
- **Source:** `https://www.railtram.com.au/gpu-class`
- **Raw engine:** `Alco 251B`
- **type_id:** 2 (Diesel)
- **manufacturer:** AE Goodwin
- **introduced_year:** 2011
- **Safe for Prudence:** Yes

### GWA (id=111)
- **Source:** `https://www.railtram.com.au/gwa-class`
- **Raw engine:** `EMD 710G3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2011
- **Safe for Prudence:** Yes

### GWB (id=112)
- **Source:** `https://www.railtram.com.au/gwb-class`
- **Raw engine:** `EMD 710G3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Progress Rail
- **introduced_year:** 2019
- **Safe for Prudence:** Yes

### GWN (id=113)
- **Source:** `https://www.railtram.com.au/gwn-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Evans Deakin Industries/EMD
- **introduced_year:** 2013
- **Safe for Prudence:** Yes

### GWU (id=114)
- **Source:** `https://www.railtram.com.au/gwu-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2012
- **Safe for Prudence:** Yes

### H (id=115)
- **Source:** MISSING
- **Proposed updates:** none
- **Safe for Prudence:** No

### HL (id=116)
- **Source:** `https://www.railtram.com.au/hl-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1969
- **Safe for Prudence:** Yes

### J (id=117)
- **Source:** `https://www.railtram.com.au/j-class`
- **Raw engine:** `EMD 567C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1966
- **Safe for Prudence:** Yes

### K (id=118)
- **Source:** `https://www.railtram.com.au/k-class`
- **Raw engine:** `EE 12CSVT`
- **type_id:** 2 (Diesel)
- **manufacturer:** English Electric
- **introduced_year:** 1966
- **Safe for Prudence:** Yes

### KA (id=119)
- **Source:** `https://www.railtram.com.au/ka-class`
- **Raw engine:** `EE 12CSVT`
- **type_id:** 2 (Diesel)
- **manufacturer:** English Electric
- **introduced_year:** 1971
- **Safe for Prudence:** Yes

### Comalco GT26C (id=120)
- **Source:** `https://www.railtram.com.au/comalco-gt26c-class`
- **Raw engine:** `EMD 645E3`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1972
- **Safe for Prudence:** Yes

### L (id=121)
- **Source:** `https://www.railtram.com.au/l-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering; Commonwealth Engineering
- **introduced_year:** 1967
- **Safe for Prudence:** Yes

### LDP (id=122)
- **Source:** `https://www.railtram.com.au/ldp-class`
- **Raw engine:** `EMD 710G3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2008
- **Safe for Prudence:** Yes

### RT (id=123)
- **Source:** `https://www.railtram.com.au/rt-class`
- **Raw engine:** `Fordson`
- **type_id:** 2 (Diesel)
- **manufacturer:** Victorian Railways
- **introduced_year:** 1932
- **Safe for Prudence:** Yes

### MAN (id=124)
- **Source:** `https://www.railtram.com.au/man-class`
- **Raw engine:** `EMD 710`
- **type_id:** 2 (Diesel)
- **manufacturer:** Progess Rail
- **introduced_year:** 2024
- **Safe for Prudence:** Yes

### MM (id=125)
- **Source:** `https://www.railtram.com.au/mm-class`
- **Raw engine:** `EMD 567CR`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1961
- **Safe for Prudence:** Yes

### MRL (id=126)
- **Source:** `https://www.railtram.com.au/mrl-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL/General Electric
- **introduced_year:** 2014
- **Safe for Prudence:** Yes

### N (id=127)
- **Source:** `https://www.railtram.com.au/n-class`
- **Raw engine:** `EMD 645E3C (N451–60); EMD 645E3B (N461–75)`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1986
- **Safe for Prudence:** Yes

### ORN (id=129)
- **Source:** `https://www.railtram.com.au/orn-class`
- **Raw engine:** `EMD 710`
- **type_id:** 2 (Diesel)
- **manufacturer:** Progress Rail
- **introduced_year:** 2022
- **Safe for Prudence:** Yes

### ORQ (id=130)
- **Source:** `https://www.railtram.com.au/orq-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **introduced_year:** 2025
- **Safe for Prudence:** Yes

### P (id=131)
- **Source:** MISSING
- **Proposed updates:** none
- **Safe for Prudence:** No

### PA (id=132)
- **Source:** `https://www.railtram.com.au/pa-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** Goninan/General Electric
- **introduced_year:** 1996
- **Safe for Prudence:** Yes

### PB (id=133)
- **Source:** `https://www.railtram.com.au/pb-class`
- **Raw engine:** `Two QSK19C`
- **type_id:** 2 (Diesel)
- **manufacturer:** National Railway Equipment Company
- **introduced_year:** 2014
- **Safe for Prudence:** Yes

### PH (id=134)
- **Source:** `https://www.railtram.com.au/ph-class`
- **Raw engine:** `GE P616`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2019
- **Safe for Prudence:** Yes

### PHC (id=135)
- **Source:** `https://www.railtram.com.au/phc-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL/General Electric
- **introduced_year:** 2016
- **Safe for Prudence:** Yes

### PL (id=136)
- **Source:** `https://www.railtram.com.au/pl-class`
- **Raw engine:** `Alco 251B`
- **type_id:** 2 (Diesel)
- **manufacturer:** AE Goodwin
- **introduced_year:** 1998
- **Safe for Prudence:** Yes

### PN (id=137)
- **Source:** `https://www.railtram.com.au/pn-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2004
- **Safe for Prudence:** Yes

### PRL (id=138)
- **Source:** `https://www.railtram.com.au/prl-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering/Queensland Rail
- **introduced_year:** 2021
- **Safe for Prudence:** Yes

### PRQ (id=139)
- **Source:** `https://www.railtram.com.au/prq-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **introduced_year:** 2025
- **Safe for Prudence:** Yes

### Q (id=140)
- **Source:** `https://www.railtram.com.au/q-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1997
- **Safe for Prudence:** Yes

### QBX (id=141)
- **Source:** `https://www.railtram.com.au/qbx-class`
- **Raw engine:** `MTU Freidrichshafen 20V4000R43L`
- **type_id:** 2 (Diesel)
- **manufacturer:** CSR Ziyang Locomotive Company
- **introduced_year:** 2016
- **Safe for Prudence:** Yes

### QE (id=142)
- **Source:** `https://www.railtram.com.au/qe-class`
- **Raw engine:** `EMD 710G3C-T3`
- **type_id:** 2 (Diesel)
- **manufacturer:** Progress Rail
- **introduced_year:** 2024
- **Safe for Prudence:** Yes

### QL (id=143)
- **Source:** `https://www.railtram.com.au/ql-class`
- **Raw engine:** `7FDL-16EFI`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2021
- **Safe for Prudence:** Yes

### JT42C (id=144)
- **Source:** `https://www.railtram.com.au/jt42c-class`
- **Raw engine:** `EMD 710G3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2009
- **Safe for Prudence:** Yes

### RHA (id=145)
- **Source:** `https://www.railtram.com.au/rha-class`
- **Raw engine:** `GE V250`
- **type_id:** 2 (Diesel)
- **manufacturer:** General Electric
- **introduced_year:** 2015
- **Safe for Prudence:** Yes

### RL (id=146)
- **Source:** `https://www.railtram.com.au/rl-class`
- **Raw engine:** `EMD 645F3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** National Railway Equipment Company
- **introduced_year:** 2005
- **Safe for Prudence:** Yes

### S (id=147)
- **Source:** MISSING
- **Proposed updates:** none
- **Safe for Prudence:** No

### SCT (id=148)
- **Source:** `https://www.railtram.com.au/sct-class`
- **Raw engine:** `EMD 710G3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2007
- **Safe for Prudence:** Yes

### SSR (id=149)
- **Source:** `https://www.railtram.com.au/ssr-class`
- **Raw engine:** `EMD 710G3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2008
- **Safe for Prudence:** Yes

### T (id=150)
- **Source:** `https://www.railtram.com.au/t-class`
- **Raw engine:** `EMD 567CR (T320–98, T413–4); EMD 645E (T399–412)`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1955
- **Safe for Prudence:** Yes

### TL (id=151)
- **Source:** `https://www.railtram.com.au/tl-class`
- **Raw engine:** `EMD 567C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1955
- **Safe for Prudence:** Yes

### TR (id=152)
- **Source:** `https://www.railtram.com.au/tr-class`
- **Raw engine:** `Caterpillar 3512CHD`
- **type_id:** 2 (Diesel)
- **manufacturer:** Progress Rail
- **introduced_year:** 2014
- **Safe for Prudence:** Yes

### TT (id=153)
- **Source:** `https://www.railtram.com.au/tt-class`
- **Raw engine:** `EMD 710G3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2009
- **Safe for Prudence:** Yes

### TT2 (id=154)
- **Source:** `https://www.railtram.com.au/tt2-class`
- **Raw engine:** `EMD 710G3C-T3`
- **type_id:** 2 (Diesel)
- **manufacturer:** Progress Rail
- **introduced_year:** 2025
- **Safe for Prudence:** Yes

### UM20C (id=155)
- **Source:** `https://www.railtram.com.au/um20c-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** PT General Electric
- **introduced_year:** 1996
- **Safe for Prudence:** Yes

### V (id=156)
- **Source:** `https://www.railtram.com.au/v-class`
- **Raw engine:** `EMD 710G3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2002
- **Safe for Prudence:** Yes

### VL (id=157)
- **Source:** `https://www.railtram.com.au/vl-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Avteq
- **introduced_year:** 2007
- **Safe for Prudence:** Yes

### WH (id=158)
- **Source:** `https://www.railtram.com.au/wh-class`
- **Raw engine:** `EMD 710G3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Downer EDI
- **introduced_year:** 2010
- **Safe for Prudence:** Yes

### WRA (id=159)
- **Source:** `https://www.railtram.com.au/wra-class`
- **Raw engine:** `EMD 12-645E3B`
- **type_id:** 2 (Diesel)
- **manufacturer:** National Railway Equipment Company
- **introduced_year:** 2019
- **Safe for Prudence:** Yes

### WRB (id=160)
- **Source:** `https://www.railtram.com.au/wrb-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Comeng/Clyde Engineering
- **introduced_year:** 2020
- **Safe for Prudence:** Yes

### WRC (id=161)
- **Source:** `https://www.railtram.com.au/wrc-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Comeng/Clyde Engineering
- **introduced_year:** 2022
- **Safe for Prudence:** Yes

### WRD (id=162)
- **Source:** `https://www.railtram.com.au/wrd-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 2023
- **Safe for Prudence:** Yes

### WRE (id=163)
- **Source:** `https://www.railtram.com.au/wre-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 2023
- **Safe for Prudence:** Yes

### X (id=164)
- **Source:** `https://www.railtram.com.au/x-class`
- **Raw engine:** `EMD 645E`
- **type_id:** 2 (Diesel)
- **manufacturer:** Clyde Engineering
- **introduced_year:** 1966
- **Safe for Prudence:** Yes

### X200 (id=165)
- **Source:** `https://www.railtram.com.au/x200-class`
- **Raw engine:** `Cummins NHRS-6B1`
- **type_id:** 2 (Diesel)
- **manufacturer:** Department of Railways, New South Wales
- **introduced_year:** 1963
- **Safe for Prudence:** Yes

### XR (id=166)
- **Source:** `https://www.railtram.com.au/xr-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Freight Australia
- **introduced_year:** 2002
- **Safe for Prudence:** Yes

### XRB (id=167)
- **Source:** `https://www.railtram.com.au/xrb-class`
- **Raw engine:** `EMD 645E3C`
- **type_id:** 2 (Diesel)
- **manufacturer:** Pacific National
- **introduced_year:** 2006
- **Safe for Prudence:** Yes

### XRN (id=168)
- **Source:** `https://www.railtram.com.au/xrn-class`
- **Raw engine:** `GE 7FDL`
- **type_id:** 2 (Diesel)
- **manufacturer:** UGL
- **introduced_year:** 2010
- **Safe for Prudence:** Yes

### Y (id=169)
- **Source:** MISSING
- **Proposed updates:** none
- **Safe for Prudence:** No

### 2150 (id=171)
- **Source:** MISSING
- **Proposed updates:** none
- **Safe for Prudence:** No

---

## Pilot Classes (Already Applied)

| id | Class | type_id | manufacturer | introduced_year |
|----|-------|---------|--------------|----------------|
| 128 | NR | 2 (Diesel) | Goninan/General Electric | 1996 |
| 46 | 48 | 2 (Diesel) | AE Goodwin | 1959 |
| 57 | 81 | 2 (Diesel) | Clyde Engineering | 1982 |
| 4 | C44-9W | 2 (Diesel) | General Electric | 1995 |
| 170 | 2250 | 2 (Diesel) | Clyde Engineering / Queensland Rail | 2004 |

---

## Preview SQL (PREVIEW ONLY — DO NOT APPLY)

For Prudence review. No Iguana dry-run until Prudence clears and Trevor approves.

```sql
-- Phase 2A full batch preview
-- Goblin 2026-06-22
-- REQUIRES: Prudence clearance + Trevor approval

UPDATE classes SET type_id = 2, manufacturer = 'Orenstein & Koppel', introduced_year = 1963
WHERE id = 5 AND name = '32';

UPDATE classes SET type_id = 2, manufacturer = 'Goninan', introduced_year = 1960
WHERE id = 6 AND name = 'GE L80T';

UPDATE classes SET type_id = 2, manufacturer = 'English Electric/South Australian Railways', introduced_year = 1964
WHERE id = 7 AND name = '500';

UPDATE classes SET type_id = 2, manufacturer = 'Wabtec Corporation', introduced_year = 2022
WHERE id = 8 AND name = 'AC44C6M';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin', introduced_year = 1965
WHERE id = 9 AND name = '600';

UPDATE classes SET type_id = 2, manufacturer = 'Electro-Motive Diesel', introduced_year = 2012
WHERE id = 10 AND name = 'SD70ACe/LC';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin', introduced_year = 1959
WHERE id = 11 AND name = '830';

UPDATE classes SET type_id = 2, manufacturer = 'Electro-Motive Diesel', introduced_year = 1999
WHERE id = 12 AND name = 'SD90MAC-H Phase II';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin', introduced_year = 1991
WHERE id = 13 AND name = '900';

UPDATE classes SET type_id = 2, manufacturer = 'National Railway Equipment Company', introduced_year = 2011
WHERE id = 14 AND name = '1100';

UPDATE classes SET type_id = 2, manufacturer = 'Walkers Ltd', introduced_year = 1969
WHERE id = 15 AND name = '11';

UPDATE classes SET type_id = 2, manufacturer = 'Morris Knudsen Australia', introduced_year = 1993
WHERE id = 17 AND name = '1300';

UPDATE classes SET type_id = 2, manufacturer = 'Nydqvist & Holm AB', introduced_year = 2006
WHERE id = 18 AND name = '14';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1971
WHERE id = 19 AND name = '1600';

UPDATE classes SET type_id = 2, manufacturer = 'Commonwealth Engineering/Clyde Engineering', introduced_year = 1966
WHERE id = 20 AND name = '1720';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 2003
WHERE id = 21 AND name = '1900';

UPDATE classes SET type_id = 2, manufacturer = 'Hutt Railway Workshops', introduced_year = 1998
WHERE id = 22 AND name = 'DQ';

UPDATE classes SET type_id = 2, manufacturer = 'Commonwealth Engineering', introduced_year = 2012
WHERE id = 23 AND name = '2050';

UPDATE classes SET type_id = 2, manufacturer = 'Commonwealth Engineering/Clyde Engineering', introduced_year = 1982
WHERE id = 24 AND name = '2170F';

UPDATE classes SET type_id = 2, manufacturer = 'Commonwealth Engineering/Clyde Engineering', introduced_year = 1982
WHERE id = 25 AND name = '2170';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1969
WHERE id = 26 AND name = '22';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering/Queensland Rail', introduced_year = 1997
WHERE id = 27 AND name = '2300';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering/Queensland Rail', introduced_year = 1997
WHERE id = 28 AND name = '2300D';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering/Commonwealth Engineering', introduced_year = 1977
WHERE id = 29 AND name = '2400';

UPDATE classes SET type_id = 2, manufacturer = 'Commonwealth Engineering/Clyde Engineering', introduced_year = 1980
WHERE id = 30 AND name = '2470';

UPDATE classes SET type_id = 2, manufacturer = 'Progress Rail', introduced_year = 2019
WHERE id = 31 AND name = '2700';

UPDATE classes SET type_id = 2, manufacturer = 'Goninan/General Electric', introduced_year = 1995
WHERE id = 32 AND name = '2800';

UPDATE classes SET type_id = 2, manufacturer = 'Commonwealth Engineering; Aurizon', introduced_year = 2022
WHERE id = 33 AND name = '2900';

UPDATE classes SET type_id = 2, manufacturer = 'Goninan/General Electric', introduced_year = 1995
WHERE id = 34 AND name = '3200';

UPDATE classes SET type_id = 3, manufacturer = 'Walkers Limited', introduced_year = 2003
WHERE id = 35 AND name = '3551';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin', introduced_year = 1962
WHERE id = 36 AND name = '45';

UPDATE classes SET type_id = 3, manufacturer = 'United Group Rail/Siemens', introduced_year = 2005
WHERE id = 37 AND name = '3700';

UPDATE classes SET type_id = 3, manufacturer = 'Siemens Mobility', introduced_year = 2008
WHERE id = 38 AND name = '3800';

UPDATE classes SET type_id = 2, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2000
WHERE id = 39 AND name = '4000';

UPDATE classes SET type_id = 2, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2007
WHERE id = 40 AND name = '4100';

UPDATE classes SET type_id = 2, manufacturer = 'Electro-Motive Diesel (4314–23, 4334–46, 4356–39, 4441–71, 4473); Progress Rail (4374–4499)', introduced_year = 2005
WHERE id = 41 AND name = 'SD70ACe/LCi';

UPDATE classes SET type_id = 2, manufacturer = 'Electro-Motive Diesel', introduced_year = 2008
WHERE id = 42 AND name = 'SD70ACe';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 2001
WHERE id = 43 AND name = 'DC';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin', introduced_year = 1957
WHERE id = 44 AND name = '44';

UPDATE classes SET type_id = 2, manufacturer = 'Progress Rail', introduced_year = 2021
WHERE id = 45 AND name = '4600';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1960
WHERE id = 47 AND name = '49';

UPDATE classes SET type_id = 2, manufacturer = 'United Group Rail/General Electric', introduced_year = 2005
WHERE id = 48 AND name = '5000';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2010
WHERE id = 49 AND name = '5020';

UPDATE classes SET type_id = 2, manufacturer = 'Goninan/General Electric', introduced_year = 1987
WHERE id = 50 AND name = 'C36-7M';

UPDATE classes SET type_id = 2, manufacturer = 'United Group Rail', introduced_year = 2009
WHERE id = 51 AND name = '6000';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2012
WHERE id = 52 AND name = '6020';

UPDATE classes SET type_id = 3, manufacturer = 'Siemens Mobility', introduced_year = 2009
WHERE id = 53 AND name = '71';

UPDATE classes SET type_id = 2, manufacturer = 'Walkers Limited', introduced_year = 1970
WHERE id = 54 AND name = '73';

UPDATE classes SET type_id = 2, manufacturer = 'Commonwealth Engineering', introduced_year = 1978
WHERE id = 55 AND name = '80';

UPDATE classes SET type_id = 2, manufacturer = 'General Electric', introduced_year = 2007
WHERE id = 56 AND name = 'ES44DCi';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1994
WHERE id = 58 AND name = '82';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2008
WHERE id = 59 AND name = '83';

UPDATE classes SET type_id = 2, manufacturer = 'CSR Ziyang Locomotive Company', introduced_year = 2014
WHERE id = 60 AND name = '88';

UPDATE classes SET type_id = 2, manufacturer = 'Electro-Motive Diesel (9001–31); Downer EDI (9032–5)', introduced_year = 1994
WHERE id = 61 AND name = '90';

UPDATE classes SET type_id = 2, manufacturer = 'General Electric', introduced_year = 2014
WHERE id = 62 AND name = 'ES44ACi';

UPDATE classes SET type_id = 2, manufacturer = 'United Group Rail', introduced_year = 2008
WHERE id = 63 AND name = '92';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2012
WHERE id = 64 AND name = '93';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2025
WHERE id = 65 AND name = '94';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1969
WHERE id = 66 AND name = '422';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin (44201–44234); Commonwealth Engineering (44235–44240)', introduced_year = 1971
WHERE id = 67 AND name = '442';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1984
WHERE id = 68 AND name = 'A';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1969
WHERE id = 69 AND name = 'AB';

UPDATE classes SET type_id = 2, manufacturer = 'United Group Rail', introduced_year = 2009
WHERE id = 70 AND name = 'AC';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2011
WHERE id = 71 AND name = 'ACB';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2013
WHERE id = 72 AND name = 'ACC';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2022
WHERE id = 73 AND name = 'ACD';

UPDATE classes SET type_id = 2, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2011
WHERE id = 74 AND name = 'ACN';

UPDATE classes SET type_id = 2, manufacturer = 'Morris Knudsen Australia', introduced_year = 1994
WHERE id = 75 AND name = 'ALF';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1992
WHERE id = 76 AND name = 'AN';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1952
WHERE id = 77 AND name = 'B';

UPDATE classes SET type_id = 3, manufacturer = 'CRRC ZhuZhou Locomotive Company', introduced_year = 2018
WHERE id = 78 AND name = 'BEL';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1984
WHERE id = 79 AND name = 'BL';

UPDATE classes SET type_id = 3, manufacturer = 'Siemens Mobility', introduced_year = 2013
WHERE id = 80 AND name = 'BMACC';

UPDATE classes SET type_id = 2, manufacturer = 'Southern Shorthaul Railroad', introduced_year = 2013
WHERE id = 81 AND name = 'BRM';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1977
WHERE id = 82 AND name = 'C';

UPDATE classes SET type_id = 2, manufacturer = 'Motive Power Inc.', introduced_year = 2012
WHERE id = 83 AND name = 'MP27CN';

UPDATE classes SET type_id = 2, manufacturer = 'Motive Power Inc.', introduced_year = 2012
WHERE id = 84 AND name = 'MP33CN';

UPDATE classes SET type_id = 2, manufacturer = 'Motive Power Inc.', introduced_year = 2012
WHERE id = 85 AND name = 'MP33C';

UPDATE classes SET type_id = 2, manufacturer = 'Goninan/General Electric', introduced_year = 1989
WHERE id = 86 AND name = 'CD';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2012
WHERE id = 87 AND name = 'CEY';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2011
WHERE id = 88 AND name = 'CF';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1994
WHERE id = 89 AND name = 'CK';

UPDATE classes SET type_id = 2, manufacturer = 'Morris Knudsen Australia', introduced_year = 1993
WHERE id = 90 AND name = 'CLF';

UPDATE classes SET type_id = 2, manufacturer = 'Morris Knudsen Australia', introduced_year = 1993
WHERE id = 91 AND name = 'CLP';

UPDATE classes SET type_id = 2, manufacturer = 'Motive Power Inc.', introduced_year = 2013
WHERE id = 92 AND name = 'CM';

UPDATE classes SET type_id = 2, manufacturer = 'Windhoff', introduced_year = 2002
WHERE id = 93 AND name = 'CS';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1972
WHERE id = 94 AND name = 'DAZ';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1982
WHERE id = 95 AND name = 'DBZ';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering/Queensland Rail', introduced_year = 2008
WHERE id = 96 AND name = 'DFZ';

UPDATE classes SET type_id = 2, manufacturer = 'Walkers Limited', introduced_year = 1966
WHERE id = 97 AND name = 'DH';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1971
WHERE id = 99 AND name = 'DR';

UPDATE classes SET type_id = 2, manufacturer = 'Goninan/General Electric', introduced_year = 1990
WHERE id = 100 AND name = 'EL';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2015
WHERE id = 101 AND name = 'FIE';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1966
WHERE id = 102 AND name = 'FJ';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1970
WHERE id = 103 AND name = 'FL';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2003
WHERE id = 104 AND name = 'FQ';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1984
WHERE id = 105 AND name = 'G';

UPDATE classes SET type_id = 2, manufacturer = 'Goninan/General Electric', introduced_year = 2003
WHERE id = 106 AND name = 'GL';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1951
WHERE id = 107 AND name = 'GM1';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1955
WHERE id = 108 AND name = 'GM12';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1990
WHERE id = 109 AND name = 'GML';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin', introduced_year = 2011
WHERE id = 110 AND name = 'GPU';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2011
WHERE id = 111 AND name = 'GWA';

UPDATE classes SET type_id = 2, manufacturer = 'Progress Rail', introduced_year = 2019
WHERE id = 112 AND name = 'GWB';

UPDATE classes SET type_id = 2, manufacturer = 'Evans Deakin Industries/EMD', introduced_year = 2013
WHERE id = 113 AND name = 'GWN';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2012
WHERE id = 114 AND name = 'GWU';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1969
WHERE id = 116 AND name = 'HL';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1966
WHERE id = 117 AND name = 'J';

UPDATE classes SET type_id = 2, manufacturer = 'English Electric', introduced_year = 1966
WHERE id = 118 AND name = 'K';

UPDATE classes SET type_id = 2, manufacturer = 'English Electric', introduced_year = 1971
WHERE id = 119 AND name = 'KA';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1972
WHERE id = 120 AND name = 'Comalco GT26C';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering; Commonwealth Engineering', introduced_year = 1967
WHERE id = 121 AND name = 'L';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2008
WHERE id = 122 AND name = 'LDP';

UPDATE classes SET type_id = 2, manufacturer = 'Victorian Railways', introduced_year = 1932
WHERE id = 123 AND name = 'RT';

UPDATE classes SET type_id = 2, manufacturer = 'Progess Rail', introduced_year = 2024
WHERE id = 124 AND name = 'MAN';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1961
WHERE id = 125 AND name = 'MM';

UPDATE classes SET type_id = 2, manufacturer = 'UGL/General Electric', introduced_year = 2014
WHERE id = 126 AND name = 'MRL';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1986
WHERE id = 127 AND name = 'N';

UPDATE classes SET type_id = 2, manufacturer = 'Progress Rail', introduced_year = 2022
WHERE id = 129 AND name = 'ORN';

UPDATE classes SET type_id = 2, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2025
WHERE id = 130 AND name = 'ORQ';

UPDATE classes SET type_id = 2, manufacturer = 'Goninan/General Electric', introduced_year = 1996
WHERE id = 132 AND name = 'PA';

UPDATE classes SET type_id = 2, manufacturer = 'National Railway Equipment Company', introduced_year = 2014
WHERE id = 133 AND name = 'PB';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2019
WHERE id = 134 AND name = 'PH';

UPDATE classes SET type_id = 2, manufacturer = 'UGL/General Electric', introduced_year = 2016
WHERE id = 135 AND name = 'PHC';

UPDATE classes SET type_id = 2, manufacturer = 'AE Goodwin', introduced_year = 1998
WHERE id = 136 AND name = 'PL';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2004
WHERE id = 137 AND name = 'PN';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering/Queensland Rail', introduced_year = 2021
WHERE id = 138 AND name = 'PRL';

UPDATE classes SET type_id = 2, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2025
WHERE id = 139 AND name = 'PRQ';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1997
WHERE id = 140 AND name = 'Q';

UPDATE classes SET type_id = 2, manufacturer = 'CSR Ziyang Locomotive Company', introduced_year = 2016
WHERE id = 141 AND name = 'QBX';

UPDATE classes SET type_id = 2, manufacturer = 'Progress Rail', introduced_year = 2024
WHERE id = 142 AND name = 'QE';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2021
WHERE id = 143 AND name = 'QL';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2009
WHERE id = 144 AND name = 'JT42C';

UPDATE classes SET type_id = 2, manufacturer = 'General Electric', introduced_year = 2015
WHERE id = 145 AND name = 'RHA';

UPDATE classes SET type_id = 2, manufacturer = 'National Railway Equipment Company', introduced_year = 2005
WHERE id = 146 AND name = 'RL';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2007
WHERE id = 148 AND name = 'SCT';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2008
WHERE id = 149 AND name = 'SSR';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1955
WHERE id = 150 AND name = 'T';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1955
WHERE id = 151 AND name = 'TL';

UPDATE classes SET type_id = 2, manufacturer = 'Progress Rail', introduced_year = 2014
WHERE id = 152 AND name = 'TR';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2009
WHERE id = 153 AND name = 'TT';

UPDATE classes SET type_id = 2, manufacturer = 'Progress Rail', introduced_year = 2025
WHERE id = 154 AND name = 'TT2';

UPDATE classes SET type_id = 2, manufacturer = 'PT General Electric', introduced_year = 1996
WHERE id = 155 AND name = 'UM20C';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2002
WHERE id = 156 AND name = 'V';

UPDATE classes SET type_id = 2, manufacturer = 'Avteq', introduced_year = 2007
WHERE id = 157 AND name = 'VL';

UPDATE classes SET type_id = 2, manufacturer = 'Downer EDI', introduced_year = 2010
WHERE id = 158 AND name = 'WH';

UPDATE classes SET type_id = 2, manufacturer = 'National Railway Equipment Company', introduced_year = 2019
WHERE id = 159 AND name = 'WRA';

UPDATE classes SET type_id = 2, manufacturer = 'Comeng/Clyde Engineering', introduced_year = 2020
WHERE id = 160 AND name = 'WRB';

UPDATE classes SET type_id = 2, manufacturer = 'Comeng/Clyde Engineering', introduced_year = 2022
WHERE id = 161 AND name = 'WRC';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 2023
WHERE id = 162 AND name = 'WRD';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 2023
WHERE id = 163 AND name = 'WRE';

UPDATE classes SET type_id = 2, manufacturer = 'Clyde Engineering', introduced_year = 1966
WHERE id = 164 AND name = 'X';

UPDATE classes SET type_id = 2, manufacturer = 'Department of Railways, New South Wales', introduced_year = 1963
WHERE id = 165 AND name = 'X200';

UPDATE classes SET type_id = 2, manufacturer = 'Freight Australia', introduced_year = 2002
WHERE id = 166 AND name = 'XR';

UPDATE classes SET type_id = 2, manufacturer = 'Pacific National', introduced_year = 2006
WHERE id = 167 AND name = 'XRB';

UPDATE classes SET type_id = 2, manufacturer = 'UGL', introduced_year = 2010
WHERE id = 168 AND name = 'XRN';

```

---

*Ledger built 2026-06-22. 163 non-pilot classes.*
*Next step: Prudence review + Trevor approval before any apply.*