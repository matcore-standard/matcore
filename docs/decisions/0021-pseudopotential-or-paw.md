# 0021 — Pseudopotential or PAW dataset

Date: 2026-11-06. Status: accepted. Decided by: Ellad Tadmor (committee decision).

## Context
Community feedback on dft `core-electron-treatment` › `pseudopotential`: "no obvious place to put PAW details. Is it just supposed to be under pseudopotential?"

The container's description already reads 'For type "Pseudopotential", or type "PAW", additional information about the pseudopotentials.', and its `checksum` note gives a VASP POTCAR file, a PAW potential, as its example; but its name and every other description say only "pseudopotential". Its required `type` has the terms Norm conserving and Ultrasoft, neither of which describes a PAW dataset.

Committee decision: rename `pseudopotential` to `pseudopotential-or-paw`.

Keeping the name and adding a note that PAW datasets belong there was weighed and rejected: it breaks no instance, but the feedback shows the existing description was missed.

## Decision
1. **Rename.** `core-electron-treatment` › `pseudopotential` becomes `pseudopotential-or-paw`; it stays optional and repeatable, and its subproperties keep their names, order and flags.
2. **`type`** stays required; its open terms, alphabetical, are Norm conserving, PAW, Ultrasoft.
3. **Wording.** In the descriptions and notes of the container and its subproperties, "the pseudopotential" becomes "the pseudopotential or PAW dataset" ("PAW dataset" being the usual term). The container's description ends "additional information about each pseudopotential or PAW dataset."; the checksum's "of the pseudopotential file" becomes "of the pseudopotential or PAW dataset file".

## Consequences
- One pull request applies the decision (schema, tests, regenerated page); examples/dft.xml renames `<pseudopotential>`.
- The rename breaks instances written against 0.5.0; the next release's entry says so.
