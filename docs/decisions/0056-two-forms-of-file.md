# 0056 — Two forms of `file`

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding C3 of the minimal–dft analysis (2026-11-08): `file` has two shapes. dft `pseudopotential-or-paw › file`, `localized-orbital-basis-set › file` and minimal `provenance › file` hold `name*` and `checksum*` (0032). minimal `software › file` also holds `description`, `contents`, `encoding` and `link` (0043). The difference follows the purpose: a pseudopotential or basis-set file comes from a library its entry already identifies (repository, version, doi), and is named so that a reader can verify they have the same one; an input file is given so that the calculation can be understood or repeated, and needs a description and its contents or a link. Giving the first kind all members would invite copying a library file into the record.

## Decision
1. **No property changes.**
2. **The rule is stated** in CLAUDE.md's conventions for schema YAML and applied to new properties: "A file named so that a reader can verify it has `name` and `checksum` (0032). A file the record carries or points to also has `description`, `contents`, `encoding` and `link` (0043)."

## Consequences
- No pull request; the rule is recorded with this ruling.
