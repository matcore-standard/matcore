# 0033 — Author of the MatCore metadata record

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee change: after `matcore-id`, add a repeatable `matcore-author` with the same schema as `creator`, listing the entity that created the MatCore metadata record.

`creator` and `contributor` name who made the dataset; `matcore-id` and `matcore-date` identify and date the metadata record, but nothing names who wrote it. The record is often written by someone other than the dataset's creators (a curator, a repository, a parser).

## Decision
1. **A new top-level property `matcore-author`**, after `matcore-id` and before `matcore-date`: required, repeatable, with `creator`'s structure (0014): `name*`, a repeatable `identifier` (`value*`, `scheme*` with terms ORCID, ROR, DOI, SWHID, ISNI and creator's note) and a repeatable `affiliation` (`name*`, at most one `identifier` with schemes ROR and ISNI), with creator's examples. Descriptions:
   - `matcore-author`: "An entity (e.g. person, organization, software agent) responsible for creating the MatCore metadata record, and their institutional affiliation if relevant."
   - `name`: "The name of the entity that created the metadata record."
   - `identifier`: "A unique, persistent identifier that globally and unambiguously identifies the entity that created the metadata record."
   - `affiliation`: "The affiliation of the entity that created the metadata record if they have one."
2. **examples/minimal.xml** gains, after `matcore-id`, a `matcore-author` with name "Ellad B. Tadmor", identifier https://orcid.org/0000-0003-3311-6299 (scheme ORCID; Annex I's https form, check digit verified) and affiliation name "University of Minnesota", as given by the decider. (Amended 2026-11-07: the ORCID iD added after PR #64.)

## Consequences
- One pull request applies item 1 and item 2 (schema, tests, regenerated page, example). No MatCore instances exist yet, so the new required property breaks none.
- tests/test_properties.py's check that creator and contributor follow 0014 covers matcore-author too, as it does provenance's agent (0030).
