# 0018 — Core-electron treatment and wavefunction representation

Date: 2026-11-06. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on dft: "The schema should separate the wavefunction/basis representation from the core-electron treatment, since LAPW is best categorized as an all-electron basis-set method, while PAW is an augmented-wave/frozen-core valence-electron treatment."

In the baseline, `core-electron-model` › `type` has the terms All Electron, LAPW, Pseudopotential, PAW, and `valence-electron-model` › `type` has Plane waves, LAPW, Localized orbitals, PAW. LAPW and PAW appear in both lists, and a single "Localized orbitals" term covers several distinct kinds of basis.

## Decision
1. **Renames.** `core-electron-model` becomes `core-electron-treatment`; `valence-electron-model` becomes `wavefunction-representation`. Their subproperties keep their names, order and requirements.
2. **`core-electron-treatment` › `type`**: open terms, alphabetical: All-electron, PAW, Pseudopotential. LAPW leaves this list.
3. **`wavefunction-representation` › `type`** (still repeatable): open terms, alphabetical: Gaussian basis sets, LAPW, Local atomic orbitals, Numerical atomic orbitals, Plane waves, Real space grids. PAW and Localized orbitals leave this list.
4. **Spelling** follows §1.3's sentence case: "All-electron" (was "All Electron"), "Plane waves" (plural, as before), "Gaussian basis sets".
5. **Notes.** The core terms keep their baseline definitions, in alphabetical order. The note on the representation terms groups them, without making the groups part of the metadata, and gives each a one-phrase explanation: basis-function expansions (Gaussian basis sets, Local atomic orbitals, Numerical atomic orbitals, Plane waves), grid methods (Real space grids), augmented methods (LAPW). "Local atomic orbitals" is the general term for atom-centered orbitals, used when neither of the two more specific terms applies. The groups are numbered in the note. Its wording:

   > The terms fall into three groups. (1) Basis-function expansions: "Gaussian basis sets" – Atom-centered Gaussian-type orbitals. "Local atomic orbitals" – Atom-centered orbitals of a form not covered by the previous or the next term, e.g. Slater-type orbitals. "Numerical atomic orbitals" – Atom-centered orbitals tabulated numerically, zero beyond a cutoff radius. "Plane waves" – Periodic plane waves up to a kinetic-energy cutoff. (2) Grid methods: "Real space grids" – Values on a mesh of points in real space (finite differences or finite elements). (3) Augmented methods: "LAPW" – Linearized Augmented Plane Wave: atomic-like functions inside spheres around the atoms, plane waves between them.
6. **Descriptions.**
   - `core-electron-treatment`: "The treatment of the core electrons in the calculation."; its `type`: "The method used to treat the core electrons."
   - `wavefunction-representation`: "The representation used to expand the electronic wave functions."; its `type`: "The method used to represent the electronic wave functions."
   - `localized-orbital-basis-set` keeps its name: 'For type "Gaussian basis sets", "Local atomic orbitals" or "Numerical atomic orbitals", additional information about the basis set.' MBPT's container of the same name is unchanged.
   - `kinetic-energy-cutoff` and `charge-density-cutoff` begin 'For type "LAPW" or "Plane waves", …' instead of 'For type not "Localized orbitals", …'.
   - `pseudopotential` is unchanged: 'For type "Pseudopotential", or type "PAW", …'.

## Consequences
- One pull request revises both properties (schema, tests, regenerated page). examples/dft.xml renames `<core-electron-model>` and `<valence-electron-model>`; their contents (Pseudopotential; Plane waves at 250.0 eV) already fit the new terms.
- Both renames break instances written against 0.5.0; the next release's entry in releases.yaml says so.
