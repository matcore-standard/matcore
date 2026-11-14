# 0067 — Algorithm terms name major classes; specifics go in a description

Date: 2026-11-14. Status: accepted. Decided by: Ellad Tadmor.

## Context
A reviewer found that ps `algorithm` names metadynamics only at the level of the parent method: well-tempered, multiple-walker, parallel-bias and infrequent metadynamics cannot be told apart. Most algorithms have many variants, and a list of terms that tried to name them all would never be complete. The terms of 0064 item 4 already include some variants (Bond-boost and Strain-boost hyperdynamics, ART nouveau, GaMD, Transition interface sampling).

The same reviewer found no place for the numerical evaluation of elastic constants from the Born matrix (LAMMPS compute born/matrix), which fits neither minimization nor dynamics among the baseline's calculation types.

## Decision
1. **ps `algorithm` terms name major classes of algorithms, not their variants.** Bond-boost hyperdynamics, Strain-boost hyperdynamics, ART nouveau, GaMD and Transition interface sampling are removed; such a variant is given by its class (Hyperdynamics, ART, aMD, Transition path sampling) and named in `description`. No metadynamics variant is added. The terms stay open, so an unlisted procedure can still be given.
2. **ps `settings` gains an optional `description`** after `algorithm`: "Further information on the algorithms of these settings, e.g. the variant used, and an explanation of their computation-parameter entries." A scalar string, kind inapplicable, values null.
3. **algorithm's second note** becomes: "Numerical parameters of a procedure, e.g. the time step of Velocity Verlet or the number of images of NEB, are given as `computation-parameter` entries; its variant, e.g. well-tempered metadynamics, and other specifics are given in `description`."
4. **A property computed from derivatives of an interaction model**, e.g. elastic constants from the Born matrix, is a computation with task Property calculation that names the PIM or electronic-structure computation providing the energies as an input with the role Interaction model. The schema does not change.

## Consequences
- Amends 0064 item 4: ps `algorithm` has 39 terms. 0066 item 3's four search terms are classes and stay.
- No released instance breaks: `algorithm` was filled after 0.6.0, and `description` is optional.
- Applied in the ps `algorithm` pull request (0064 PR (b)).
- Item 4 meets 0065's open point on the `method` of a computation with no method term: a static Born-matrix evaluation moves no particles, so PS does not fit it as defined. That point stays PROPOSED, NOT DECIDED.
