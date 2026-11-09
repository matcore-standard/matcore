# 0050 — Initial magnetic moments and magnetic order; the Kind MagneticMoment

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding B2 of the minimal–dft analysis (2026-11-08): dft `calculation-physics` says whether a calculation is spin polarized (collinear or noncollinear, 0022), but not how the spins were started, and the starting moments decide which magnetic state the self-consistent cycle reaches. Codes take them per atom or per species (e.g. VASP `MAGMOM` in Bohr magnetons, Quantum ESPRESSO `starting_magnetization` per species). MatCore has no list of atoms, so a moment is given per species, as 0047 gives a pseudopotential.

The magnetic order of the material modeled (e.g. ferromagnetic or antiferromagnetic Fe) is a physical description, not a DFT setting: classical spin dynamics, Monte Carlo on a spin model and DFT all model one. It also covers what moments per species cannot express, e.g. antiferromagnetic Cr, whose atoms of one species carry opposite moments.

Annex U has no Kind for magnetic moment. A fixed total magnetization (e.g. a molecule's spin multiplicity) is a constraint that could later be a condition like `net-charge` (0049); it is not decided here.

## Decision
1. **A new Kind, MagneticMoment**, in schema/units.yaml, with the units `mu_B` (the Bohr magneton) and `J/T`. Following 0040, each unit is added by its own pull request with every field traced to a primary source named in the pull request; the first adds the Kind.
2. **dft `settings` gains `initial-magnetic-moment`** after `calculation-physics`: optional, repeatable, a container of:
   - `species*`: as `pseudopotential-or-paw › species` (0047). Description: "The element or user-defined species whose atoms start with this moment, as written in a material component's formula."
   - `value*`: float, extent `any`, Kind MagneticMoment, recommended unit `mu_B`. Note: "Note: A signed number for collinear spin polarization; a vector of three Cartesian components for noncollinear spin polarization, as `calculation-physics` states."
   - `unit*`: the fixed form (0015).

   Description: "The magnetic moment per atom of a species at the start of the self-consistent cycle."
3. **minimal `material-component` gains `magnetic-order`** after `phase`: optional, not repeatable; string, `[]`, inapplicable. Open terms: Nonmagnetic, Ferromagnetic, Antiferromagnetic, Ferrimagnetic, Paramagnetic, Noncollinear. Description: "The arrangement of the magnetic moments in the material component as modeled." Note defining each term: "Nonmagnetic" – No magnetic moments; "Ferromagnetic" – Moments aligned parallel; "Antiferromagnetic" – Equal moments aligned antiparallel, with no net moment; "Ferrimagnetic" – Unequal moments aligned antiparallel, with a net moment; "Paramagnetic" – Moments present but disordered, e.g. modeled as disordered local moments; "Noncollinear" – Moments not along one axis, e.g. a spin spiral.

## Consequences
- Pull requests: the unit `mu_B` with the Kind MagneticMoment; the unit `J/T`; then items 2 and 3, with tests and the regenerated pages. Both properties are optional; no example changes.
- PROPOSED, NOT DECIDED: a condition for a fixed total magnetization or spin multiplicity.
