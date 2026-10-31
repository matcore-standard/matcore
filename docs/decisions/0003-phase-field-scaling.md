# 0003 — `scaling` subproperty for nondimensional phase-field lengths and times

Date: 2026-10-31. Status: accepted. Decided by: Ellad Tadmor.

## Context
Phase-field simulations are often run in nondimensional units (e.g. grid spacing 1, time step 0.01). Under 0001, `domain-size` and `grid-spacing` have Kind Length and `time-step-size` has Kind Time, and Annex U Rule 3 forbids `dimensionless` for a dimensioned Kind, so nondimensional values would be non-conformant.

## Decision
- `domain-size`, `grid-spacing` and `time-step-size` each have a required subproperty `scaling` with enum [`physical`, `nondimensional`].
- When `scaling` = `physical`, `unit` SHALL be an Annex U symbol of the property's Kind (Length, or Time for `time-step-size`).
- When `scaling` = `nondimensional`, `unit` SHALL be `dimensionless`.
- Recommended units (informative): `m` for `domain-size` and `grid-spacing`, `s` for `time-step-size`.
- Note for each of the three properties: the characteristic length and time scales used for the nondimensionalization should be recorded as `model-parameter` entries so the values can be interpreted.
- The validator checks this conditional rule.

## Consequences
Nondimensional phase-field data are conformant, and the unit check still applies to physical data. This is the first rule in which the allowed unit depends on the value of another subproperty; it has the same shape as the `convention` rule for `k-point-spacing` (0001 A3.1).
