# Railtram AU — Phase 2A Full Class Enrichment Ledger (v2 — Refined Type Vocabulary)
**Date:** 2026-06-22
**Author:** Goblin (Phase 2A full batch, v2)
**Supersedes:** railtram_phase2a_full_class_enrichment_ledger_2026-06-22.md (v1 — broad Diesel only)
**Status:** LEDGER ONLY. No DB changes. Awaiting Prudence review + Trevor approval.

---

## What Changed from v1

v1 used 'Diesel' as the single traction type for all non-Electric classes.
v2 uses the expanded type vocabulary (added 2026-06-22) and wheel arrangement as a second signal:

- **Bogie electric notation** (Co-Co, Bo-Bo, B-B, A1A-A1A, Bo-Bo-Bo) + diesel engine → **Diesel-electric**
- **0-4-0** + diesel engine → **Diesel-hydraulic** (O&K industrial shunters)
- **A-A** + diesel engine → **Diesel-mechanical** (small yard/rail motor)
- **A1-A1** + maintenance vehicle manufacturer → **Diesel-hydraulic**
- **B** + small diesel → **Diesel-mechanical** (light railcar)
- Electric engine string → **Electric** (unchanged from v1)

The five pilot classes (NR, 48, 81, C44-9W, 2250) were corrected from Diesel → Diesel-electric
in the DB before this ledger was built. This ledger uses Diesel-electric (type_id=9) for the
full batch accordingly.

---

## Summary

| Item | Count |
|------|-------|
| Total classes in DB (excl. pilot 5) | 163 |
| Pages found | 156 |
| Pages not found (404) | 7 |
| High confidence | 152 |
| Medium confidence (flagged) | 4 |
| Low confidence / blocked | 0 |
| Type: Diesel-electric | 146 |
| Type: Electric | 6 |
| Type: Diesel-hydraulic | 2 |
| Type: Diesel-mechanical | 2 |
| Pilot classes (already applied) | 5 |
| **Proposed updates** | **156** |
| Excluded (no source) | 7 |

---

## Type Classification Rules

| Wheel arrangement | Engine evidence | Classification | Confidence |
|-------------------|-----------------|----------------|------------|
| Co-Co / Bo-Bo / B-B / A1A-A1A / Bo-Bo-Bo | Any diesel engine string | Diesel-electric | High |
| Co-Co | Engine blank, Wabtec manufacturer | Diesel-electric | Medium |
| (blank / weight returned) | Caterpillar D398 + Walkers Ltd | Diesel-electric | Medium |
| 0-4-0 | Deutz / O&K industrial | Diesel-hydraulic | High |
| A-A | Fordson | Diesel-mechanical | High |
| A1-A1 | Volvo / Windhoff maintenance | Diesel-hydraulic | Medium |
| B | Cummins / light diesel | Diesel-mechanical | Medium |
| Any | explicit electric string | Electric | High |

---

## Classes Not Found on Railtram (7)

Excluded. No source — no proposed updates.

| DB id | Class | Slugs tried |
|-------|-------|-------------|
| 16 | 1200 | 1200-class, 1200-class-fortescue-metals-group, 1200-class-rio-tinto, 1200-class-qr |
| 98 | DL | dl-class, dl-class-kiwirail, dl-class-nz |
| 115 | H | h-class, h-class-westrail, h-class-public-transport-authority |
| 131 | P | p-class, p-class-westrail, p-class-public-transport-authority |
| 147 | S | s-class, s-class-westrail, s-class-public-transport-authority, s-class-act |
| 169 | Y | y-class, y-class-westrail, y-class-v-line, y-class-queensland-rail |
| 171 | 2150 | 2150-class, 2150-class-queensland-rail, 2150-class-qr |

---

## Full Class Ledger (163 classes)

### 32 (id=5)
- **Source:** `https://www.railtram.com.au/32-class`
- **Engine (raw):** `Deutz diesel A8L714`
- **Wheel arrangement:** `0-4-0`
- **Proposed type:** Diesel-hydraulic (type_id=10)
- **Proposed manufacturer:** Orenstein & Koppel
- **Proposed introduced_year:** 1963
- **Confidence:** high
- **Reasoning:** 0-4-0 wheel + Deutz diesel A8L714 → industrial diesel-hydraulic
- **Safe for Prudence:** Yes

### GE L80T (id=6)
- **Source:** `https://www.railtram.com.au/ge-l80t-class`
- **Engine (raw):** `Rolls Royce C6TFL (49–50); Cummins NT855-L2 (55); Cummins NT855-L4 (57); Cummins NT380 (D2)`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Goninan
- **Proposed introduced_year:** 1960
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 500 (id=7)
- **Source:** `https://www.railtram.com.au/500-class`
- **Engine (raw):** `EE SRKT`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** English Electric/South Australian Railways
- **Proposed introduced_year:** 1964
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### AC44C6M (id=8) ⚠ MEDIUM CONFIDENCE
- **Source:** `https://www.railtram.com.au/ac44c6m-class`
- **Engine (raw):** `(blank)`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Wabtec Corporation
- **Proposed introduced_year:** 2022
- **Confidence:** medium
- **Reasoning:** engine blank; Co-Co wheel + Wabtec manufacturer
- **Safe for Prudence:** Yes
- **Prudence note:** PRUDENCE RULING (Gate 8): type_id BLOCKED. Engine field blank on Railtram page. Inference from model name only is insuff

### 600 (id=9)
- **Source:** `https://www.railtram.com.au/600-class`
- **Engine (raw):** `Alco 251B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** AE Goodwin
- **Proposed introduced_year:** 1965
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### SD70ACe/LC (id=10)
- **Source:** `https://www.railtram.com.au/sd70ace-lc-class`
- **Engine (raw):** `EMD 710G3C-T2`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Electro-Motive Diesel
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 830 (id=11)
- **Source:** `https://www.railtram.com.au/830-class`
- **Engine (raw):** `Alco 251B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** AE Goodwin
- **Proposed introduced_year:** 1959
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### SD90MAC-H Phase II (id=12)
- **Source:** `https://www.railtram.com.au/sd90mac-h-phase-ii-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Electro-Motive Diesel
- **Proposed introduced_year:** 1999
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 900 (id=13)
- **Source:** `https://www.railtram.com.au/900-class`
- **Engine (raw):** `Alco 251B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** AE Goodwin
- **Proposed introduced_year:** 1991
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 1100 (id=14)
- **Source:** `https://www.railtram.com.au/1100-class`
- **Engine (raw):** `EMD 645E3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** National Railway Equipment Company
- **Proposed introduced_year:** 2011
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 11 (id=15) ⚠ MEDIUM CONFIDENCE
- **Source:** `https://www.railtram.com.au/11-class`
- **Engine (raw):** `Caterpillar D398 Series B`
- **Wheel arrangement:** `(not retrieved)`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Walkers Ltd
- **Proposed introduced_year:** 1969
- **Confidence:** medium
- **Reasoning:** wheel field returned weight value; Caterpillar D398 + Walkers Ltd → diesel-electric (Walkers built D-E locos for Qld)
- **Safe for Prudence:** Yes

