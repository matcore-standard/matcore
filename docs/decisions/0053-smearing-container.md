# 0053 — Smearing leaves the k-point mesh

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding C5 of the minimal–dft analysis (2026-11-08): dft `k-point-mesh` holds three properties of the mesh (`type`, `number-of-points`, `shift`) and three of the electronic occupations (`smearing-type`, `smearing-width`, `smearing-parameter`). Smearing assigns fractional occupations to states near the Fermi level; it is often needed because of k-point sampling in metals, but it is not part of the mesh, and it also applies where there is no mesh (e.g. a molecule in a Gaussian-basis code). As placed, such a calculation must give a `k-point-mesh` to state its smearing.

## Decision
1. **dft `settings` gains `smearing`** after `k-point-mesh`: optional, not repeatable, a container. Description: "The method of assigning fractional occupations to electronic states near the Fermi level, and its parameters." Its members, in order, moved from `k-point-mesh` with their descriptions, values and notes unchanged:
   - `type` (was `smearing-type`), optional as before;
   - `width` (was `smearing-width`), with the note of 0052;
   - `parameter` (was `smearing-parameter`), a generic parameter (0016), repeatable as before.
2. **`k-point-mesh`** keeps `type`, `number-of-points` and `shift`.
3. **examples/dft.json** moves its smearing width (0.05 eV) from `k-point-mesh` to `smearing › width`.

## Consequences
- One pull request applies items 1–3 (schema, tests, regenerated page, example), with 0052's note. It breaks 0.6.0 dft instances that give smearing.
- References to `smearing-type`, `smearing-width` or `smearing-parameter` in notes and in CLAUDE.md are updated in the same pull request.
