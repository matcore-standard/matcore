# 0055 — When a `doi` string, when an `identifier` container

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding C2 of the minimal–dft analysis (2026-11-08): the standard identifies things in two ways. Four properties are a `doi` string in Annex I's https form (minimal `publication` and `dataset-location`, dft `pseudopotential-or-paw` and `localized-orbital-basis-set`; 0014, settled 2026-11-04). Others are an `identifier` container of a value and a scheme (0014): creator, contributor and record-author with their affiliations (ORCID, ISNI, ROR), funder (ROR, ISNI), topology (AFLOW, InChI, SMILES; 0034), software (DOI, SWHID; 0043). The difference follows an unwritten rule: a container where several schemes are in use for the thing identified, a `doi` string where DOI is the scheme in practice (papers, deposited datasets, published pseudopotential libraries). Turning the `doi` strings into containers would add a scheme field with one value.

## Decision
1. **No property changes.** The four `doi` strings stay.
2. **The rule is stated** in CLAUDE.md's conventions for schema YAML and applied to new properties (mbpt, ml and derived have `doi` fields to come): "An `identifier` container (value and scheme, Annex I) is used where more than one identifier scheme is in use for the thing identified; a `doi` string, in Annex I's DOI form, where DOI is the scheme in use. Another address is given in a `link`."

## Consequences
- No pull request; the rule is recorded with this ruling.
