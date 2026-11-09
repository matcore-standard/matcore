# 0058 — Where the version of an exchange-correlation library is given

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding C7 of the minimal–dft analysis (2026-11-08): dft `xc-functional › normalization` names a functional by the components of a library (`source`: LibXC; 0017). The library's release can affect the result, since functionals are fixed and changed between releases. minimal `software › dependency` (0043) already holds a component a code was built with that can change its results, with its version; nothing in dft points to it.

## Decision
1. **`normalization › source`** gains the note: "Note: Give the version of the library as a `dependency` of the simulation code in minimal `software`."

## Consequences
- One pull request applies item 1 (schema, a test, regenerated page). Wording only.
