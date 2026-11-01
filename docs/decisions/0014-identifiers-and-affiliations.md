# 0014 — Identifiers with a scheme; affiliation as a container

Date: 2026-11-01. Status: accepted. Decided by: Ellad Tadmor.

## Context
In the baseline, `creator` and `contributor` (minimal) each have four subproperties: `name`, `affiliation` (a repeatable string), `creator-identifier` or `contributor-identifier`, and `affiliation-identifier` (both repeatable strings).

- **Affiliations and their identifiers are unlinked.** Two independently repeatable lists cannot say which identifier belongs to which affiliation.
- **Identifiers cannot be checked.** The definitions require "a unique, persistent URI", while the values text allows ORCID, ROR, DOI, SWHID "or other suitable identifier", some of which have no URI form. A URI check alone accepts any well-formed URI, valid identifier or not.

DataCite Metadata Schema 4.6 solves both. A `nameIdentifier` (0–n) carries a required `nameIdentifierScheme`. Each `affiliation` (0–n) carries at most one `affiliationIdentifier`, with a required `affiliationIdentifierScheme`. The format of a value depends on its scheme.

## Decision
1. **Structure.** `creator` and `contributor` both take this form, keeping their own required and repeatable flags:
   ```
   creator | contributor        container
   ├── name*                    string
   ├── identifier               container, repeatable
   │   ├── value*               string
   │   └── scheme*              string; terms: ORCID, ROR, DOI, SWHID, ISNI
   └── affiliation              container, repeatable
       ├── name*                string
       └── identifier           container, at most once
           ├── value*           string
           └── scheme*          string; terms: ROR, ISNI
   ```
   `creator-identifier` and `contributor-identifier` become `identifier`. The string `affiliation` becomes `affiliation` › `name`. `affiliation-identifier` becomes `affiliation` › `identifier`, one per affiliation. The definitions speak of an identifier rather than a URI. ISNI is not in the baseline; it is added because DataCite lists it for both persons and organizations.
2. **Open schemes.** `scheme` is an open vocabulary (0013): an unlisted scheme conforms and is reported as user-specified.
3. **Scheme table.** `schema/identifier-schemes.yaml` is the single source of the rule each listed scheme's values follow, as units.yaml is for units. Each entry gives the entities it identifies, the canonical form of a value (full URI or bare identifier, as the scheme's own documentation prescribes), a regular expression for that form, its check-digit algorithm or none, a valid example, and the scheme's documentation as source. Every field is traced to that primary source; nothing is invented. A scheme is added by pull request with its source.
4. **Validation.**
   - **The standard:** `validate_schema.py` checks that every entry is complete, that each example matches its pattern and passes its checksum, and that every scheme a property lists in `terms` is in the table.
   - **Instances (status step 9):** a value whose scheme is in the table is checked against that scheme's pattern and checksum. A value whose scheme is not in the table cannot be checked; it is accepted with a notice.

## Consequences
- **Order of work.**
  1. A pull request builds the table, with the five schemes above and the checks of item 4.
  2. The property pull requests for `creator`, then `contributor`, apply item 1, citing this record.
- **Examples.** `examples/minimal.xml` changes in the `creator` pull request (0012): each `<affiliation>` text becomes an `<affiliation>` with a `<name>`.
- **Open questions,** settled in the table's pull request:
  - Is the table published on the site, as an annex of the standard?
  - Should other identifier properties (e.g. dft `unique-identifier`) use it?
- This changes the standard beyond the baseline and goes into the next release.

## Settled 2026-11-01 (Ellad Tadmor)
1. The table is published as **Annex I — Identifier Schemes**, normative, beside Annex U. Its table is generated from `schema/identifier-schemes.yaml` by build_docs.py, as Tables U.3 and U.4 are from units.yaml; the YAML prevails.
2. dft `unique-identifier` holds a hash (e.g. SHA256), not an identifier in a scheme, and does not use the table. Whether and how the dft `doi` properties check against the table's DOI entry is decided in their property pull request.
