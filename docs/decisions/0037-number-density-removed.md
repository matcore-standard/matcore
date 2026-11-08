# 0037 — Number density is removed from the simulation conditions

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee feedback on minimal `computation › simulation-conditions › number-density`: drop it, since it is redundant with the number of particles and the volume, and could contradict them if the three are given inconsistently.

`number-density` ("The total number of particles comprising the material divided by the volume it occupies.") is N/V, and both `number-of-particles` and `volume` are conditions beside it. `mass-density` is not redundant in the same way: it also needs the particle masses, which the schema does not give (a user-defined species `J…` of 0034 has none).

## Decision
1. **`simulation-conditions › number-density` is removed.** A simulation set up at a given number density gives `number-of-particles` and `volume` instead.
2. `mass-density` and the other conditions are unchanged. The Kind `NumberDensity` and the unit `1/angstrom^3` stay in Annex U, which lists units independently of the properties that use them.

## Consequences
- One pull request applies item 1 (schema, tests, regenerated page). It breaks 0.5.0 instances that give `number-density`. examples/minimal.xml does not give it.
- 0035 item 2 lists twelve numerical conditions; eleven remain.
