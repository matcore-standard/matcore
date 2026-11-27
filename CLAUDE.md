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
  (minimal, dft, pim, ps, mbpt, ml, pf, derived; pim added by 0046, md renamed ps by 0061). THIS IS
  THE STANDARD.
- `schema/units.yaml` — Annex U, the normative unit table (kinds, symbols, QUDT/GNU mapping, SI factors).
  The single source of Annex U's Tables U.3 and U.4, which build_docs.py generates into
  annex-u-units.md; it prevails over the annex. Factors are exact decimal text, e.g. "1e3" (0009).
- `schema/identifier-schemes.yaml` — Annex I, the identifier schemes (ORCID, ROR, DOI, SWHID, ISNI;
  AFLOW, InChI and SMILES for crystal structures and molecules, 0034): for each, entities
  identified, canonical form, pattern, check digit, example, source. Single source
  of Annex I's Table I.1 and of identifier checks (scripts/check_identifiers.py), as units.yaml is
  for units; it prevails over the annex (0014).
- `schema/meta-schema.yaml` — JSON Schema (written in YAML) that section files must satisfy.
- `docs/standard/*.md` — prose chapters (index = title and 1. Preamble, annex-u-units,
  annex-i-identifiers) plus GENERATED chapters (02, 03, 05–08, pim.md and ps.md, named in build_docs.PAGES;
  revision-history; and the marked regions in
  index and the annexes: version line, Tables U.3/U.4, Table I.1).
  Never hand-edit generated parts; edit the YAML and run
  `scripts/build_docs.py`.
- `docs/decisions/` — decision records: internal committee information, not published on the site
  (0004). 0001 is the units change list (not yet applied; see Status). The frozen Google Doc export
  is stored there as the baseline artifact.
- `scripts/validate_schema.py` — checks section files against the meta-schema and units.yaml. It
  validates the standard itself, not instance files (the instance validator is status step 9).
  scripts/check_formula.py (0034) parses formulas and checks the examples' material components.
- `scripts/build_docs.py` — regenerates docs from YAML in the layout of 0007; tested by
  tests/test_build_docs.py. Its `--show-legacy` option is no longer needed: no legacy text remains.
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
  tolerance; `basis` for exciton-momentum before 0072 made it fractional).
  PROPOSED, NOT DECIDED: a field such as `determined-by: criterion` naming what fixes an `any`, so the
  validator can check that the subproperty exists and is required.
- `kind`: a key of units.yaml#kinds, or reserved `dimensionless` | `inapplicable` | `any`.
  string/bool/file properties are always `inapplicable`; a physical quantity is never typed as a
  string. (The meaning of `file` in an instance is PROPOSED, NOT DECIDED; define it in the data
  model, independent of any serialization.)
- `recommended-unit`: informative only; must be a symbol in units.yaml with matching kind.
  Null when kind is `dimensionless` (0004 items 39, 48).
  No recommended unit when kind is `any` (0019).
- `convention`: an optional property field in meta-schema.yaml, rendered by build_docs.py but
  used by no property; the units model below expresses conventions as subproperties instead.
  PROPOSED, NOT DECIDED: remove the field, or define its use, when the next convention-like
  property comes up (mbpt exciton-momentum's `basis`). (Superseded in part: 0072 gives
  exciton-momentum no `basis`; the field waits for the next convention-like property.)
- `values`: structured; replaces the old prose "Values" (0002). Null or a mapping of `terms` (open
  vocabulary: unlisted strings conform, reported as user-specified, near-misses as possible typos),
  `enum` (closed list), `minimum`/`maximum` (inclusive), `format` (a JSON Schema 2020-12 format
  name, always checked), `pattern`, `examples` (data; must satisfy the property), `note` (0013).
  Most vocabularies are open: use `terms` for "Other user-specified value", `enum` only where an
  unlisted value would make the data meaningless. Keys apply together and are tied to `type`
  (terms/enum/format/pattern: string; minimum/maximum: int, float); at most one of terms/enum and
  of format/pattern (0013). A term's definition is prose in `note`, in the baseline's wording;
  terms and enum stay plain lists (0013, settled 2026-11-02). Values that depend on a sibling use
  `depends-on` (the sibling) and `cases` (its listed values → the values that apply); with no
  matching case any value of the type is accepted (0013, settled 2026-11-03). For an array value
  (an extent listing dimensions) the keys apply to each component, and each example is a whole array; the
  pages say "for each component" for bounds (0013, settled 2026-11-05).
- `legacy_*` fields hold the Google Doc prose from the baseline migration. Delete each one once its
  content is transferred to the typed fields; the original wording remains in the baseline .docx and
  in git history (tag v0.9-baseline). A section is complete when no legacy_* remain.
- An `identifier` container (value and scheme, Annex I) is used where more than one identifier
  scheme is in use for the thing identified; a `doi` string, in Annex I's DOI form, where DOI is the
  scheme in use. Another address is given in a `link` (0055).
- A file named so that a reader can verify it has `name` and `checksum` (0032). A file the record
  carries or points to also has `description`, `contents`, `encoding` and `link` (0043; 0056).
- Names match `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` (enforced by meta-schema.yaml). A name is plural only when
  its value is a list (open extent); a repeatable property stays singular. `unit` is singular.
  A property whose value is the label of a structure or computation is named for the referent followed
  by `-label`, e.g. `computation-label` (0062).

## Units model (decided; see docs/decisions/0001 Part A and docs/standard/annex-u-units.md)
- Every dimensioned value in an instance file carries a `unit`; no default unit is ever implied.
- The schema declares `kind` + `recommended-unit`, not a fixed unit. Validation = kind compatibility
  via the dimension vector in units.yaml, using the closed symbol set. No unit parsing.
- A property is either a leaf (a value of its own, no subproperties) or a container (subproperties,
  typed fields null), never both. A leaf has kind inapplicable or dimensionless; a dimensionless
  leaf carries no `unit`. A quantity with a physical kind (a units.yaml kind other than
  dimensionless) is a container holding two leaves: `value` (required, fixed description; carries
  type, extent, kind, recommended-unit, values) and `unit` (one fixed form: string, [],
  inapplicable, values null, fixed description). validate_schema.py checks all of this; generic
  parameters (value kind any) and free-form units are outside the check (0015, third amendment
  2026-11-04, which reverses the second).
- A value that varies is given as repeated entries, each with a `qualifier` leaf (open terms
  Average, Final, Initial, Maximum, Minimum; one fixed form) beside `value` and `unit`; a
  dimensionless value may sit in a container with a qualifier and no unit. Without a qualifier a
  condition's value holds throughout (0035, amending 0015 and 0026).
- Reserved kinds: dimensionless (ratios, counts), inapplicable (non-quantities), any (fixed by the
  instance or by a required enumerated subproperty).
  Angles and moles are NOT dimensionless.
- Conventions a unit cannot express (2π in reciprocal lengths, lattice vs Cartesian basis) are separate
  required enumerated subproperties (`convention`, `basis`), never encoded in the unit string. A reduced
  (nondimensional) PF length or time is written with unit `dimensionless`, with no flag (0075, amending 0003).
- Energy and MolarEnergy are distinct kinds (Annex U Rule 8). kJ/mol, kcal/mol → MolarEnergy.
- CODATA 2022 factors are normative; QUDT (CODATA 2006) and GNU Units 2.23 (CODATA 2018) are stale.
- GNU Units pinned to 2.23 / definitions.units 3.19 for `x-gnu:` escape expressions.
- "Annex" (ISO usage), normative. Use "Kind" (not "Quantity kind") in the schema, the standard's prose
  and new text. Decision records are not rewritten. "Quantity kind" remains where it refers to QUDT's
  concept.

## Generic parameters and free-form units (decided; see docs/decisions/0001 and 0003)
Three groups, not to be merged:
1. Generic parameters: xc-parameter and smearing › parameter (dft; 0004 item 47, moved by 0053), computation-parameter
   and td-parameter (ps), model-parameter (pf), calculation-parameter (derived). Their `value` has
   type any, extent any, kind any; the instance supplies type, shape and unit. The generic-parameter
   rule applies to these only. The instance type is one of float, int, string, bool, and is stated
   in the instance, not inferred from how the value is written; each serialization (defined in
   §1.3) defines how.
   The value need not be a scalar (0004).
2. Free-form units: field-variable, free-energy-density (pf). No `value`; a free-form `unit` whose kind
   the schema does not fix.
