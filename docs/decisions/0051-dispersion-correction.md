# 0051 — The dispersion correction

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding B4 of the minimal–dft analysis (2026-11-08): dft `calculation-physics` has the term "Van der Waals" (0022) but not which treatment, and corrections such as D2, D3 and D4 give different results with the same functional. Whether `xc-functional › name` may carry the correction (e.g. PBE-D3) was PROPOSED, NOT DECIDED (0022, 0024).

Dispersion is treated either by an additive correction to a functional (D2, D3, D3(BJ), D4, Tkatchenko–Scheffler, many-body dispersion) or by a functional that includes it (e.g. vdW-DF, vdW-DF2, rVV10), which is named as a functional.

## Decision
1. **dft `settings` gains `dispersion-correction`** after `calculation-physics`: optional, not repeatable; string, `[]`, inapplicable, recommended unit null. Open terms: D2, D3, D3(BJ), D4, TS, MBD. Description: "The additive correction for van der Waals dispersion applied to the functional." Values note defining the terms: "D2", "D3", "D4" – Grimme's corrections of those generations; "D3(BJ)" – D3 with Becke–Johnson damping; "TS" – Tkatchenko–Scheffler; "MBD" – Many-body dispersion. Note: "Note: Give it when `calculation-physics` lists Van der Waals and the dispersion is added to the functional. A functional that includes dispersion itself (e.g. vdW-DF, rVV10) is named in `xc-functional › name`."
2. **`xc-functional › name` names the functional alone** (e.g. PBE, not PBE-D3); the correction is given in `dispersion-correction`. Its note says so. This settles the question left open by 0022 and 0024.

## Consequences
- One pull request applies items 1–2 (schema, tests, regenerated page). The property is optional and the note adds guidance; no example changes.
