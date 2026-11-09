# 0047 — The species of a pseudopotential, PAW dataset or basis set

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding A2 of the minimal–dft analysis (2026-11-08): dft `pseudopotential-or-paw` is repeatable and gives a name, a type, the number of valence electrons and the file's origin, but not the element it is for. In a structure of several elements (e.g. SiO2) the entries cannot be told apart, and the valence count does not identify the element, since datasets for one element differ in it (e.g. Ti with 4 or 12 valence electrons). `localized-orbital-basis-set` has the same gap; basis sets are commonly assigned per element (e.g. def2-TZVP on a metal, def2-SVP on hydrogen), though a family such as cc-pVTZ is often named once for every species.

minimal `chemical-potential › species` (0042) already refers to a species by its spelling in a material component's formula, including a user-defined species (0034).

## Decision
1. **`pseudopotential-or-paw` gains `species*`** after `name`: required, not repeatable; string, `[]`, inapplicable, recommended unit null. Description: "The element or user-defined species this pseudopotential or PAW dataset is for, as written in a material component's formula." Examples: Si, Ja. One entry is given per species.
2. **`localized-orbital-basis-set` gains `species`** after `type`: optional, repeatable; string, `[]`, inapplicable, recommended unit null; the same description with "basis set" for "pseudopotential or PAW dataset". Note: "Note: Give the species this basis set is used for. Omit it when one basis set is used for every species."
3. **examples/dft.json** gives `"species": "Si"` in its pseudopotential entry.

## Consequences
- One pull request applies items 1–3 (schema, tests, regenerated page, example). Item 1 breaks 0.6.0 dft instances.
- The step 9 instance validator checks that each species named is in a material component's formula of a structure the computation models, as for `chemical-potential › species`.