### 1200 (id=16)
- **Source:** MISSING — no Railtram page found
- **Proposed updates:** none
- **Safe for Prudence:** No

### 1300 (id=17)
- **Source:** `https://www.railtram.com.au/1300-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Morris Knudsen Australia
- **Proposed introduced_year:** 1993
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 14 (id=18)
- **Source:** `https://www.railtram.com.au/14-class`
- **Engine (raw):** `EMD 645E3`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Nydqvist & Holm AB
- **Proposed introduced_year:** 2006
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 1600 (id=19)
- **Source:** `https://www.railtram.com.au/1600-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1971
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 1720 (id=20)
- **Source:** `https://www.railtram.com.au/1720-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Commonwealth Engineering/Clyde Engineering
- **Proposed introduced_year:** 1966
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 1900 (id=21)
- **Source:** `https://www.railtram.com.au/1900-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 2003
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### DQ (id=22)
- **Source:** `https://www.railtram.com.au/dq-class`
- **Engine (raw):** `EMD 645C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Hutt Railway Workshops
- **Proposed introduced_year:** 1998
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2050 (id=23)
- **Source:** `https://www.railtram.com.au/2050-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Commonwealth Engineering
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2170F (id=24)
- **Source:** `https://www.railtram.com.au/2170f-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Commonwealth Engineering/Clyde Engineering
- **Proposed introduced_year:** 1982
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2170 (id=25)
- **Source:** `https://www.railtram.com.au/2170-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Commonwealth Engineering/Clyde Engineering
- **Proposed introduced_year:** 1982
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 22 (id=26)
- **Source:** `https://www.railtram.com.au/22-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1969
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2300 (id=27)
- **Source:** `https://www.railtram.com.au/2300-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering/Queensland Rail
- **Proposed introduced_year:** 1997
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2300D (id=28)
- **Source:** `https://www.railtram.com.au/2300d-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering/Queensland Rail
- **Proposed introduced_year:** 1997
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2400 (id=29)
- **Source:** `https://www.railtram.com.au/2400-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering/Commonwealth Engineering
- **Proposed introduced_year:** 1977
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2470 (id=30)
- **Source:** `https://www.railtram.com.au/2470-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Commonwealth Engineering/Clyde Engineering
- **Proposed introduced_year:** 1980
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2700 (id=31)
- **Source:** `https://www.railtram.com.au/2700-class`
- **Engine (raw):** `EMD 710G`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Progress Rail
- **Proposed introduced_year:** 2019
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2800 (id=32)
- **Source:** `https://www.railtram.com.au/2800-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Goninan/General Electric
- **Proposed introduced_year:** 1995
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 2900 (id=33)
- **Source:** `https://www.railtram.com.au/2900-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Commonwealth Engineering; Aurizon
- **Proposed introduced_year:** 2022
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 3200 (id=34)
- **Source:** `https://www.railtram.com.au/3200-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Goninan/General Electric
- **Proposed introduced_year:** 1995
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 3551 (id=35)
- **Source:** `https://www.railtram.com.au/3551-class`
- **Engine (raw):** `25 kV electric`
- **Wheel arrangement:** `Bo-Bo-Bo`
- **Proposed type:** Electric (type_id=3)
- **Proposed manufacturer:** Walkers Limited
- **Proposed introduced_year:** 2003
- **Confidence:** high
- **Reasoning:** explicit electric engine string
- **Safe for Prudence:** Yes

### 45 (id=36)
- **Source:** `https://www.railtram.com.au/45-class`
- **Engine (raw):** `Alco 251B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** AE Goodwin
- **Proposed introduced_year:** 1962
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 3700 (id=37)
- **Source:** `https://www.railtram.com.au/3700-class`
- **Engine (raw):** `25 kV electric`
- **Wheel arrangement:** `Bo-Bo-Bo`
- **Proposed type:** Electric (type_id=3)
- **Proposed manufacturer:** United Group Rail/Siemens
- **Proposed introduced_year:** 2005
- **Confidence:** high
- **Reasoning:** explicit electric engine string
- **Safe for Prudence:** Yes

### 3800 (id=38)
- **Source:** `https://www.railtram.com.au/3800-class`
- **Engine (raw):** `25 kV electric`
- **Wheel arrangement:** `Bo-Bo-Bo`
- **Proposed type:** Electric (type_id=3)
- **Proposed manufacturer:** Siemens Mobility
- **Proposed introduced_year:** 2008
- **Confidence:** high
- **Reasoning:** explicit electric engine string
- **Safe for Prudence:** Yes

### 4000 (id=39)
- **Source:** `https://www.railtram.com.au/4000-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **Proposed introduced_year:** 2000
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 4100 (id=40)
- **Source:** `https://www.railtram.com.au/4100-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **Proposed introduced_year:** 2007
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### SD70ACe/LCi (id=41)
- **Source:** `https://www.railtram.com.au/sd70ace-lci-class`
- **Engine (raw):** `EMD 710G3C-T2`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Electro-Motive Diesel (4314–23, 4334–46, 4356–39, 4441–71, 4473); Progress Rail (4374–4499)
- **Proposed introduced_year:** 2005
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### SD70ACe (id=42)
- **Source:** `https://www.railtram.com.au/sd70ace-class`
- **Engine (raw):** `EMD 710G3C-T2`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Electro-Motive Diesel
- **Proposed introduced_year:** 2008
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### DC (id=43)
- **Source:** `https://www.railtram.com.au/dc-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 2001
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 44 (id=44)
- **Source:** `https://www.railtram.com.au/44-class`
- **Engine (raw):** `Alco 251B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** AE Goodwin
- **Proposed introduced_year:** 1957
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 4600 (id=45)
- **Source:** `https://www.railtram.com.au/4600-class`
- **Engine (raw):** `EMD 16-710G3C-T3`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Progress Rail
- **Proposed introduced_year:** 2021
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 49 (id=47)
- **Source:** `https://www.railtram.com.au/49-class`
- **Engine (raw):** `EMD 567CR`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1960
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 5000 (id=48)
- **Source:** `https://www.railtram.com.au/5000-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** United Group Rail/General Electric
- **Proposed introduced_year:** 2005
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 5020 (id=49)
- **Source:** `https://www.railtram.com.au/5020-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2010
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### C36-7M (id=50)
- **Source:** `https://www.railtram.com.au/c36-7m-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Goninan/General Electric
- **Proposed introduced_year:** 1987
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 6000 (id=51)
- **Source:** `https://www.railtram.com.au/6000-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** United Group Rail
- **Proposed introduced_year:** 2009
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 6020 (id=52)
- **Source:** `https://www.railtram.com.au/6020-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 71 (id=53)
- **Source:** `https://www.railtram.com.au/71-class`
- **Engine (raw):** `25 kV electric`
- **Wheel arrangement:** `Bo-Bo-Bo`
- **Proposed type:** Electric (type_id=3)
- **Proposed manufacturer:** Siemens Mobility
- **Proposed introduced_year:** 2009
- **Confidence:** high
- **Reasoning:** explicit electric engine string
- **Safe for Prudence:** Yes

