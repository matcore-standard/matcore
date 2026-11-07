# 0022 — The terms of calculation-physics

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor (committee decision, with two additions).

## Context
Community feedback on dft `calculation-physics`:
- "What is intended with relativistic effects, is this referring to spin-orbit coupling?"
- "If I have non-collinear spin polarization, should I indicate also "spin polarization" always? Or "spin polarization" refers to collinear (in which case I would write it explicitly)."

The property is optional and repeatable, one phenomenon per entry. Its open terms, from the baseline, are Relativistic effects, Spin polarization, Noncollinear spin polarization, On-site correlation and Van der Waals; its note reads '"On-site correlation" – e.g. DFT+U.'

"Relativistic effects" is ambiguous: a scalar-relativistic treatment is the default in most calculations, built into the pseudopotential or PAW dataset in plane-wave codes, while the choice a user makes is whether to include spin-orbit coupling. "Orbital polarization" has more than one reading; here it is the orbital-polarization correction, a term added to the Hamiltonian that enlarges the orbital magnetic moment (Brooks), and not the orbital ordering obtained with DFT+U, which "On-site correlation" covers.

Committee decision: drop "Relativistic effects"; add "Orbital polarization" and "Spin-orbit coupling". The committee decision does not answer the second question; items 2 and 3 below do.

## Decision
1. **Terms** (open, alphabetical): Collinear spin polarization, Noncollinear spin polarization, On-site correlation, Orbital polarization, Spin-orbit coupling, Van der Waals. "Relativistic effects" leaves the list; a scalar- or fully relativistic treatment, where a code offers the choice, is given as a user-specified value.
2. **Spin polarization.** "Spin polarization" is renamed "Collinear spin polarization", so that each spin term names its case. An instance gives at most one of the two spin terms.
3. **Note.** One phrase per term, then the rule of item 2:

   > "Collinear spin polarization" – Spin-polarized, with all magnetic moments parallel or antiparallel to one axis. "Noncollinear spin polarization" – Spin-polarized, with magnetic moments free to point in any direction. "On-site correlation" – e.g. DFT+U. "Orbital polarization" – A correction that enhances the orbital magnetic moment, e.g. Brooks' orbital-polarization term. "Spin-orbit coupling" – The coupling of the electron spin to its orbital motion. "Van der Waals" – Dispersion interactions, by a correction or a nonlocal functional. Give at most one of the two spin-polarization terms. Other phenomena are listed independently, e.g. a noncollinear calculation with spin-orbit coupling gives "Noncollinear spin polarization" and "Spin-orbit coupling".

## Consequences
- One pull request applies the decision (schema, test, regenerated page). examples/dft.xml has no `calculation-physics` element and needs no change.
- The vocabulary is open: a 0.5.0 instance giving "Relativistic effects" or "Spin polarization" still conforms, reported as user-specified.
- "At most one of the two spin terms" is a rule the schema cannot express yet; it is stated in the note and reviewed by hand (0012).
