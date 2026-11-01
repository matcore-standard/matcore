# Contributing to MatCore

- Feedback on the standard: open a GitHub issue using the "Standard feedback" template.
- Changes to the schema are made by pull request against `schema/*.yaml`. Never edit the generated
  chapters in `docs/standard/02-*.md` … `08-*.md` or `annex-u-table.md`; they are rebuilt from the YAML.
- Every PR must pass `scripts/validate_schema.py`. Run `scripts/build_docs.py --show-legacy` and commit the result.
- Each substantive change should reference a decision record in `docs/decisions/`. Add a new numbered
  record (NNNN-short-title.md: context, decision, consequences) when the committee decides something.
- Units: symbols must come from `schema/units.yaml`. To add a unit, add a row with a verified QUDT IRI
  (or null) and a CODATA-2022-based SI factor, and say in the PR how it was verified.