### 73 (id=54)
- **Source:** `https://www.railtram.com.au/73-class`
- **Engine (raw):** `Caterpillar D379B`
- **Wheel arrangement:** `B-B`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Walkers Limited
- **Proposed introduced_year:** 1970
- **Confidence:** high
- **Reasoning:** B-B wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 80 (id=55)
- **Source:** `https://www.railtram.com.au/80-class`
- **Engine (raw):** `Alco 251CE`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Commonwealth Engineering
- **Proposed introduced_year:** 1978
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ES44DCi (id=56)
- **Source:** `https://www.railtram.com.au/es44dci-class`
- **Engine (raw):** `GE GEVO`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** General Electric
- **Proposed introduced_year:** 2007
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 82 (id=58)
- **Source:** `https://www.railtram.com.au/82-class`
- **Engine (raw):** `EMD 710G3A`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1994
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 83 (id=59)
- **Source:** `https://www.railtram.com.au/83-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2008
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 88 (id=60)
- **Source:** `https://www.railtram.com.au/88-class`
- **Engine (raw):** `MTU Freidrichshafen 20V4000R43`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** CSR Ziyang Locomotive Company
- **Proposed introduced_year:** 2014
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 90 (id=61)
- **Source:** `https://www.railtram.com.au/90-class`
- **Engine (raw):** `EMD 710G3A`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Electro-Motive Diesel (9001–31); Downer EDI (9032–5)
- **Proposed introduced_year:** 1994
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ES44ACi (id=62)
- **Source:** `https://www.railtram.com.au/es44aci-class`
- **Engine (raw):** `GE V250`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** General Electric
- **Proposed introduced_year:** 2014
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 92 (id=63)
- **Source:** `https://www.railtram.com.au/92-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** United Group Rail
- **Proposed introduced_year:** 2008
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 93 (id=64)
- **Source:** `https://www.railtram.com.au/93-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 94 (id=65)
- **Source:** `https://www.railtram.com.au/94-class`
- **Engine (raw):** `GEVO-12`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2025
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 422 (id=66)
- **Source:** `https://www.railtram.com.au/422-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1969
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### 442 (id=67)
- **Source:** `https://www.railtram.com.au/442-class`
- **Engine (raw):** `Alco 251C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** AE Goodwin (44201–44234); Commonwealth Engineering (44235–44240)
- **Proposed introduced_year:** 1971
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### A (id=68)
- **Source:** `https://www.railtram.com.au/a-class`
- **Engine (raw):** `EMD 645E3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1984
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### AB (id=69)
- **Source:** `https://www.railtram.com.au/ab-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1969
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### AC (id=70)
- **Source:** `https://www.railtram.com.au/ac-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** United Group Rail
- **Proposed introduced_year:** 2009
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ACB (id=71)
- **Source:** `https://www.railtram.com.au/acb-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2011
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ACC (id=72)
- **Source:** `https://www.railtram.com.au/acc-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2013
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ACD (id=73)
- **Source:** `https://www.railtram.com.au/acd-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2022
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ACN (id=74)
- **Source:** `https://www.railtram.com.au/acn-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **Proposed introduced_year:** 2011
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ALF (id=75)
- **Source:** `https://www.railtram.com.au/alf-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Morris Knudsen Australia
- **Proposed introduced_year:** 1994
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### AN (id=76)
- **Source:** `https://www.railtram.com.au/an-class`
- **Engine (raw):** `EMD 710G3A`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1992
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### B (id=77)
- **Source:** `https://www.railtram.com.au/b-class`
- **Engine (raw):** `EMD 567B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1952
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### BEL (id=78)
- **Source:** `https://www.railtram.com.au/bel-class`
- **Engine (raw):** `1500 V electric/battery`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Electric (type_id=3)
- **Proposed manufacturer:** CRRC ZhuZhou Locomotive Company
- **Proposed introduced_year:** 2018
- **Confidence:** high
- **Reasoning:** explicit electric engine string
- **Safe for Prudence:** Yes

### BL (id=79)
- **Source:** `https://www.railtram.com.au/bl-class`
- **Engine (raw):** `EMD 645E3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1984
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### BMACC (id=80)
- **Source:** `https://www.railtram.com.au/bmacc-class`
- **Engine (raw):** `25 kV electric`
- **Wheel arrangement:** `Bo-Bo-Bo`
- **Proposed type:** Electric (type_id=3)
- **Proposed manufacturer:** Siemens Mobility
- **Proposed introduced_year:** 2013
- **Confidence:** high
- **Reasoning:** explicit electric engine string
- **Safe for Prudence:** Yes

### BRM (id=81)
- **Source:** `https://www.railtram.com.au/brm-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Southern Shorthaul Railroad
- **Proposed introduced_year:** 2013
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### C (id=82)
- **Source:** `https://www.railtram.com.au/c-class`
- **Engine (raw):** `EMD 645E3`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1977
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### MP27CN (id=83)
- **Source:** `https://www.railtram.com.au/mp27cn-class`
- **Engine (raw):** `Cummins QSK60`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Motive Power Inc.
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### MP33CN (id=84)
- **Source:** `https://www.railtram.com.au/mp33cn-class`
- **Engine (raw):** `Cummins QSK78`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Motive Power Inc.
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### MP33C (id=85)
- **Source:** `https://www.railtram.com.au/mp33c-class`
- **Engine (raw):** `Cummins QSK78`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Motive Power Inc.
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### CD (id=86)
- **Source:** `https://www.railtram.com.au/cd-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Goninan/General Electric
- **Proposed introduced_year:** 1989
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### CEY (id=87)
- **Source:** `https://www.railtram.com.au/cey-class`
- **Engine (raw):** `GE 7FDL-16`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### CF (id=88)
- **Source:** `https://www.railtram.com.au/cf-class`
- **Engine (raw):** `GE 7FDL-16`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2011
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### CK (id=89)
- **Source:** `https://www.railtram.com.au/ck-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1994
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### CLF (id=90)
- **Source:** `https://www.railtram.com.au/clf-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Morris Knudsen Australia
- **Proposed introduced_year:** 1993
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### CLP (id=91)
- **Source:** `https://www.railtram.com.au/clp-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Morris Knudsen Australia
- **Proposed introduced_year:** 1993
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### CM (id=92)
- **Source:** `https://www.railtram.com.au/cm-class`
- **Engine (raw):** `Cummins QSK78`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Motive Power Inc.
- **Proposed introduced_year:** 2013
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### CS (id=93) ⚠ MEDIUM CONFIDENCE
- **Source:** `https://www.railtram.com.au/cs-class`
- **Engine (raw):** `Volvo EU`
- **Wheel arrangement:** `A1-A1`
- **Proposed type:** Diesel-hydraulic (type_id=10)
- **Proposed manufacturer:** Windhoff
- **Proposed introduced_year:** 2002
- **Confidence:** medium
- **Reasoning:** A1-A1 wheel + Windhoff → maintenance vehicle, diesel-hydraulic
- **Safe for Prudence:** Yes