3. Typed properties with a required unit: grid-spacing (Length, recommended m) and time-step-size
   (Time, recommended s) (pf). Handled like temperature, not as generic parameters. With
   domain-size, their `unit` is a Length (Time) symbol, or `dimensionless` in reduced units, the
   characteristic scale then given as a model-parameter (0075, amending 0003's `scaling`).
Every `unit` subproperty has kind inapplicable and holds an Annex U symbol or `dimensionless`. The
`x-gnu:` escape (Annex U Rule 4) is permitted only where the schema does not fix the kind: groups 1
and 2, and the `unit` beside any other `value` of kind any (dft SCF tolerance, 0019); group 3 and all
other typed properties use Annex U symbols only (0001 A1.1).
PROPOSED, NOT DECIDED: state conditional validation rules (the allowed unit or values of one
subproperty depend on another's value: `scaling` for PF lengths and
times) once in §1.3, so each property refers to the rule rather than restating it. Needs a decision
before implementation, when the first such property comes up; whether
0013's `depends-on`/`cases` can express it is part of that decision. (dft k-point-spacing, the
first candidate, is removed: 0004 item 47; mbpt exciton-momentum, the second, is fractional with no
`basis`: 0072; PF's `scaling`, the third, is dropped: 0075.)
Group 1 is defined once in §1.3 as a *generic parameter* (0016): a container of `name*`, `value*`
(type, extent and kind any), `unit*` (fixed description "The unit in which the associated value is
expressed." (0001 B9) and the A3.2 note) and `description`, in that order. It is recognised by a
`value` whose type and kind are both any, with no tag (0019 amends 0016); validate_schema.py checks
each one against the canonical form.

## Instance serialization (decided; see docs/decisions/0044)
The standard is agnostic to serialization format, as §1.3 states; its examples are illustrative only
and do not prescribe a format for any implementation. Any serialization that preserves the property
hierarchy, the required/repeatable semantics and the value/unit/convention structure is conformant.
JSON (RFC 8259, UTF-8, `.json`) is the first serialization: the examples are written in it and the
MatCore tools (status item 9) read and write it (0044). Mapping (0044 item 2): an instance is an
object with one member per section (minimal, dft, ...); a container is an object, a leaf a JSON
value of its Type; a repeatable property is always an array; an extent is nested arrays, first index
outermost (0038); an omitted optional property is absent, never null. A generic parameter's object
carries a JSON-only member `type` (float, int, string, bool). A JSON Schema generated from the YAML
validates the examples in CI (status step 7).

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
  2.1–2.8 (pim inserted as 2.3 by 0046); Annex U; Annex I (0014)) and Revision History; no tabs; no right-hand TOC (page
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
  B2 (added note) is declined (2026-11-17, mbpt dielectric-matrix PR); B9 is decided for generic parameters (0016); B5 is
  settled as fractional shifts, k-point-spacing removed and methfessel-paxton-order replaced by a
  generic smearing-parameter (0004 item 47).
  B4's Ė symbol needs no decision: the baseline .docx already writes the strain-rate tensor as Ė
  (Word equation objects), and the migration dropped the dot; the computation PR restores it.

## Migration losses found by the 2026-11-03 audit of the .docx
All 518 descriptions and legacy texts, the Preamble, the section introductions and the example
captions were compared with the baseline .docx. Apart from intentional changes, these were lost:
- §1.3 bullet nesting (three levels in the .docx; flat on the site), and the bullet symbol of
  each level (● ○ ■ in the .docx; ● at every level in the theme).
- The italics of *universal* in the minimal introduction.
- The space after "Note:" in five notes (minimal method-class, md particle-interactions, ml
  ml-task › type, the two mbpt dielectric-matrix notes) and in some legacy texts.
- Subscripts and superscripts (σ₁₁, e₁, a₀, G₀W₀ written σ11, e1, a0, G0W0) in ten minimal
  simulation-conditions entries and mbpt self-consistency; the dot of Ė in minimal strain-rate;
  ASCII `|` replaced by `│` in minimal cell and cell-reference. Restored in those properties' PRs:
  minimal computation's are restored; mbpt self-consistency's remain.

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
     examples against a generated schema is status step 7. (Superseded: the examples are JSON, the
     first serialization, by 0044.)
   - [done] Property layout chosen after rendered options were compared (0007).
   - [done, PR #1] build_docs.py renders the standard from the YAML
     in the layout of 0007 (tests in tests/test_build_docs.py); layout.css and layout.js in
     docs/assets/matcore/; mkdocs.yml has the settings 0007 lists. legacy_* fields hidden unless
     --show-legacy is passed, and CI builds with --show-legacy until step 5 is complete. (Superseded: step 5 is
     complete and CI builds without the flag, decided by the human 2026-11-22.)
   - [done, PR #1] Annex U's Tables U.3 and U.4 generated from schema/units.yaml; the separate
     generated page removed (0009).
   - [done] Decision records are internal committee information: docs/decisions/, including the
     baseline .docx, is excluded from the site build (`exclude_docs` in mkdocs.yml; an unlinked page
     would still appear in sitemap.xml and the site search). They stay in the public GitHub
     repository. Site pages do not link to them.
   - [done, PR #3] Versioning (0010): releases.yaml, generated Revision History, version line on
     standard pages, versioned permalinks, CI deploys per version. 0.4.0 released 2026-11-01
     (tag v0.4.0). 0.5.0 released 2026-11-04 (tag v0.5.0; minimal complete). 0.6.0 released 2026-11-08
     (tag v0.6.0 on b688e40; dft complete; rulings 0016–0043); the site's `latest` is 0.6.0 and `dev`
     is main. (An earlier v0.6.0 tag on 2908f57 failed CI's release check and was moved.) 0.7.0 released 2026-11-22
     (tag v0.7.0 on 19b4b3d; step 5 complete, every section filled); the site's `latest` is 0.7.0 (checked in
     gh-pages versions.json) and `dev` is main. 0.8.0 released 2026-11-23 (tag v0.8.0 on 2b13114; rulings 0078-0084:
     the JSON Schema, §1.4, and the committee review's feedback); the site's `latest` is 0.8.0 (checked in gh-pages
     versions.json). Its tag run's first deploy failed: pushed together with main, it raced main's dev deploy to
     gh-pages and was rejected; the re-run (attempt 2) deployed it. Decided by the human 2026-11-23: deploys wait for one
     another. [done, PR #147 merged 2026-11-23]
     .github/workflows/ci.yml: the job's concurrency group is shared by push runs (deploy-gh-pages) and unique per
     pull-request run, cancel-in-progress false, queue max (a waiting run is kept, not replaced; GitHub's
     control-workflow-concurrency how-to, read 2026-11-23); tests/test_ci.py (new). The deploy path is verified only
     at the next push to main.
   - 0.8.1 prepared 2026-11-27, a patch (0010 item 1): website only, no change to the standard (the collapsible
     Revision History rows and the smaller menu logo, PR #148; the supporters in the bottom bar, PR #149; CI deploys
     serialized, PR #147, not listed in the entry); release commit on main, awaiting the human's push and the tag
     v0.8.1.
   - Changes to the standard since 0.8.1, for the next release's entry in releases.yaml: none yet.
   - Changes to the standard from 0.7.0 to 0.8.0 (released in 0.8.0, its entry in releases.yaml summarizing them): a JSON Schema generated from
     the standard is published with each version and linked from §1.4; it checks the examples (0078); a new §1.4
     Serialization states what any serialization must preserve and JSON's mapping, and a record's own Properties are
     named with the prefix x- (0079); dft core-electron-treatment › type is All-electron or Frozen core, PAW being
     named once, as a dataset type (0080; breaks 0.7.0 records with core type Pseudopotential or PAW); the derived
     families Mechanical, Thermodynamic and Transport are widened (strengths, hardness, melting temperature, viscosity,
     defect mobilities), and the derived introduction points paths found by the NEB to PS (0081); ps settings gains an
     optional, repeatable particle-constraint for a constraint on, or a potential applied to, a group of particles
     (0082); §1.2 states that MatCore is a reporting standard and which part of a record holds which metadata, and §1.3
     how a Property is identified and how a change is made (0083); dft and mbpt localized-orbital-basis-set are renamed
     atom-centered-basis-set (0083; breaks 0.7.0 records that use them); a generic parameter whose value is a string or
     bool has no unit, pf boundary-condition and initial-condition and pim charge-interaction and magnetic-interaction
     take the singular, and matcore comes first in minimal (0084; breaks 0.7.0 records with the old names or a unit on a
     string or bool parameter).
   - Changes to the standard from 0.6.0 to 0.7.0 (released in 0.7.0, its entry in releases.yaml summarizing them): the
     examples are written in JSON, the first serialization, and §1.3 says so (0044); a required
     matcore container gives the standard version, an optional link to it, the dataset's id and
     version, the record's author and creation date, replacing matcore-id, matcore-author and
     matcore-date (0045; breaks 0.6.0 instances); structures and computations are labelled, a computation
     gives its task, structures and inputs (other computations with a role), simulation-conditions is
     renamed `conditions` and is optional, interaction-model is removed, method gains TB, MS and PIM,
     and dft's properties sit in `settings` blocks naming their computations (0046; breaks 0.6.0
     instances); a new section 2.3 Particle Interaction Model (pim) holds md's model properties, md
     keeps the dynamics in `settings`, and mbpt, ml, pf and derived become 2.5–2.8 (0046; breaks
     0.6.0 md instances); a pseudopotential or PAW dataset names its species (required) and a
     basis set may (0047; breaks 0.6.0 dft instances); relaxation-tolerance-stress is added and the
     tolerances apply to task Optimization (0048); dispersion-correction is added and
     xc-functional › name gives the functional alone (0051); the smearing width is noted as not an
     imposed temperature (0052); smearing moves out of k-point-mesh into `smearing` (0053; breaks
     0.6.0 dft instances); the dft introduction is updated (0054); lapw-basis-cutoff is added (0057);
     the LibXC version is a software dependency (0058); k-point-mesh names the cell it samples
     (0059); the Kind ElectricCharge and the units e and C are added, and the
     condition net-charge (0049); the Kind MagneticMoment and the units mu_B
     and J/T are added, with dft initial-magnetic-moment and minimal material-component ›
     magnetic-order (0050); pim theory-level is filled, terms Physics-based and
     Machine-learned, model-type, the functional form, particle-style, with the term
     Nucleus, bonding-type, Reactive meaning no predetermined bonding topology, and
     charge-interactions, electric-dipole-variability's description fixed (0046; step 5);
     spin-style keeps Classical spin and Coupled spin lattice, three electronic or quantum terms
     removed, and magnetic-dipole is filled; pim is complete (0060; step 5); section 2.4 is renamed
     Particle Simulation (PS), key ps, with a new introduction, and Leadership adds a PIM committee
     (0061; breaks 0.6.0 md instances); a property holding the label of a structure or computation
     is named for it: computation-label in settings and input, structure-label in computation (0062);
     computation explains a simulation run in stages as computations linked by input role Initial
     configuration, which carries over the state (0063); method names the method section, PS replacing
     MD, MS, MC and CGMD, method-class gives a PS computation's particle entity, task names the goal
     with a new Transition state search (Superseded: renamed Transition path by 0065), and the PS introduction and §1.2 name Monte Carlo (0064;
     breaks 0.6.0 instances with method MD, MC or CGMD); each method term is defined by the kind of
     methods it covers (0064, amended 2026-11-14); task gains Structure generation and Equilibration,
     Transition path covers path sampling, and Training covers any model fitted to data (0065);
     computation gains an optional description, for a protocol such as a structure search's (0066);
     ps algorithm is a required, repeatable term naming a major class of procedure, 39 terms in eight
     groups, with an optional settings description for variants and parameters (0064, 0066, 0067);
     ps computation-parameter is a generic parameter with an Annex U unit (0016); pim long-range-electrostatics is renamed electrostatic-summation, gains
     Short-range and redefines None (0068); ps initialization is a string for what the computation sets
     up itself (step 5); ps thermodynamic-constraint's
     method is repeatable with grouped thermostat, barostat and particle-exchange terms, type gains
     ΔμNPT and points to conditions, and td-parameter is a generic parameter; ps is complete (0069);
     mbpt's properties sit in `settings` blocks naming their computations, and starting-point is
     removed, the DFT computation named as input role Starting point (0046); mbpt-method's
     self-consistency becomes gw-self-consistency and bse-self-consistency, the combined terms removed,
     evGW added, GW followed by BSE one computation of type GW/BSE (0070); dft xc-functional › name is
     given without a Hubbard correction (PBE, not PBE+U), DFT+U being calculation-physics On-site
     correlation (review 2026-11-16); mbpt dielectric-matrix's typed fields filled, its plane-wave cutoff
     described as set separately from the wavefunction cutoff (step 5); mbpt gw-bands is replaced by a
     self-energy container of band-range, number-of-bands and band-terminator, and dielectric-matrix gains
     band-terminator (0071); mbpt bse-hamiltonian's typed fields filled, exciton-momentum given in fractions
     of the reciprocal lattice vectors with no unit (0072; step 5); mbpt bse-kernel-truncation's typed fields
     filled with coulomb-truncation's terms, mbpt is complete (step 5); ml's properties sit in `settings`
     blocks naming their computations, ml-task is not repeatable, training-data, training-method and
     model-performance move into ml-model, training-hyperparameters is renamed hyperparameter and
     validation evaluation-method (0073); ml ml-task's type has the terms Property prediction, Structure
     generation, Synthesis prediction, Ranking, Clustering and Embedding, an MLIP being described in pim
     (0073; step 5); ml ml-model's own members filled, with a generic architecture-parameter and model-size
     the number of trainable parameters (0073; step 5); ml training-data filled, its size an int, its split
     described in words, data in the record named as an input with role Training data (0073; step 5); ml
     training-method filled, with a new loss-function and a generic hyperparameter whose role
     training-procedure explains (0073; step 5); ml model-performance filled, validation replaced by
     evaluation-method, with a new metric (subset Training, Validation or Test; quantity; measure; value;
     unit) and applicability-domain (0073; step 5); a new ml inference describes how a dataset was produced
     from the model: input-data, conditioning, sampling-procedure, a generic inference-parameter,
     number-generated and filtering (0073); ml interpretability-method moves inside ml-model and is filled;
     ml is complete (0073 amendment; step 5); pf's properties sit in `settings` blocks naming their
     computations, physical-phenomena is renamed physical-phenomenon, free-energy free-energy-density (now
     repeatable), driving-energy free-energy-density-term and domain-and-mesh domain, governing-equation › type
     repeats, and mesh-type moves into numerical-method (0074); pf physical-phenomenon is filled, with the
     terms Fracture and Plasticity added and every term defined (0074; step 5); pf problem-specification is filled:
     time-dependence is removed, the time-evolution state being given in minimal conditions,
     additional-energy-contribution is replaced by free-energy-density › contribution, governing-equation › type has
     nine defined terms with Navier-Stokes, Multi-phase-field, Mechanical equilibrium and Poisson, and
     free-energy-density › unit is the unit of the density (0074 amendment; step 5); pf domain is filled:
     domain-size is a value + unit, `dimensionless` in reduced units with no `scaling` flag (0075, amending 0003),
     boundary-conditions is a container of type (Dirichlet, Neumann, Zero-Neumann, Periodic; Fixed and Free removed),
     boundary and field-variable, and NoFlux is Zero-Neumann (0074, 0075; step 5); pf numerical-method is filled:
     evolved-variable, spatial-discretization-parameter and mesh-file are added, grid-spacing and time-step-size are
     value + unit with no `scaling` flag, temporal-discretization's Implicit and Explicit are removed and Mixed is IMEX,
     mesh-type loses Cartesian, and solver has nine defined terms (0074, 0075; step 5); pf mesh-file is repeatable,
     one entry per file (decided by the human 2026-11-20); pf variables is filled: model-parameter is a generic
     parameter, each field variable is its own entry, and pf is complete (0016, 0074; step 5); in the JSON
     examples a generic parameter's object carries `type`, now checked (0044 item 3); derived's properties sit in
     `settings` blocks naming the computations that obtain them, of any method, its single-method limit removed,
     calculation-method replaced by procedure with calculation-parameter beside it, and the section titled Derived
     Property (DP); minimal method-class gains Post-processing and method gains DP (0076); the derived introduction
     describes the usual record, one DP computation with one entry per property (decided by the human 2026-11-22);
     minimal computation notes that a record explains the dataset, not its workflow, giving a computation only for
     results in the dataset or settings a reader needs (0077); derived-property is filled: type names the kind of
     property (14 terms, Scattering covering X-rays and neutrons), name and procedure are added, calculation-parameter
     is a generic parameter, and derived is complete, so every section is complete (0076; step 5); every note that
     defines terms lists them one per line (0007 item 5).
   - Changes to the standard from 0.5.0 to 0.6.0 (released in 0.6.0): §1.3
     defines the generic parameter, checked by validate_schema.py (0016); dft xc-functional's
     typed fields filled (step 5); dft core-electron-model's typed fields filled, pseudopotential
     gains a checksum beside unique-identifier (step 5); dft valence-electron-model's typed fields
     filled, the basis set given the same checksum split (step 5); dft calculation-physics's typed
     fields filled (step 5); dft k-point-mesh's typed fields filled, k-point-spacing removed and
     methfessel-paxton-order replaced by a generic smearing-parameter (0004 item 47) (step 5); dimensionless
     values written as leaves again, with no unit (0015, third amendment; 0004 item 48); dft
     xc-functional gains a `name` and a `normalization` (0017); dft core-electron-model and
     valence-electron-model renamed core-electron-treatment and wavefunction-representation, with
     new terms (0018; breaks 0.5.0 instances); dft self-consistent-field-convergence's typed fields
     filled, its tolerance given a criterion and an open Kind, a generic parameter recognised by
     Type and Kind any, §1.3's Kind `any` reworded (0019); `method` renamed `method-density` (breaks
     0.5.0 instances) and `method-diagonalization` added (0020); dft pseudopotential renamed
     `pseudopotential-or-paw`, its type gaining the term PAW (0021; breaks 0.5.0 instances); dft
     relaxation-tolerance-energy's typed fields filled (step 5); dft relaxation-tolerance-forces's
     typed fields filled (step 5); dft comment's typed fields filled, dft complete (step 5); dft
     calculation-physics drops Relativistic effects, renames Spin polarization to Collinear spin
     polarization, adds Orbital polarization and Spin-orbit coupling (0022); the energy of dft
     relaxation-tolerance-energy and of the SCF criterion "Energy" defined: the free energy
     E − TS when occupations are smeared, the total energy otherwise (0023); dft xc-functional's
     list of named functionals moved from description's note to name's (0024); §1.1 states the
     goals of FAIR data and AI readiness (0004 item 50); minimal material-component moves into
     a new top-level `structure` and gains form, role and fraction, `phases` becomes an optional
     repeatable `phase` with Single crystal and Polycrystal (0025; breaks 0.5.0 instances);
     simulation-conditions explains varying conditions in its description and flags them as
     spatially-varying or time-varying, and composition is given as set up when it varies (0026);
     the phase term Quasicrystal has long-range order without translational periodicity (0027);
     §1.3 spells out KIM, CODATA and IRI and describes QUDT (0004 item 51);
     §1.2 distinguishes methods that supply energies and forces, and computation gains
     interaction-model with a note on method (0028); `citation` renamed `publication`, and a
     new optional `dataset-location` says where the dataset is stored (0029); funding award-title is
     optional, provenance is recommended and its agent is structured like a creator (0030); license is a
     repeatable container of an SPDX identifier or LicenseRef-, a name, a link and what it applies
     to (0031); provenance and the dft pseudopotential and basis set give a file holding its
     checksums instead of a checksum naming its file (0032); a required matcore-author names who
     created the metadata record (0033); a material component's composition is one chemical
     formula (groups, decimal counts, variables in braces, user-defined species J…) with
     `variable` and `topology` (AFLOW, InChI, SMILES, added to Annex I), and `constituent` is removed
     (0034; breaks 0.5.0 instances); a varying value is given as repeated entries with a `qualifier`
     (Average, Final, Initial, Maximum, Minimum): the twelve numerical simulation conditions and
     fraction become repeatable, number-of-particles, strain and fraction become containers, and
     variable's type is renamed qualifier (0035; breaks 0.5.0 instances); simulation-conditions › type
     becomes a container of thermodynamic-state, system-openness, time-dependence and
     spatial-uniformity, and the flags spatially-varying and time-varying are removed (0036; breaks
     0.5.0 instances); simulation-conditions › number-density is removed (0037; breaks 0.5.0
     instances); §1.3 states that a multi-dimensional value is a list of lists, first index
     outermost, and cell and cell-reference say each row is a vector in Cartesian components (0038);
     every simulation condition is defined as imposed, and a measured quantity is a result, not a
     condition (0039); the conditions electric-field, magnetic-field (as B) and body-force (per unit
     mass) are added, with the Kinds ElectricFieldStrength, MagneticFluxDensity and Acceleration and
     the units V/m, V/angstrom, T and m/s^2 (0040); electrode-potential is added with a required
     reference (SHE, RHE, Vacuum), the Kind ElectricPotential and the unit V (0041);
     chemical-potential is added with species and an optional relative-to (0042); software is one
     entry per layer with role, description, link, revision, identifier, dependency and build-options,
     and file gains encoding and checksum (0043).
   - [done, PR #6] 0007's open points resolved except three optional additions:
     container tables show Required and Repeatable only; no alias addresses for now; logo redrawn
     as SVG (logo.svg; logo-light.svg on dark backgrounds; favicon).
   - [done, PR #26 merged 2026-11-04] Menu consistency: the entries under "2. Schema" get
     the left bar the theme draws under "1. Preamble"; clicking the current page's entry collapses
     and expands what is listed under it (headings or property tree) instead of reloading the page.
   - [done, PR #31 merged 2026-11-04] A "Collapse all" button at the end of each schema
     page's key line closes every open property block (0007, resolved 2026-11-04); added by
     layout.js.
   - [done, PR #101 merged 2026-11-14] Values text in paragraphs (0007 item 5,
     amended 2026-11-14; ruling 0056e8b on main): allowed values first; depends-on cases as a list,
     one item per case; values.note as its own paragraph headed **Clarifications:**; legacy text its
     own paragraph. build_docs.py splits values_text() into allowed_values() and the paragraphs;
     tests/test_build_docs.py gains test_definitions_are_set_apart_from_the_values_they_define;
     02-minimal, 03-dft, 05-mbpt, 07-pf and pim pages regenerated.
   - Long definition notes by 0007 item 5, amended again 2026-11-14: a values.note defining many terms
     is Markdown of several lines in the YAML, a bold label per group of terms and a list with one item
     per term; a multi-line note renders under **Clarifications:** as its own paragraph, a one-line
     note inline as before; bold labels, not headings, so the menu and TOC are unchanged; 0013's
     definitions stay prose. ps algorithm is the first; another long note (e.g. minimal task, method)
     is converted when its property next changes or by a change of its own. Implemented in the ps
     algorithm PR (branch ps-algorithm-0064).
   - Requested by the human 2026-11-22 (derived type's clarification was dense): every values.note that defines two or
     more terms is converted to this list form by a change of its own (0007 item 5, amended again): 57 notes in all eight
     sections, one line `- "Term" – definition` per term, "One of:" and each item's final full stop or semicolon dropped
     (as in ps algorithm), prose after the last definition kept as a paragraph below the list (eight notes, e.g. phase's
     "Omit for a component whose form is Molecule."), dft wavefunction-representation's numbered groups as bold labels;
     a script made the change and a check confirmed that every word of every note is kept. tests/test_schema.py gains a
     test that every note defining terms gives one line per term; thirteen tests that compared a note's wording are
     updated to the list form (same words). Judgment call: the rule covers two-term notes too, for one form throughout.
     [done, PR #137 merged 2026-11-22] schema/*.yaml (all eight),
     tests/test_schema.py, tests/test_computations.py, tests/test_properties.py, tests/test_build_docs.py, pages
     regenerated; rendering checked in the browser (derived type, dft wavefunction-representation and
     calculation-physics).
   PROPOSED, NOT DECIDED: "Expand all", a tree that follows scrolling, a dark scheme (0007 item 14).
   Requested by the human 2026-11-23: the Revision History's descriptions were too long; each release's row starts
   closed and opens and closes as a whole (a box opening inside the description cell was tried and rejected); the
   left-menu logo is reduced to the size of the "MatCore" lettering. [done, PR #148 merged
   2026-11-23] scripts/build_docs.py (release_row: the history is an HTML table in a
   div.mc-revisions; a release of several changes is tr.mc-release, its version a toggle button, its changes a list
   with data-more "+N more"), docs/assets/matcore/layout.js (marks the table mc-collapsible and toggles a row on a
   click anywhere on it; without the script every row shows open), layout.css (a closed row shows its first change,
   clamped to two lines, and "+N more"; short columns on one line; logo 1.8rem to 1.1rem), revision-history.md
   regenerated; tests: test_build_docs (a new test of the row), test_releases (the matcore.org rows compared word for
   word instead of character for character, since the markup changed). Checked in the browser at desktop and phone
   widths (the table scrolls sideways on a phone, as before).
   Requested by the human 2026-11-23: the bottom bar's "Made with Material for MkDocs" is replaced by "MatCore is
   supported by" and white-on-black logos of NSF, OpenKIM and Matterstack (the human's files; Matterstack's inverted),
   on one line, spaced, in proportion to the text. [done, PR #149 merged 2026-11-23] overrides/partials/copyright.html (a new override of the theme's partial; re-check on theme
   upgrades), docs/assets/matcore/supporters/ (nsf.png, openkim.png, matterstack.png, 96 px tall, white on
   transparent; OpenKIM's own black box kept), layout.css (the bar black; the logos 2em, 1.5em and .8em tall, gap
   1.6em, no wrapping); each logo links to its site, opening in a new tab: https://www.nsf.gov/ (the human gave
   https://www.nsf.org/, NSF International, and chose nsf.gov when asked), https://openkim.org, https://matterstack.ai.
   Checked in the browser at desktop and phone widths; the links checked in a fresh build (mkdocs serve does not
   reload overrides/).
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
5. [done, PR #136 merged 2026-11-22: every section declares legacy_complete] One PR per top-level property, covering
   all of its subproperties: 48 PRs (0004). Each PR,
   in this order: (a) cross-check the property against the baseline .docx (name, definition,
   values, required, repeatable, subproperty tree) so no definition or value was lost or altered
   in migration, and correct any migration error before filling anything; (b) fill
   type/extent/kind/recommended-unit/values, applying 0001 Part A to the property, and delete its
   legacy_* fields; (c) list in the PR description every judgment call in the mapping, so the
   human can decide. A section is complete when no legacy_* fields remain in its file.
   Sections go in the order minimal, dft, pim, ps (md before 0061), mbpt, ml, pf, derived, and properties in file order
   within a section (0004 item 35; pim before md, settled 2026-11-10 in 0046). PROPOSED, NOT DECIDED:
   since 0046 a method section's properties sit in one `settings` block, so its PRs go one per member
   of `settings`.
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
   funding › funder is restructured like affiliation (name + at most one identifier, schemes ROR
   and ISNI), since the Crossref Open Funder Registry moves into ROR (0014, settled 2026-11-04).
   [done, PR #12 merged 2026-11-01] schema/identifier-schemes.yaml built (ORCID, ROR, DOI, SWHID,
   ISNI, each traced to its documentation), checked by validate_schema.py, published as Annex I.
   dft `unique-identifier` is a hash and does not use it (0014, settled 2026-11-01). Every `doi`
   property is a string in Annex I's https URI form, its pattern copied exactly from the table's
   DOI entry and kept in step by a test (0014, settled 2026-11-04).
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
   examples/minimal.xml writes <phases>Crystal</phases>; legacy_* deleted. (Superseded:
   concentration is an atomic fraction, 0–1, by 0004 item 46. `phases` is now a repeatable
   `phase` inside structure › material-component, by 0025, PR #55.)
   [done] Recommended unit null for dimensionless kinds (0004 item 39).
   [done, PR #21 merged 2026-11-03] Concentrations of a material component sum to
   100 (0004 item 40): the sentence is in concentration's note. (Superseded: they sum to 1, 0004
   item 46.)
   [done] species stays elements only: no isotopes or pseudo-species (0004 item 41).
   [done] Long value lists render inline (0004 item 42).
   [done, PR #22 merged 2026-11-03] 0015: scripts/check_units.py (called by
   validate_schema.py) checks the fixed `unit` form; 0001 A1.1/A1.2 applied to §1.3 with "Kind".
   (A1.1/A1.2 were missed when step 3 handed Part A to step 5.)
   [done, PR #23 merged 2026-11-04] §1.3 and migration fixes: the nesting restored;
   0004 items 43–45 applied; *universal* restored in the minimal introduction and the space after
   "Note:" in the five notes; nested bullets use the .docx's symbols ● ○ ■ (disc, circle,
   square in layout.css); tests/test_preamble.py checks the nesting, the notes and the bullets.
   [done, PR #24 merged 2026-11-04] 0013 `depends-on`/`cases`: meta-schema.yaml
   (`$defs/value-keys`, shared by values and each case; the two keys come together; cases do not
   nest), check_values.dependency_errors() (called by validate_schema.py with the siblings),
   build_docs.py ("Depends on `x`. For `A`: …"), tests.
   [done, PR #25 merged 2026-11-04] computation: method's terms depend on method-class
   (0013 depends-on/cases); simulation-conditions typed per 0001 A2.2, its ten physical
   quantities containers of the fixed `value` and `unit` (0015, amended 2026-11-04); type has
   open terms; the .docx notation restored (subscripts, Ė, |); legacy_* deleted. The same PR
   applies the 0015 amendment: check_units.py checks leaves, containers and value + unit; §1.3's
   units bullet reworded.
   [done, PR #27 merged 2026-11-04] citation: a repeatable container; reference a free string;
   doi in Annex I's https URI form (0014, settled 2026-11-04), its pattern locked to the table by
   tests/test_properties.py; link format uri; legacy_* deleted. Both uri links of minimal get an
   example: citation › link the Si GAP paper's arXiv page, software › file › link its ColabFit page.
   (Superseded: citation is renamed publication by 0029, PR #60.)
   [done, PR #28 merged 2026-11-04] 0015's second amendment: check_units.py
   requires every numerical leaf (kind physical or dimensionless) to be a `value` beside a `unit`;
   concentration (an atomic fraction 0–1, 0004 item 46), number-of-particles and strain as
   value + unit, recommended unit `dimensionless`; examples/minimal.xml writes the Si
   concentration as 1 with unit dimensionless; §1.3's units bullet covers pure numbers.
   (Superseded: reversed by the third amendment, PR #42; dimensionless values are leaves.)
   [done, PR #29 merged 2026-11-04] 0015 second amendment item 4: check_units.py requires
   the note "The only allowed unit is `dimensionless`." on the `unit` beside every dimensionless
   `value`, and no note elsewhere; the `unit` of concentration, number-of-particles and strain
   carry it. (Superseded: lapsed with the third amendment, PR #42.)
   [done, PR #30 merged 2026-11-04] funding: award-title and award-number strings; funder a
   container like affiliation (name + at most one ROR/ISNI identifier; 0014, settled 2026-11-04),
   with NSF as the example (ROR https://ror.org/021nxhr62, award 2404283); legacy_* deleted.
   (Superseded: award-title is optional by 0030, PR #61.)
   [done, PR #32 merged 2026-11-04] related-content: `links` (a list) renamed `link`, one
   URI per entry since related-content repeats, in the form of citation's link (format uri;
   example the Cambridge deposit of Si_PRX_GAP); description a string; its definition made
   singular ("Another dataset that is connected to the current one in some manner."); legacy_*
   deleted. (Superseded: the Cambridge deposit is the Si GAP dataset itself; it moves to
   dataset-location's examples by 0029, PR #60, and related-content › link has no example.)
   [done, PR #33 merged 2026-11-04] provenance: event-type open terms (definitions in the
   note); date the creation-date pattern, copied and locked by a test; agent a string (superseded:
   structured like creator by 0030, PR #61); `comments`
   renamed `comment` (a scalar); checksum a repeatable container (file, algorithm with SPDX 2.3.1
   §8.4 terms, value in lowercase hex), replacing the baseline's two-string list, defined as "A
   digital fingerprint for the dataset or an associated file modified by the provenance event.";
   legacy_* deleted. (Superseded: a file holds its checksums by 0032, PR #63.)
   [done, PR #34 merged 2026-11-04] matcore-id: a required scalar string, no pattern, since the
   baseline calls the example's format tentative; legacy_* deleted. (Superseded: it is matcore › id by
   0045.)
   PROPOSED, NOT DECIDED (for step 6): the form of a MatCore ID, including whether it has a URI
   form (so it could be a related-content link), and who issues one; matcore › id (0045) is required,
   yet the standard does not say where an author obtains it.
   [done, PR #35 merged 2026-11-04] (Superseded: matcore › creation-date by 0045.) matcore-date:
   written as creation-date (same pattern,
   examples and note, locked by a test); legacy_* deleted. provenance › date gets creation-date's
   note too (missed in PR #33), and a test now compares all of its values.
   [done, PR #36 merged 2026-11-04] license: a required string holding an SPDX license
   expression, described in its note (the SPDX specification 2.3.1, the SPDX License List,
   LicenseRef-), with no list copied into the schema; legacy_* deleted. minimal is complete: it
   declares `legacy_complete: true` (0004 item 36). (Superseded: license is a repeatable
   container of identifier, name, link and applies-to by 0031, PR #62.)
   [done, PR #37 merged 2026-11-04] dft xc-functional: type open terms (LDA, GGA, Meta GGA,
   Hybrid, ML; definitions in the note); description keeps the baseline's guide as its note, with
   the baseline's typo VMN corrected to VWN (Vosko–Wilk–Nusair);
   xc-parameter is the first generic parameter in the form of 0016, the baseline's hint on its
   description moved to a note on xc-parameter; legacy_* deleted. The same PR adds
   scripts/check_generic.py (called by validate_schema.py) and §1.3's definition of the term.
   [done, PR #38 merged 2026-11-04] dft core-electron-model: type and pseudopotential
   type open terms; number-of-valence-electrons value + unit (int, minimum 1); doi in Annex I's
   form; a new `checksum` (provenance's file, algorithm, value) for a checksum of the
   pseudopotential file, `unique-identifier` kept for any other designation, each note pointing
   to the other; examples/dft.xml writes the valence-electron count as value + unit; legacy_*
   deleted. (Superseded: number-of-valence-electrons is a leaf again, PR #42; a file holds its
   checksums by 0032, PR #63.)
   [done, PR #39 merged 2026-11-04] dft valence-electron-model: type open terms
   (repeatable); the localized-orbital basis set gets the pseudopotential's checksum /
   unique-identifier split and Annex I's doi; kinetic-energy-cutoff and charge-density-cutoff
   value + unit (Energy, recommended eV, minimum 0; 0001 A3.1); two baseline typos fixed (a
   trailing comma, a stray space); examples/dft.xml writes the cutoff as 250.0 eV; legacy_*
   deleted. (Superseded: a file holds its checksums by 0032, PR #63.)
   [done, PR #40 merged 2026-11-04] dft calculation-physics: a repeatable string with
   open terms (the baseline's five), "e.g. DFT+U" in the note; legacy_* deleted.
   [done, PR #41 merged 2026-11-04] dft k-point-mesh (0004 item 47): type terms Regular
   gamma-centered, Regular shifted, Irregular; number-of-points value + unit (int [3], minimum 1);
   k-point-spacing removed; shift fractional (float [3], dimensionless); smearing-type terms with
   Fermi-Dirac and Marzari-Vanderbilt; smearing-width in eV; methfessel-paxton-order replaced by
   the generic smearing-parameter; examples/dft.xml loses its spacing, writes the smearing width
   as 0.05 eV and the mesh type as Regular shifted (was Monkhorst-Pack); legacy_* deleted.
   (Superseded: number-of-points and shift are leaves again, PR #42.)
   [done, PR #42 merged 2026-11-05] 0015's third amendment: check_units.py applies
   the value + unit rule to physical kinds only and rejects a unit beside a dimensionless value;
   minimal concentration, number-of-particles, strain and dft number-of-valence-electrons,
   number-of-points, shift are leaves again (recommended unit null); examples/minimal.xml and
   examples/dft.xml write the concentration and the valence-electron count as bare numbers;
   §1.3's units bullet says a pure number carries no unit.
   [done, PR #43 merged 2026-11-05] 0013 settlement 3: build_docs.py renders bounds on a
   value whose extent lists dimensions as "…, for each component." (scalars and extent any keep
   the plain wording); tests/test_build_docs.py covers both; only dft number-of-points changes.
   [done, PR #44 merged 2026-11-05] dft xc-functional revised by 0017: a new optional
   `name` (examples PBE, HSE06) and `normalization` container (`components*`, a list, example
   GGA_X_PBE + GGA_C_PBE; `source*`, open terms LibXC); `type` stays the family; description's
   LibXC hint now points to `normalization`; examples/dft.xml unchanged. build_docs.py renders a
   list-valued example as `[a, b]` (it was Python's repr; this is the first such example).
   PROPOSED, NOT DECIDED (step 9): the instance validator warns when `type` and the components'
   LibXC family prefix disagree; LibXC does not document its prefixes, so a source is needed first.
   [done, PR #45 merged 2026-11-06] dft core-electron-model and valence-electron-model revised
   by 0018: renamed `core-electron-treatment` (terms All-electron, PAW, Pseudopotential) and
   `wavefunction-representation` (terms Gaussian basis sets, LAPW, Local atomic orbitals,
   Numerical atomic orbitals, Plane waves, Real space grids; a note groups them as (1), (2), (3)
   and explains each in a phrase, wording in 0018); descriptions of both,
   localized-orbital-basis-set and the two cutoffs reworded; examples/dft.xml renamed to match.
   Reviewer feedback 2026-11-22 on dft core-electron-treatment: its first sentence repeats the feedback 0018 answered
   (separate basis from core treatment; LAPW is an all-electron basis method), and adds that PAW is a frozen-core
   valence treatment, not a peer of All-electron or Pseudopotential, the current solution being to fill LAPW or PAW
   twice. LAPW: already met by 0018 (LAPW only in wavefunction-representation; core All-electron). PAW: still written
   twice (core type PAW and pseudopotential-or-paw › type PAW). PROPOSED, NOT DECIDED: core-electron-treatment › type
   becomes All-electron or Frozen core (core electrons not treated explicitly; their effect through a pseudopotential or
   PAW dataset, described in pseudopotential-or-paw, whose type says Norm conserving, Ultrasoft or PAW); breaks 0.7.0
   records with core type Pseudopotential or PAW. The human asked to see the resulting schema before deciding. (Superseded:
   decided by 0080.)
   Core electrons by 0080 (ruling 2026-11-22, from that feedback, after the human saw the resulting schema and asked
   where LAPW goes: in wavefunction-representation, unchanged): core-electron-treatment › type has open terms
   All-electron (every electron treated explicitly, even where a code holds the deepest core states fixed) and Frozen
   core (core electrons not treated explicitly; their effect through a pseudopotential or PAW dataset described in
   pseudopotential-or-paw); Pseudopotential and PAW leave the list; pseudopotential-or-paw keeps its type terms (Norm
   conserving, PAW, Ultrasoft) and is described 'For type "Frozen core", …'; examples/dft.json's core type becomes
   Frozen core. Breaks 0.7.0 records with core type Pseudopotential or PAW (still conformant, open terms). PROPOSED,
   NOT DECIDED (0080): a sentence in LAPW's definition covering APW+lo and LAPW with local orbitals; a step 9 warning
   for LAPW with Frozen core. Ruling committed on main (223d638).
   [done, PR #141 merged 2026-11-22] 0080: schema/dft.yaml (core type terms and
   their definitions, pseudopotential-or-paw's description), examples/dft.json (core type Frozen core; its dataset
   stays Ultrasoft), tests/test_dft_rulings.py (a new test of 0080's wording, the dataset's terms, LAPW's place and the
   example), tests/test_properties.py (the 0018 structure test's core terms), 03-dft and the JSON Schema regenerated.
   [done, PR #46 merged 2026-11-06] dft self-consistent-field-convergence, by 0019 and 0020:
   tolerance a container of criterion* (open terms Energy, Charge density, Potential), value* (float, kind
   any, minimum 0, no unit check against the criterion) and unit* (a generic parameter's unit);
   check_generic.py recognises a generic parameter by a value of type and kind any; `method`
   renamed `method-density` (Simple mixing, Pulay mixing, DIIS, Broyden mixing); new repeatable
   `method-diagonalization` (Car-Parrinello, Chebyshev filtering, Conjugate gradient, Davidson
   method, Direct diagonalization, Lanczos, LOBPCG, RMM-DIIS); legacy_* deleted.
   [done, PR #47 merged 2026-11-06] dft core-electron-treatment › pseudopotential renamed
   `pseudopotential-or-paw` by 0021: type terms Norm conserving, PAW, Ultrasoft; "the
   pseudopotential" becomes "the pseudopotential or PAW dataset" in its descriptions and notes;
   examples/dft.xml renamed to match.
   [done, PR #48 merged 2026-11-06] dft relaxation-tolerance-energy: value + unit (Energy,
   recommended eV, minimum 0; 0001 A3.1); legacy_* deleted.
   [done, PR #49 merged 2026-11-06] dft relaxation-tolerance-forces: value + unit (Force,
   recommended eV/angstrom, minimum 0; 0001 A3.1); legacy_* deleted.
   [done, PR #50 merged 2026-11-06] dft comment: a repeatable scalar string, values null; legacy_*
   deleted. dft is complete: it declares `legacy_complete: true` (0004 item 36).
   [done, PR #51 merged 2026-11-07] dft calculation-physics revised by 0022: terms Collinear spin
   polarization, Noncollinear spin polarization, On-site correlation, Orbital polarization,
   Spin-orbit coupling, Van der Waals; a note defining each, allowing at most one of the two spin
   terms and asking for one entry per phenomenon.
   [done, PR #52 merged 2026-11-07] dft relaxation-tolerance-energy and SCF criterion "Energy"
   revised by 0023: the description drops "Total"; a note defines the energy (free energy E − TS
   with smeared occupations, total energy otherwise, not extrapolated to zero smearing); the SCF
   note's "Energy" refers to it (stating the definition in place, or linking, was declined).
   [done, PR #53 merged 2026-11-07] dft xc-functional name and description by 0024: both kept (a
   merge into `name` was declined); the list of named functionals moves to name's note with the
   pointer to normalization, and name's examples (PBE, HSE06) are removed; description's note
   states its use; examples/dft.xml gives <name>PW91</name>.
   PROPOSED, NOT DECIDED: whether name's note says that a dispersion correction's name may form
   part of `name` (e.g. PBE-D3) and that the correction is also recorded as calculation-physics
   "Van der Waals" (0022, 0024). (Superseded: settled by 0051; name gives the functional alone.)
   [done, PR #54 merged 2026-11-07] §1.1 FAIR data and AI readiness (0004 item 50): one sentence
   at the end of the first paragraph, no link; the paragraph's double space removed.
   [done, PR #55 merged 2026-11-07] minimal structure by 0025: a required, repeatable top-level
   `structure` (an optional description, then material-component, moved inside it, with no
   structure-level type);
   material-component gains a required `form` (open terms 2D material, Bulk, Chain, Cluster,
   Molecule, Monolayer, Nanoparticle, Nanoribbon, Nanotube, Nanowire, Slab, Thin film), an
   optional `role` (Adsorbate, Core, Film, Inclusion, Layer, Matrix, Shell, Solute, Solvent,
   Substrate) and an optional `fraction` (atomic, 0–1); `phases` renamed `phase`, optional and
   a repeatable scalar, Crystal replaced by Single crystal and Polycrystal, Molecule removed,
   Gas redefined; description gains a note on facets and orientations; examples/minimal.xml
   gets a Bulk and a Slab structure (breaks 0.5.0 instances).
   [done, PR #56 merged 2026-11-07] minimal varying conditions by 0026: simulation-conditions ›
   description covers how any condition varies in space or time and what a varying condition's value represents
   (initial, mean or final, or the value in one region); the simulation-conditions note, reworded
   without "SubSubProperties", says a varying condition gives a single representative value;
   stress's note says "cell" for "the cell subproperty"; strain-rate drops "constant throughout
   the simulation"; concentration and fraction notes give the composition as set up when it
   changes (e.g. semi-grand-canonical). Two optional bool flags, spatially-varying and
   time-varying, follow description. (Superseded: the "as set up" notes by 0035; the flags by
   0036's spatial-uniformity and time-dependence.)
   PROPOSED, NOT DECIDED (md): a semi-grand-canonical term for thermodynamic-constraint › type,
   and whether its `system` states the region as 0026's description does. (Superseded: decided by
   0069, term ΔμNPT; the region a value applies to stays in conditions › description, 0035 item 4.)
   [done, PR #57 merged 2026-11-07] minimal phase › Quasicrystal by 0027: "A solid material
   with long-range order but without translational periodicity, e.g. one whose diffraction
   pattern shows five-fold rotational symmetry." (the baseline's said short-range order only).
   [done, PR #59 merged 2026-11-07] minimal combined methods by 0028: §1.2 distinguishes
   methods that supply energies and forces from those that use them; `method` gets a note (give the method that produces the
   data; the force source goes in interaction-model); new optional repeatable
   `interaction-model` after method (open terms CC, DFT, Empirical potential, ML potential, QMC,
   Tight binding). (Superseded in part: interaction-model and the note are replaced by 0046's
   input links, PR #83.)
   PROPOSED, NOT DECIDED: how md particle-interactions › model-type relates to
   interaction-model (md PR) (Superseded: 0046 removes interaction-model and moves the model to pim); whether 0028's rule matches MODA's classification principle
   (check the MODA source).
   [done, PR #58 merged 2026-11-07] Preamble acronyms by 0004 item 51: KIM, CODATA and IRI
   spelled out at their first use in §1.3, each expansion traced to its defining body; QUDT,
   which gives no expansion, described in its own words.
   [done, PR #60 merged 2026-11-07] minimal publication and dataset-location by 0029: `citation`
   renamed `publication` (papers describing the dataset); new optional, repeatable top-level `dataset-location`
   (repository, doi, link*) for where the dataset is stored; the Cambridge deposit moves from
   related-content › link's example to dataset-location's, and examples/minimal.xml gains a
   dataset-location.
   [done, PR #61 merged 2026-11-07] minimal funding and provenance by 0030: award-title
   optional; provenance gets a note recommending it; provenance › agent takes creator's structure (required, repeatable).
   [done, PR #62 merged 2026-11-07] minimal license by 0031: license a required, repeatable container (identifier*, an
   SPDX expression or LicenseRef-; name; link; applies-to); the note says to give the short
   identifier and, for a LicenseRef, its name and a link; data-license examples;
   examples/minimal.xml keeps GPL-3.0-only (the deposit's license) as an entry.
   [done, PR #63 merged 2026-11-07] file with checksum by 0032: minimal provenance › checksum becomes provenance › file
   (name*, checksum* repeatable of algorithm* and value*); dft pseudopotential-or-paw and
   localized-orbital-basis-set › checksum become › file likewise, their notes and
   unique-identifier's naming file.
   [done, PR #64 merged 2026-11-07] matcore-author by 0033: a new required, repeatable top-level
   property after matcore-id, with creator's structure, naming who created the metadata record;
   examples/minimal.xml gives Ellad B. Tadmor, University of Minnesota. (Superseded: matcore ›
   record-author by 0045.)
   [done, PR #65 merged 2026-11-07] 0033 amended: the example's matcore-author gains ORCID
   https://orcid.org/0000-0003-3311-6299; tests/test_examples.py checks every identifier in the
   minimal example against Annex I.
   [done, PR #66 merged 2026-11-08] minimal composition formula by 0034: material-component's `constituent` replaced by
   `formula*` (grammar in its note), `variable` (name*, value*, type*; type required, and Final
   added, by the amendments of 2026-11-08) and `topology` (substance, identifier with schemes AFLOW,
   InChI and SMILES; replaces `molecule` by the second amendment); scripts/check_formula.py parses
   and checks formulas (called by validate_schema.py; reused by step 9); Annex I gains AFLOW, InChI
   and SMILES rows;
   examples/minimal.xml writes <formula>Si</formula>. (Superseded in part: `variable › type` is
   renamed `qualifier` by 0035.)
   [done, PR #67 merged 2026-11-08] qualified values by 0035: a `qualifier` leaf (Average, Final, Initial, Maximum, Minimum;
   fixed form, checked by check_units.py) wherever a value varies; the twelve numerical
   simulation conditions repeatable with an optional qualifier (number-of-particles and strain
   become containers of value + qualifier); fraction a repeatable value + qualifier, its "as set
   up" sentence removed; variable › type renamed qualifier (still required); simulation-conditions'
   note and description reworded (amends 0015 and 0026; breaks 0.5.0 instances). (Superseded in
   part: number-density is removed by 0037, so eleven conditions remain.)
   [done, PR #68 merged 2026-11-08] simulation type by 0036: simulation-conditions › type becomes a container of
   thermodynamic-state* (Equilibrium, Steady state, Transient), system-openness (Isolated, Closed,
   Open), time-dependence (Constant, Varying, Cyclic) and spatial-uniformity (Uniform, Nonuniform,
   Periodic), with a note pointing to description; spatially-varying and time-varying removed
   (reverses 0026 item 5); examples/minimal.xml nests Equilibrium under thermodynamic-state
   (breaks 0.5.0 instances).
   PROPOSED, NOT DECIDED (md): how thermodynamic-constraint (the ensemble) relates to
   system-openness (0036). (Superseded in part: 0042 item 3 decides that md does not repeat a
   quantity simulation-conditions holds and adds only how a condition is enforced and the
   ensemble; how the ensemble term relates to system-openness is settled in the md PR.)
   [done, PR #69 merged 2026-11-08] number-density removed by 0037: simulation-conditions › number-density dropped as
   redundant with number-of-particles and volume (breaks 0.5.0 instances).
   [done, PR #70 merged 2026-11-08] array order by 0038: §1.3's Extent bullet says a multi-dimensional value is a list of
   lists, first index outermost, and a serialization preserves the nesting; cell and
   cell-reference notes say value[i][j] is the j-th Cartesian component, in the frame of the
   simulation, of the i-th vector (rows a, b, c); extent stays [3, 3].
   [done, PR #71 merged 2026-11-08] imposed conditions by 0039: every simulation-condition definition says the value is
   imposed and uses its own term (temperature, stress, ...); the note says a measured quantity is a
   result, not a condition; heat-flux and temperature-gradient say to give whichever is imposed;
   basis notes and two value notes tidied. Wording only.
   PROPOSED, NOT DECIDED: whether the minimal metadata should list the quantities a dataset
   contains (e.g. energies, forces, a heat flux) (0039).
   [done, PR #77 merged 2026-11-08] applied fields by 0040: Kinds ElectricFieldStrength, MagneticFluxDensity, Acceleration;
   units V/m, V/angstrom, T, m/s^2, one PR each with every field traced (the first of each Kind adds
   the Kind); then electric-field (V/m), magnetic-field (B, T) and body-force (per unit mass, m/s^2)
   as [3] vector conditions after temperature-gradient. Ruling committed on main. [done, PR #72
   merged 2026-11-08] unit V/m with the Kind ElectricFieldStrength.
   [done, PR #73 merged 2026-11-08] unit V/angstrom.
   [done, PR #74 merged 2026-11-08] unit T with the Kind MagneticFluxDensity.
   [done, PR #75 merged 2026-11-08] unit m/s^2 with the Kind Acceleration. The conditions in PR #77.
   [done, PR #78 merged 2026-11-08] electrode potential by 0041: Kind ElectricPotential; unit V by its own PR; then
   electrode-potential (value, unit, reference* with terms SHE, RHE, Vacuum, qualifier) after
   body-force, for the working electrode. Ruling committed on main. [done, PR #76 merged 2026-11-08]
   unit V with the Kind ElectricPotential. The condition in PR #78.
   PROPOSED, NOT DECIDED: an `electrode` subproperty naming the electrode, so several electrodes can
   each have entries (0041).
   PROPOSED, NOT DECIDED (md): a minimal `chemical-potential` condition (repeatable, naming a
   species from `formula`, Energy or MolarEnergy), since 0036 lets a simulation be Open but not say
   to what; decided together with md's thermodynamic-constraint (0040; revisits 0026). (Superseded:
   decided by 0042 before md.)
   [done, PR #79 merged 2026-11-08] chemical potential by 0042: simulation-conditions › chemical-potential (value in Energy,
   recommended eV; unit; species*; relative-to for a difference; qualifier, its note "for the
   species") after electrode-potential.
   [done, PR #80 merged 2026-11-08] software layers by 0043: software is one entry per layer (outermost first), gaining role
   (Calculation method, Script, Simulation code, Workflow framework), description, link, revision,
   identifier (DOI, SWHID), dependency (name, version, role) and build-options; file gains encoding
   (Base64) and, by the amendment of 2026-11-08, checksum in 0032's structure; examples/minimal.xml gives CASTEP role Simulation code.
   PROPOSED, NOT DECIDED: a recommended format for the full software environment that a record
   points to (e.g. the HPC software metadata standard in preparation at BSC; CodeMeta, SPDX or
   CycloneDX SBOMs, Spack specifications to check); KIM IDs as an Annex I scheme (0043).
   [done, PR #82 merged 2026-11-08] matcore container by 0045: a required top-level `matcore` (standard-version*, standard-link,
   id*, dataset-version*, record-author*, creation-date*) replaces matcore-id, matcore-author and
   matcore-date; dataset-version is 1 + the number of provenance Version update events; the example
   gives 0.6.0, the v0.6.0 tag address, id mc-ad83jsd3 and dataset-version 1.
   PROPOSED, NOT DECIDED: GitHub releases with Zenodo so each release gets a DOI (0010), the step it
   adds to the release procedure, and a .zenodo.json or CITATION.cff for the record's metadata (0045).
   [done, PR #83 merged 2026-11-09] computations and links by 0046 (ruling
   committed on main 278596e): structure and computation get a required `label`;
   computation gains `task`, `structure` (labels) and `input` (computation label + role:
   Interaction model, Initial configuration, Starting point, Training data, Parameters, Source
   data); simulation-conditions renamed `conditions`, optional; interaction-model removed (reverses
   0028 item 3); method terms TB, MS (molecular statics, described by md with MD) and PIM; software role Interaction model; every method section's
   properties inside a repeatable `settings` naming the computations of its method; §1.2 states
   that MatCore describes a dataset and does not reproduce its execution. One PR for minimal, dft,
   the Preamble and the examples (breaks 0.6.0 instances). The new pim section (Particle
   Interaction Model) and md's reduction to dynamics come in the md PRs; mbpt starting-point
   becomes an input in the mbpt PR. 0046's Consequences list its PROPOSED, NOT DECIDED points (pim's
   number, a series of runs as one computation or several, a model's citation, QM/MM regions, an
   Electronic method with a learned ingredient, eFF's nuclei, KIM IDs in Annex I, whether a DFT
   relaxation is DFT/Optimization or MS + DFT, md's title). (eFF's nuclei settled 2026-11-10: a
   particle-style term Nucleus, applied in the particle-style PR.)
   [done, PR #85 merged 2026-11-10] species of a pseudopotential, PAW dataset or basis set by 0047 (A2 of the analysis,
   ruling 2026-11-09): pseudopotential-or-paw gains required `species` after name;
   localized-orbital-basis-set gains optional repeatable `species` after type (omitted when one basis
   set serves every species); examples/dft.json gives Si.
   [done, PR #85 merged 2026-11-10] relaxation stress tolerance by 0048 (A4 remainder, ruling 2026-11-09): dft gains
   relaxation-tolerance-stress (value + unit, Pressure, GPa, minimum 0) after the force tolerance;
   all three tolerances note "Give it when the computation's task is Optimization."
   [done, PRs #86, #87, #90] net charge by 0049 (B1, ruling 2026-11-09): Kind ElectricCharge with units e and C, one
   PR each with every field traced (the first adds the Kind); then minimal conditions › net-charge
   (value float, ElectricCharge, recommended e; unit; qualifier) after number-of-particles.
   [done, PR #86 merged 2026-11-10] unit e with the Kind ElectricCharge (QUDT ElectricCharge,
   A0E1L0I0M0H0T1D0; unit QUDT E, GNU Units e, factor 1.602176634e-19 exact).
   [done, PR #87 merged 2026-11-10] unit C (QUDT C, GNU Units C, factor 1, exact).
   [done, PR #90 merged 2026-11-10] the condition net-charge after number-of-particles.
   [done, PRs #88, #89, #91] magnetic moments and order by 0050 (B2, ruling 2026-11-09): Kind MagneticMoment with units
   mu_B and J/T, one PR each with every field traced; then dft initial-magnetic-moment (species*,
   value* extent any in mu_B, unit*) after calculation-physics, and minimal material-component ›
   magnetic-order (open terms Nonmagnetic, Ferromagnetic, Antiferromagnetic, Ferrimagnetic,
   Paramagnetic, Noncollinear) after phase. PROPOSED, NOT DECIDED: a condition for a fixed total
   magnetization or spin multiplicity.
   [done, PR #88 merged 2026-11-10] unit mu_B with the Kind MagneticMoment (QUDT MagneticMoment,
   A0E1L2I0M0H0T0D0; no QUDT unit, so Note 7 lists it; GNU Units mu_B; factor 9.2740100657e-24,
   CODATA 2022).
   [done, PR #89 merged 2026-11-10] unit J/T (QUDT J-PER-T, GNU Units J/T, factor 1, exact).
   [done, PR #91 merged 2026-11-10] dft initial-magnetic-moment after calculation-physics
   (before dispersion-correction) and minimal material-component › magnetic-order after phase.
   [done, PR #85 merged 2026-11-10] dispersion correction by 0051 (B4, ruling 2026-11-09): dft dispersion-correction (open
   terms D2, D3, D3(BJ), D4, TS, MBD) after calculation-physics; xc-functional › name names the
   functional alone, its note saying so.
   [done, PR #85 merged 2026-11-10] smearing-width note by 0052 (B5, ruling 2026-11-09): the width is an energy, k_B T for
   Fermi-Dirac, and not a temperature imposed in `conditions`.
   [done, PR #85 merged 2026-11-10] smearing container by 0053 (C5, ruling 2026-11-09): dft settings gains `smearing` after
   k-point-mesh holding type, width and parameter (were k-point-mesh › smearing-type, smearing-width,
   smearing-parameter); examples/dft.json moves its width; references (e.g. the generic-parameter
   list above) updated in the same PR.
   [done, PR #85 merged 2026-11-10] dft introduction by 0054 (C1, ruling 2026-11-09): the 0018 names, and a sentence that
   the properties are given in settings blocks naming DFT computations (pim and md get the
   sentence in their own PRs).
   [done, PR #85 merged 2026-11-10] LAPW basis cutoff by 0057 (C6, ruling 2026-11-09): wavefunction-representation gains
   lapw-basis-cutoff (dimensionless RKmax, minimum 0) after kinetic-energy-cutoff, whose description
   narrows to plane waves and LAPW given as an energy.
   [done, PR #85 merged 2026-11-10] LibXC version by 0058 (C7, ruling 2026-11-09): normalization › source notes that the
   library's version is a software dependency.
   [done, PR #85 merged 2026-11-10] k-point mesh note by 0059 (C8, ruling 2026-11-09): the mesh samples the cell of minimal
   conditions › cell; a mesh that varies between configurations omits number-of-points and is
   explained in comment. All findings of the 2026-11-08 analysis are now ruled on (0046–0059;
   B3 and C4 declined); rulings 0047–0059 committed on main (34b7740, pushed). 0055 and 0056
   need no PR. Implementation groups proposed: (1) units e (with Kind ElectricCharge), C, mu_B (with
   Kind MagneticMoment), J/T, one PR each with traced fields; (2) net-charge (0049); (3) the
   magnetic properties (0050); (4) the dft changes (0047, 0048, 0051–0054, 0057–0059), one PR or
   several as the human decides. Awaiting the human's choice of which group to start (dft changes
   first was suggested, as they need no new units).
   PROPOSED, NOT DECIDED (rest of the 2026-11-08 analysis): A2 a required species on
   pseudopotential-or-paw and localized-orbital-basis-set (Superseded: decided by 0047); A3 a thermodynamic-state term for static
   calculations (Superseded by 0046: task Single point, conditions optional); A4 a minimal task
   (Superseded: 0046 adds `task`, the tolerances stay in dft, and 0048 adds a stress tolerance); B missing dft settings (total charge (Superseded: a minimal condition by 0049), initial magnetic moments (Superseded: 0050), DFT+U values and
   scheme (Declined by the human 2026-11-09 as too detailed; "On-site correlation" stays the only mark), vdW correction method (Superseded: 0051), a note that the smearing width is not the temperature (Superseded: 0052)
   condition); C the dft introduction's pre-0018 names (Superseded: 0054), doi strings vs identifier containers (Superseded: both kept, rule stated by 0055), two
   shapes of `file` (Superseded: both kept, rule stated by 0056), `comment` vs `description` (Declined by the human 2026-11-09: comment holds information not covered by the recorded settings, not a description, and repeats for unrelated points; left as is), smearing under k-point-mesh (Superseded: 0053), RKmax for LAPW (Superseded: 0057), the
   LibXC version as a software dependency (Superseded: 0058).
   0046 item 8 amended 2026-11-09: a PIM computation is the evaluation of energies and forces,
   whatever code performs it, its software listing every layer (e.g. LAMMPS and a KIM model);
   md charge-interactions and magnetic-interactions move whole to pim, describing the interaction
   as evaluated (charge equilibration and long-range sums included), since they couple the model
   and the code; degrees of freedom propagated in time (iEL, Drude, LLG spins) are named in pim,
   their thermostats are md thermodynamic-constraint entries naming them in `system`.
   0046 open points settled 2026-11-09: pim is 2.3, before md (md, mbpt, ml, pf, derived become
   2.4–2.8 in titles and menu labels; existing page files keep their names and addresses; pim's
   page is docs/standard/pim.md); md's title is unchanged; a DFT relaxation stays one computation
   (DFT, task Optimization) with dft's relaxation tolerances, MS being for relaxations with a PIM.
   (Superseded in part: such a relaxation is PS with task Optimization, by 0064.)
   [done, PR #84 merged 2026-11-09] the pim section and md reduced to dynamics by
   0046 items 8 and 9, structure only (no typed field filled): schema/pim.yaml (2.3) with settings ›
   computation, theory-level, model-type, particle-style (now repeatable), bonding-type,
   charge-interactions, magnetic-interactions, legacy text moved with them; md (2.4) is settings ›
   computation, algorithm, computation-parameter, initialization, thermodynamic-constraint; md
   computation › mode and particle-interactions › source removed; mbpt, ml, pf, derived renumbered
   2.5–2.8; build_docs.PAGES keeps page files (pim.md new); §1.2's list gains PIM;
   examples/pim.json from md.json's model, md.json in settings.
   PROPOSED, NOT DECIDED: pim's properties are taken up before md's in status step 5, in file order
   (Superseded: settled 2026-11-10, pim first);
   md's introduction says "classical molecular dynamics" though md now also serves AIMD and MS, and
   §1.2's list says "MD: Classical molecular dynamics". (Superseded: settled by 0061.)
   [done, PR #92 merged 2026-11-10] pim theory-level: string, open terms Physics-based,
   Machine-learned (0046 item 8), defined in the note; description "How the functional form of the
   model was obtained."; legacy_* deleted; examples/pim.json writes Physics-based.
   [done, PR #93 merged 2026-11-10] pim model-type: string with the baseline's examples
   (Lennard-Jones, EAM, MACE) and a note that the specific parameterization (OpenKIM model, NIST IPR
   record, published potential file) is the computation's software; legacy_* deleted.
   [done, PR #94 merged 2026-11-10] pim particle-style: string, open terms the baseline's
   seven plus Nucleus (0046, settled 2026-11-10), definitions and "one entry for each kind of
   particle" in the note; description "The nature of the discrete entities whose interactions the
   model describes."; legacy_* deleted; examples/pim.json writes Atom.
   [done, PR #95 merged 2026-11-10] pim bonding-type: string, open terms Reactive, Bonded
   fixed, Bonded mutable; Reactive defined as a model without a predetermined bonding topology
   (decided in review 2026-11-10), so pair, EAM and ML potentials are Reactive; "during a
   simulation"; *a priori* italics restored; legacy_* deleted.
   [done, PR #96 merged 2026-11-11] pim charge-interactions: the container and its
   six string subproperties (charge-origin, charge-style, charge-variability,
   long-range-electrostatics, electric-dipole, electric-dipole-variability) with the baseline's
   open terms, defined in the notes; electric-dipole-variability's description, a copy of
   charge-variability's, says "electric dipoles"; "Fixed" says "during a simulation"; legacy_*
   deleted.
   Electrostatic summation by 0068 (ruling 2026-11-14, from reviewer feedback): pim
   charge-interactions › long-range-electrostatics is renamed `electrostatic-summation` (description
   "Method used to compute the electrostatic interactions between the charges."; the name
   electrostatic-interactions declined, as it parallels the container charge-interactions); a term
   "Short-range" after Direct (within a cutoff, possibly shifted or damped, e.g. Wolf, DSF); "None"
   redefined as no electrostatic interactions computed from the charges, a model without charges
   omitting charge-interactions. The reviewer's point that the code, not the model, does the
   long-range sum was already settled by 0046 item 8 (amended 2026-11-09). No released instance
   breaks. [done, PR #108 merged 2026-11-14]
   pim.yaml (rename, Short-range, None with the sentence on models without charges in its note),
   tests/test_computations.py (vocabulary, names, a test of 0068's wording), pim page regenerated.
   Spin styles by 0060 (ruling 2026-11-12): pim magnetic-interactions › spin-style keeps open terms
   Classical spin and Coupled spin lattice; Ab initio, Tight binding and Quantum spin dynamics are
   removed, since 0046 does not count them as particle interaction models (spin-polarized DFT or TB
   is a computation of its own, named as an input with the role Interaction model);
   magnetic-dipole a string with examples Heisenberg, Multi-spin, Zeeman and a note pointing to the
   magnetic-field condition. PROPOSED, NOT DECIDED (0060): a TB section; where quantum spin dynamics
   is described; a method term for spin dynamics on a fixed lattice (with md algorithm).
   [done, PR #97 merged 2026-11-12] pim magnetic-interactions by 0060: spin-style
   and magnetic-dipole filled, legacy_* deleted; pim is complete and declares
   `legacy_complete: true` (0004 item 36). pim's introduction gains 0054's sentence on settings
   blocks.
   [done, PR #97] pim in file order: settings › theory-level (done, PR #92), model-type (done, PR #93), particle-style (done, PR #94), bonding-type (done, PR #95),
   charge-interactions (done, PR #96), magnetic-interactions (done, PR #97) (computation needs no fill).
   Particle Simulation by 0061 (ruling 2026-11-12): section 2.4 is retitled "2.4 Particle Simulation
   (PS) Metadata" (MatCore-PS), key `ps` (schema/ps.yaml, examples/ps.json, docs/standard/ps.md,
   addresses `#ps.…`; breaks 0.6.0 md instances); method terms MD and MS unchanged; a new
   introduction without "classical", with 0054's settings sentence; §1.2 lists "PS: Particle
   simulation (molecular dynamics, molecular statics and related methods)"; MatCore-MD becomes
   MatCore-PS in §1.2 and About; Leadership renames "Method: Molecular Dynamics" to "Method: Particle
   Simulation" and adds "Method: Particle Interaction Model" with "TBD". PROPOSED, NOT DECIDED
   (0061): whether PS describes Monte Carlo (method MC); the PIM committee's members. (Superseded in
   part: PS describes Monte Carlo, and MC is a group of ps algorithm terms, by 0064.)
   [done, PR #98 merged 2026-11-12] the 0061 rename: schema/ps.yaml, examples/ps.json,
   docs/standard/ps.md (04-md.md removed), build_docs.PAGES, check_examples.SECTIONS, mkdocs.yml nav,
   §1.2, About and Leadership; tests updated, two new tests in tests/test_computations.py.
   Label references by 0062 (ruling 2026-11-12): a property whose value is the label of a structure or
   computation is named for it: settings › computation (dft, pim, ps) and minimal computation › input ›
   computation become `computation-label`, minimal computation › structure becomes `structure-label`
   (all added after 0.6.0, so no released instance breaks).
   [done, PR #99 merged 2026-11-12] the 0062 rename: schema minimal, dft, pim, ps;
   the four examples (keys only); tests/test_computations.py updated, with a test that every
   label-holding property is named *-label; pages regenerated.
   Staged simulations by 0063 (ruling 2026-11-12, from reviewer feedback): minimal computation gains a
   note: a simulation run in stages is one computation per stage whose method, settings or conditions
   differ and whose data matter; each names the stage it continues from as input role Initial
   configuration, which carries over the final state; the links give the order; a ramp within a stage
   is qualified condition entries; the full protocol is workflow provenance (§1.2). Initial
   configuration's definition adds the carried-over state, e.g. velocities. A protocol object and an
   order field are declined.
   [done, PR #100 merged 2026-11-12] the 0063 note: schema/minimal.yaml (computation note,
   Initial configuration definition), tests/test_computations.py, 02-minimal.md regenerated.
   Grouping computations by 0077 (ruling 2026-11-22, from the review of 0076's worked Raman example): minimal
   `computation` gains a note before 0063's: the record explains the dataset, not its workflow (§1.2); a computation is
   given for calculations whose results are in the dataset or whose method or settings a reader needs; steps serving
   one purpose with one method are one computation (e.g. the DP steps giving phonon modes and a Raman spectrum); a
   step that only prepares another (e.g. a relaxation fixing the cell for later single points) may be left out or
   mentioned in that computation's description. 0063 stands as the same test for staged simulations. A procedure's
   parameters are given with the procedure, in the section describing it, even when applied in another computation's
   calculations (e.g. a Raman calculation's finite-difference displacement in its derived entry). No released
   instance breaks. Ruling committed on main (48adc35).
   [done, PR #135 merged 2026-11-22] 0077 note: schema/minimal.yaml
   (computation's first note, the ruling's text verbatim, before 0063's), tests/test_computations.py (a new test; the
   0063 test's list of notes gains it), 02-minimal regenerated; no example changes.
   Decided by the human 2026-11-22 for the derived property PR: type's term "X-ray scattering" becomes "Scattering"
   (X-ray and neutron diffraction, reflectivity, pair-distribution functions), electron diffraction staying under
   Microscopy, electron; Vibrational and Spectroscopy, vibrational both stay, defined apart (the vibrations
   themselves; a simulated spectrum for comparison with a measurement).
   Reviewer feedback 2026-11-22 on derived type's families: (1) Mechanical: tensile, yield and fracture stresses and
   strengths, hardness; (2) Thermodynamic: thermodynamic integration, melting temperature; (3) a new
   "Transformation-pathway": nudged elastic band, energy maps, minimum energy paths; (4) are diffusion and viscosity
   Transport, and where do defect mobilities go (point defects, dislocations, grain boundaries)? Analysis: (1) and (2)
   exist since 0076, the examples are new; thermodynamic integration is a procedure (ps algorithm, task Free energy
   calculation), not a property; (3) paths and barriers are computed by PS computations of task Transition path, and a
   derived block may name such a computation (0076 item 1), so a type term is needed to classify them; (4) diffusion is
   Transport (mass), viscosity is momentum transport, absent from Transport's definition. PROPOSED, NOT DECIDED: add the
   reviewer's examples to Mechanical and Thermodynamic (not thermodynamic integration); a term "Transition path"
   named after minimal task (energy barriers, minimum energy paths, energy landscapes, transition rates); Transport
   covers momentum (viscosity) and the motion of defects under a driving force (dislocation and grain-boundary
   mobility), point-defect migration barriers being Transition path. (Superseded: decided by 0081, without a new term.)
   Derived families by 0081 (ruling 2026-11-22, from that feedback): Mechanical's definition and examples gain tensile,
   yield and fracture strengths and hardness; Thermodynamic's gain a melting temperature (thermodynamic integration not
   listed: a procedure in ps); Transport covers charge, heat, mass and momentum (viscosity) and the motion of defects
   under a driving force (dislocation and grain-boundary mobility); no transition-path family (the human asked whether
   it would repeat ps algorithm NEB and minimal task Transition path; it would): the introduction says a result its
   computation already names, e.g. a path and barrier found by the NEB, needs no derived entry, while a property
   obtained from such results, e.g. a rate, is one. Terms unchanged; no record breaks. Ruling committed on
   main (a25366a). [done, PR #142 merged 2026-11-22] schema/derived.yaml (the
   three definitions, the introduction's three family lines, and a sentence in its second paragraph: a result its
   computation already names needs no derived entry, e.g. a path and barrier found by ps algorithm NEB with task
   Transition path; a rate from them is one), tests/test_computations.py (a new test of 0081's wording), 08-derived
   regenerated; the JSON Schema is unchanged (it carries descriptions, not term definitions).
   [done, PR #136 merged 2026-11-22] derived derived-property (step 5, 0076
   items 4, 5): derived-property noted one entry per property; type a string with 14 open terms, each defined in a
   note drafted in this PR, its description "The kind of property computed."; name a new required string (examples
   Raman spectrum, Phonon dispersion); description a string; procedure a required string, "How the property was
   obtained from the results of the computations named in minimal `computation › input`.", its note asking for the
   role of each calculation-parameter entry and placing the parameters of requested calculations here (0077 item 3);
   calculation-parameter a generic parameter (0016), its description "A parameter of the procedure that obtained the
   derived property." and a note with examples (supercell, displacement, broadening, the baseline's NMR coupling
   constant); legacy_* deleted; derived is complete and declares `legacy_complete: true`, so every section is
   complete and status step 5 is done once this merges; the introduction's list of families uses Scattering and
   matches type's terms (locked by a test); examples/derived.json gives name Raman spectrum;
   tests/test_computations.py (a new test; the structure test's lists gain name); tests/test_schema.py's
   legacy_complete test plants a legacy field in a copy of derived; tests/test_build_docs.py's main() test checks
   that no page shows legacy text even with --show-legacy; 08-derived regenerated. Follow-up, PROPOSED, NOT
   DECIDED: remove --show-legacy from CI (.github/workflows/ci.yml) and from the working rules once this merges,
   since no legacy text remains. (Superseded: decided by the human 2026-11-22. [in progress, branch
   drop-show-legacy: done, PR #138 merged 2026-11-22] The flag leaves CI, README.md, CONTRIBUTING.md and the working
   lines of CLAUDE.md; README's editing step names values.note instead of legacy_values; build_docs.py keeps the
   option, its docstring saying no legacy text remains (judgment call: removing it would also remove the legacy
   rendering and its test); history entries and decision records are left as written.)
   [done, PR #110] md (ps after 0061) in file order, starting with algorithm (computation-label needs no fill;
   algorithm done, PR #106; computation-parameter done, PR #107; initialization done, PR #109; thermodynamic-constraint done, PR #110; ps is complete; next mbpt).
   [done, PR #111 merged 2026-11-15] mbpt structure by 0046 items 7
   and 10, no typed field filled: mbpt's properties move unchanged into a required, repeatable
   `settings` whose first member is computation-label; starting-point is removed (an MBPT computation
   names its DFT computation as input role Starting point); the introduction drops "starting point",
   gains 0054's settings sentence and says the DFT computation is named as that input;
   examples/mbpt.json in settings, with label g0w0 and without starting-point; tests in
   tests/test_computations.py; 05-mbpt regenerated (property addresses gain `settings.`). Then mbpt's
   properties in file order: mbpt-method, dielectric-matrix, gw-bands, bse-hamiltonian,
   bse-kernel-truncation.
   The DFT-to-MBPT link is one-way (checked 2026-11-15): every self-consistency variant, QSGW
   included, iterates within the MBPT computation and does not re-run the DFT one, so input role
   Starting point fits; a DFT stage chain (SCF, then non-SCF with many bands) is one computation per
   stage (0063). PROPOSED, NOT DECIDED (for the mbpt-method PR): whether GW followed by BSE
   ("GW/BSE", "evGW+BSE") is one MBPT computation, as in the baseline, or two, the BSE naming the GW
   as input role Starting point (0046). (Superseded: decided by 0070, one computation of type GW/BSE.)
   GW and BSE by 0070 (ruling 2026-11-16, from review of mbpt-method): mbpt-method › self-consistency is
   replaced by two optional properties, gw-self-consistency (open terms G0W0, GW0, G0W, evGW, scGW, QSGW)
   and bse-self-consistency (BSE0, scBSE); the combined terms evGW+BSE and scGW+BSE are removed; "evGW" –
   Eigenvalue-only self-consistent GW is added; type keeps GW, BSE and GW/BSE, GW followed by BSE being
   one computation of type GW/BSE (qualifies 0063 for MBPT); a note says which property follows type;
   the terms stay ASCII and the definitions write subscript zero (G₀W₀), since the digit zero looks
   like the letter O in the site's fonts. Two structures were declined: the baseline's combined terms,
   and GW and BSE as two computations linked by input role Starting point. No released instance breaks.
   PROPOSED, NOT DECIDED (0070): whether the step 9 validator checks which property follows type.
   [done, PR #112 merged 2026-11-16] mbpt mbpt-method (step 5),
   applying 0070: type string with terms GW, BSE, GW/BSE, defined in a new note (GW/BSE one
   computation; BSE alone names its quasiparticle energies' computation as input role Starting point);
   gw-self-consistency and bse-self-consistency optional strings, the baseline's definitions with
   subscript zero, evGW defined, scGW narrowed to energies and wavefunctions, BSE0's definition no
   longer saying GW energies; each with a note "Give it when `type` is …"; legacy_* deleted;
   examples/mbpt.json writes gw-self-consistency; test in tests/test_computations.py; 05-mbpt
   regenerated.
   Raised by the human 2026-11-16, PROPOSED, NOT DECIDED: where TDDFT, EOM-CC, ADC
   and QMC belong. By 0064's method definitions, TDDFT is DFT (a dft extension or its own section),
   EOM-CC is CC and QMC is QMC (future sections), and ADC, a propagator method from diagrammatic
   perturbation theory, fits MBPT's definition, though quantum chemistry groups it with CC.
   Reviewer feedback 2026-11-16 on the baseline's mbpt starting-point (term "DFT+U"): DFT+U should be a
   separate flag, not an xc-functional, as dft calculation-physics has it. Already met: starting-point
   is removed (0046), the starting DFT computation records the functional in xc-functional and DFT+U
   as calculation-physics "On-site correlation"; the U values were declined 2026-11-09. Decided by the
   human 2026-11-16: xc-functional › name's note, which says to give the functional without a dispersion
   correction (0051), adds "Likewise give it without a Hubbard correction (e.g. PBE, not PBE+U), which
   is given as calculation-physics "On-site correlation"." [done, PR #113 merged
   2026-11-16] schema/dft.yaml, tests/test_dft_rulings.py (a new test; the 0051
   test checks its sentence with `in` instead of `endswith`), 03-dft regenerated.
   [done, PR #114 merged 2026-11-17] mbpt dielectric-matrix
   (step 5): planewave-basis-cutoff value + unit (Energy, recommended eV, minimum 0; 0001 A5);
   localized-orbital-basis-set a string (example cc-pV6Z; stray space before the period removed); frequency
   and coulomb-truncation strings with the baseline's open terms, each defined in a note drafted in this PR
   (judgment calls); response-basis-size an int leaf, q-points int [3] (dimensionless, minimum 1); the "either
   ... but not both" notes kept (0011 item 3); legacy_* deleted; examples/mbpt.json corrected from the source
   dataset (Materials Cloud 2023.92, Yambo input ppa_48kp.in): the cutoff is NGsBlkXp 12 Ry (the baseline's
   60.0 was the wavefunction cutoff, ecutwfc 60 Ry), q-points [48, 48, 1], frequency Godby-Needs (Yambo's
   ppa), response-basis-size 200 (BndsRnXp); test in tests/test_computations.py; 05-mbpt regenerated.
   Reviewer feedback 2026-11-17, answered: the cutoff's recommended unit stays eV (0001 A5, decided); codes
   differ (Yambo Ry, ABINIT ecuteps Ha, VASP ENCUTGW eV), and an instance gives its own unit. Decided by the
   human 2026-11-17: planewave-basis-cutoff's description drops "This is the same as the kinetic energy
   cutoff" and says it is set separately from, and usually lower than, the wavefunction cutoff (dft
   kinetic-energy-cutoff); 0001's B2 note ("should agree with it") is declined.
   Reviewer feedback 2026-11-17: add "Brunelva-Gonze" to coulomb-truncation. Held by the human 2026-11-17:
   no such truncation was found; the name is Yambo's GW terminator (GTermKind "BG", Bruneval-Gonze), the
   extrapolar approximation of F. Bruneval and X. Gonze, Phys. Rev. B 78, 085125 (2008), which reduces the
   number of empty states, as the source dataset's input uses it. Not a coulomb-truncation term (decided by
   the human 2026-11-17): a truncation and a terminator are separate choices, set together in that input
   (CUTGeo "box z" with GTermKind "BG"). Decided by the human 2026-11-17: the term's home is decided in the
   gw-bands PR. PROPOSED, NOT DECIDED (for that PR): an optional string `band-terminator`, open terms None
   and Bruneval-Gonze, its definition citing Bruneval and Gonze (2008), placed beside the band counts it
   corrects (response-basis-size for the polarization sum, Yambo XTermKind; gw-bands or the self-energy band
   range, Yambo GTermKind); confirm the reading with the reviewer. (Superseded: decided by 0071.)
   Self-energy bands by 0071 (ruling 2026-11-17, from reviewer feedback: codes give the corrected bands as a
   range, e.g. 35 to 70, and sum different numbers of bands for W and G, e.g. 500 and 600): mbpt gw-bands is
   replaced by an optional container `self-energy` (note "Give it when `type` is GW or GW/BSE.") holding
   band-range (int [2], first and last corrected band, counted from 1 at the lowest band in the
   calculation), number-of-bands (renamed from number-bands by the 0071 amendment; the bands in the self-energy's sum over states; band-range's last band does
   not exceed it) and band-terminator (open terms None, Bruneval-Gonze, the extrapolar approximation of
   Bruneval and Gonze 2008); dielectric-matrix gains the same band-terminator after response-basis-size,
   which already holds the polarizability's count; the sums stay counts, not ranges; Bruneval-Gonze is
   not a coulomb-truncation term. No released instance breaks. PROPOSED, NOT DECIDED (0071): whether the
   step 9 validator checks band-range against number-of-bands.
   [done, PR #115 merged 2026-11-17] mbpt self-energy by 0071 (step 5,
   in place of gw-bands): schema/mbpt.yaml (self-energy container after dielectric-matrix; band-terminator in
   dielectric-matrix after response-basis-size; gw-bands and its legacy_* deleted); examples/mbpt.json gives
   band-range [3, 4] (QPkrange), number-of-bands 200 (GbndRnge) and band-terminator Bruneval-Gonze (GTermKind
   "BG"), from Yambo input ppa_48kp.in of Materials Cloud 2023.92; tests/test_computations.py (a new test;
   two name lists updated); 05-mbpt regenerated.
   Decided in review 2026-11-17 (0071 amendment): number-bands renamed number-of-bands, its description "the
   sum runs over bands 1 to number-of-bands", band numbering stated once in band-range; band-terminator's
   note names the extrapolar approximation without a citation, as no other term cites a paper.
   [done, PR #116 merged 2026-11-17] mbpt bse-hamiltonian (step 5):
   typed fields filled by the rulings below and 0072, legacy_* deleted, the container noted "Give it when
   `type` is BSE or GW/BSE.", k-point-mesh read against minimal conditions › cell (0059), exciton-multiplicity
   and diagonalization terms defined in notes drafted in this PR (judgment calls); test in
   tests/test_computations.py; 05-mbpt regenerated. Next: bse-kernel-truncation, then mbpt is complete. Cross-check
   2026-11-17: names, definitions, terms and repeatable match the .docx; exciton-momentum's Values text was
   changed by 0001 B3 (step 4, intended); the description lacks its final period (as in the .docx); the
   source dataset (Materials Cloud 2023.92) has no BSE input, so examples/mbpt.json stays GW only. Decided
   by the human 2026-11-17: number-valence-bands and number-conduction-bands stay counts from the valence
   band top and the conduction band bottom, "corrected" becoming "included"; diagonalization keeps
   Tamm-Dancoff and Full diagonalization, defined in a note as the approximation (coupling block dropped or
   kept), the solver not recorded.
   Exciton momentum by 0072 (ruling 2026-11-17, amending 0001 A5): exciton-momentum is a float [3]
   dimensionless leaf, no unit, in fractions of the reciprocal lattice vectors of minimal conditions ›
   cell (as k-point-mesh, 0059); a note gives Q = Q₁b₁ + Q₂b₂ + Q₃b₃, [0, 0, 0] the optical limit, and
   that it is the exciton's momentum, not a code's input shift (BerkeleyGW's exciton_Q_shift is −Q). A5's
   basis, unit and 2π convention are declined, so no conditional rule is needed yet. No released
   instance breaks.
   [done, PR #117 merged 2026-11-17] mbpt bse-kernel-truncation
   (step 5): cross-check 2026-11-17, description and terms match the .docx; a string with dielectric-matrix ›
   coulomb-truncation's terms and definitions (Ismail-Beigi, Rozzi, Spencer-Alavi), locked equal by a test, and
   the note "Give it when `type` is BSE or GW/BSE." (judgment call); legacy_* deleted; mbpt is complete and
   declares `legacy_complete: true`; tests/test_build_docs.py's --show-legacy check moves from mbpt to ml;
   05-mbpt regenerated; examples/mbpt.json unchanged. Next: ml.
   ml, analysed 2026-11-18 before any ml PR. Cross-check against the .docx: names, definitions, values
   text and required marks match (only curly apostrophes differ). ml is not yet in `settings` (0046 item 7).
   Reviewer feedback 2026-11-18: (1) ml-task › type: is an MLIP "Property prediction", and should a smooth
   E(positions) be told apart from arbitrary property maps (e.g. Tc from composition)? (2) training-data
   holds the train/validation/test split (dataset-split); can the three subsets be given explicitly?
   (3) training-method › training-procedure: does it mean the loss, or should the loss be its own property?
   (4) training-hyperparameters: use subproperties; overlap with model-architecture (layers, nodes)?
   (5) model-performance › validation: validation is for hyperparameter tuning, testing assesses the model.
   The human also asked for an analysis of the whole ml schema. PROPOSED, NOT DECIDED (recommendations,
   for a ruling 0073): (a) a structure PR as for mbpt (PR #111): ml's properties in `settings` with
   computation-label, the introduction gains 0054's sentence; (b) an MLIP's training is an ML computation
   (task Training) and the trained potential's evaluations a PIM computation (theory-level Machine-learned)
   naming it as input role Parameters; 0046 does not say which method the training computation has;
   (c) ml-task › type gains "Interatomic potential" (energy of a configuration of particles as a function
   of their positions, forces as its gradient), told apart from "Property prediction" (a property of a
   material or structure); ml-task becomes non-repeatable, as type already repeats; type's definitions
   written in a note; the example's type corrected to Structure generation (WyFormer generates de novo);
   (d) training-data entries gain a required `subset` (terms Training, Validation, Test) with their own
   size, so the three subsets are given explicitly; the property renamed `data` or kept; dataset-split
   keeps how the split was made (random, stratified, by composition, k-fold); source used only for data
   outside the record, data in the record being an input with role Training data (0046's open point);
   (e) training-method gains `loss-function` (string: the quantities fitted and their weights, e.g.
   energies, forces and stresses); training-procedure is the optimization procedure (e.g. Adam, L-BFGS,
   closed-form least squares) and, by 0065 item 5, an active-learning selection criterion;
   (f) training-hyperparameters becomes a repeatable generic parameter (0016; as 0001 A6 suggested),
   for training settings only (learning rate, batch size, epochs, early stopping); model-architecture
   keeps the architecture (layers, nodes, cutoff radius, body order) and gains an optional repeatable
   generic parameter `architecture-parameter`, so a cutoff radius carries a unit; notes point each to the
   other; (g) model-performance › validation is replaced by `evaluation-method` (hold-out test set,
   k-fold cross-validation) and a repeatable `metric` (subset Validation/Test/Training, quantity, measure
   MAE/RMSE/R²/..., value and unit of kind any); (h) smaller: model-size an int number of trainable
   parameters; training-data size an int, contents saying what an item is; transfer-learning names a
   pretrained model as software or as input role Parameters; algorithm stays a free string. (Superseded:
   decided by 0073.)
   The human's answers 2026-11-18: (1) MLIPs belong to pim: MatCore documents the methods that generate a
   dataset, and an MLIP is an ingredient, not an end; not every ml-task term may be relevant (Superseded:
   (b) and (c)'s Interatomic potential). (2) A split is usually made at training time by percentages;
   dataset-split stays a description in words, the structured subsets being overly specific (Superseded:
   (d)'s subset). (3) Write out the proposed training-method schema. (4) Hyperparameters as generic
   parameters need a description of the overall process that refers to them and explains their role, as
   elsewhere (ps settings › description, 0067). (5) (g) accepted. The analysis should judge the section as
   a whole: does it document ML methods that generate datasets?
   Revised proposal, PROPOSED, NOT DECIDED (for 0073): the baseline is a model card (how a model was built)
   and has nothing on how the data were produced from the model. Two ML computations: training (task
   Training) and inference (Structure generation, Property calculation, ...), the inference naming the
   training as input role Parameters, or a model trained elsewhere given as software. settings ›
   computation-label*, ml-task* (type* the kind of result: Property prediction, Structure generation (with
   structure prediction merged in), Synthesis prediction, Ranking, Clustering, Embedding; description),
   ml-model* (algorithm*, target-variable*, input-feature, model-architecture, architecture-parameter
   generic, model-size int), training-data (as baseline, dataset-split in words), training-method
   (training-procedure* describing the process and the role of each hyperparameter, loss-function,
   hyperparameter generic, transfer-learning), a new `inference` (input-data, conditioning,
   sampling-procedure, inference-parameter generic, number-generated, filtering), model-performance
   (evaluation-method*, metric repeatable with subset, quantity, measure, value, unit; uncertainty-
   quantification, saying whether per-item uncertainties are in the dataset; a new applicability-domain),
   interpretability-method. Open with it: how an MLIP's fit is recorded in pim, which has no training
   properties; a software role for a trained model. (Superseded: decided by 0073.)
   Raised by the human 2026-11-19: training-data and training-method inside ml-model, since they say how
   the model was built. Recommended in reply, PROPOSED, NOT DECIDED: yes, and model-performance with them,
   since test metrics describe the model; ml-model then holds what the model is, how it was built and how
   good it is, and inference how the dataset was produced from it. Checks on a generated set (validity,
   uniqueness, novelty) go in inference › filtering, as they describe the output, not the model.
   (Superseded: decided by 0073.)
   ML section by 0073 (ruling 2026-11-19, from the review of 2026-11-18): the section documents how a
   dataset is produced from a model, not only the model; an MLIP is pim, not ml. ML work is a training
   computation and an inference computation (both method ML), the inference naming the training as input
   role Parameters or a model trained elsewhere as software. settings › computation-label*; ml-task* not
   repeatable, type* terms Property prediction, Structure generation (structure prediction merged in),
   Synthesis prediction, Ranking, Clustering, Embedding, defined in a note that sends MLIPs to pim;
   ml-model* holds algorithm*, target-variable*, input-feature, model-architecture (explaining the new
   generic architecture-parameter), model-size (int, trainable parameters), then training-data
   (dataset-split in words; source only for data outside the record), training-method
   (training-procedure* explaining the new generic hyperparameter, which replaces
   training-hyperparameters and settles 0001 A6 for ML; new loss-function; transfer-learning) and
   model-performance (evaluation-method* replaces validation; new metric: subset*, quantity*, measure*,
   value* kind any, unit*; uncertainty-quantification says whether per-item uncertainties are in the
   dataset; new applicability-domain); a new inference after ml-model (input-data, conditioning,
   sampling-procedure explaining the generic inference-parameter, number-generated, filtering, which
   holds the checks on a generated set); interpretability-method stays in settings. Applied in a
   structure PR (settings, moves, renames, introduction; examples/ml.json in settings with type
   Structure generation) and then the step 5 property PRs in file order, each adding its new members.
   No released instance breaks. PROPOSED, NOT DECIDED (0073): how pim records an MLIP's fit; a minimal
   software role for a trained model; whether interpretability-method belongs inside ml-model
   (Superseded: decided by the 0073 amendment).
   [done, PR #118 merged 2026-11-19] ml structure by 0073, no typed
   field filled: ml's properties in a required, repeatable `settings` whose first member is
   computation-label; ml-task not repeatable; training-data, training-method and model-performance moved
   unchanged into ml-model after model-size; training-hyperparameters renamed hyperparameter and validation
   renamed evaluation-method (legacy text kept); interpretability-method last in settings; the introduction
   gains 0054's sentence; examples/ml.json in settings with label wyformer-generation, ml-task an object,
   type Structure generation, training-data inside ml-model; tests/test_computations.py (a new test; the
   label test gains ml); 06-ml regenerated (addresses gain `settings.` and `ml-model.`). The new members
   (architecture-parameter, loss-function, metric, applicability-domain, inference) come in the property PRs.
   Then ml's properties in file order: ml-task, ml-model (perhaps one PR per member), inference,
   interpretability-method.
   [done, PR #119 merged 2026-11-19] ml ml-task (step 5) by 0073 item 2: type a
   string with open terms Property prediction, Structure generation, Synthesis prediction, Ranking,
   Clustering, Embedding, each defined in a note drafted in this PR (judgment calls; Structure generation
   includes crystal structure prediction for a given composition); a second note sends machine-learned
   interatomic potentials to pim; the baseline's repeat note and both descriptions kept; description a
   string; legacy_* deleted; test in tests/test_computations.py; 06-ml regenerated; examples/ml.json
   unchanged (already Structure generation).
   Decided by the human 2026-11-19: ml-model is filled in four PRs, not one: (1) the model's own members
   with architecture-parameter, (2) training-data, (3) training-method with loss-function and hyperparameter,
   (4) model-performance with metric and applicability-domain.
   [done, PR #120 merged 2026-11-19] ml ml-model, part 1 (step 5, 0073 item 3):
   the container keeps its description and gains a note that an inference computation whose model is
   trained in the record gives only algorithm and target-variable; algorithm a string, examples Neural
   network, Random forest, Gaussian process (from the baseline's text); target-variable and input-feature
   repeatable strings, input-feature's guidance as a note; model-architecture a string whose note asks it to
   explain each architecture-parameter entry; a new architecture-parameter, a generic parameter (0016;
   e.g. layers, nodes, cutoff radius, body order; training settings point to hyperparameter); model-size an
   int, "The number of trainable parameters of the machine learning model.", minimum 1; legacy_* of these
   deleted; tests/test_computations.py (a new test; the structure test's list gains architecture-parameter);
   06-ml regenerated; examples/ml.json unchanged.
   [done, PR #121 merged 2026-11-19] ml ml-model, part 2 (step 5, 0073
   item 4): training-data's nine members filled, baseline descriptions kept; strings except size, an int
   (dimensionless, minimum 1; judgment call, 0073 does not state it) whose note says contents names the
   item; notes drafted from the baseline's Values text for contents (what one item is), source (data in
   the record is an input with role Training data, not given here), missing-data and dataset-split (in
   words, e.g. random 80/10/10, stratified, k-fold); legacy_* deleted; examples/ml.json size 45231, its
   text moved into contents; test in tests/test_computations.py; 06-ml regenerated.
   [done, PR #122 merged 2026-11-19] ml ml-model, part 3 (step 5,
   0073 item 5): training-method's members in the order training-procedure*, loss-function (new),
   hyperparameter, transfer-learning; training-procedure a string whose note lists the optimizer,
   schedule, stopping rule and an active-learning loop with its selection criterion (0065 item 5) and asks
   for the role of each hyperparameter entry; loss-function a string, "The quantities fitted in training
   and how they are weighted." (example energies, forces, stresses 1:100:10); hyperparameter a repeatable
   generic parameter (0016; learning rate, batch size, epochs, early-stopping patience; architecture numbers
   point to architecture-parameter); transfer-learning a string, the baseline's examples as a note;
   legacy_* deleted; tests/test_computations.py (a new test; the structure test's list gains
   loss-function); 06-ml regenerated; examples/ml.json unchanged (its source gives no training settings).
   [done, PR #123 merged 2026-11-19] ml ml-model, part 4 (step 5,
   0073 item 6): evaluation-method* a repeatable string (as validation was), its note telling validation
   (tuning, stopping) from testing; a new repeatable metric of subset* (terms Training, Validation, Test,
   defined), quantity* (examples Formation energy, Forces), measure* (terms MAE, RMSE, R², Accuracy,
   defined), value* (float, kind any) and unit* (the generic unit, as the dft SCF tolerance); uncertainty-
   quantification a string whose note asks whether per-item uncertainties are in the dataset; a new
   applicability-domain string; legacy_* deleted; tests/test_computations.py (a new test; the structure
   test's list gains metric and applicability-domain); 06-ml regenerated; examples/ml.json unchanged.
   Judgment calls: Accuracy added for classifiers; R² written with a superscript; evaluation-method stays
   repeatable. Then interpretability-method, and inference, complete ml.
   [done, PR #124 merged 2026-11-19] ml inference (step 5, 0073 item 7): a
   new optional container after ml-model, its note "Give it for a computation that applies a trained
   model"; input-data (data in the record is an input, e.g. role Source data), conditioning,
   sampling-procedure (explains each inference-parameter entry) and filtering (with the checks on a
   generated set: valid, unique, novel) strings; inference-parameter a generic parameter (0016);
   number-generated an int, "The number of outputs of the machine learning model kept in the dataset.", a
   number drawn before filtering stated in filtering (judgment call: kept, not drawn); all descriptions and
   notes drafted in this PR; examples/ml.json gains number-generated 10000 and filtering "Only formally valid
   Wyckoff representations are kept.", from the deposit's README ("10k formally valid Wyckoff
   representations generated by WyFormer trained on MP-20", read through the figshare API, 2026-11-19);
   tests/test_computations.py (a new test; the structure test's list gains inference); 06-ml regenerated.
   Also found in that README, for a later PR: WyFormer was trained on MP-20's train and validation parts
   only; its Wyckoff representations were turned into structures by DiffCSP++ (9999 of 10,000), then
   relaxed by CHGNet and DFT, each a further computation.
   0073 amended 2026-11-19 (decided by the human): interpretability-method moves inside ml-model, after
   model-performance, since it explains the model, not how the dataset was produced; settings holds
   computation-label, ml-task, ml-model and inference. Applied in the interpretability-method PR, which
   also declares ml complete.
   [done, PR #125 merged 2026-11-19] ml interpretability-method
   (step 5, 0073 amendment): moved inside ml-model after model-performance; a string whose note gives the
   baseline's guidance (approach and results; feature importance, global surrogate models, LIME, SHAP,
   saliency maps); legacy_* deleted; ml is complete and declares `legacy_complete: true`;
   tests/test_computations.py (a new test; the structure test's lists updated); tests/test_build_docs.py's
   --show-legacy check and tests/test_schema.py's legacy_complete check move from ml to pf, which still holds
   legacy text; 06-ml regenerated; examples/ml.json unchanged. Next: pf.
   pf cross-check 2026-11-19 against the .docx: names, definitions, values text, required and repeatable
   match; the differences are intended (free-energy › unit's definition by 0001 B11/A7.3; Δx and Δt restored
   in the accuracy orders, lost as equation objects in the export).
   PF section by 0074 (ruling 2026-11-19, from review): pf in `settings` with computation-label;
   physical-phenomena renamed physical-phenomenon, gaining Fracture and Plasticity; time-dependence loses
   Property prediction; free-energy renamed free-energy-density and repeatable (one entry per term);
   governing-equation › type repeatable, Fluid renamed Navier-Stokes, Multi renamed Multi-phase-field, Coupled
   and Diffuse removed, Mechanical equilibrium and Poisson added (solved within the one PF computation),
   evolved-variable "The name of the field-variable being evolved by this equation.", driving-energy renamed
   free-energy-density-term; anti-trapping and sharp- or thin-interface given as user-specified types; no
   property for a TDB file; domain-and-mesh renamed domain, mesh-type moved to numerical-method; domain-size
   noted as a characteristic size for irregular geometries; boundary-conditions NoFlux becomes Zero-Neumann,
   the boundaries given in a new numerical-method › mesh-file (0056's full file form); initial-conditions
   from an algorithm or a distribution are user-specified; numerical-method gains a generic
   spatial-discretization-parameter and an optional repeatable evolved-variable naming the equations an entry
   solves (one entry per group solved differently); temporal-discretization loses Implicit and Explicit; solver
   gains Explicit and further solvers; field-variable documents one entry per field (e.g. per component).
   Applied in a structure PR, then the property PRs in file order. PROPOSED, NOT DECIDED (0074): the further
   solver terms; free-energy-density › unit dropping "or of the free energy"; temporal-discretization's Mixed and
   the spelling Crank-Nicolson; how a boundary condition names its boundary, and Fixed vs Dirichlet, Free vs
   Zero-Neumann; time-dependence vs minimal conditions › type (0036). (Superseded: the unit and time-dependence points are
   settled by the 0074 amendment of 2026-11-20; the boundary points by
   0075; the solver terms, Mixed and the spelling by the second amendment of 2026-11-20.)
   Ruling 0074 committed on main (e394bf7). [done, PR #126 merged 2026-11-19]
   pf structure by 0074, no typed field filled: pf's properties in a required, repeatable `settings` whose
   first member is computation-label; physical-phenomena renamed physical-phenomenon, free-energy renamed
   free-energy-density and repeatable, driving-energy renamed free-energy-density-term, governing-equation ›
   type repeatable, domain-and-mesh renamed domain, mesh-type moved into numerical-method after
   spatial-accuracy-order (legacy text kept); the introduction gains 0054's sentence; examples/pf.json in
   settings with label nucleation under the new names, type and free-energy-density as lists;
   tests/test_computations.py (a new test; the label test gains pf); 07-pf regenerated (addresses gain
   `settings.`). Then pf's properties in file order: physical-phenomenon, problem-specification, domain,
   numerical-method, variables.
   [done, PR #127 merged 2026-11-20] pf physical-phenomenon (step 5,
   0074 item 2): a repeatable string with open terms the baseline's seven plus Fracture and Plasticity, each
   defined in a note drafted in this PR (judgment calls); a note "Give one entry for each process modeled.";
   baseline description kept; legacy_* deleted; test in tests/test_computations.py; 07-pf regenerated;
   examples/pf.json unchanged (its "Homogeneous nucleation (single seed)" is a user-specified value).
   PROPOSED, NOT DECIDED: a term Nucleation, since the section's own example models it.
   0074 amended 2026-11-20 (decided by the human, from the problem-specification cross-check): free-energy-density ›
   unit drops 0001 A7.3's parenthesis ("The physical unit of the free energy density.", the .docx wording) and
   expression becomes "The mathematical expression of the free energy density."; problem-specification ›
   time-dependence is removed, since it repeats minimal conditions › type › thermodynamic-state (0036, 0042 item 3),
   its term Stationary becoming a note on temporal-discretization to omit it for a problem solved without time
   integration (in the numerical-method PR), and "time-evolution state" leaves problem-specification's description
   and the introduction; additional-energy-contribution is removed and free-energy-density gains an optional
   `contribution` after name (open terms Chemical, Interfacial, Elastic, Plastic, Electrical, Magnetic, Fluid-solid
   interaction, Solid-solid interaction). No released instance breaks. Amendment committed on main (fef95d8).
   PF domain by 0075 (ruling 2026-11-20, from the domain cross-check): 0003's `scaling` is dropped, a reduced length
   or time having unit `dimensionless` and its characteristic scale a model-parameter, noted on domain-size,
   grid-spacing and time-step-size (value + unit, Length or Time, m or s); boundary-conditions becomes a repeatable
   container of type* (Dirichlet, Neumann, Zero-Neumann, Periodic, defined; Fixed and Free removed), boundary (a
   boundary in mesh-file or a description such as "x = 0") and field-variable (the field constrained), boundary and
   field-variable omitted when the condition applies to all. Settles 0074's boundary points and the §1.3 conditional
   rule for `scaling`. No released instance breaks. Ruling committed on main (4ad61a8).
   0074's second amendment 2026-11-20 (decided by the human, from the numerical-method cross-check): solver gets open
   terms Explicit, Direct, Conjugate gradient, BiCGSTAB, GMRES, Multigrid, Newton, Newton-Krylov, Picard, defined, with
   a note asking for one entry per layer and naming the providing library as software; temporal-discretization's Mixed
   becomes IMEX and the spellings are Crank-Nicolson and Adams-Bashforth; mesh-type loses Cartesian (overlapping
   Regular, Rectilinear and the coordinate-system term) and writes Adaptive mesh refinement. Amendment
   committed on main (683d561). Found in the source
   (benchmark8a.py at abffcd9) for that PR: dx = dy = 0.4, dt = 0.01, a FiPy TransientTerm with implicit diffusion and
   five sweeps per step (first order, i.e. Backward Euler).
   [done, PR #130 merged 2026-11-20] pf numerical-method (step 5, 0074 item 5
   and second amendment, 0075): cross-check 2026-11-20, names, definitions and terms match the .docx (Δx and Δt
   restored, lost as equation objects); members in the order evolved-variable (new, repeatable, path note, given when
   equations are solved differently), spatial-discretization (six terms defined), spatial-discretization-parameter
   (new, generic, 0016), spatial-accuracy-order and temporal-accuracy-order (int, dimensionless, minimum 1), mesh-type
   (seven terms defined), mesh-file (new; minimal computation › software › file's members verbatim, 0056; a note on
   when to give it and that boundary-conditions › boundary names its boundaries), temporal-discretization (six terms
   defined; note omitting it for a stationary problem), grid-spacing and time-step-size (name with the baseline's
   examples, value float Length m / Time s minimum 0, unit, description; reduced-unit note, 0075), solver (nine terms
   defined, one entry per layer, the library as software); grid-spacing's description drops "physical"; solver's
   description "A numerical algorithm used to solve the discretized equations." (was "algorithm or backend");
   legacy_* deleted; examples/pf.json from the source: Backward Euler (was Implicit), grid spacing 0.4 (was 1.0),
   accuracy orders and step values as numbers, solver Picard (the five sweeps) before FiPy Default Linear Solver;
   tests/test_computations.py (a new test, the structure test's numerical-method list, a module-level no_legacy helper
   replacing two copies); 07-pf regenerated. Judgment calls: all definitions, member order, the example's Picard.
   Decided by the human 2026-11-20, after PR #130: numerical-method › mesh-file is repeatable, since a mesh may be
   split over several files (e.g. its structure and its boundaries); its description says "A file holding the mesh or
   part of it" and a note asks for one entry per file. [done, PR #131 merged 2026-11-20]
   schema/pf.yaml, tests/test_computations.py, 07-pf regenerated; examples/pf.json unchanged (no
   mesh file).
   [done, PR #132 merged 2026-11-20] pf variables (step 5, 0016, 0074 item 6):
   cross-check 2026-11-20, names, definitions and terms match the .docx (Tables PF-1, PF-6, PF-7); model-parameter a
   generic parameter (0016), its note giving kappa, W and mobility and the characteristic length and time of reduced
   units (0075); field-variable noted one entry per field (0074 item 6), name with examples phi, c, T and a note naming
   the three properties that refer to it by name, type Scalar, Vector, Tensor defined, unit a free-form unit with
   A3.2's note ("The unit in which the field variable is expressed."), description with the baseline's examples;
   legacy_* deleted; pf is complete and declares `legacy_complete: true`; tests/test_schema.py's legacy_complete check
   and tests/test_build_docs.py's --show-legacy check move from pf to derived. Decided by the human 2026-11-20: 0044
   item 3 is implemented in scripts/check_examples.py (a generic parameter's JSON object requires `type`, float, int,
   string or bool, and its value or each component has that type; the member is rejected elsewhere), tested in
   tests/test_examples.py; examples/pf.json's model parameters are numbers with "type": "float" (Δf = 1/(15√2) checked
   against benchmark8a.py; r_0 = 5.05 is factor × 5 with the factor passed on the command line, not in the repository);
   tests/test_computations.py (a new test); 07-pf regenerated. Next: derived.
   derived, analysed 2026-11-20 before any derived PR, at the human's request (is the section still sound now that
   a dataset may combine methods?). Cross-check against the .docx: names, definitions, values text, required and
   repeatable match. Findings: (1) derived is the only section not in `settings`: its properties name no computation,
   so a derived property cannot say which computation obtained it or from what; (2) its introduction limits it to a
   single method, which 0046's input links make unnecessary: a property from several computations is a computation
   with task Property calculation naming them as input role Source data (or Interaction model, 0067); (3) a
   post-processing step with no physical model of its own (force constants from finite-difference forces, a Raman
   tensor from susceptibilities, an XRD pattern from a structure, a vibrational DOS from a trajectory) has no
   `method` term, though `method` is required: the open point of 0065 on computations with no method term; (4)
   calculation-method repeats to chain steps, which 0046 now gives as computations; (5) type's terms mix kinds of
   quantity (Electronic, Magnetic, Transport) with techniques (Linear-response, NMR, Microscopy) and lack Mechanical
   (elastic constants) and Thermodynamic (free energies, heat capacities, formation energies); description holds both
   the property's name and its explanation. PROPOSED, NOT DECIDED (recommendations, for a ruling): (a) derived's
   properties sit in `settings` with computation-label, as in every method section; a derived block may name any
   computation that obtains a property (e.g. a DFT computation by DFPT, a PS computation giving a Green-Kubo
   conductivity), beside that computation's method block; (b) the single-method note and the MBPT exception are
   removed, the introduction saying that combinations are input links; (c) `method` gains a term for a computation
   that derives a property with no model of its own, naming the derived section (name and method-class to decide;
   MODA's post-processing step to be checked as a source), closing 0065's open point for such computations; (d)
   derived-property gains `name*` (e.g. Raman spectrum, phonon dispersion), description an explanation; (e)
   calculation-method is flattened: `procedure*` (a string explaining each calculation-parameter entry, as ps settings
   › description, 0067) and the generic `calculation-parameter` sit in derived-property; (f) type is reworded as the
   kind of property, Linear-response replaced by Vibrational, Mechanical and Thermodynamic added (terms to settle in
   the property PR); (g) examples/derived.json names a Raman computation. No change proposed to how results are
   listed (0039's open question). (Superseded: decided by 0076.)
   Derived section by 0076 (ruling 2026-11-21, from the analysis above; the human chose each recommendation):
   derived's properties sit in `settings` with computation-label, a derived block naming any computation that obtains a
   property; the single-method note and the MBPT exception are removed, the introduction pointing to input roles
   Source data and Interaction model; minimal method-class gains Post-processing (CWA 17284:2018 §3.12, checked in
   the CWA's text 2026-11-21: "operations on raw output of solvers without altering the physical system state") and
   method gains "DP" – Derived Property under it, naming the derived section; derived-property's members are type*,
   name* (new), description*, procedure* (replacing calculation-method, explaining each parameter) and the generic
   calculation-parameter; type is the kind of property, Linear-response replaced by Vibrational, Mechanical and
   Thermodynamic added; a margin-of-error property (CWA Table 7 item 4.3) is declined (0039). Settles 0065's open point
   for post-processing computations. No released instance breaks. Ruling committed on main (cd80617).
   [done, PR #133 merged 2026-11-22] derived structure by 0076, no typed field
   filled: derived's properties in a required, repeatable `settings` whose first member is computation-label;
   derived-property inside it, its calculation-method removed, the method's description moved up as `procedure`
   (required) and calculation-parameter moved up (legacy text kept for both); the introduction rewritten without the
   single-method note and the MBPT exception, naming input roles Source data and Interaction model, method DP and
   0054's settings sentence, its list of examples unchanged until the type PR; MatCore-Der becomes MatCore-DP and §1.2's
   "DER:" becomes "DP:" (judgment call: the section's abbreviation follows its method term, as DFT, PS, PF do);
   minimal method-class gains Post-processing, its note saying the other categories come from MODA and
   Post-processing from CWA 17284:2018 §3.12; method gains case Post-processing → DP, defined at the end of method's
   note; examples/derived.json in settings, label raman, calculation-method's text as procedure;
   tests/test_computations.py (two new tests; the method test and the label test updated); 02-minimal, 08-derived and
   index regenerated. Then derived's property PRs: derived-property (type with its terms, name, description,
   procedure, calculation-parameter), one PR or several as the human decides.
   Changed in review 2026-11-21 (the human): the title is "2.8 Derived Property (DP) Metadata", as every method
   section names its abbreviation; the introduction is rewritten for clarity: what a derived property is (a Raman
   spectrum from DFT phonons and susceptibilities), the two kinds of computation that obtain one (method DP with
   method-class Post-processing, set in minimal `computation`; or another method's computation with a block in both
   sections), and the input roles in plain terms (Source data for results already computed, Interaction model for
   energies and forces requested as it proceeds), a multi-step or multi-method property being a chain of
   computations; its list of examples applies 0076 item 5 now: Linear-response becomes Vibrational, Mechanical and
   Thermodynamic are added, the list kept alphabetical. Tests check the title and the three families.
   Raised by the human 2026-11-22, on a worked Raman example (six computations: a DFT relaxation, DFT forces on
   displaced cells, a DP phonon computation, DFT susceptibilities, a DP Raman computation, each DP one with its own
   derived block): is this too detailed for MatCore, which explains a dataset and does not give its workflow (§1.2),
   and what do the derived blocks add beyond minimal computations of the same name? Answer given: the schema does not
   require that granularity; the example (and the draft introduction's sentence "recorded as a chain of
   computations, one for each step") chose it. Minimal says how each computation works and what it used (method,
   task, input, software); the derived block says what property came out and how it was obtained (type, name,
   procedure, parameters), as a dft block holds a DFT computation's settings; the duplication in the example came
   from splitting one post-processing into two DP computations and from computation › description restating the
   procedure. PROPOSED, NOT DECIDED: (a) the derived introduction replaces "one for each step" with guidance to
   group: a computation is separate only where its method differs or its results are in the dataset; post-processing
   steps that share one procedure are one DP computation, its properties being entries of one derived block; (b) the
   same guidance for every section as a note on minimal `computation`, beside 0063's staged-simulation note; (c) the
   procedure is given in derived, not repeated in computation › description. With (a), the Raman example is two
   computations: dft (DFT, Single point: displaced-cell forces and susceptibilities) and raman (DP, Property
   calculation, input dft as Source data; software phonopy and a script), with one derived block holding the phonon
   modes and the Raman spectrum.
   Decided by the human 2026-11-22 (changed in review, derived-structure): (a) and (c) are adopted in the
   derived introduction, which replaces "one for each step" with a paragraph: the record explains the dataset, not
   its workflow; a computation is separate only when its method differs or its results are in the dataset;
   post-processing steps serving one purpose are one DP computation with one derived-property entry per property;
   how a property was obtained, including the parameters of the calculations its procedure requests from other
   computations (e.g. the finite-difference displacement), is given in the entry's procedure and
   calculation-parameter, as a method's settings are in its section, not in those computations' descriptions. The
   test of derived's structure checks the paragraph. (b), the same grouping guidance as a note on minimal
   `computation` for every section, remains PROPOSED, NOT DECIDED.
   Decided by the human 2026-11-22, after PR #133: the derived introduction is shortened to reflect the simplified
   structure: a definition (with the Raman example), then the usual record in one paragraph: one minimal computation
   of method DP (method-class Post-processing) naming its sources in `input` (Source data, or Interaction model), its
   block giving one derived-property entry per property with procedure and calculation-parameter (e.g. the
   finite-difference displacement), and a property obtained within another method's computation given in a block
   naming that computation; then the list of families. The two-kinds list, the long input-role paragraph and the
   grouping paragraph are dropped, the grouping rule being 0077's note in minimal. [done, PR #134 merged
   2026-11-22] schema/derived.yaml, tests/test_computations.py (the
   introduction's prose is two paragraphs and keeps the essentials), 08-derived regenerated.
   [done, PR #129 merged 2026-11-20] pf domain (step 5, 0074 item 4, 0075): cross-check
   2026-11-20, names, definitions and terms match the .docx apart from 0074's move of mesh-type; the container's
   description drops "topological discretization details" (the mesh is in numerical-method); dimensionality and
   coordinate-system strings with the baseline's terms; domain-size value (float [:], Length, m, minimum 0) + unit, with
   notes on the order of the extents, reduced units (0075) and irregular geometries (0074); boundary-conditions a
   repeatable container of type* (Dirichlet, Neumann, Zero-Neumann, Periodic, defined), boundary and field-variable,
   its description singular; initial-conditions a repeatable string with the baseline's examples and a note on states
   given in words; legacy_* deleted; examples/pf.json domain-size [100.0, 100.0] dimensionless and boundary condition
   Periodic, checked against the source (FiPy benchmark 8a, github.com/guyer/phasefieldbenchmark-8 at abffcd9,
   params8a.yaml Lx = Ly = 100, PeriodicGrid2D); test in tests/test_computations.py; 07-pf regenerated.
   Found for the numerical-method PR: the source's dx is 0.4 (params8a.yaml), the example's grid-spacing 1.0; the
   example's numbers are strings ("1.0"), to be written as numbers.
   Changed in review 2026-11-20 (the human): a note that refers to another property gives its path within the settings
   block, e.g. `variables › field-variable`, `numerical-method › mesh-file`, `variables › model-parameter`, not its
   bare name; applied to boundary, field-variable and domain-size's notes (in PR #129). The same defect is
   in problem-specification's evolved-variable and free-energy-density-term notes (PR #128, merged); fixed in this
   PR too (decided by the human 2026-11-20), with the test of problem-specification checking their paths.
   [done, PR #128 merged 2026-11-20] pf problem-specification (step 5,
   0074 item 3 and amendment): cross-check 2026-11-20, names, definitions and terms match the .docx apart from 0074's
   renames, type made repeatable, and the unit wording; time-dependence and additional-energy-contribution removed,
   "time-evolution state" dropped from the description and the introduction; governing-equation noted one entry per
   equation; type a repeatable string with the nine terms of 0074, each defined in a note drafted in this PR, and a
   note sending anti-trapping and sharp- or thin-interface formulations to user-specified values; evolved-variable and
   free-energy-density-term strings naming a field-variable or free-energy-density entry, the latter's description
   reworded ("A term of the free energy density that drives this equation."); free-energy-density described as one
   term, noted one entry per term; its name a string; a new repeatable contribution with the amendment's terms,
   defined; description's six model terms defined; expression and unit as the amendment says, unit a free-form unit
   with A3.2's note; legacy_* deleted; examples/pf.json loses time-dependence and gives f_total contribution
   Interfacial and Chemical; test in tests/test_computations.py; 07-pf regenerated. Judgment calls: all term
   definitions; contribution repeatable; the example's contribution read from its expression.
   [done, PR #109 merged 2026-11-14] ps initialization: a
   scalar string, values null, the baseline description kept; a note gives what the computation sets
   up itself (velocities from a distribution with a random seed, spins) and points a carried-over
   configuration to input role Initial configuration (0063) and imposed values to conditions (0042
   item 3); legacy_* deleted; test in tests/test_computations.py; ps page regenerated; examples/ps.json
   unchanged.
   Reviewer feedback 2026-11-14 (written before 0046 and 0061; "thermodynamic-integration" read as
   thermodynamic-constraint): one script runs several MD stages with different ensembles, e.g. a
   two-phase melting point (two NPT regions at different temperatures, then NPH for all atoms), so
   the constraint belongs to each computation. Already met by 0046 and 0063: one computation per stage,
   linked by input role Initial configuration, each with its own ps settings block naming it by
   computation-label; thermodynamic-constraint repeats, its `system` naming the region.
   PROPOSED, NOT DECIDED (for the thermodynamic-constraint PR): where each region's temperature goes,
   since 0042 item 3 keeps temperature in minimal `conditions`, which has no field naming a region
   (only conditions › description and spatial-uniformity Nonuniform). (Superseded: decided by 0069:
   conditions › description states it (0035 item 4); no region field, as 0026 declined one.)
   Raised by the human 2026-11-14: the algorithm enforcing a constraint (thermostat, barostat, GCMC)
   and the grouping of individual conditions into an ensemble. In reply: both are still in ps
   thermodynamic-constraint (`type` the ensemble, `method` the algorithm, `td-parameter` its
   parameters), legacy until its PR; 0042 item 3 splits the roles: conditions hold the values, ps the
   ensemble and how it is enforced. PROPOSED, NOT DECIDED (for that PR): `method` repeatable, one entry
   per algorithm (e.g. Nosé-Hoover thermostat with Parrinello-Rahman barostat), its terms depending on
   `type` by 0013 depends-on/cases as in the baseline; the instance validator (step 9) checking that
   the ensemble's fixed quantities are given in conditions (e.g. NVT a temperature, μVT a
   chemical-potential and system-openness Open). (Superseded in part: 0069 makes `method` repeatable
   with one grouped list, Thermostats, Barostats and Particle exchange, without depends-on, since
   Andersen and Berendsen name both a thermostat and a barostat; the validator check stays for step 9.)
   Thermodynamic constraints by 0069 (ruling 2026-11-15): ps thermodynamic-constraint › method
   repeatable, one entry per thermostat, barostat or particle-exchange scheme (not tied to ps
   algorithm), open terms grouped as Thermostats (Andersen thermostat,
   Berendsen thermostat, CSVR, Langevin, Nosé-Hoover, Nosé-Hoover chain, Velocity rescaling), Barostats
   (Andersen barostat, Berendsen barostat, CauchyStat, Nosé-Hoover barostat, Parrinello-Rahman) and
   Particle exchange (GCMC, SGCMC), each defined in a phrase; Monte Carlo acceptance rules stay in
   algorithm; type gains ΔμNPT (semi-grand canonical); a note on type says the ensemble names the
   fixed quantities, whose values are in minimal conditions and not repeated in ps; system a required
   string ("Entire system", a group of atoms, or degrees of freedom such as Drude particles or spins),
   different values on different parts stated in conditions › description (0035 item 4); a region
   field on conditions declined (too detailed; 0026); td-parameter a generic parameter (0016) of
   enforcement parameters only. No released instance breaks. PROPOSED, NOT DECIDED (0069): whether
   the step 9 validator checks type against conditions (fixed quantities present; μ ensembles with
   system-openness Open, 0036). [done, PR #110 merged 2026-11-15] ps thermodynamic-constraint by 0069: system, type, method, description and
   td-parameter filled as the ruling states, method's 14 definitions drafted in this PR (judgment
   calls), type's and td-parameter's notes point to minimal conditions; legacy_* deleted; ps is complete
   and declares `legacy_complete: true`; tests/test_computations.py gains two tests;
   tests/test_build_docs.py's --show-legacy check moves from ps to mbpt, which still holds legacy text;
   ps page regenerated; examples/ps.json unchanged (its source names no thermostat).
   [done, PR #107 merged 2026-11-14] ps
   computation-parameter: the
   generic-parameter form of 0016 (name, value of type/extent/kind any, unit with 0001 B9's
   description and A3.2's note, description), checked by check_generic.py; a note gives the
   baseline's two examples (moved from description's legacy values) with the time step, NEB images
   and 0066 item 4's search settings; legacy_* deleted; test in tests/test_computations.py; ps page
   regenerated; examples/ps.json unchanged. Each
   property follows 0042 item 3: no
   quantity that minimal `conditions` (simulation-conditions before 0046) holds is repeated; md adds only how a condition is enforced
   (thermostat, barostat and their parameters) and the ensemble.
   Method, task and algorithm by 0064 (ruling 2026-11-14): minimal `method` names the method section,
   PS replacing MD, MS, MC and CGMD (cases Atomistic PIM, PS; Mesoscopic DDD, KMC, PIM, PS);
   method-class notes that a PS computation takes its particles' entity; `task` names the goal, with
   Optimization local or global, a new Transition state search (Superseded: renamed Transition path by 0065), and Dynamics and Sampling told apart
   by whether the time evolution is the result; ps `algorithm` a required, repeatable string with
   open terms in eight groups (the baseline's, less PMF, plus the reviewer's, NEB, Metropolis and
   Hybrid Monte Carlo; aMD and GaMD under enhanced sampling); the PS introduction and §1.2 name Monte
   Carlo; a relaxation using another computation's forces is PS with task Optimization (was MS).
   Reverses 0061 item 2; breaks 0.6.0 instances with method MD, MC or CGMD. Two PRs: (a) minimal,
   ps introduction, §1.2, tests; (b) ps algorithm (step 5). PROPOSED, NOT DECIDED (0064): a DFT
   relaxation also described as PS + DFT single point to record its minimizer; KMC and Multiscale
   sections; property layers, term identifiers, what a computation computes.
   [done, PR #102 merged 2026-11-14] 0064 PR (a): minimal method (PS replaces MD,
   MS, MC, CGMD; new description and PS definition), method-class note, task terms by goal with
   Transition state search and a note; ps introduction and §1.2 name Monte Carlo;
   tests/test_computations.py; 02-minimal, ps and index pages regenerated.
   0064 amended 2026-11-14: each definition in method's note is the expansion plus a short phrase
   stating the kind of methods the term covers, naming no methods outside the terms (wording in 0064).
   [done, PR #103 merged 2026-11-14] Applied to schema/minimal.yaml, with
   tests/test_computations.py matching the note exactly and 02-minimal regenerated; before PR (b).
   Task terms by 0065 (ruling 2026-11-14, from the human's feedback on task): Transition state search
   renamed "Transition path" (saddle points, minimum energy paths, reactive trajectory ensembles and
   their rates; Dynamics drops path sampling); "Structure generation" added, in the human's wording
   (creation, modification or enumeration of configurations before energy or force evaluations;
   generative models do not optimize; rattled or strained configurations are generated); "Equilibration"
   added (a state prepared as another computation's Initial configuration, its data not for analysis);
   Training reworded to cover any model fitted to data (force matching, Boltzmann inversion, cluster
   expansions); Active learning and Post-processing declined (a workflow of computations; provenance
   events or Property calculation). Amends 0064 item 3; breaks no released instance. PROPOSED, NOT
   DECIDED (0065): whether Structure generation is a computation only when its configurations are in
   the dataset or another's input; the `method` of a computation with no method term (generation
   without a model, a non-ML fit such as force matching, featurization). (Superseded in part: post-processing
   computations take method DP, by 0076.)
   [done, PR #104 merged 2026-11-14] 0065 applied: minimal task terms and note,
   tests/test_computations.py, 02-minimal regenerated; before 0064 PR (b).
   Structure searches by 0066 (ruling 2026-11-14, from reviewer feedback: a global minimum found by
   sampling inputs and minimizing thousands of structures, with no place for how phase space was
   sampled): a search run by its own driver is one PS computation, task Optimization, naming the
   energy computation (task Single point) as input role Interaction model; the driver's candidates and
   their local relaxations are part of it, the minimizer a second algorithm entry; 0065 item 2's split
   into Structure generation + Optimization applies only when candidates are created apart (a
   generative model, an enumeration), named as Initial configuration; ps algorithm's Global
   optimization group gains Random structure search, Evolutionary algorithm, Particle swarm
   optimization and Minima hopping (amends 0064 item 4, in PR (b)); the search's settings, including
   the local relaxation tolerances, are ps computation-parameter entries; minimal computation gains an
   optional `description` after label; the ranking, energies found and how often the lowest recurred
   are results, left to 0039's open question. Amends 0064 item 4 and 0065 item 2; breaks no released
   instance. PROPOSED, NOT DECIDED (0066): whether a single DFT relaxation may also be PS with a DFT
   Single point. The rest rides on the ps algorithm and computation-parameter PRs.
   [done, PR #105 merged 2026-11-14] 0066 item 5:
   minimal computation › description (optional scalar string) after label;
   tests/test_computations.py; 02-minimal regenerated.
   Algorithm classes by 0067 (ruling 2026-11-14, from reviewer feedback: metadynamics variants,
   Born-matrix elastic constants): ps algorithm terms name major classes only, so Bond-boost and
   Strain-boost hyperdynamics, ART nouveau, GaMD and Transition interface sampling are removed (39
   terms; amends 0064 item 4); ps settings gains an optional `description` after algorithm for the
   variant and other specifics and to explain computation-parameter entries; algorithm's second note
   points to it; a property from derivatives of an interaction model (elastic constants from the Born
   matrix) is task Property calculation naming the PIM or electronic computation as input role
   Interaction model, no schema change. A suggestion to add four metadynamics variant terms was
   declined. Applied in the ps algorithm PR (branch ps-algorithm-0064).
   [done, PR #106 merged 2026-11-14] 0064 PR (b), with 0066
   item 3 and 0067: ps algorithm required, repeatable, 39 open terms in eight groups, each defined in
   values.note as grouped lists (0007 item 5, amended again; build_docs.py renders a multi-line note
   under its own Clarifications paragraph, tested in tests/test_build_docs.py); definitions other than
   0064's Harmonic and 0066's four drafted in this PR, listed as judgment calls; a note asks for one
   entry per procedure and points thermostats to thermodynamic-constraint; a second note, decided in
   review, puts numerical parameters in computation-parameter and the variant in description; ps
   settings › description added (0067); legacy_* deleted; examples/ps.json gives Velocity Verlet (the
   baseline example has no algorithm); tests; ps page regenerated.
   The notes below are its background.
   PROPOSED, NOT DECIDED (ruling 0064, from reviewer feedback on rare-event methods, 2026-11-13):
   ps algorithm repeatable, with open terms grouped in its note by function (time integration, local
   minimization, global optimization, saddle points and paths, accelerated dynamics, enhanced
   sampling and free energy, path sampling); KMC variants left to a future KMC section. Declined by
   the human 2026-11-13: separate `time-scale` and `sampling-bias` properties, since the algorithm
   terms imply them. Open, from the analysis of minimal method-class, method and task against the
   groups: task mixes mechanism (Dynamics, Sampling) with goal (Optimization, Free energy
   calculation, ...), and has no term for saddle-point and path searches; method's MD, MS and CGMD
   repeat what task and method-class say (one term PS was suggested); whether PS describes MC
   (0061); a DFT relaxation's minimizer cannot be recorded (0046 settlement).
   Raised by the human 2026-11-14, PROPOSED, NOT DECIDED: a method section "Multiscale" for spatial
   (QC, hot-QC, bridging scales), temporal (accelerated MD, KMC) and coupled (hyper-QC) methods. Points
   raised in reply: the abbreviation MS is taken by molecular statics; Voter's accelerated MD
   (hyperdynamics, ParRep, TAD) and Hamelberg's aMD share the name; whether accelerated MD stays a ps
   algorithm and KMC gets its own section or both go to Multiscale; QM/MM regions (0046) belong to
   the same question. Also suggested: `method` gets one term per method section, the section then
   describing the specific approach.
   Survey of other standards, 2026-11-14 (for 0064; PROPOSED, NOT DECIDED): MODA (CWA 17284:2018
   §3.10) strictly separates model and solver, and RoMM (2017) files MC and accelerated MD as
   solvers; ASMO (OCDO) keeps ComputationalMethod (MD, MS, MC, KMC, DFT), SimulationAlgorithm and
   the activity apart; QCSchema separates model, driver and procedure (QCPortal has `neb`); NOMAD's
   workflow classes, CML CompChem's task and FAIRmat Area C's feedback (item 4) mix goal and
   procedure or call MD a method. Revised suggestion: keep MD, MS and MC as method terms (solver
   families, all described by ps; withdraws the single term PS); task by goal only, with Transition
   state search; ps algorithm the specific solver; a Multiscale section for coupled models in
   MODA's terms (iterative or tight coupling; one-way linking stays `input`), accelerated MD staying
   a ps algorithm and KMC its own section. (Superseded in part, human's direction 2026-11-14:
   `method` names the method sections: PS replaces MD, MS, MC and CGMD, method-class giving
   Atomistic or Mesoscopic; MD, MS and MC become groups of ps algorithm terms, with a Monte Carlo
   group added; terms without a section (CC, QMC, TB, DDD, KMC) stay. To be drafted as 0064,
   reversing 0061 item 2; breaks 0.6.0 instances.) Departures from the surveyed standards, to state
   in 0064: method-class is given for every computation, a PS computation taking its particles'
   entity (MODA classifies models, not solvers, and would class AIMD by DFT); MD, MS and MC are not
   method terms (ASMO's ComputationalMethod has them); thermostats stay ps settings (RoMM counts them
   as materials relations). PROPOSED, NOT DECIDED, beyond 0064: marking each property's layer (model,
   numerical setting, dataset, provenance, ...), as nomad-simulations' ModelMethod/NumericalSettings
   split and FAIRmat Area C items 2–3 suggest; mapping terms to external identifiers (ASMO, EMMO);
   what a computation computes (QCSchema's driver), which overlaps 0039's open question. Also found: minimal method-class's note calls RoMM (DOI
   10.2777/404734) "the MODA standard", and Data-driven comes from RoMM, not the CWA.
   Reviewer feedback on three levels, checked against 0046 and 0064 on 2026-11-14: (1) energies and
   forces (and charges, spins, electronic properties) of a configuration, (2) an ensemble average or
   optimization using them (MD, MC, minimization), (3) a property combined from several level-2
   results (e.g. stress vs strain giving an elastic constant). 0046 makes them computations linked by
   input roles: level 1 is task Single point in pim or an electronic section, level 2 a PS computation
   naming it as Interaction model, level 3 task Property calculation naming its sources as Source
   data. PROPOSED, NOT DECIDED: the derived introduction still says a derived property rests on a
   single method and combinations of methods (e.g. MD and ML) are not supported, which 0046's input
   links contradict; settled in the derived PR, which 0046 already leaves to decide how a derived
   property names its source. The DFT relaxation (DFT, task Optimization; 0046 settlement, 0066's open
   point) is where levels 1 and 2 still meet in one computation.
6. [todo] Committee decisions and community feedback (user will supply, after step 5):
   one decision record + one PR each.
   A reviewer's written feedback on MatCore-MD v0.3.0 (committee review of 2026-09-23, by email), reviewed 2026-11-22
   against the current schema. Already addressed: stages, ramps and carry-over of state (0063, 0035, 0026); a thermostat
   on a group of atoms (0069 `system`); rare-event and accelerated methods (ps algorithm: hyperdynamics, ParRep, TAD,
   aMD, replica exchange, basin hopping and filling, forward flux and transition path sampling, milestoning, string,
   dimer, ART, eigenvector following, steered and targeted MD; 0064, 0066); variants (bond- and strain-boost, GaMD, TIS,
   ART nouveau, metadynamics variants) in ps settings › description (0067); Born-matrix elastic constants (0067); the
   simulated-annealing schedule (qualified temperature entries, 0035, with computation-parameter and description);
   the μσT gloss (fixed). KMC variants wait for a KMC section (0064). Not addressed: (1) constraints on groups of
   particles (fixed, tethered, restricted to a plane or line, rigid bodies, holonomic constraints such as SHAKE,
   RATTLE or LINCS, centre-of-mass constraints, prescribed motion of a block); (2) flexible (Green's function)
   boundary conditions; (3) applied potentials (walls, indenters, synthetic grain-boundary driving forces); (4) the
   reviewer's point that PF has boundary conditions and PS none; (5) SLLOD / Lees-Edwards shear (not raised as a term,
   but implied).
   Particle constraints by 0082 (ruling 2026-11-22, from that feedback; the human decided each item): ps settings gains
   an optional, repeatable `particle-constraint` after thermodynamic-constraint, "A constraint on, or a potential
   applied to, a group of particles.": system* (words, as thermodynamic-constraint › system; no atom indices or code
   group names), type* with open terms in two groups, motion constraints (Fixed, Tethered, Restricted, Rigid body,
   Holonomic, Centre of mass, Prescribed motion, Flexible boundary) and applied potentials (Wall, Indenter, Driving
   potential), and description (form, variant, and the role of each computation-parameter entry, 0067). No ps
   boundary-conditions property: particle boundaries are minimal conditions › cell-periodicity with particle-constraint
   entries, the counterpart of PF's. SLLOD needs no change (strain-rate with qualified entries; a user-specified
   algorithm term; Lees-Edwards in description). No released record breaks. Ruling committed on main (250b96e).
   [done, PR #143 merged 2026-11-22] 0082: schema/ps.yaml
   (particle-constraint last in settings; a note on one entry per group and on cell-periodicity; system's note on
   words, not atom indices; the eleven term definitions, drafted in this PR (judgment calls); description naming
   computation-parameter), tests/test_computations.py (a new test; the ps settings list gains the member), ps page and
   JSON Schema regenerated; examples/ps.json reviewed, unchanged (no constraint in its source). Rendering checked in
   the browser.
   FAIRmat Area C's written feedback (committee review of 2026-09-23, by email; eight points on semantic scope and
   interoperability with nomad-simulations and PMDCore), reviewed 2026-11-23 against the current schema. Already
   addressed: (4) method vs workflow (method and task, computations linked by input; 0046, 0064, 0065); (5)
   simulation-conditions decomposed into typed conditions, the ensemble and time step in ps, convergence in dft
   (0035-0042, 0069, 0082); (6) open vocabularies for method, task, xc type, basis type, pseudopotential type, k-point
   mesh, smearing and ensemble, an unlisted value kept and reported as user-specified (0013); (7) LibXC normalization
   (0017), DFT+U and dispersion apart from the functional name (0051, review 2026-11-16); (2, in part) "material" split
   into structure › material-component's formula, form, phase and role (0025, 0034); (8, in part) added Properties
   prefixed x- (0079), versioning (0010). Not addressed, PROPOSED, NOT DECIDED (recommendations): (a) point 1, the
   semantic level: §1.1 or §1.2 states that MatCore is a reporting standard for datasets, not an ontology, and is
   aligned with ontologies and richer schemas through mappings; (b) point 6, dft wavefunction-representation ›
   localized-orbital-basis-set and mbpt dielectric-matrix › localized-orbital-basis-set renamed
   `atom-centered-basis-set`, since they hold basis functions centred on atoms, not localized orbitals (breaks 0.7.0
   records that use them; no example does); (c) points 2-3, the layers (dataset, structure, computation, method
   settings, results): a paragraph in §1.2 saying which part of the schema holds each, results left to 0039's open
   question, instead of a per-property layer tag; (d) point 2, identifiers: §1.3 states that a Property is identified
   by its path (e.g. `dft.settings.xc-functional`), cited per version by its permalink; IRIs on matcore.org wait until
   the domain points to the site; (e) point 8, governance: a short paragraph on how a Property is proposed (issue or
   pull request), reviewed by the section's committee, and renamed or removed (a breaking change listed in Revision
   History, 0010); (f) point 6, a vocabulary of software codes, and normalized values beside other free values:
   declined (no community list; xc is the one field with a normalization source); (g) mappings to nomad-simulations,
   PMDCore and OPTIMADE: later, as a non-normative annex or a step 9 tool, with FAIRmat's collaboration. (Superseded:
   decided by 0083.)
   Semantic scope and basis-set name by 0083 (ruling 2026-11-23, from that feedback; the human chose each
   recommendation): (1) §1.2 says MatCore is a reporting standard, not an ontology, its Properties defined in words and
   alignable with ontologies and richer schemas through mappings; (2) a §1.2 paragraph says which part of a record holds
   the dataset, the modelled system, the computations, their settings and derived properties, the results being in the
   dataset (no per-property layer tag); (3) §1.3 says a Property is identified by its path (e.g.
   dft.settings.xc-functional), a version's definition cited by its permalink, IRIs waiting for matcore.org; (4) a §1.3
   paragraph after versioning: a change is proposed as an issue or pull request, reviewed by the section's committee,
   decided by the Standard Committee; renames and removals are breaking, listed in the Revision History; no deprecation
   period below 1.0; (5) dft wavefunction-representation › and mbpt dielectric-matrix › localized-orbital-basis-set
   renamed atom-centered-basis-set (breaks 0.7.0 records using it; no example does), Wannier functions and localized
   molecular orbitals being derived results (a DP computation, e.g. software Wannier90, naming its source as Source
   data); (6) software-code vocabulary and general normalized values declined; (7) mappings later, with FAIRmat.
   PROPOSED, NOT DECIDED (0083): a note on atom-centered-basis-set pointing Wannier functions and localized molecular
   orbitals to derived (Superseded: declined by the human 2026-11-23); the IRI form once matcore.org points to the site. Ruling committed on main (4840fe7); two PRs: the
   Preamble (items 1-4) and the rename (item 5).
   [done, PR #144 merged 2026-11-23] 0083 items 1-4:
   docs/standard/index.md (§1.2 gains two paragraphs at its end, the parts of a record and the reporting-standard
   sentence; §1.3 gains a paragraph before the x- paragraph on a Property's path and permalink, and one after the
   versioning line on how a change is proposed, reviewed by the Standard Committee members of its section (linked to
   Leadership) and decided, renames and removals breaking and listed in the Revision History); tests/test_preamble.py
   (a new test). Judgment calls: placement of each paragraph; "can be aligned" (no mappings exist yet).
   [done, PR #145 merged 2026-11-23] 0083 item 5:
   schema/dft.yaml and schema/mbpt.yaml (the name, "atom-centered basis set" in five dft descriptions, mbpt's
   description "For a code using basis functions centered on atoms, the name of the basis set.", the two "either ...
   or" notes), by script; tests/test_properties.py (a new test; the structure tests renamed), test_computations.py and
   test_dft_rulings.py renamed; 03-dft, 05-mbpt and the JSON Schema regenerated; no example uses it. Judgment calls:
   US spelling, as the schema's "modeled"; minimal method's TB definition keeps "a basis of localized orbitals" (the
   usual wording for tight binding, outside the ruling). The Wannier note is declined by the human 2026-11-23 (committed without it).
   A reviewer's spreadsheet of fourteen items (committee review of 2026-09-23, by email; errors, typos and vocabularies in
   minimal, DFT, MBPT, MD and PF), reviewed 2026-11-23 against the current schema: all are addressed, nothing to
   decide. temperature-gradient is TemperatureGradient, K/m (step 5, PR #25); provenance › date reads "The date and
   time when the change was made." (PR #33); the "Nonstandard" simulation type is gone, type being a container of four
   vocabularies (0036); cell-reference writes |a₀|, |b₀|, |c₀| (PR #25); heat-flux and temperature-gradient give
   whichever is imposed, a measured value being a result (0039); units: any Annex U symbol of the right Kind, no
   normalization to SI, the recommended unit informative, x-gnu: only where the Kind is any (0001, 0015, §1.3); LAPW
   and PAW (0018, 0080); mbpt starting-point and its type removed, the DFT computation named as input role Starting
   point (0046), DFT+U as calculation-physics On-site correlation (review 2026-11-16); the planewave-basis-cutoff note
   (step 4); μσT's gloss (fixed); pf time-dependence removed (0074 amendment); "paramter" and time-step-size's "grid
   spacing" text gone (PR #130). Left open, as before: whether minimal lists the quantities a dataset contains (0039).
   A reviewer's written comments on minimal and other sections (committee review of 2026-09-23, by email; questions on
   purpose and use, then specific points), reviewed 2026-11-23. Already addressed: wrappers and scripts (software one
   entry per layer, roles Calculation method, Script, Simulation code, Workflow framework, with description, link,
   identifier DOI/SWHID and dependency; 0043); phase "Cluster", nanostructures, surfaces and thin films (form terms,
   0025); how structures were built (task Structure generation, 0065); the root element (JSON, a matcore container,
   0044, 0045); cell as a 3x3 array (0038); units in the record (value + unit, 0015); non-SPDX licenses (LicenseRef-,
   0031); "0" vs "o" in GW terms (0070); the Ry cutoff (recommended eV, the instance gives its own unit);
   methfessel-paxton-order (a generic smearing parameter, 0004 item 47); singular names (the naming rule). Answered by
   scope, no change: a record describes a dataset, not a method or wrapper alone (§1.2), so a material-agnostic method
   has no record of its own; results are in the dataset (0083). Not addressed, PROPOSED, NOT DECIDED (recommendations):
   (a) a generic parameter whose value is a string or bool carries no unit (amends 0016's unit*; §1.3,
   check_generic.py, the JSON Schema); (b) four repeatable Properties break the rule that a repeatable Property stays
   singular: pf domain › boundary-conditions and initial-conditions, pim charge-interactions and magnetic-interactions,
   renamed boundary-condition, initial-condition, charge-interaction, magnetic-interaction (breaks 0.7.0 records);
   `settings` kept as a mass noun; (c) matcore › id gets a note: the dataset's persistent identifier that is the same
   for all versions (e.g. a Zenodo concept DOI), otherwise an identifier the record author generates (e.g. a UUID); no
   central registry (settles the step 6 open point on the MatCore ID); (d) matcore moves to the top of minimal, since it
   identifies the record (no record breaks); (e) links between records for shared components: not now
   (related-content links datasets); (f) purpose, central databases and record generators: answered in the reply,
   parsers being status step 9. (Superseded: (a), (b), (d) decided by 0084; (c) withdrawn, see below.)
   Generic units, singular names, matcore first by 0084 (ruling 2026-11-23, from that review; the human chose each
   recommendation): (1) a generic parameter whose value is a string or bool has no unit; unit is required for float
   and int (amends 0016; §1.3, check_generic.py, the JSON Schema via the JSON `type` member); (2) pf domain ›
   boundary-conditions and initial-conditions, pim charge-interactions and magnetic-interactions renamed
   boundary-condition, initial-condition, charge-interaction, magnetic-interaction; settings kept; (3) matcore becomes
   minimal's first top-level Property. Breaks 0.7.0 records with the old names or a unit on a string or bool
   parameter. The human corrected (c): the reviewer asks how MatCore ids are assigned (e.g. minted by a central service
   through a software tool, or another way); that process is undecided, and no note is added to matcore › id.
   PROPOSED, NOT DECIDED: how MatCore ids are assigned (replaces the earlier step 6 point on the MatCore ID's form and
   issuer). Ruling committed on main (4d1f109).
   [done, PR #146 merged 2026-11-23] 0084: (1)
   scripts/check_generic.py (UNIT_GIVEN; unit not required, with that note), the ten generic parameters' unit in dft,
   ps, pf, ml and derived (required false, the note; by script), scripts/build_json_schema.py (unit required for float
   and int, forbidden for string and bool), §1.3's definition; (2) pf boundary-condition and initial-condition, pim
   charge-interaction and magnetic-interaction (by script, with examples/pf.json and tests/test_computations.py); (3)
   matcore first in schema/minimal.yaml and examples/minimal.json. Tests: test_generic (a new test), test_json_schema
   (string and bool without unit, float and int with), test_schema (a new test: a repeatable Property's name is
   singular, except settings, species, calculation-physics, number-of-particles), test_properties (matcore first;
   two generic structure tests), test_preamble (the unit clause). Pages and JSON Schema regenerated; rendering
   checked. Found, not changed: examples/minimal.json gives standard-version 0.6.0.
   The human's summary of the committee review's feedback (Feedback_summary/feedback_summary.docx, outside the
   repository), checked 2026-11-23: its ten items (FAIRmat's semantic level, identifiers, layers, method vs workflow,
   conditions, vocabularies and governance; FAIRmat's LibXC normalization; one reviewer's spatial and temporal
   inhomogeneity and rare-event methods) are all addressed (0017, 0035-0042, 0046, 0063-0069, 0079, 0082, 0083), apart
   from two points deferred by 0083: resolvable IRIs (until matcore.org points to the site) and mappings to other
   schemas (with FAIRmat). The summary is unfinished: the list after "the following are absent:" and the MBPT, ML, PF
   and Derived sections are empty, and the other two reviews (0084 and the spreadsheet) are not in it.
7. [done, PR #140 merged 2026-11-22: §1.4 and the generated JSON Schema] Define, as a section of the standard, the
   serialization requirements that any format must
   satisfy (not a specific format). Provide example instances in examples/ in at least one
   serialization, generated from the same source, and validate them in CI against a schema
   generated from the YAML for that serialization.
   Order (0004): the examples and generated schema come after step 5, which fills the typed fields;
   this step may run alongside step 6, and the requirements section may be written earlier. It
   opens with a decision record choosing the first serialization, which step 9 then uses.
   [done] First serialization chosen: JSON (0044).
   [done, PR #81 merged 2026-11-08] JSON examples by 0044: the seven examples converted from XML by script; check_examples.py,
   check_formula.py and build_docs.py read JSON; meta-schema `file` requires .json; §1.3 says the
   examples are in JSON.
   JSON Schema by 0078 (ruling 2026-11-22; the human chose each recommendation after an explanation of what a JSON
   Schema is and which files it checks): scripts/build_json_schema.py generates one JSON Schema (draft 2020-12) from
   schema/*.yaml and units.yaml into docs/standard/matcore.schema.json, generated, committed (CI's staleness check),
   published with each version and linked from §1.3; it describes a whole record (minimal required, other sections
   optional, nothing else; each section in $defs, against which the single-section examples are checked); it checks
   names, required, repeatable as arrays, containers as objects, Type and Extent, values' bounds, patterns and formats;
   units by Kind (Annex U symbols of the value's Kind, plus dimensionless for 0075's reduced lengths and times; any
   symbol, dimensionless or x-gnu: where the schema does not fix the Kind); a generic parameter's JSON `type` and
   value (0044 item 3); open terms, x-gnu validity, label references, formula grammar and check digits are left to
   their own checks or step 9; validate_schema.py checks the examples against it and check_examples.py is removed. No
   property changes. The other part of step 7, the requirements any serialization must meet, is a separate change. (Superseded in
   part: 0079 lets x- members through.)
   Ruling committed on main (b89ee14).
   [done, PR #139 merged 2026-11-22] 0078: scripts/build_json_schema.py (new) builds
   the schema; build_docs.py's main writes it to docs/standard/matcore.schema.json with the pages, so CI's single build
   step and its stale-page check cover it (judgment call, in place of a separate CI step); every property's description
   is carried into the schema; a repeatable property is an array of at least one entry (judgment call); a Type with
   Extent any, and a generic parameter's value, are a value or arrays of it to any depth ($defs any-depth-<type>);
   validate_schema.py checks the generated schema and validates every example against its section's $defs entry, with
   format checking; scripts/check_examples.py removed, check_formula.py takes SECTIONS from the generator;
   tests/test_json_schema.py (new: the old structural and generic cases, units by Kind, reduced lengths, the record's
   top level, every example, the committed copy) and tests/test_examples.py reduced to its identifier test;
   tests/test_build_docs.py expects the schema among the written files; §1.3 links to the schema, saying what it
   checks and what it does not; README.md and CONTRIBUTING.md list it among the generated files.
   Extensions and §1.4 by 0079 (ruling 2026-11-22, from the conflict found while drafting step 7's requirements:
   §1.3 allows arbitrary added Properties, 0078's schema rejects unknown names): a record may add Properties of its own,
   at any level, named with the prefix `x-` (e.g. x-beamline); the standard's names never begin with x- (meta-schema);
   the JSON Schema accepts any x- member and rejects other unknown names (amends 0078 item 3); §1.3's sentence reworded;
   a new §1.4 Serialization holds the definition of a serialization, the requirements any serialization must meet, the
   JSON serialization (RFC 8259, UTF-8, .json, 0044's mapping, generic parameters' `type`, the x- prefix) and the link
   to the JSON Schema, both moved from §1.3; the menu lists 1.1–1.4. Ruling committed on main (bee7edf).
   [done, PR #140 merged 2026-11-22] 0079: schema/meta-schema.yaml's
   name pattern refuses x- (a negative lookahead); scripts/build_json_schema.py accepts `^x-` members (any value) on
   every object and on the record, the schema regenerated; docs/standard/index.md: §1.3's sentence on added Properties
   reworded with the x- prefix, the definition of a serialization and the JSON Schema paragraph moved into a new
   §1.4 Serialization, which states six requirements any serialization SHALL meet, then JSON (Request for Comments
   (RFC) 8259, UTF-8, .json) and 0044's mapping with the generic parameter's `type` and the x- members, then the JSON
   Schema; tests: test_preamble (a new test of §1.4; RFC spelled out at first use), test_schema (x-beamline refused as
   a standard name), test_json_schema (x- members accepted at any level, a misspelled name still rejected); the menu
   lists 1.1–1.4 (checked in the browser).
8. [merged into step 2] Site content migration from matcore.org.
9. [todo] `matcore` Python package: validator, then parsers, then Pyodide web tools. After step 7;
   the validator reuses step 7's generated schema (0004).
   PROPOSED, NOT DECIDED: serialization(s) the tools read and write beyond the first one chosen in
   step 7.

## Working rules (apply in every session)
- Session practice (how the work proceeds, not decisions about the standard; 0004 item 49):
  - Keep CLAUDE.md, docs/decisions and anything else a new session needs current with the state
    of this one at every step, so that a session that ends without warning can be resumed where
    it left off: each ruling as it is made, each open question as it is raised (as PROPOSED, NOT
    DECIDED), and the state of the work in progress (the branch, whether it is committed, pushed
    or in a pull request, and what awaits the human). Before ending each turn, check whether
    anything said, found or decided in it exists only in the conversation, and if so record it;
    when a later change makes an earlier entry untrue, mark that entry "(Superseded: …)".
  - The human runs `mkdocs serve` on port 8000 in this folder, so the local site shows whatever is
    checked out. Say so before switching branches, and keep the folder on the branch under review.
  - A ruling is committed on main first; the branch for its pull request is cut from that commit.
  - A property pull request's description has these parts: the cross-check against the .docx,
    the changes (file by file), changes decided in review, judgment calls, and the checks run
    (including that /ponytail-review was done and whether Codex ran). After opening it, offer
    Auto-fix; a fix it needs is committed and handed to the human to push.
  - After a merge: pull main, delete the merged local branch, mark the status entry "[done, PR #N
    merged <date>]", and commit that alone as "Record <property> as merged in PR #N".
  - A status entry later reversed or replaced keeps its text and gets a "(Superseded: …)" note.
- Text added to the Preamble (docs/standard/index.md) defines each acronym at its first use in
  the Preamble, unless the Preamble already defines it or it is well known and understood in
  context (e.g. AI, SI, XML, JSON): spelled out, acronym in parentheses (0004 item 51).
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
  `uv run python scripts/build_docs.py`,
  `uv run mkdocs build --strict`. Commit any files
  build_docs.py regenerates with the change; CI fails if the committed copies are stale. Never
  hand-edit generated files under docs/standard/ (02-*.md … 08-*.md, pim.md, ps.md, revision-history.md, the
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
