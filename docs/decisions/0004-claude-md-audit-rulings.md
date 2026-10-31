# 0004 — Rulings on the CLAUDE.md audit

Date: 2026-10-31. Status: accepted. Decided by: Ellad Tadmor.

## Context
CLAUDE.md stated a number of rules that no decision record backed. Each was reviewed one by one and ruled a decision, a proposal, or a correction. Rulings recorded elsewhere are not repeated here: the A3.3 removal (0001), the generic-parameter groups and the Annex U Rule 4 amendment (0001), and phase-field scaling (0003).

## Decisions
1. **Status of 0001.** Part A is accepted. In Part B, B1, B3, B4 (the unit), B6, B7, B8, B10 and B11 are accepted; B2 (the added note), B4 (the Ė symbol), B5 and B9 are proposals awaiting a decision; B12 needs no action. A6 is a proposal.
2. **GitHub organization.** The repository stays at `matcore-standard/matcore`. The name `matcore` is held by a dormant personal account; a GitHub support request to contact the owner is pending and unlikely to succeed. If `matcore` is released, whether to move to it or point it at `matcore-standard` will be decided then.
3. **Repository URL.** Only mkdocs.yml contains the repository URL. Other files link relative to the site or read it from mkdocs.yml.
4. **Baseline .docx.** The frozen Google Doc export stays in docs/decisions/ and is excluded from the published site. It remains downloadable from the public repository itself.
5. **Schema YAML is regular.** No YAML anchors or aliases, custom tags, includes or templating in schema files.
6. **Field set and order.** Each property entry has exactly the fields `name, required, description, type, extent, kind, recommended-unit, values, repeatable, [convention], [notes], [legacy_values], [legacy_unit], [subproperties]`, in that order. validate_schema.py will enforce the order.
7. **`any` is not limited to generic parameters.** `type`, `extent` and `kind` may be `any` wherever the schema leaves the field open and something else fixes it: the instance (generic parameters) or a required enumerated subproperty (e.g. `criterion` for the SCF tolerance, `basis` for exciton-momentum).
8. **Extent notation.** In YAML the open-length colon is quoted (`[":"]`); in prose and generated docs it is written `[:]`.
9. **Inapplicable kinds.** string, bool and file properties have kind `inapplicable`; a physical quantity is never typed as a string.
10. **Recommended unit.** Informative only; it must be an Annex U symbol whose kind matches the property's kind.
11. **Structured `values`.** `values` is structured and replaces the prose "Values" (0002). Its key set is a proposal.
12. **`legacy_*` fields.** The baseline prose is kept in `legacy_*` fields during migration and deleted once its content is transferred to the typed fields. The original wording remains in the baseline .docx and in git history (tag `v0.9-baseline`). A section is complete when no `legacy_*` fields remain.
13. **Names.** Names match `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`. A name is plural only when its value is a list (open extent); a repeatable property with a single value per occurrence stays singular. `unit` is singular.
14. **Terminology.** "Annex" for Annex U, which is normative. "Kind", not "Quantity kind", in the schema, the standard's prose and new text. Decision records are not rewritten. "Quantity kind" remains where it refers to QUDT's concept.
15. **Funding.** The MatCore effort is funded by NSF DMR Award #2404283 and supported through the KIM Initiative.

## Consequences
CLAUDE.md is updated to match, and every unbacked statement in it is marked PROPOSED, NOT DECIDED. Follow-up changes: exclude the .docx from the site build (4); tighten the name pattern in the meta-schema (13); add a field-order check to validate_schema.py (6); reword Annex U to "Kind" when 0001 Part A is applied (14).