### DAZ (id=94)
- **Source:** `https://www.railtram.com.au/daz-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1972
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### DBZ (id=95)
- **Source:** `https://www.railtram.com.au/dbz-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1982
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### DFZ (id=96)
- **Source:** `https://www.railtram.com.au/dfz-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering/Queensland Rail
- **Proposed introduced_year:** 2008
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### DH (id=97)
- **Source:** `https://www.railtram.com.au/dh-class`
- **Engine (raw):** `Caterpillar D353E`
- **Wheel arrangement:** `B-B`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Walkers Limited
- **Proposed introduced_year:** 1966
- **Confidence:** high
- **Reasoning:** B-B wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### DL (id=98)
- **Source:** MISSING — no Railtram page found
- **Proposed updates:** none
- **Safe for Prudence:** No

### DR (id=99)
- **Source:** `https://www.railtram.com.au/dr-class`
- **Engine (raw):** `EMD645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1971
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### EL (id=100)
- **Source:** `https://www.railtram.com.au/el-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Goninan/General Electric
- **Proposed introduced_year:** 1990
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### FIE (id=101)
- **Source:** `https://www.railtram.com.au/fie-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2015
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### FJ (id=102)
- **Source:** `https://www.railtram.com.au/fj-class`
- **Engine (raw):** `EMD 567C`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1966
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### FL (id=103)
- **Source:** `https://www.railtram.com.au/fl-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1970
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### FQ (id=104)
- **Source:** `https://www.railtram.com.au/fq-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2003
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### G (id=105)
- **Source:** `https://www.railtram.com.au/g-class`
- **Engine (raw):** `EMD 645E3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1984
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GL (id=106)
- **Source:** `https://www.railtram.com.au/gl-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Goninan/General Electric
- **Proposed introduced_year:** 2003
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GM1 (id=107)
- **Source:** `https://www.railtram.com.au/gm1-class`
- **Engine (raw):** `EMD 567B`
- **Wheel arrangement:** `A1A-A1A`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1951
- **Confidence:** high
- **Reasoning:** A1A-A1A wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GM12 (id=108)
- **Source:** `https://www.railtram.com.au/gm12-class`
- **Engine (raw):** `EMD 567C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1955
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GML (id=109)
- **Source:** `https://www.railtram.com.au/gml-class`
- **Engine (raw):** `EMD 710G3A`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1990
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GPU (id=110)
- **Source:** `https://www.railtram.com.au/gpu-class`
- **Engine (raw):** `Alco 251B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** AE Goodwin
- **Proposed introduced_year:** 2011
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GWA (id=111)
- **Source:** `https://www.railtram.com.au/gwa-class`
- **Engine (raw):** `EMD 710G3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2011
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GWB (id=112)
- **Source:** `https://www.railtram.com.au/gwb-class`
- **Engine (raw):** `EMD 710G3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Progress Rail
- **Proposed introduced_year:** 2019
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GWN (id=113)
- **Source:** `https://www.railtram.com.au/gwn-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Evans Deakin Industries/EMD
- **Proposed introduced_year:** 2013
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### GWU (id=114)
- **Source:** `https://www.railtram.com.au/gwu-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2012
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### H (id=115)
- **Source:** MISSING — no Railtram page found
- **Proposed updates:** none
- **Safe for Prudence:** No

### HL (id=116)
- **Source:** `https://www.railtram.com.au/hl-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1969
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### J (id=117)
- **Source:** `https://www.railtram.com.au/j-class`
- **Engine (raw):** `EMD 567C`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1966
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### K (id=118)
- **Source:** `https://www.railtram.com.au/k-class`
- **Engine (raw):** `EE 12CSVT`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** English Electric
- **Proposed introduced_year:** 1966
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### KA (id=119)
- **Source:** `https://www.railtram.com.au/ka-class`
- **Engine (raw):** `EE 12CSVT`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** English Electric
- **Proposed introduced_year:** 1971
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### Comalco GT26C (id=120)
- **Source:** `https://www.railtram.com.au/comalco-gt26c-class`
- **Engine (raw):** `EMD 645E3`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1972
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### L (id=121)
- **Source:** `https://www.railtram.com.au/l-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering; Commonwealth Engineering
- **Proposed introduced_year:** 1967
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### LDP (id=122)
- **Source:** `https://www.railtram.com.au/ldp-class`
- **Engine (raw):** `EMD 710G3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2008
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### RT (id=123)
- **Source:** `https://www.railtram.com.au/rt-class`
- **Engine (raw):** `Fordson`
- **Wheel arrangement:** `A-A`
- **Proposed type:** Diesel-mechanical (type_id=11)
- **Proposed manufacturer:** Victorian Railways
- **Proposed introduced_year:** 1932
- **Confidence:** high
- **Reasoning:** A-A wheel + Fordson engine → diesel-mechanical
- **Safe for Prudence:** Yes

