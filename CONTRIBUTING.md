# Contributing to MatCore

- Feedback on the standard: open a GitHub issue using the "Standard feedback" template.
- Changes to the schema are made by pull request against `schema/*.yaml`. Never edit the generated
  chapters in `docs/standard/02-*.md` … `08-*.md` or the marked Tables U.3 and U.4 in `annex-u-units.md`;
  they are rebuilt from the YAML.
- Every PR must pass `scripts/validate_schema.py`. Run `scripts/build_docs.py --show-legacy` and commit the result.
- Each substantive change should reference a decision record in `docs/decisions/`. Add a new numbered
  record (NNNN-short-title.md: context, decision, consequences) when the committee decides something.
- Versions: the standard's version and history live in `schema/releases.yaml`; releases are cut per
  milestone, not per change (see the README, "Releasing a version").
- Units: symbols must come from `schema/units.yaml`. To add a unit, add a row with a verified QUDT IRI
  (or null) and a CODATA-2022-based SI factor, and say in the PR how it was verified. Write the factor
  as quoted decimal text with its published digits (e.g. `si_factor: "5.29177210544e-11"`); Annex U's
  tables are regenerated from `units.yaml` by `scripts/build_docs.py`.
