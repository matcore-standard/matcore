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
  The single source of Annex U's Tables U.3 and U.4, which build_docs.py generates into
  annex-u-units.md; it prevails over the annex. Factors are exact decimal text, e.g. "1e3" (0009).
- `schema/identifier-schemes.yaml` — Annex I, the identifier schemes (ORCID, ROR, DOI, SWHID, ISNI):
  for each, entities identified, canonical form, pattern, check digit, example, source. Single source
  of Annex I's Table I.1 and of identifier checks (scripts/check_identifiers.py), as units.yaml is
  for units; it prevails over the annex (0014).
- `schema/meta-schema.yaml` — JSON Schema (written in YAML) that section files must satisfy.
- `docs/standard/*.md` — prose chapters (index = title and 1. Preamble, annex-u-units,
  annex-i-identifiers) plus GENERATED chapters (02–08, revision-history, and the marked regions in
  index and the annexes: version line, Tables U.3/U.4, Table I.1).
  Never hand-edit generated parts; edit the YAML and run
  `scripts/build_docs.py --show-legacy`.
- `docs/decisions/` — decision records: internal committee information, not published on the site
  (0004). 0001 is the units change list (not yet applied; see Status). The frozen Google Doc export
  is stored there as the baseline artifact.
- `scripts/validate_schema.py` — checks section files against the meta-schema and units.yaml. It
  validates the standard itself, not instance files (the instance validator is status step 9).
- `scripts/build_docs.py` — regenerates docs from YAML in the layout of 0007; tested by
  tests/test_build_docs.py. Run it with `--show-legacy` until status step 5 is complete (CI does).
  CI runs both scripts.
- `docs/assets/matcore/` — layout.css and layout.js for the standard pages (0007).

## Conventions for schema YAML (decided; see docs/decisions/0002 and 0004)
Keep it regular: no YAML anchors or aliases, custom tags, includes or templating.
Each property entry has exactly these fields, in this order (validate_schema.py enforces the order):
`name, required, description, type, extent, kind, recommended-unit, values, repeatable,
[convention], [notes], [legacy_values], [legacy_unit], [subproperties]`.
- `type` ∈ string | float | int | bool | file | any. A container (subproperties, no value of its
  own) has type, extent, kind, recommended-unit and values all null (0004 item 37).
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
  Null when kind is `dimensionless` (0004 item 39).
  PROPOSED, NOT DECIDED: no recommended unit when kind is `any`.
- `values`: structured; replaces the old prose "Values" (0002). Null or a mapping of `terms` (open
  vocabulary: unlisted strings conform, reported as user-specified, near-misses as possible typos),
  `enum` (closed list), `minimum`/`maximum` (inclusive), `format` (a JSON Schema 2020-12 format
  name, always checked), `pattern`, `examples` (data; must satisfy the property), `note` (0013).
  Most vocabularies are open: use `terms` for "Other user-specified value", `enum` only where an
  unlisted value would make the data meaningless. Keys apply together and are tied to `type`
  (terms/enum/format/pattern: string; minimum/maximum: int, float); at most one of terms/enum and
  of format/pattern (0013). A term's definition is prose in `note`, in the baseline's wording;
  terms and enum stay plain lists (0013, settled 2026-11-02). Deferred to the first property that
  needs them: values that depend on another property (0013 item 4 holds the proposal).
- `legacy_*` fields hold the Google Doc prose from the baseline migration. Delete each one once its
  content is transferred to the typed fields; the original wording remains in the baseline .docx and
  in git history (tag v0.9-baseline). A section is complete when no legacy_* remain.
- Names match `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` (enforced by meta-schema.yaml). A name is plural only when
  its value is a list (open extent); a repeatable property stays singular. `unit` is singular.

## Units model (decided; see docs/decisions/0001 Part A and docs/standard/annex-u-units.md)
- Every dimensioned value in an instance file carries a `unit`; no default unit is ever implied.
- The schema declares `kind` + `recommended-unit`, not a fixed unit. Validation = kind compatibility
  via the dimension vector in units.yaml, using the closed symbol set. No unit parsing.
- A property with a physical kind (a units.yaml kind other than dimensionless) has exactly one
  required `unit` subproperty in one fixed form (string, [], inapplicable, values null, fixed
  description), and a dimensionless or inapplicable property has none; validate_schema.py checks
  both. A `unit` under a container (generic parameters, free-form units) is outside the check (0015).
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
rule rather than restating it. Needs a decision before implementation. Decide it together with the
`depends-on`/`cases` proposal of 0013 item 4, when md opens.
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

