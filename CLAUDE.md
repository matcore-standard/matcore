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
  (minimal, dft, pim, md, mbpt, ml, pf, derived; pim added by 0046). THIS IS THE STANDARD.
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
  annex-i-identifiers) plus GENERATED chapters (02–08 and pim.md, named in build_docs.PAGES;
  revision-history; and the marked regions in
  index and the annexes: version line, Tables U.3/U.4, Table I.1).
  Never hand-edit generated parts; edit the YAML and run
  `scripts/build_docs.py --show-legacy`.
- `docs/decisions/` — decision records: internal committee information, not published on the site
  (0004). 0001 is the units change list (not yet applied; see Status). The frozen Google Doc export
  is stored there as the baseline artifact.
- `scripts/validate_schema.py` — checks section files against the meta-schema and units.yaml. It
  validates the standard itself, not instance files (the instance validator is status step 9).
  scripts/check_formula.py (0034) parses formulas and checks the examples' material components.
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
  Null when kind is `dimensionless` (0004 items 39, 48).
  No recommended unit when kind is `any` (0019).
- `convention`: an optional property field in meta-schema.yaml, rendered by build_docs.py but
  used by no property; the units model below expresses conventions as subproperties instead.
  PROPOSED, NOT DECIDED: remove the field, or define its use, when the next convention-like
  property comes up (mbpt exciton-momentum's `basis`).
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
  required enumerated subproperties (`convention`, `basis`, `scaling`), never encoded in the unit string.
- Energy and MolarEnergy are distinct kinds (Annex U Rule 8). kJ/mol, kcal/mol → MolarEnergy.
- CODATA 2022 factors are normative; QUDT (CODATA 2006) and GNU Units 2.23 (CODATA 2018) are stale.
- GNU Units pinned to 2.23 / definitions.units 3.19 for `x-gnu:` escape expressions.
- "Annex" (ISO usage), normative. Use "Kind" (not "Quantity kind") in the schema, the standard's prose
  and new text. Decision records are not rewritten. "Quantity kind" remains where it refers to QUDT's
  concept.

## Generic parameters and free-form units (decided; see docs/decisions/0001 and 0003)
Three groups, not to be merged:
1. Generic parameters: xc-parameter and smearing › parameter (dft; 0004 item 47, moved by 0053), computation-parameter
   and td-parameter (md), model-parameter (pf), calculation-parameter (derived). Their `value` has
   type any, extent any, kind any; the instance supplies type, shape and unit. The generic-parameter
   rule applies to these only. The instance type is one of float, int, string, bool, and is stated
   in the instance, not inferred from how the value is written; each serialization (defined in
   §1.3) defines how.
   The value need not be a scalar (0004).
2. Free-form units: field-variable, free-energy (pf). No `value`; a free-form `unit` whose kind
   the schema does not fix.
3. Typed properties with a required unit: grid-spacing (Length, recommended m) and time-step-size
   (Time, recommended s) (pf). Handled like temperature, not as generic parameters. With
   domain-size they carry a required `scaling` subproperty [physical, nondimensional]; when
   nondimensional, `unit` SHALL be `dimensionless` (0003).
Every `unit` subproperty has kind inapplicable and holds an Annex U symbol or `dimensionless`. The
`x-gnu:` escape (Annex U Rule 4) is permitted only where the schema does not fix the kind: groups 1
and 2, and the `unit` beside any other `value` of kind any (dft SCF tolerance, 0019); group 3 and all
other typed properties use Annex U symbols only (0001 A1.1).
PROPOSED, NOT DECIDED: state conditional validation rules (the allowed unit or values of one
subproperty depend on another's value: `basis` for exciton-momentum, `scaling` for PF lengths and
times) once in §1.3, so each property refers to the rule rather than restating it. Needs a decision
before implementation, when the first such property comes up (mbpt exciton-momentum); whether
0013's `depends-on`/`cases` can express it is part of that decision. (dft k-point-spacing, the
first candidate, is removed: 0004 item 47.)
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
  B2 (added note) is PROPOSED, NOT DECIDED; B9 is decided for generic parameters (0016); B5 is
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
     --show-legacy is passed, and CI builds with --show-legacy until step 5 is complete.
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
     is main. (An earlier v0.6.0 tag on 2908f57 failed CI's release check and was moved.)
   - Changes to the standard since 0.6.0, for the next release's entry in releases.yaml: the
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
     Nucleus, and bonding-type, Reactive meaning no predetermined bonding topology (0046; step 5).
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
   Sections go in the order minimal, dft, pim, md, mbpt, ml, pf, derived, and properties in file order
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
   and whether its `system` states the region as 0026's description does.
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
   §1.2's list says "MD: Classical molecular dynamics".
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
   [in progress, branch pim-charge-interactions] pim charge-interactions: the container and its
   six string subproperties (charge-origin, charge-style, charge-variability,
   long-range-electrostatics, electric-dipole, electric-dipole-variability) with the baseline's
   open terms, defined in the notes; electric-dipole-variability's description, a copy of
   charge-variability's, says "electric dipoles"; "Fixed" says "during a simulation"; legacy_*
   deleted.
   [todo] pim in file order: settings › theory-level (done, PR #92), model-type (done, PR #93), particle-style (done, PR #94), bonding-type (done, PR #95),
   charge-interactions, magnetic-interactions (computation needs no fill).
   [todo] md in file order, starting with computation. Each md property follows 0042 item 3: no
   quantity that minimal `conditions` (simulation-conditions before 0046) holds is repeated; md adds only how a condition is enforced
   (thermostat, barostat and their parameters) and the ensemble.
6. [todo] Committee decisions and community feedback (user will supply, after step 5):
   one decision record + one PR each.
7. [todo] Define, as a section of the standard, the serialization requirements that any format must
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
