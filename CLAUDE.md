# CLAUDE.md — standing context for Claude Code sessions in the MatCore repository

Read this before any change. It records design decisions made by the MatCore committee (via the
lead editor) in September–October 2026. Do not reopen settled decisions unless the user asks; add new
decisions to docs/decisions/ as short numbered files.

## What this repository is
The source of truth for the MatCore metadata standard for computational materials science
(https://matcore.org). The former Google Doc is retired; this repo replaces it.
GitHub organization: `matcore-standard`, repository `matcore-standard/matcore`. (The name `matcore` is held
by a dormant personal account; if it is ever released, rename the org and immediately re-create an empty
`matcore-standard` organization so the old URLs keep redirecting.) Only mkdocs.yml and README.md contain the
repository URL; keep it that way.
The MatCore effort is funded by NSF DMR Award #2404283 and supported through the KIM Initiative.

- `schema/<section>.yaml` — the standard's property hierarchy, one file per section
  (minimal, dft, md, mbpt, ml, pf, derived). THIS IS THE STANDARD.
- `schema/units.yaml` — Annex U, the normative unit table (kinds, symbols, QUDT/GNU mapping, SI factors).
- `schema/meta-schema.yaml` — JSON Schema (written in YAML) that section files must satisfy.
- `docs/standard/*.md` — prose chapters (01-introduction, annex-u-units) plus GENERATED chapters
  (02–08, annex-u-table). Never hand-edit generated files; edit the YAML and run `scripts/build_docs.py`.
- `docs/decisions/` — decision records. 0001 is the units change list (not yet applied; see Status).
  The frozen Google Doc export is stored there as the baseline artifact.
- `scripts/validate_schema.py` — must pass before any commit touching schema/.
- `scripts/build_docs.py` — regenerates docs from YAML. CI runs both.

## Conventions for schema YAML (keep it regular; no includes, no macros)
Each property entry has exactly these fields, in this order:
`name, required, description, type, extent, kind, recommended-unit, values, repeatable,
[convention], [notes], [legacy_values], [legacy_unit], [subproperties]`.
- `type` ∈ string | float | int | bool | file | any. `any` only for the `value` of generic parameters.
- `extent`: KIM notation. `[]` scalar, `[3,3]` fixed, `[":"]` open length (quote the colon in YAML);
  `any` (rank unknown) only for generic parameters. In prose write `[:]` without quotes.
- `kind`: a key of units.yaml#kinds, or reserved `dimensionless` | `inapplicable` | `any`.
  string/bool/file properties are always `inapplicable`.
- `recommended-unit`: informative only; must be a symbol in units.yaml with matching kind.
- `values`: structured (enum / minimum / maximum / format / pattern / examples / note). Replaces the old prose "Values".
- `legacy_*` fields hold the Google Doc prose from the baseline migration. Delete each one as the
  typed fields for that property are filled in. The baseline is complete when no legacy_* remain.
- Names are lowercase-hyphenated. `unit` is singular everywhere.

## Units model (decided; see docs/decisions/0001 and docs/standard/annex-u-units.md)
- Every dimensioned value in an instance file carries a `unit`; no default unit is ever implied.
- The schema declares `kind` + `recommended-unit`, not a fixed unit. Validation = kind compatibility
  via the dimension vector in units.yaml, using the closed symbol set. No unit parsing.
- Reserved kinds: dimensionless (ratios, counts), inapplicable (non-quantities), any (generic params).
  Angles and moles are NOT dimensionless.
- Conventions a unit cannot express (2π in reciprocal lengths, lattice vs Cartesian basis) are separate
  required enumerated subproperties (`convention`, `basis`, `scaling`), never encoded in the unit string.
- Energy and MolarEnergy are distinct kinds (Annex U Rule 8). kJ/mol, kcal/mol → MolarEnergy.
- CODATA 2022 factors are normative; QUDT (CODATA 2006) and GNU Units 2.23 (CODATA 2018) are stale.
- GNU Units pinned to 2.23 / definitions.units 3.19 for `x-gnu:` escape expressions.
- "Annex" (ISO usage), normative; use "Kind" (not "Quantity kind") in all text.

## Generic parameters and free-form units (decided; see docs/decisions/0001 and 0003)
Three groups, not to be merged:
1. Generic parameters: xc-parameter (dft), computation-parameter and td-parameter (md),
   model-parameter (pf), calculation-parameter (derived). Their `value` has type any, extent any,
   kind any; the instance supplies type, shape and unit. The generic-parameter rule applies to
   these only. (Restricting the instance type to float|int|string|bool: PROPOSED, NOT DECIDED.)
2. Free-form units: field-variable, free-energy (pf). No `value`; a free-form `unit` whose kind
   the schema does not fix.
3. Typed properties with a required unit: grid-spacing (Length, recommended m) and time-step-size
   (Time, recommended s) (pf). Handled like temperature, not as generic parameters. With
   domain-size they carry a required `scaling` subproperty [physical, nondimensional]; when
   nondimensional, `unit` SHALL be `dimensionless` (0003).
Every `unit` subproperty has kind inapplicable and holds an Annex U symbol or `dimensionless`. The
`x-gnu:` escape (Annex U Rule 4) is permitted only in groups 1 and 2, where the schema does not fix
the kind; group 3 and all other typed properties use Annex U symbols only (0001 A1.1).
PROPOSED, NOT DECIDED: state conditional validation rules (the allowed unit or values of one
subproperty depend on another's value: `convention` for k-point-spacing, `basis` for
exciton-momentum, `scaling` for PF lengths and times) once in §1.3, so each property refers to the
rule rather than restating it. Needs a decision before implementation.
PROPOSED, NOT DECIDED: define this pattern once in §1.3 under a name such as "generic parameter", with
each such entry tagged `pattern: generic-parameter` and checked by validate_schema.py against one
canonical definition. Needs a decision before implementation.

## Instance serialization
XML is the working assumption for instance files (unit/convention/basis as attributes of the value
element; child-element form also conformant). Define the XML mapping before building tools.
A JSON mapping may follow from the same data model.

## Website and tools (decided)
- Static site, MkDocs (Material), GitHub Pages, custom domain matcore.org, versioned with `mike`.
  Generated on every push to main by .github/workflows/ci.yml. No dynamic server.
- Tools: one Python package `matcore` (validator CLI + parsers for VASP/QE/LAMMPS output → MatCore XML),
  run in-browser via Pyodide for the website validator/visualizer/forms. Web forms are the fallback;
  parsers are the primary generator.
- Licenses: CC BY 4.0 (standard text/schema), Apache-2.0 (code). Tagged releases get a Zenodo DOI.

## Known defects in the baseline (fix in the Part B PR)
- `localized-orbital-basis-set` (DFT-1) vs `localized-orbitals-basis-set` (DFT-4) vs
  `local-orbital-basis-set` (MBPT-1): three spellings. Migration aliased DFT-4 to the DFT-1 form.
- Table MD-3 was malformed in the Google Doc: its header row was actually the `source` parent row.
  Migration handled it; check md.yaml › computation-parameter / source for correctness.
- All items in docs/decisions/0001-units-change-list.md Part B.

## Status / next steps (update this list as work lands)
1. [done] Baseline migration of Google Doc → schema/*.yaml (255 properties; typed fields present
   as null stubs; legacy_* preserved).
2. [todo] Website cleanup so changes can be reviewed on the rendered site (tabs, toc_depth,
   remove placeholder pages, table rendering in build_docs.py, --show-legacy flag).
3. [todo] PR: apply docs/decisions/0001-units-change-list.md Part A (kind/recommended-unit/convention).
4. [todo] PR: apply 0001 Part B fixes + the known baseline defects listed above.
5. [todo] One PR per section, in the order minimal, dft, md, mbpt, ml, pf, derived: fill
   type/extent/kind/values for every property, deleting its legacy_* fields as each is done.
   For each PR: (a) cross-check every property against the baseline .docx so no definition or
   value was lost or altered in migration; (b) list in the PR description any property where
   the typed fields required a judgment call, so the user can decide; (c) a section is complete
   only when no legacy_* fields remain in its file. Add a check to validate_schema.py that fails
   if a section file declares `legacy_complete: true` but still contains legacy_* fields.
6. [todo] Committee decisions and community feedback (user will supply, after step 5):
   one decision record + one PR each.
7. [todo] XML mapping spec; example instances in examples/; CI validates examples against generated XSD.
8. [todo] MkDocs site content: migrate About/Leadership/Feedback/Revision history from matcore.org.
9. [todo] `matcore` Python package: validator, then parsers, then Pyodide web tools.

## Working rules (apply in every session)
- Decisions are made only by the human running the session. Never treat a suggestion, whether yours,
  from CLAUDE.md, or from an earlier conversation, as decided unless the human has explicitly confirmed
  it. If you find something in CLAUDE.md or in your task that is not backed by a decision record or an
  explicit confirmation, do not act on it: mark it 'PROPOSED, NOT DECIDED' in CLAUDE.md and raise it
  with the human to get a decision. Record every confirmed decision in docs/decisions/ before
  implementing it.
- Environment: use the `matcore` conda environment for every command (`conda activate matcore`;
  create it from environment.yml). Never pip-install into the system Python.
- Permissions: propose changes, let the user review the diff, then commit. Never commit anything
  the user has not approved. A commit contains only what its message describes; if a change outside
  the current task seems necessary, say so and get agreement first.
- One decision per pull request. Write or update a record in docs/decisions/ before making the
  change, and reference it in the commit message.
- Memory lives in the repository, not in chat. Whenever a decision is made or changed in
  conversation, update the relevant section of this file and the status list in the same commit as
  the work. At the end of every session, update the status list to say exactly what was done and
  what remains, and commit it. Assume the conversation will not be available next time.
- Before every commit run: `python scripts/validate_schema.py`, `python scripts/build_docs.py`,
  `mkdocs build --strict`. Never hand-edit generated files under docs/standard/ (02-*.md … 08-*.md,
  annex-u-table.md).
- Never invent QUDT IRIs, physical constants or unit symbols; units.yaml was verified against
  primary sources. New units need a verified source stated in the PR.