## Versions and releases (decided; see docs/decisions/0010)
- Semantic versioning MAJOR.MINOR.PATCH; below 1.0, breaking changes or new property sets raise MINOR,
  editorial or non-breaking fixes raise PATCH. A release is cut per milestone (a status step or a batch
  of committee decisions), never per change.
- schema/releases.yaml is the single source: the release history, newest first; the newest entry is the
  current version. build_docs.py generates the Revision History page and the version line on every
  standard page from it. Section files carry no version.
- A release: one commit on main adding the new entry, then the human tags it vX.Y.Z and pushes the tag;
  CI checks the tag against releases.yaml and deploys X.Y.Z with alias `latest`. Pushes to main deploy
  only `dev`, labelled as unreleased. Permalinks copy the concrete version's address (`latest` resolved;
  `dev` with a warning). The tag v0.9-baseline marks the baseline commit and is not a release.

## Website and tools (see docs/decisions/0000, 0004, 0007 and 0008)
- Static site, MkDocs (Material), GitHub Pages, versioned with `mike`; built on every push to main
  by .github/workflows/ci.yml; no dynamic server (0000). The site is served at
  matcore-standard.github.io/matcore for now. matcore.org will point to it as soon as the site is
  clean and operational, replacing the current site there (0004).
- Standard section pages follow docs/decisions/0007 (decided): every property, at every depth, is
  the same collapsible block; title bar = bold name, red asterisk if required, `autorenew` /
  `autorenew-off` icon for repeatable / at most once; body = description, six-column attribute table
  (Required, Repeatable, Type, Extent, Kind, Rec. unit), values, nested subproperties. Citable
  address per property (`#section.path.to.property`, static id) with a permalink button; property
  tree under the page's entry in the left menu (0008), breadcrumb bar on narrow screens; stacked
  table on phones; site-wide palette sampled from the logo. Implementation: scripts/build_docs.py (markup) and
  docs/assets/matcore/layout.css and layout.js. Read 0007, including its implementation
  constraints, before changing how the pages look or behave; its open points are PROPOSED, NOT
  DECIDED.
