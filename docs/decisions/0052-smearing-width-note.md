# 0052 — The smearing width is not an imposed temperature

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding B5 of the minimal–dft analysis (2026-11-08): dft `smearing-width` is an energy, and for Fermi-Dirac smearing it equals k<sub>B</sub>T for an electronic temperature T. A record of ab initio MD gives both that width and the temperature imposed on the ions (minimal `conditions › temperature`), often of similar size. Nothing warns a writer, or a converter of code input, not to give the electronic temperature as a condition, which would claim a thermostat that was not used.

## Decision
1. **`smearing-width`** gains the note: "Note: Give the width as an energy; for Fermi-Dirac smearing it is k<sub>B</sub>T, where T is the electronic temperature. It is not a temperature imposed on the simulated system, which is given in `conditions`."

## Consequences
- One pull request applies item 1 (schema, a test, regenerated page). Wording only; no instance changes. If the smearing properties move out of `k-point-mesh` (finding C5), the note moves with `smearing-width`.
