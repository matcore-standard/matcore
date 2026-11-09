# 0057 — The LAPW basis cutoff

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding C6 of the minimal–dft analysis (2026-11-08): dft `wavefunction-representation › kinetic-energy-cutoff` applies to "LAPW" or "Plane waves" as an energy. Plane-wave codes take an energy cutoff, but LAPW codes usually set the basis by RKmax, the product of the smallest muffin-tin radius and the largest plane-wave wavevector, a dimensionless number (e.g. WIEN2k; `rgkmax` in exciting), which cannot be converted to an energy without the muffin-tin radius. The name `rkmax` was declined in favour of an English name that states the property's purpose; the description keeps the term RKmax so that it can be found.

`charge-density-cutoff` has the same mismatch for LAPW (a wavevector, e.g. WIEN2k's GMAX); it matters less to the result and is not changed.

## Decision
1. **`wavefunction-representation` gains `lapw-basis-cutoff`** after `kinetic-energy-cutoff`: optional, not repeatable; float, `[]`, dimensionless, recommended unit null, minimum 0; a leaf with no unit (0015). Description: "For type "LAPW", the cutoff of the basis, given as the product of the smallest muffin-tin radius and the largest plane-wave wavevector, R<sub>MT</sub>K<sub>max</sub> (RKmax)."
2. **`kinetic-energy-cutoff`'s description** becomes: "For type "Plane waves", or for "LAPW" when the code takes the cutoff as an energy, the maximum kinetic energy of the plane waves included in the calculation of wave functions."

## Consequences
- One pull request applies items 1–2 (schema, tests, regenerated page). The property is optional; no example changes.