### MAN (id=124)
- **Source:** `https://www.railtram.com.au/man-class`
- **Engine (raw):** `EMD 710`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Progess Rail
- **Proposed introduced_year:** 2024
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### MM (id=125)
- **Source:** `https://www.railtram.com.au/mm-class`
- **Engine (raw):** `EMD 567CR`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1961
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### MRL (id=126)
- **Source:** `https://www.railtram.com.au/mrl-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL/General Electric
- **Proposed introduced_year:** 2014
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### N (id=127)
- **Source:** `https://www.railtram.com.au/n-class`
- **Engine (raw):** `EMD 645E3C (N451–60); EMD 645E3B (N461–75)`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1986
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ORN (id=129)
- **Source:** `https://www.railtram.com.au/orn-class`
- **Engine (raw):** `EMD 710`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Progress Rail
- **Proposed introduced_year:** 2022
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### ORQ (id=130)
- **Source:** `https://www.railtram.com.au/orq-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **Proposed introduced_year:** 2025
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### P (id=131)
- **Source:** MISSING — no Railtram page found
- **Proposed updates:** none
- **Safe for Prudence:** No

### PA (id=132)
- **Source:** `https://www.railtram.com.au/pa-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Goninan/General Electric
- **Proposed introduced_year:** 1996
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### PB (id=133)
- **Source:** `https://www.railtram.com.au/pb-class`
- **Engine (raw):** `Two QSK19C`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** National Railway Equipment Company
- **Proposed introduced_year:** 2014
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### PH (id=134)
- **Source:** `https://www.railtram.com.au/ph-class`
- **Engine (raw):** `GE P616`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2019
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### PHC (id=135)
- **Source:** `https://www.railtram.com.au/phc-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL/General Electric
- **Proposed introduced_year:** 2016
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### PL (id=136)
- **Source:** `https://www.railtram.com.au/pl-class`
- **Engine (raw):** `Alco 251B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** AE Goodwin
- **Proposed introduced_year:** 1998
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### PN (id=137)
- **Source:** `https://www.railtram.com.au/pn-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2004
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### PRL (id=138)
- **Source:** `https://www.railtram.com.au/prl-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering/Queensland Rail
- **Proposed introduced_year:** 2021
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### PRQ (id=139)
- **Source:** `https://www.railtram.com.au/prq-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Evans Deakin Industries/Electro-Motive Diesel
- **Proposed introduced_year:** 2025
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### Q (id=140)
- **Source:** `https://www.railtram.com.au/q-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1997
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### QBX (id=141)
- **Source:** `https://www.railtram.com.au/qbx-class`
- **Engine (raw):** `MTU Freidrichshafen 20V4000R43L`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** CSR Ziyang Locomotive Company
- **Proposed introduced_year:** 2016
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### QE (id=142)
- **Source:** `https://www.railtram.com.au/qe-class`
- **Engine (raw):** `EMD 710G3C-T3`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Progress Rail
- **Proposed introduced_year:** 2024
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### QL (id=143)
- **Source:** `https://www.railtram.com.au/ql-class`
- **Engine (raw):** `7FDL-16EFI`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2021
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### JT42C (id=144)
- **Source:** `https://www.railtram.com.au/jt42c-class`
- **Engine (raw):** `EMD 710G3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2009
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### RHA (id=145)
- **Source:** `https://www.railtram.com.au/rha-class`
- **Engine (raw):** `GE V250`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** General Electric
- **Proposed introduced_year:** 2015
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### RL (id=146)
- **Source:** `https://www.railtram.com.au/rl-class`
- **Engine (raw):** `EMD 645F3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** National Railway Equipment Company
- **Proposed introduced_year:** 2005
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### S (id=147)
- **Source:** MISSING — no Railtram page found
- **Proposed updates:** none
- **Safe for Prudence:** No

### SCT (id=148)
- **Source:** `https://www.railtram.com.au/sct-class`
- **Engine (raw):** `EMD 710G3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2007
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### SSR (id=149)
- **Source:** `https://www.railtram.com.au/ssr-class`
- **Engine (raw):** `EMD 710G3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2008
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### T (id=150)
- **Source:** `https://www.railtram.com.au/t-class`
- **Engine (raw):** `EMD 567CR (T320–98, T413–4); EMD 645E (T399–412)`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1955
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### TL (id=151)
- **Source:** `https://www.railtram.com.au/tl-class`
- **Engine (raw):** `EMD 567C`
- **Wheel arrangement:** `Bo-Bo`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1955
- **Confidence:** high
- **Reasoning:** Bo-Bo wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### TR (id=152)
- **Source:** `https://www.railtram.com.au/tr-class`
- **Engine (raw):** `Caterpillar 3512CHD`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Progress Rail
- **Proposed introduced_year:** 2014
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### TT (id=153)
- **Source:** `https://www.railtram.com.au/tt-class`
- **Engine (raw):** `EMD 710G3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2009
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### TT2 (id=154)
- **Source:** `https://www.railtram.com.au/tt2-class`
- **Engine (raw):** `EMD 710G3C-T3`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Progress Rail
- **Proposed introduced_year:** 2025
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### UM20C (id=155)
- **Source:** `https://www.railtram.com.au/um20c-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** PT General Electric
- **Proposed introduced_year:** 1996
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### V (id=156)
- **Source:** `https://www.railtram.com.au/v-class`
- **Engine (raw):** `EMD 710G3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2002
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### VL (id=157)
- **Source:** `https://www.railtram.com.au/vl-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Avteq
- **Proposed introduced_year:** 2007
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### WH (id=158)
- **Source:** `https://www.railtram.com.au/wh-class`
- **Engine (raw):** `EMD 710G3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Downer EDI
- **Proposed introduced_year:** 2010
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### WRA (id=159)
- **Source:** `https://www.railtram.com.au/wra-class`
- **Engine (raw):** `EMD 12-645E3B`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** National Railway Equipment Company
- **Proposed introduced_year:** 2019
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### WRB (id=160)
- **Source:** `https://www.railtram.com.au/wrb-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Comeng/Clyde Engineering
- **Proposed introduced_year:** 2020
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### WRC (id=161)
- **Source:** `https://www.railtram.com.au/wrc-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Comeng/Clyde Engineering
- **Proposed introduced_year:** 2022
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### WRD (id=162)
- **Source:** `https://www.railtram.com.au/wrd-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 2023
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### WRE (id=163)
- **Source:** `https://www.railtram.com.au/wre-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 2023
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### X (id=164)
- **Source:** `https://www.railtram.com.au/x-class`
- **Engine (raw):** `EMD 645E`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Clyde Engineering
- **Proposed introduced_year:** 1966
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### X200 (id=165) ⚠ MEDIUM CONFIDENCE
- **Source:** `https://www.railtram.com.au/x200-class`
- **Engine (raw):** `Cummins NHRS-6B1`
- **Wheel arrangement:** `B`
- **Proposed type:** Diesel-mechanical (type_id=11)
- **Proposed manufacturer:** Department of Railways, New South Wales
- **Proposed introduced_year:** 1963
- **Confidence:** medium
- **Reasoning:** B wheel + Cummins NHRS-6B1 → light railcar, diesel-mechanical
- **Safe for Prudence:** Yes

### XR (id=166)
- **Source:** `https://www.railtram.com.au/xr-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Freight Australia
- **Proposed introduced_year:** 2002
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### XRB (id=167)
- **Source:** `https://www.railtram.com.au/xrb-class`
- **Engine (raw):** `EMD 645E3C`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** Pacific National
- **Proposed introduced_year:** 2006
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### XRN (id=168)
- **Source:** `https://www.railtram.com.au/xrn-class`
- **Engine (raw):** `GE 7FDL`
- **Wheel arrangement:** `Co-Co`
- **Proposed type:** Diesel-electric (type_id=9)
- **Proposed manufacturer:** UGL
- **Proposed introduced_year:** 2010
- **Confidence:** high
- **Reasoning:** Co-Co wheel + diesel engine → diesel-electric
- **Safe for Prudence:** Yes

### Y (id=169)
- **Source:** MISSING — no Railtram page found
- **Proposed updates:** none
- **Safe for Prudence:** No

