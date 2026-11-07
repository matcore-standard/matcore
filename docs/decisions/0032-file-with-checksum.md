# 0032 — A file holds its checksums

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee change: in `provenance`, replace `checksum › file` by `file › checksum`, a repeatable container `file` holding the file's `name` and a `checksum` of `algorithm` and `value`; make the same change wherever else `checksum` appears.

`checksum` (file, algorithm, value) appears in three places: minimal `provenance › checksum` (repeatable, one entry per checksum), and dft `core-electron-treatment › pseudopotential-or-paw › checksum` and `wavefunction-representation › localized-orbital-basis-set › checksum` (each at most once). Structured by checksum, a file with two checksums repeats its name; structured by file, the name is given once and the checksums sit under it.

## Decision
1. **minimal `provenance › checksum`** is replaced by **`provenance › file`**: optional, repeatable, a container. Description: "A file of the dataset, or associated with it, modified by the provenance event." Its subproperties, in order:
   - **`name`**: required; string, `[]`, inapplicable. Description: "The name of the file."
   - **`checksum`**: required, repeatable (a file may have checksums by several algorithms), a container. Description: "A digital fingerprint of the file, computed by a named algorithm." Its subproperties are the present `algorithm` and `value`, unchanged (terms and note of SPDX 2.3.1 §8.4; lowercase hexadecimal pattern).
2. **dft `pseudopotential-or-paw › checksum`** is replaced by **`pseudopotential-or-paw › file`**, with the same subproperties: optional, not repeatable (as the present checksum). Description: "The pseudopotential or PAW dataset file, with its checksums." Its note becomes "Note: Use file when the pseudopotential or PAW dataset is identified by a checksum of its file (e.g. the SHA256 hash of a VASP POTCAR file). For any other designation, use unique-identifier." `unique-identifier`'s note becomes "Note: For a checksum of the pseudopotential or PAW dataset file, use file instead."
3. **dft `localized-orbital-basis-set › checksum`** is replaced likewise by **`localized-orbital-basis-set › file`**. Description: "The localized-orbital basis set file, with its checksums." Its note becomes "Note: Use file when the basis set is identified by a checksum of its file. For any other designation, use unique-identifier." `unique-identifier`'s note becomes "Note: For a checksum of the basis set file, use file instead."

All three `file` containers have the same subproperties, so a checksum is written the same way everywhere.

## Consequences
- One pull request applies items 1–3 (schemas, tests, regenerated pages). The examples give no checksum and need no change. No MatCore instances exist yet, so the restructuring breaks none.
- minimal `computation › software › file` (name, description, contents, link) is a different property and is unchanged.
