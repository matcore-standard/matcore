# 0080 — Core electrons: all-electron or frozen core

Date: 2026-11-22. Status: accepted. Decided by: Ellad Tadmor.

## Context
Reviewer feedback on dft, 2026-11-22: "The schema should separate the wavefunction/basis representation from the core-electron treatment, since LAPW is best categorized as an all-electron basis-set method, while PAW is an augmented-wave/frozen-core valence-electron treatment rather than a peer category to "All Electron" or "Pseudopotential". Atm solution is to fill twice (core and valence) LAPW or PAW if used."

The first sentence repeats the feedback that 0018 answered.
- 0018 separated `core-electron-treatment` from `wavefunction-representation`.
- LAPW is now only a term of `wavefunction-representation › type`, so an LAPW calculation gives "All-electron" for its core and "LAPW" for its basis: two different facts.

The point about PAW still holds:
- `core-electron-treatment › type` lists All-electron, PAW and Pseudopotential as peers.
- `pseudopotential-or-paw › type` lists Norm conserving, PAW and Ultrasoft.
- A PAW calculation therefore writes "PAW" twice.

PAW, like a pseudopotential, keeps the core electrons out of the calculation and represents their effect through a dataset for each species. It is a kind of dataset, not a third way of treating the core.

## Decision
1. **`core-electron-treatment › type`** has the open terms All-electron and Frozen core, defined:
   - "All-electron" – All of the electrons are treated explicitly, the core electrons included, even where a code holds the deepest core states fixed at their atomic form
   - "Frozen core" – The core electrons are not treated explicitly; their effect on the valence electrons enters through a pseudopotential or a PAW dataset, described in `pseudopotential-or-paw`

   "Pseudopotential" and "PAW" leave this list.
2. **`pseudopotential-or-paw`** keeps its name, members and `type` terms (Norm conserving, PAW, Ultrasoft), which say which kind of dataset. Its description becomes: 'For type "Frozen core", additional information about each pseudopotential or PAW dataset.'
3. **`wavefunction-representation`** does not change. LAPW stays there (0018).

## Consequences
- One pull request: schema/dft.yaml, examples/dft.json (its core type becomes Frozen core), tests and the regenerated page.
- Breaks 0.7.0 records that give the core type as "Pseudopotential" or "PAW". The vocabulary is open (0013), so such a record still conforms, and the term is reported as user-specified. The next release's entry says so.
- PROPOSED, NOT DECIDED:
  - a sentence in LAPW's definition saying that its variants (APW+lo, LAPW with local orbitals) are written "LAPW";
  - a warning from the step 9 validator when "LAPW" is given with "Frozen core".