- Navigation follows docs/decisions/0008 (decided): left menu, collapsed to Home · About · Standard ·
  Contact; Standard ▸ Browse Standard (numbered as on matcore.org: 1. Preamble, 1.1–1.3; 2. Schema,
  2.1–2.7; Annex U; Annex I (0014)) and Revision History; no tabs; no right-hand TOC (page
  headings in the left menu, toc_depth 2); logo before "MatCore" in the menu title. Menu labels are set in mkdocs.yml `nav`.
  Browse Standard opens the Preamble (docs/standard/index.md), which overrides/partials/nav-item.html
  (a one-line change to the theme's template; re-apply on theme upgrades) also lists as "1. Preamble".
  Home page: no visible title, no links line.
- Tools: one Python package named `matcore`, run in-browser via Pyodide (0000, 0006).
  PROPOSED, NOT DECIDED: its contents (a command-line validator; parsers for VASP, QE and LAMMPS
  output; web validator, visualizer and forms); parsers as the primary generator of instances, web forms as the
  fallback. The serialization(s) it reads and writes: see status step 9.
- Licenses: CC BY 4.0 (standard text/schema), Apache-2.0 (code). Tagged releases get a Zenodo DOI.

## Known defects in the baseline (fixed in status step 4, PR #8)
All items below are fixed: the MBPT entry is renamed `localized-orbital-basis-set` and both MBPT notes
name the properties correctly; MD-3 was checked against the docx and matches; the accepted Part B
items are applied in their "alone" form (see 0001's note). Kept for reference.
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
   - [done, PR #1 merged 2026-11-01] Menu as in 0008 (replaces the navigation tabs of
     0004 item 21). Contact page migrated; the Feedback placeholder is removed.
   - [done, PR #2] Content of About MatCore, Leadership and Revision
     History migrated from matcore.org (this was step 8), with the edits of 0004 item 32. Page
     titles and section headings site-wide made compact (0008 item 8).
   - [done, PR #1] Section titles (schema/*.yaml `title`, used for page headings and
   menu labels): 2.1 Minimal MatCore Metadata, 2.2 Density Functional Theory (DFT) Metadata, …,
   2.7 Derived Property Metadata (0008).
   - Under Standard, each section shows its introduction and its examples, as on matcore.org.
     Storage (0004): each schema/<section>.yaml has a top-level `introduction` (Markdown in a
     literal block, one per section) and gets `examples` (a list; each entry has `caption`, `file`
     in examples/, `source`, optional `notes`). Text comes from the baseline .docx as it is.
     [done, PR #1] `introduction`: in meta-schema.yaml, filled from the .docx for
     all seven sections, rendered under the section title (0008 item 6).
     [done, PR #2] `examples`: in meta-schema.yaml; one XML example per
     section in examples/, taken from the .docx; PF's missing first 26 lines restored from
     matcore.org and Minimal's method-class closing tag corrected (0004 item 33; not noted on
     the site); rendered at the end of each section page with highlighting. Validating
     examples against a generated schema is status step 7.
   - [done] Property layout chosen after rendered options were compared (0007).
   - [done, PR #1] build_docs.py renders the standard from the YAML
     in the layout of 0007 (tests in tests/test_build_docs.py); layout.css and layout.js in
     docs/assets/matcore/; mkdocs.yml has the settings 0007 lists. legacy_* fields hidden unless
     --show-legacy is passed, and CI builds with --show-legacy until step 5 is complete.
   - [done, PR #1] Annex U's Tables U.3 and U.4 generated from schema/units.yaml; the separate
     generated page removed (0009).
   - [done] Decision records are internal committee information: docs/decisions/, including the
     baseline .docx, is excluded from the site build (`exclude_docs` in mkdocs.yml; an unlinked page
     would still appear in sitemap.xml and the site search). They stay in the public GitHub
     repository. Site pages do not link to them.
   - [done, PR #3] Versioning (0010): releases.yaml, generated Revision History, version line on
     standard pages, versioned permalinks, CI deploys per version. 0.4.0 released 2026-11-01
     (tag v0.4.0); the site's `latest` is 0.4.0 and `dev` is main.
   - Changes to the standard since 0.4.0, for the next release's entry in releases.yaml: the
     Preamble's italics fixed (PR #4); contributor and its affiliation optional, and exactly one
     basis entry for the MBPT dielectric matrix (0011); creator and contributor descriptions
     reworded (primary creator vs secondary contributor); step 4: 0001 Part B fixes (B1, B3, B4,
     B6, B7, B8, B10, B11) and the MBPT `local-orbital-basis-set` renamed `localized-orbital-basis-set`;
     Annex U says "Kind" for MatCore's kinds (0004 item 14); Annex I, Identifier Schemes, added (0014);
     creator and contributor restructured by 0014 (`identifier` with value + scheme; `affiliation` a
     container with name + at most one identifier) and their typed fields filled (step 5); title's
     typed fields filled (step 5); the Minimal example's title made descriptive (0004 item 38);
     creation-date's typed fields filled, its two date forms as a pattern (step 5); description's
     and disclaimer's typed fields filled (step 5); material-component's typed fields filled, with
     `phase` renamed `phases` (a list), concentration in atomic percent (0–100) and species an enum
     of the 118 IUPAC element symbols (step 5); concentration's note states that a material
     component's concentrations sum to 100 (0004 item 40).
   - [done, PR #6] 0007's open points resolved except three optional additions:
     container tables show Required and Repeatable only; no alias addresses for now; logo redrawn
     as SVG (logo.svg; logo-light.svg on dark backgrounds; favicon).
   PROPOSED, NOT DECIDED: "Expand all", a tree that follows scrolling, a dark scheme (0007 item 14).
3. [done, PR #9 merged 2026-11-01] Apply 0001 Part A (kind/recommended-unit/convention): merged
   into step 5, property by property (0004). What remained of this step did not belong to any one
   property; each was its own change.
   [done, PR #9] Annex U reworded to "Kind", keeping "quantity kind" where it means
   QUDT's concept; the Table U.3 and U.4 headers say "Kind" (0004 item 14).
   [done] The check for XML-specific wording is closed: Annex U has none, and 0001 A1.3 is not
   applied, since §1.3 already makes the XML examples illustrative (0004 item 34).
   [done, PR #9] The name pattern in meta-schema.yaml is tightened (0004 item 13).
   [done, PR #9] validate_schema.py checks the field order of every property; 38
   entries were reordered to match, with no change to their content (0004 item 6).
4. [done, PR #8 merged 2026-11-01] 0001 Part B fixes ("alone" forms) and the known
   baseline defects (0004 item 25; see 0001's note). Done before step 5 (0004).
5. [todo] One PR per top-level property, covering all of its subproperties: 48 PRs (0004). Each PR,
   in this order: (a) cross-check the property against the baseline .docx (name, definition,
   values, required, repeatable, subproperty tree) so no definition or value was lost or altered
   in migration, and correct any migration error before filling anything; (b) fill
   type/extent/kind/recommended-unit/values, applying 0001 Part A to the property, and delete its
   legacy_* fields; (c) list in the PR description every judgment call in the mapping, so the
   human can decide. A section is complete when no legacy_* fields remain in its file.
   Sections go in the order minimal, dft, md, mbpt, ml, pf, derived, and properties in file order
   within a section (0004 item 35).
   A complete section file declares `legacy_complete: true` at its top level; validate_schema.py
   fails if it does while legacy_* fields remain (0004 item 36).
   [done, PR #10 merged 2026-11-01] `legacy_complete` added to meta-schema.yaml and the check to
   validate_schema.py.
   [done, PR #11 merged 2026-11-01] 0013 implemented: `terms` in meta-schema.yaml;
   scripts/check_values.py checks every property's values (called by validate_schema.py), with all
   JSON Schema formats checked through jsonschema's `format-nongpl` extra; build_docs.py renders
   every values key.
   creator and contributor are restructured by 0014: `identifier` containers (value + scheme,
   open terms) and `affiliation` as a container (name + at most one identifier).
   [done, PR #12 merged 2026-11-01] schema/identifier-schemes.yaml built (ORCID, ROR, DOI, SWHID,
   ISNI, each traced to its documentation), checked by validate_schema.py, published as Annex I.
   dft `unique-identifier` is a hash and does not use it; the dft `doi` properties are decided in
   their PR (0014, settled 2026-11-01).
   [done, PR #13 merged 2026-11-02] creator: restructured by 0014, typed fields filled,
   legacy_* deleted; examples/minimal.xml affiliations get a `name`; tests/test_properties.py
   locks the 0014 tree.
   [done, PR #14 merged 2026-11-02] contributor: restructured by 0014 as creator,
   keeping its own required flag (optional, 0011); tests/test_properties.py covers both.
   [done, PR #15 merged 2026-11-02] title: a required scalar string, legacy_* deleted.
   [done, PR #17 merged 2026-11-02] creation-date: a required scalar string whose pattern
   admits YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssZ, legacy_* deleted.
   [done, PR #18 merged 2026-11-02] description: a required scalar string; the baseline's
   storage-format guidance kept as values.note; legacy_* deleted.
   [done, PR #19 merged 2026-11-02] disclaimer: an optional scalar string, legacy_* deleted.
   [done, PR #20 merged 2026-11-03] material-component: `phases` (renamed from
   `phase`; open terms, definitions in the note per 0013's settlement), concentration in atomic
   percent, species an enum of the IUPAC symbols (from CIAAW's Standard Atomic Weights table);
   examples/minimal.xml writes <phases>Crystal</phases>; legacy_* deleted.
   [done] Recommended unit null for dimensionless kinds (0004 item 39).
   [done, PR #21 merged 2026-11-03] Concentrations of a material component sum to
   100 (0004 item 40): the sentence is in concentration's note.
   [done] species stays elements only: no isotopes or pseudo-species (0004 item 41).
   [done] Long value lists render inline (0004 item 42).
   [todo] 0015: the `unit` check in validate_schema.py and 0001 A1.1/A1.2 in §1.3 (one PR), before
   the computation PR. (A1.1/A1.2 were missed when step 3 handed Part A to step 5.)
   [todo] The rest of minimal in file order, starting with computation.
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
  `uv run python scripts/build_docs.py --show-legacy` (the flag until status step 5 is complete),
  `uv run mkdocs build --strict`. Commit any files
  build_docs.py regenerates with the change; CI fails if the committed copies are stale. Never
  hand-edit generated files under docs/standard/ (02-*.md … 08-*.md, revision-history.md, the
  marked regions in index.md, annex-u-units.md and annex-i-identifiers.md) (0004, 0009, 0010, 0014).
- Examples follow the standard (0012): every change to schema/*.yaml includes reviewing every
  example in examples/ and updating any that no longer conform, in the same change.
  validate_schema.py (via scripts/check_examples.py) fails on structural mismatches; rules the
  schema cannot express yet (e.g. "exactly one of") are reviewed by hand.
- Never invent QUDT identifiers, physical constants or unit symbols. units.yaml was verified against
  QUDT Units 3.3.0, GNU Units 2.23 (definitions.units 3.19) and NIST CODATA 2022. A new unit is
  added by pull request, with each of its fields (kind, QUDT identifier or null, GNU Units name,
  SI factor, source) traced to a primary source named in the PR. A new kind needs a decision
  record (0004). Likewise, every field of an identifier scheme (form, pattern, check digit,
  example) is traced to the scheme's own documentation, and a new scheme is added by PR (0014).
