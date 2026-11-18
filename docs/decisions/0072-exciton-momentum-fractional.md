# 0072 — Exciton momentum in fractions of the reciprocal lattice vectors

Date: 2026-11-17. Status: accepted. Decided by: Ellad Tadmor.

## Context
0001 A5 (accepted) makes mbpt `bse-hamiltonian › exciton-momentum` a container: `basis` (cartesian or reciprocal-lattice-fractional), a `value` whose Kind depends on the basis (InverseLength or dimensionless), a `unit`, and, for the Cartesian basis, a `convention` stating whether the factor 2π is included. 0013's `depends-on`/`cases` constrains values, not the Kind of a unit, so the schema could not check that form; it needs the conditional rule that CLAUDE.md marks PROPOSED, NOT DECIDED.

Fractional coordinates need no unit and no 2π convention. The coefficients of Q = Q₁b₁ + Q₂b₂ + Q₃b₃ are the same whichever convention defines the bᵢ, since Q and the bᵢ scale together. The bᵢ follow from the real-space cell, which minimal `conditions › cell` records; dft `k-point-mesh` is read against that cell already (0059). 0004 item 47 chose the same fractional form for the k-point shift.

Codes give the momentum in this form or as an index into it:
- BerkeleyGW's `exciton_Q_shift` takes Qx Qy Qz "in crystal coordinates". Its manual warns that the shift is minus the exciton's center-of-mass momentum (kernel keywords and absorption overview, BerkeleyGW 4.0).
- Yambo selects the momentum by its index in the q-point grid (`BSEQptR`), index 1 being q = 0 (developers' answers on the Yambo forum).

The cost is that the coordinates mean nothing without the cell, and are wrong if the code used a different cell (primitive vs conventional) from the one recorded. dft `k-point-mesh` and mbpt `k-point-mesh` and `q-points` carry the same dependence.

## Decision
1. **`exciton-momentum` is a leaf:** float, extent [3], kind dimensionless, no unit: the exciton's center-of-mass crystal momentum in fractions of the reciprocal lattice vectors of the cell in minimal `conditions › cell`. This amends 0001 A5 for this property; no `basis`, `unit` or `convention` subproperty.
2. **A note states** that Q = Q₁b₁ + Q₂b₂ + Q₃b₃, with bᵢ the reciprocal lattice vectors of that cell; that [0, 0, 0] is the optical limit; and that the value is the exciton's momentum, not an input shift that a code may define with the opposite sign.

## Consequences
- Applied in the bse-hamiltonian pull request (status step 5): schema/mbpt.yaml, tests and the regenerated mbpt page. examples/mbpt.json has no BSE settings (its source dataset has no BSE input) and is unchanged.
- No released instance breaks: mbpt's properties were legacy text in 0.6.0.
- exciton-momentum is no longer the first case of the conditional validation rule. That rule stays PROPOSED, NOT DECIDED until another property needs it.
