# 0048 — A stress tolerance for cell relaxation; when the relaxation tolerances apply

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding A4 of the minimal–dft analysis (2026-11-08), as left after 0046: dft gives `relaxation-tolerance-energy` and `relaxation-tolerance-forces`, but a cell relaxation (variable-cell) also stops when the stress is close enough to its target, and that criterion has no place. The target is minimal `conditions › stress` (Kind Pressure, recommended GPa). Since 0046 a computation states its task, and the tolerances mean something only for task Optimization; nothing says so. 0046 (settled 2026-11-09) keeps a DFT relaxation as one computation, with its tolerances in dft.

## Decision
1. **dft gains `relaxation-tolerance-stress`** after `relaxation-tolerance-forces`: optional, not repeatable, a container of `value*` (float, `[]`, Kind Pressure, recommended unit GPa, minimum 0) and `unit*` (the fixed form, 0015), as `relaxation-tolerance-forces` is. Description: "Maximum stress convergence criterion for cell relaxation, relative to the stress imposed in `conditions`."
2. **`relaxation-tolerance-energy`, `relaxation-tolerance-forces` and `relaxation-tolerance-stress`** each carry the note "Note: Give it when the computation's task is Optimization." On relaxation-tolerance-energy it follows the note of 0023.
3. The descriptions of the energy and force tolerances keep "atomic relaxation": atomic positions are relaxed in both fixed-cell and variable-cell optimization.

## Consequences
- One pull request applies items 1–2 (schema, tests, regenerated page). The new property is optional; no instance or example changes.