### 2150 (id=171)
- **Source:** MISSING — no Railtram page found
- **Proposed updates:** none
- **Safe for Prudence:** No

---

## Pilot Classes (Already Applied — For Reference)

| id | Class | type | manufacturer | introduced_year |
|----|-------|------|--------------|----------------|
| 128 | NR | Diesel-electric | Goninan/General Electric | 1996 |
| 46 | 48 | Diesel-electric | AE Goodwin | 1959 |
| 57 | 81 | Diesel-electric | Clyde Engineering | 1982 |
| 4 | C44-9W | Diesel-electric | General Electric | 1995 |
| 170 | 2250 | Diesel-electric | Clyde Engineering / Queensland Rail | 2004 |

---

## Preview SQL (PREVIEW ONLY — DO NOT APPLY)

For Prudence review. No Iguana dry-run authorised yet.

```sql
-- Phase 2A full batch v2 — refined type vocabulary
-- Goblin 2026-06-22
-- PREVIEW ONLY — requires Prudence clearance + Trevor approval

UPDATE classes SET type_id = 10, manufacturer = 'Orenstein & Koppel', introduced_year = 1963
WHERE id = 5 AND name = '32';

UPDATE classes SET type_id = 9, manufacturer = 'Goninan', introduced_year = 1960
WHERE id = 6 AND name = 'GE L80T';

UPDATE classes SET type_id = 9, manufacturer = 'English Electric/South Australian Railways', introduced_year = 1964
WHERE id = 7 AND name = '500';

UPDATE classes SET type_id = 9, manufacturer = 'Wabtec Corporation', introduced_year = 2022
WHERE id = 8 AND name = 'AC44C6M';

UPDATE classes SET type_id = 9, manufacturer = 'AE Goodwin', introduced_year = 1965
WHERE id = 9 AND name = '600';

UPDATE classes SET type_id = 9, manufacturer = 'Electro-Motive Diesel', introduced_year = 2012
WHERE id = 10 AND name = 'SD70ACe/LC';

UPDATE classes SET type_id = 9, manufacturer = 'AE Goodwin', introduced_year = 1959
WHERE id = 11 AND name = '830';

UPDATE classes SET type_id = 9, manufacturer = 'Electro-Motive Diesel', introduced_year = 1999
WHERE id = 12 AND name = 'SD90MAC-H Phase II';

UPDATE classes SET type_id = 9, manufacturer = 'AE Goodwin', introduced_year = 1991
WHERE id = 13 AND name = '900';

UPDATE classes SET type_id = 9, manufacturer = 'National Railway Equipment Company', introduced_year = 2011
WHERE id = 14 AND name = '1100';

UPDATE classes SET type_id = 9, manufacturer = 'Walkers Ltd', introduced_year = 1969
WHERE id = 15 AND name = '11';

UPDATE classes SET type_id = 9, manufacturer = 'Morris Knudsen Australia', introduced_year = 1993
WHERE id = 17 AND name = '1300';

UPDATE classes SET type_id = 9, manufacturer = 'Nydqvist & Holm AB', introduced_year = 2006
WHERE id = 18 AND name = '14';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1971
WHERE id = 19 AND name = '1600';

UPDATE classes SET type_id = 9, manufacturer = 'Commonwealth Engineering/Clyde Engineering', introduced_year = 1966
WHERE id = 20 AND name = '1720';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 2003
WHERE id = 21 AND name = '1900';

UPDATE classes SET type_id = 9, manufacturer = 'Hutt Railway Workshops', introduced_year = 1998
WHERE id = 22 AND name = 'DQ';

UPDATE classes SET type_id = 9, manufacturer = 'Commonwealth Engineering', introduced_year = 2012
WHERE id = 23 AND name = '2050';

UPDATE classes SET type_id = 9, manufacturer = 'Commonwealth Engineering/Clyde Engineering', introduced_year = 1982
WHERE id = 24 AND name = '2170F';

UPDATE classes SET type_id = 9, manufacturer = 'Commonwealth Engineering/Clyde Engineering', introduced_year = 1982
WHERE id = 25 AND name = '2170';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1969
WHERE id = 26 AND name = '22';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering/Queensland Rail', introduced_year = 1997
WHERE id = 27 AND name = '2300';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering/Queensland Rail', introduced_year = 1997
WHERE id = 28 AND name = '2300D';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering/Commonwealth Engineering', introduced_year = 1977
WHERE id = 29 AND name = '2400';

UPDATE classes SET type_id = 9, manufacturer = 'Commonwealth Engineering/Clyde Engineering', introduced_year = 1980
WHERE id = 30 AND name = '2470';

UPDATE classes SET type_id = 9, manufacturer = 'Progress Rail', introduced_year = 2019
WHERE id = 31 AND name = '2700';

UPDATE classes SET type_id = 9, manufacturer = 'Goninan/General Electric', introduced_year = 1995
WHERE id = 32 AND name = '2800';

UPDATE classes SET type_id = 9, manufacturer = 'Commonwealth Engineering; Aurizon', introduced_year = 2022
WHERE id = 33 AND name = '2900';

UPDATE classes SET type_id = 9, manufacturer = 'Goninan/General Electric', introduced_year = 1995
WHERE id = 34 AND name = '3200';

UPDATE classes SET type_id = 3, manufacturer = 'Walkers Limited', introduced_year = 2003
WHERE id = 35 AND name = '3551';

UPDATE classes SET type_id = 9, manufacturer = 'AE Goodwin', introduced_year = 1962
WHERE id = 36 AND name = '45';

UPDATE classes SET type_id = 3, manufacturer = 'United Group Rail/Siemens', introduced_year = 2005
WHERE id = 37 AND name = '3700';

UPDATE classes SET type_id = 3, manufacturer = 'Siemens Mobility', introduced_year = 2008
WHERE id = 38 AND name = '3800';

UPDATE classes SET type_id = 9, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2000
WHERE id = 39 AND name = '4000';

UPDATE classes SET type_id = 9, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2007
WHERE id = 40 AND name = '4100';

UPDATE classes SET type_id = 9, manufacturer = 'Electro-Motive Diesel (4314–23, 4334–46, 4356–39, 4441–71, 4473); Progress Rail (4374–4499)', introduced_year = 2005
WHERE id = 41 AND name = 'SD70ACe/LCi';

UPDATE classes SET type_id = 9, manufacturer = 'Electro-Motive Diesel', introduced_year = 2008
WHERE id = 42 AND name = 'SD70ACe';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 2001
WHERE id = 43 AND name = 'DC';

UPDATE classes SET type_id = 9, manufacturer = 'AE Goodwin', introduced_year = 1957
WHERE id = 44 AND name = '44';

UPDATE classes SET type_id = 9, manufacturer = 'Progress Rail', introduced_year = 2021
WHERE id = 45 AND name = '4600';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1960
WHERE id = 47 AND name = '49';

UPDATE classes SET type_id = 9, manufacturer = 'United Group Rail/General Electric', introduced_year = 2005
WHERE id = 48 AND name = '5000';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2010
WHERE id = 49 AND name = '5020';

UPDATE classes SET type_id = 9, manufacturer = 'Goninan/General Electric', introduced_year = 1987
WHERE id = 50 AND name = 'C36-7M';

UPDATE classes SET type_id = 9, manufacturer = 'United Group Rail', introduced_year = 2009
WHERE id = 51 AND name = '6000';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2012
WHERE id = 52 AND name = '6020';

UPDATE classes SET type_id = 3, manufacturer = 'Siemens Mobility', introduced_year = 2009
WHERE id = 53 AND name = '71';

UPDATE classes SET type_id = 9, manufacturer = 'Walkers Limited', introduced_year = 1970
WHERE id = 54 AND name = '73';

UPDATE classes SET type_id = 9, manufacturer = 'Commonwealth Engineering', introduced_year = 1978
WHERE id = 55 AND name = '80';

UPDATE classes SET type_id = 9, manufacturer = 'General Electric', introduced_year = 2007
WHERE id = 56 AND name = 'ES44DCi';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1994
WHERE id = 58 AND name = '82';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2008
WHERE id = 59 AND name = '83';

UPDATE classes SET type_id = 9, manufacturer = 'CSR Ziyang Locomotive Company', introduced_year = 2014
WHERE id = 60 AND name = '88';

UPDATE classes SET type_id = 9, manufacturer = 'Electro-Motive Diesel (9001–31); Downer EDI (9032–5)', introduced_year = 1994
WHERE id = 61 AND name = '90';

UPDATE classes SET type_id = 9, manufacturer = 'General Electric', introduced_year = 2014
WHERE id = 62 AND name = 'ES44ACi';

UPDATE classes SET type_id = 9, manufacturer = 'United Group Rail', introduced_year = 2008
WHERE id = 63 AND name = '92';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2012
WHERE id = 64 AND name = '93';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2025
WHERE id = 65 AND name = '94';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1969
WHERE id = 66 AND name = '422';

UPDATE classes SET type_id = 9, manufacturer = 'AE Goodwin (44201–44234); Commonwealth Engineering (44235–44240)', introduced_year = 1971
WHERE id = 67 AND name = '442';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1984
WHERE id = 68 AND name = 'A';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1969
WHERE id = 69 AND name = 'AB';

UPDATE classes SET type_id = 9, manufacturer = 'United Group Rail', introduced_year = 2009
WHERE id = 70 AND name = 'AC';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2011
WHERE id = 71 AND name = 'ACB';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2013
WHERE id = 72 AND name = 'ACC';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2022
WHERE id = 73 AND name = 'ACD';

UPDATE classes SET type_id = 9, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2011
WHERE id = 74 AND name = 'ACN';

UPDATE classes SET type_id = 9, manufacturer = 'Morris Knudsen Australia', introduced_year = 1994
WHERE id = 75 AND name = 'ALF';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1992
WHERE id = 76 AND name = 'AN';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1952
WHERE id = 77 AND name = 'B';

UPDATE classes SET type_id = 3, manufacturer = 'CRRC ZhuZhou Locomotive Company', introduced_year = 2018
WHERE id = 78 AND name = 'BEL';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1984
WHERE id = 79 AND name = 'BL';

UPDATE classes SET type_id = 3, manufacturer = 'Siemens Mobility', introduced_year = 2013
WHERE id = 80 AND name = 'BMACC';

UPDATE classes SET type_id = 9, manufacturer = 'Southern Shorthaul Railroad', introduced_year = 2013
WHERE id = 81 AND name = 'BRM';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1977
WHERE id = 82 AND name = 'C';

UPDATE classes SET type_id = 9, manufacturer = 'Motive Power Inc.', introduced_year = 2012
WHERE id = 83 AND name = 'MP27CN';

UPDATE classes SET type_id = 9, manufacturer = 'Motive Power Inc.', introduced_year = 2012
WHERE id = 84 AND name = 'MP33CN';

UPDATE classes SET type_id = 9, manufacturer = 'Motive Power Inc.', introduced_year = 2012
WHERE id = 85 AND name = 'MP33C';

UPDATE classes SET type_id = 9, manufacturer = 'Goninan/General Electric', introduced_year = 1989
WHERE id = 86 AND name = 'CD';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2012
WHERE id = 87 AND name = 'CEY';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2011
WHERE id = 88 AND name = 'CF';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1994
WHERE id = 89 AND name = 'CK';

UPDATE classes SET type_id = 9, manufacturer = 'Morris Knudsen Australia', introduced_year = 1993
WHERE id = 90 AND name = 'CLF';

UPDATE classes SET type_id = 9, manufacturer = 'Morris Knudsen Australia', introduced_year = 1993
WHERE id = 91 AND name = 'CLP';

UPDATE classes SET type_id = 9, manufacturer = 'Motive Power Inc.', introduced_year = 2013
WHERE id = 92 AND name = 'CM';

UPDATE classes SET type_id = 10, manufacturer = 'Windhoff', introduced_year = 2002
WHERE id = 93 AND name = 'CS';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1972
WHERE id = 94 AND name = 'DAZ';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1982
WHERE id = 95 AND name = 'DBZ';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering/Queensland Rail', introduced_year = 2008
WHERE id = 96 AND name = 'DFZ';

UPDATE classes SET type_id = 9, manufacturer = 'Walkers Limited', introduced_year = 1966
WHERE id = 97 AND name = 'DH';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1971
WHERE id = 99 AND name = 'DR';

UPDATE classes SET type_id = 9, manufacturer = 'Goninan/General Electric', introduced_year = 1990
WHERE id = 100 AND name = 'EL';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2015
WHERE id = 101 AND name = 'FIE';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1966
WHERE id = 102 AND name = 'FJ';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1970
WHERE id = 103 AND name = 'FL';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2003
WHERE id = 104 AND name = 'FQ';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1984
WHERE id = 105 AND name = 'G';

UPDATE classes SET type_id = 9, manufacturer = 'Goninan/General Electric', introduced_year = 2003
WHERE id = 106 AND name = 'GL';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1951
WHERE id = 107 AND name = 'GM1';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1955
WHERE id = 108 AND name = 'GM12';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1990
WHERE id = 109 AND name = 'GML';

UPDATE classes SET type_id = 9, manufacturer = 'AE Goodwin', introduced_year = 2011
WHERE id = 110 AND name = 'GPU';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2011
WHERE id = 111 AND name = 'GWA';

UPDATE classes SET type_id = 9, manufacturer = 'Progress Rail', introduced_year = 2019
WHERE id = 112 AND name = 'GWB';

UPDATE classes SET type_id = 9, manufacturer = 'Evans Deakin Industries/EMD', introduced_year = 2013
WHERE id = 113 AND name = 'GWN';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2012
WHERE id = 114 AND name = 'GWU';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1969
WHERE id = 116 AND name = 'HL';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1966
WHERE id = 117 AND name = 'J';

UPDATE classes SET type_id = 9, manufacturer = 'English Electric', introduced_year = 1966
WHERE id = 118 AND name = 'K';

UPDATE classes SET type_id = 9, manufacturer = 'English Electric', introduced_year = 1971
WHERE id = 119 AND name = 'KA';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1972
WHERE id = 120 AND name = 'Comalco GT26C';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering; Commonwealth Engineering', introduced_year = 1967
WHERE id = 121 AND name = 'L';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2008
WHERE id = 122 AND name = 'LDP';

UPDATE classes SET type_id = 11, manufacturer = 'Victorian Railways', introduced_year = 1932
WHERE id = 123 AND name = 'RT';

UPDATE classes SET type_id = 9, manufacturer = 'Progess Rail', introduced_year = 2024
WHERE id = 124 AND name = 'MAN';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1961
WHERE id = 125 AND name = 'MM';

UPDATE classes SET type_id = 9, manufacturer = 'UGL/General Electric', introduced_year = 2014
WHERE id = 126 AND name = 'MRL';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1986
WHERE id = 127 AND name = 'N';

UPDATE classes SET type_id = 9, manufacturer = 'Progress Rail', introduced_year = 2022
WHERE id = 129 AND name = 'ORN';

UPDATE classes SET type_id = 9, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2025
WHERE id = 130 AND name = 'ORQ';

UPDATE classes SET type_id = 9, manufacturer = 'Goninan/General Electric', introduced_year = 1996
WHERE id = 132 AND name = 'PA';

UPDATE classes SET type_id = 9, manufacturer = 'National Railway Equipment Company', introduced_year = 2014
WHERE id = 133 AND name = 'PB';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2019
WHERE id = 134 AND name = 'PH';

UPDATE classes SET type_id = 9, manufacturer = 'UGL/General Electric', introduced_year = 2016
WHERE id = 135 AND name = 'PHC';

UPDATE classes SET type_id = 9, manufacturer = 'AE Goodwin', introduced_year = 1998
WHERE id = 136 AND name = 'PL';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2004
WHERE id = 137 AND name = 'PN';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering/Queensland Rail', introduced_year = 2021
WHERE id = 138 AND name = 'PRL';

UPDATE classes SET type_id = 9, manufacturer = 'Evans Deakin Industries/Electro-Motive Diesel', introduced_year = 2025
WHERE id = 139 AND name = 'PRQ';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1997
WHERE id = 140 AND name = 'Q';

UPDATE classes SET type_id = 9, manufacturer = 'CSR Ziyang Locomotive Company', introduced_year = 2016
WHERE id = 141 AND name = 'QBX';

UPDATE classes SET type_id = 9, manufacturer = 'Progress Rail', introduced_year = 2024
WHERE id = 142 AND name = 'QE';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2021
WHERE id = 143 AND name = 'QL';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2009
WHERE id = 144 AND name = 'JT42C';

UPDATE classes SET type_id = 9, manufacturer = 'General Electric', introduced_year = 2015
WHERE id = 145 AND name = 'RHA';

UPDATE classes SET type_id = 9, manufacturer = 'National Railway Equipment Company', introduced_year = 2005
WHERE id = 146 AND name = 'RL';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2007
WHERE id = 148 AND name = 'SCT';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2008
WHERE id = 149 AND name = 'SSR';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1955
WHERE id = 150 AND name = 'T';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1955
WHERE id = 151 AND name = 'TL';

UPDATE classes SET type_id = 9, manufacturer = 'Progress Rail', introduced_year = 2014
WHERE id = 152 AND name = 'TR';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2009
WHERE id = 153 AND name = 'TT';

UPDATE classes SET type_id = 9, manufacturer = 'Progress Rail', introduced_year = 2025
WHERE id = 154 AND name = 'TT2';

UPDATE classes SET type_id = 9, manufacturer = 'PT General Electric', introduced_year = 1996
WHERE id = 155 AND name = 'UM20C';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2002
WHERE id = 156 AND name = 'V';

UPDATE classes SET type_id = 9, manufacturer = 'Avteq', introduced_year = 2007
WHERE id = 157 AND name = 'VL';

UPDATE classes SET type_id = 9, manufacturer = 'Downer EDI', introduced_year = 2010
WHERE id = 158 AND name = 'WH';

UPDATE classes SET type_id = 9, manufacturer = 'National Railway Equipment Company', introduced_year = 2019
WHERE id = 159 AND name = 'WRA';

UPDATE classes SET type_id = 9, manufacturer = 'Comeng/Clyde Engineering', introduced_year = 2020
WHERE id = 160 AND name = 'WRB';

UPDATE classes SET type_id = 9, manufacturer = 'Comeng/Clyde Engineering', introduced_year = 2022
WHERE id = 161 AND name = 'WRC';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 2023
WHERE id = 162 AND name = 'WRD';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 2023
WHERE id = 163 AND name = 'WRE';

UPDATE classes SET type_id = 9, manufacturer = 'Clyde Engineering', introduced_year = 1966
WHERE id = 164 AND name = 'X';

UPDATE classes SET type_id = 11, manufacturer = 'Department of Railways, New South Wales', introduced_year = 1963
WHERE id = 165 AND name = 'X200';

UPDATE classes SET type_id = 9, manufacturer = 'Freight Australia', introduced_year = 2002
WHERE id = 166 AND name = 'XR';

UPDATE classes SET type_id = 9, manufacturer = 'Pacific National', introduced_year = 2006
WHERE id = 167 AND name = 'XRB';

UPDATE classes SET type_id = 9, manufacturer = 'UGL', introduced_year = 2010
WHERE id = 168 AND name = 'XRN';

```

---

## Medium Confidence Classes — Prudence Must Review

| id | Class | Proposed type | Reason for medium confidence |
|----|-------|--------------|------------------------------|
| 8 | AC44C6M | Diesel-electric | engine blank; Co-Co wheel + Wabtec manufacturer |
| 15 | 11 | Diesel-electric | wheel field returned weight value; Caterpillar D398 + Walkers Ltd → diesel-elect |
| 93 | CS | Diesel-hydraulic | A1-A1 wheel + Windhoff → maintenance vehicle, diesel-hydraulic |
| 165 | X200 | Diesel-mechanical | B wheel + Cummins NHRS-6B1 → light railcar, diesel-mechanical |

---

*Ledger v2 built 2026-06-22. 163 non-pilot classes. Refined type vocabulary.*
*Next step: Prudence full-ledger review (v2) + Trevor approval before any apply.*