# CLAUDE.md — standing context for Claude Code sessions in the MatCore repository

Read this before any change. It summarizes decisions recorded in docs/decisions/ and marks anything
not yet decided as 'PROPOSED, NOT DECIDED'. A statement without a record or that label is an error in
this file; raise it with the human. Do not reopen recorded decisions unless the human asks.

## What this repository is
The source of truth for the MatCore metadata standard for computational materials science
(https://matcore.org). The former Google Doc is retired; this repo replaces it.
GitHub organization: `matcore-standard`, repository `matcore-standard/matcore` (decided; see 0000). The
name `matcore` is held by a dormant personal account; a GitHub support request to contact the owner is
pending and unlikely to succeed. If `matcore` is ever released, whether to move to it or point it at
`matcore-standard` is an open decision. Only mkdocs.yml contains the repository URL; keep it that way.
Other files link relative to the site or read it from mkdocs.yml (0004).
The MatCore effort is funded by NSF DMR Award #2404283 and supported through the KIM Initiative (0004).

- `schema/<section>.yaml` — the standard's property hierarchy, one file per section
  (minimal, dft, md, mbpt, ml, pf, derived). THIS IS THE STANDARD.
- `schema/units.yaml` — Annex U, the normative unit table (kinds, symbols, QUDT/GNU mapping, SI factors).
- `schema/meta-schema.yaml` — JSON Schema (written in YAML) that section files must satisfy.
- `docs/standard/*.md` — prose chapters (01-introduction, annex-u-units) plus GENERATED chapters
  (02–08, annex-u-table). Never hand-edit generated files; edit the YAML and run `scripts/build_docs.py`.
- `docs/decisions/` — decision records: internal committee information, not published on the site
  (0004). 0001 is the units change list (not yet applied; see Status). The frozen Google Doc export
  is stored there as the baseline artifact.
- `scripts/validate_schema.py` — checks section files against the meta-schema and units.yaml. It
  validates the standard itself, not instance files (the instance validator is status step 9).
- `scripts/build_docs.py` — regenerates docs from YAML. CI runs both.

## Conventions for schema YAML (decided; see docs/decisions/0002 and 0004)
Keep it regular: no YAML anchors or aliases, custom tags, includes or templating.
Each property entry has exactly these fields, in this order (validate_schema.py will enforce the order):
`name, required, description, type, extent, kind, recommended-unit, values, repeatable,
[convention], [notes], [legacy_values], [legacy_unit], [subproperties]`.
- `type` ∈ string | float | int | bool | file | any.
- `extent`: KIM notation. `[]` scalar, `[3,3]` fixed, `[":"]` open length (quote the colon in YAML);
  `any` when the shape is not fixed by the schema. In prose write `[:]` without quotes.
- `any` (for type, extent or kind) means the schema leaves the field open and something else fixes it:
  the instance (generic parameters) or a required enumerated subproperty (e.g. `criterion` for the SCF
  tolerance, `basis` for exciton-momentum).
  PROPOSED, NOT DECIDED: a field such as `determined-by: criterion` naming what fixes an `any`, so the
  validator can check that the subproperty exists and is required.
- `kind`: a key of units.yaml#kinds, or reserved `dimensionless` | `inapplicable` | `any`.
  string/bool/file properties are always `inapplicable`; a physical quantity is never typed as a
  string. (The meaning of `file` in an instance is PROPOSED, NOT DECIDED; define it in the data
  model, independent of any serialization.)
- `recommended-unit`: informative only; must be a symbol in units.yaml with matching kind.
  PROPOSED, NOT DECIDED: no recommended unit when kind is `any`; null when kind is `dimensionless`.
- `values`: structured; replaces the old prose "Values" (0002). The key set (enum / minimum / maximum /
  format / pattern / examples / note) is PROPOSED, NOT DECIDED; settle it when step 5 opens
  minimal.yaml. Open questions: open-ended enums ("Other user-specified value"), enum values that
  carry definitions, enums that depend on another property, a closed vocabulary for `format`.
- `legacy_*` fields hold the Google Doc prose from the baseline migration. Delete each one once its
  content is transferred to the typed fields; the original wording remains in the baseline .docx and
  in git history (tag v0.9-baseline). A section is complete when no legacy_* remain.
- Names match `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` (meta-schema not yet updated). A name is plural only when
  its value is a list (open extent); a repeatable property stays singular. `unit` is singular.

## Units model (decided; see docs/decisions/0001 Part A and docs/standard/annex-u-units.md)
- Every dimensioned value in an instance file carries a `unit`; no default unit is ever implied.
- The schema declares `kind` + `recommended-unit`, not a fixed unit. Validation = kind compatibility
  via the dimension vector in units.yaml, using the closed symbol set. No unit parsing.
- Reserved kinds: dimensionless (ratios, counts), inapplicable (non-quantities), any (fixed by the
  instance or by a required enumerated subproperty).
  Angles and moles are NOT dimensionless.
- Conventions a unit cannot express (2π in reciprocal lengths, lattice vs Cartesian basis) are separate
  required enumerated subproperties (`convention`, `basis`, `scaling`), never encoded in the unit string.
- Energy and MolarEnergy are distinct kinds (Annex U Rule 8). kJ/mol, kcal/mol → MolarEnergy.
- CODATA 2022 factors are normative; QUDT (CODATA 2006) and GNU Units 2.23 (CODATA 2018) are stale.
- GNU Units pinned to 2.23 / definitions.units 3.19 for `x-gnu:` escape expressions.
- "Annex" (ISO usage), normative. Use "Kind" (not "Quantity kind") in the schema, the standard's prose
  and new text. Decision records are not rewritten. "Quantity kind" remains where it refers to QUDT's
  concept.

## Generic parameters and free-form units (decided; see docs/decisions/0001 and 0003)
Three groups, not to be merged:
1. Generic parameters: xc-parameter (dft), computation-parameter and td-parameter (md),
   model-parameter (pf), calculation-parameter (derived). Their `value` has type any, extent any,
   kind any; the instance supplies type, shape and unit. The generic-parameter rule applies to
   these only. The instance type is one of float, int, string, bool, and is stated in the instance,
   not inferred from how the value is written; each serialization (defined in §1.3) defines how.
   The value need not be a scalar (0004).
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
The standard is agnostic to serialization format, as §1.3 states. The XML examples in the standard
are illustrative only and do not prescribe a format for any implementation. Any serialization that
preserves the property hierarchy, the required/repeatable semantics and the value/unit/convention
structure is conformant. The MatCore tools (status item 9) will have to choose one or more concrete
serializations to read and write; that is a tool decision, not yet made, and it does not bind other
implementations. When it is made, a format-specific schema (e.g. XSD or JSON Schema) is generated
from the YAML for that serialization and used by CI to validate the examples (0004).

## Website and tools (see docs/decisions/0000 and 0004)
- Static site, MkDocs (Material), GitHub Pages, versioned with `mike`; built on every push to main
  by .github/workflows/ci.yml; no dynamic server (0000). The site is served at
  matcore-standard.github.io/matcore for now. matcore.org will point to it as soon as the site is
  clean and operational, replacing the current site there (0004).
- Tools: one Python package named `matcore`, run in-browser via Pyodide (0000, 0006).
  PROPOSED, NOT DECIDED: its contents (a command-line validator; parsers for VASP, QE and LAMMPS
  output; web validator, visualizer and forms); parsers as the primary generator of instances, web forms as the
  fallback. The serialization(s) it reads and writes: see status step 9.
- Licenses: CC BY 4.0 (standard text/schema), Apache-2.0 (code). Tagged releases get a Zenodo DOI.

## Known defects in the baseline (fix in the Part B PR)
- `localized-orbital-basis-set` (DFT-1) vs `localized-orbitals-basis-set` (DFT-4) vs
  `local-orbital-basis-set` (MBPT-1): three spellings. Migration aliased DFT-4 to the DFT-1 form.
  Use `localized-orbital-basis-set` in all three places, including references in notes (0004).
- An mbpt.yaml note refers to `basis-cutoff-planewave`; the property is `planewave-basis-cutoff`.
  Correct the reference (0004).
- Table MD-3 was malformed in the Google Doc: its header row was actually the `source` parent row.
  Migration handled it; check md.yaml › particle-interactions / source against the docx (0004).
- The accepted items of docs/decisions/0001-units-change-list.md Part B (see its Status line).
  B2 (added note), B4 (Ė symbol), B5 and B9 are PROPOSED, NOT DECIDED.

## Status / next steps (update this list as work lands)
The audit of this file is complete (rulings in docs/decisions/0004): every statement is backed by a
record or marked PROPOSED, NOT DECIDED.

1. [done] Baseline migration of Google Doc → schema/*.yaml (255 properties; typed fields present
   as null stubs; legacy_* preserved).
2. [todo] Website cleanup: the GitHub Pages site offers the user the same options as matcore.org,
   so it can replace it (0004). Presentation may differ and should use the semantic structure of
   the YAML to improve on the live site.
   - Menu, with navigation tabs: Home · About (About MatCore, Leadership) · Standard (the standard,
     Revision History) · Contact. toc_depth 2.
   - Migrate the content of About MatCore, Leadership, Revision History and Contact from
     matcore.org (this was step 8). Contact replaces the Feedback placeholder.
   - Under Standard, each section shows its introduction and its examples, as on matcore.org.
     Storage (0004): each schema/<section>.yaml gets a top-level `introduction` (Markdown in a
     literal block, one per section) and `examples` (a list; each entry has `caption`, `file` in
     examples/, `source`, optional `notes`). Text comes from the baseline .docx as it is. Needs
     the two fields added to meta-schema.yaml, and pymdownx.highlight + superfences for code.
   - build_docs.py renders the standard from the YAML; legacy_* fields hidden unless --show-legacy
     is passed, and CI builds with --show-legacy until step 5 is complete.
   - [done] Decision records are internal committee information: docs/decisions/, including the
     baseline .docx, is excluded from the site build (`exclude_docs` in mkdocs.yml; an unlinked page
     would still appear in sitemap.xml and the site search). They stay in the public GitHub
     repository. Site pages do not link to them.
   PROPOSED, NOT DECIDED: the property layout (render options in the preview for the human to
   choose); a Revision History entry for the baseline draft.
3. [merged into step 5] Apply 0001 Part A (kind/recommended-unit/convention) property by property
   (0004). What remains of this step does not belong to any one property, each its own change:
   reword Annex U to "Kind" (0004); check 0001 (A1.3, A10) and Annex U for XML-specific wording such
   as "unit as an attribute of the value element", since normative text describes unit, convention
   and basis as subproperties and each serialization decides whether they become attributes, child
   elements or object keys (0004); tighten the name pattern in meta-schema.yaml (all 255 current
   names pass it); add a field-order check to validate_schema.py.
   PROPOSED, NOT DECIDED: do these before step 5.
4. [todo] PR: apply 0001 Part B fixes + the known baseline defects listed above. Done before step 5
   (0004).
5. [todo] One PR per top-level property, covering all of its subproperties: 48 PRs (0004). Each PR,
   in this order: (a) cross-check the property against the baseline .docx (name, definition,
   values, required, repeatable, subproperty tree) so no definition or value was lost or altered
   in migration, and correct any migration error before filling anything; (b) fill
   type/extent/kind/recommended-unit/values, applying 0001 Part A to the property, and delete its
   legacy_* fields; (c) list in the PR description every judgment call in the mapping, so the
   human can decide. A section is complete when no legacy_* fields remain in its file.
   PROPOSED, NOT DECIDED: sections in the order minimal, dft, md, mbpt, ml, pf, derived, and
   properties in file order within a section; a check in validate_schema.py that fails if a
   section file declares `legacy_complete: true` but still contains legacy_* fields.
6. [todo] Committee decisions and community feedback (user will supply, after step 5):
   one decision record + one PR each.
7. [todo] Define, as a section of the standard, the serialization requirements that any format must
   satisfy (not a specific format). Provide example instances in examples/ in at least one
   serialization, generated from the same source, and validate them in CI against a schema
   generated from the YAML for that serialization.
   Order (0004): the examples and generated schema come after step 5, which fills the typed fields;
   this step may run alongside step 6, and the requirements section may be written earlier. It
   opens with a decision record choosing the first serialization, which step 9 then uses.
8. [merged into step 2] Site content migration from matcore.org.
9. [todo] `matcore` Python package: validator, then parsers, then Pyodide web tools. After step 7;
   the validator reuses step 7's generated schema (0004).
   PROPOSED, NOT DECIDED: serialization(s) the tools read and write beyond the first one chosen in
   step 7.

## Working rules (apply in every session)
- Decisions are made only by the human running the session. Never treat a suggestion, whether yours,
  from CLAUDE.md, or from an earlier conversation, as decided unless the human has explicitly confirmed
  it. If you find something in CLAUDE.md or in your task that is not backed by a decision record or an
  explicit confirmation, do not act on it: mark it 'PROPOSED, NOT DECIDED' in CLAUDE.md and raise it
  with the human to get a decision. Record every confirmed decision in docs/decisions/ before
  implementing it.
- Write each ruling into the repository (this file, plus a decision record where needed) before
  taking up the next item; show the diff and commit once the human approves. Never commit anything
  the human has not approved. Never push; the human pushes, since every push to main redeploys the
  site (0005). A commit contains only what its message describes. An edit that the change itself
  makes necessary (a cross-reference it invalidates) belongs in the same commit and is named in the
  message; any other change outside the task is raised with the human first (0004).
- Environment: uv owns it (0006). Dependencies live in pyproject.toml (a `dev` group for site and
  test tools) and are pinned in uv.lock; run `uv sync`, then every command through `uv run`.
  Never pip-install into the system Python.
- One decision per change. Changes to schema/, the generated docs or the site's build and content go
  through a pull request, so CI checks them before they reach main; the property PRs of status
  step 5 carry their judgment-call list in the description. Rulings and repository housekeeping may
  be committed directly to main once the human approves. Reference the decision record in the
  commit message (0004).
- Memory lives in the repository, not in chat or in Claude Code's private memory. Whenever a
  decision is made or changed, update the relevant section of this file and the status list in the
  same commit as the work. Update the status list whenever a step's state changes, so it is current
  even if a session ends without warning; at the end of a session, check that it says exactly what
  was done and what remains, and commit any correction. Assume the conversation will not be
  available next time (0004).
- Before every commit run the checks CI runs: `uv run python scripts/validate_schema.py`,
  `uv run python scripts/build_docs.py`, `uv run mkdocs build --strict`. Commit any files
  build_docs.py regenerates with the change; CI fails if the committed copies are stale. Never
  hand-edit generated files under docs/standard/ (02-*.md … 08-*.md, annex-u-table.md) (0004).
- Never invent QUDT identifiers, physical constants or unit symbols. units.yaml was verified against
  QUDT Units 3.3.0, GNU Units 2.23 (definitions.units 3.19) and NIST CODATA 2022. A new unit is
  added by pull request, with each of its fields (kind, QUDT identifier or null, GNU Units name,
  SI factor, source) traced to a primary source named in the PR. A new kind needs a decision
  record (0004).
