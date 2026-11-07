# 0023 — The energy in convergence criteria

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor (committee decision, phrased by smearing and extended to the SCF criterion).

## Context
Community feedback on dft `relaxation-tolerance-energy`: "The meaning of this quantity is currently unclear. It would be helpful to specify whether this refers to the electronic free energy, the total energy excluding entropy contributions, or an energy extrapolated to zero smearing."

Its description reads "Total energy convergence criterion for atomic relaxation." The SCF tolerance's `criterion` (0019) has the same ambiguity: its note defines "Energy" as "The change in the total energy between successive iterations."

Committee decision: "Total energy for insulators and Helmholtz free energy including entropy of smeared electrons for metals."

With smeared occupations, the forces a code computes are derivatives of the free energy F = E − TS, so a relaxation driven by them minimizes F; without smearing F reduces to E. What decides between the two in a calculation is therefore whether occupations are smeared, not the material: an insulator computed with smearing has TS ≈ 0, and a metal computed with the tetrahedron method has no TS term. The rule is stated by smearing, with the committee's two cases as examples.

## Decision
1. **`relaxation-tolerance-energy`.** The description becomes "Energy convergence criterion for atomic relaxation." The property gains a note:

   > The energy is the Helmholtz free energy F = E − TS, including the entropy S of the smeared electrons at the smearing temperature T, when occupations are smeared (e.g. a metal), and the total energy E otherwise (e.g. an insulator). It is not the energy extrapolated to zero smearing.
2. **`self-consistent-field-convergence` › `tolerance` › `criterion`** (amends 0019 item 1). In the note, the definition of "Energy" becomes: '"Energy" – The change in the energy between successive iterations, defined as for `relaxation-tolerance-energy`.'

## Consequences
- One pull request applies both items (schema, tests, regenerated page). examples/dft.xml has neither element and needs no change.
- No instance is affected: the structure, terms and units are unchanged.
