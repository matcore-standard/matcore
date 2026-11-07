# 0030 — Award title, provenance note and provenance agent

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee changes to minimal metadata:
- `funding › award-title` should be optional.
- `provenance` should say that maintaining the dataset's provenance is recommended.
- `provenance › agent` should have the same schema as `creator`.

`award-title` is required today, although a funder and an award number identify an award without its title. `agent` is a single string ("Identity of the entity responsible for the change."), while `creator` and `contributor` share a structure of a name, scheme-tagged identifiers and affiliations (0014).

## Decision
1. **`funding › award-title`** becomes optional. Nothing else in `funding` changes.
2. **`provenance`** gains the note "Note: It is recommended to record the provenance of the dataset and to keep it current with each change." `provenance` stays optional.
3. **`provenance › agent`** takes `creator`'s structure: required and repeatable (several entities may make one change), a container of `name*`, a repeatable `identifier` (`value*`, `scheme*` with terms ORCID, ROR, DOI, SWHID, ISNI and creator's note) and a repeatable `affiliation` (`name*`, at most one `identifier` with schemes ROR and ISNI), with creator's descriptions and examples, worded for the change:
   - `agent`: "An entity (e.g. person, organization, software agent) responsible for the change, and their institutional affiliation if relevant."
   - `agent › name`: "The name of the entity that made the change."
   - `agent › identifier`: "A unique, persistent identifier that globally and unambiguously identifies the entity that made the change."
   - `agent › affiliation`: "The affiliation of the entity that made the change if they have one."

## Consequences
- One pull request applies items 1–3 (schema, tests, regenerated page). examples/minimal.xml has no `provenance` or award title and needs no change.
- tests/test_properties.py's check that creator and contributor follow 0014 covers agent too.
