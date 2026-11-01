# 0011 — Contributor optional; one basis entry for the MBPT dielectric matrix

Date: 2026-11-01. Status: accepted. Decided by: Ellad Tadmor.

## Context
Checking the examples against version 0.4.0 found two contradictions in the standard, both carried faithfully from the baseline .docx:

- **contributor** (minimal) was required, and so was its **affiliation**, although that property's own definition reads "…if they have one" and creator's affiliation is optional. A contributor is an entity that contributed to the dataset without being a primary creator; many datasets have none. In the DataCite Metadata Schema 4.6, Creator is Mandatory and Contributor only Recommended. The Minimal example's dataset (DOI 10.60732/8e9bc5b0) registers only ColabFit as contributor, as its registration agency, which is not a contribution in MatCore's sense.
- **dielectric-matrix** (MBPT) required both **planewave-basis-cutoff** and **local-orbital-basis-set**, while the note on each says to specify one or the other, "but not both". No dataset can satisfy both rules.

## Decision
1. `contributor` is optional (still repeatable). A dataset with no contributors in MatCore's sense omits it.
2. `contributor` › `affiliation` is optional, as for `creator`.
3. Under `dielectric-matrix`, neither `planewave-basis-cutoff` nor `local-orbital-basis-set` is required on its own; exactly one of the two must be given, as their notes state. Until conditional rules can be expressed in the schema (§1.3 proposal), this rule lives in the notes and is not checked automatically.

These depart from the baseline .docx deliberately. They are changes since 0.4.0 and go into the next release.

## Consequences
schema/minimal.yaml and schema/mbpt.yaml change; the Minimal example (no contributor) and the MBPT example (planewave cutoff only) conform as they are.
