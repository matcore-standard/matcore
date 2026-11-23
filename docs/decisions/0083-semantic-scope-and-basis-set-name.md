# 0083 — Semantic scope, layers, identifiers, governance, and the atom-centred basis set

Date: 2026-11-23. Status: accepted. Decided by: Ellad Tadmor.

## Context
FAIRmat Area C sent written feedback to the committee review of 2026-09-23 (by email). It places MatCore between nomad-simulations, a detailed simulation schema, and PMDCore, a mid-level ontology, and makes eight points. Several have been met since then:
- the method is told apart from the workflow: `method`, `task` and `input` links (0046, 0064, 0065);
- `simulation-conditions` is split into typed conditions (0035–0042), with the ensemble and time step in ps (0069) and convergence in dft;
- open vocabularies keep the user's value and report it as user-specified (0013);
- the exchange-correlation functional is normalized through LibXC (0017, 0051);
- "material" is split into a material component's formula, form, phase and role (0025, 0034);
- added Properties carry the prefix `x-` (0079).

The points still open were:
- what kind of standard MatCore is, a reporting standard or a semantic model (point 1);
- which Properties describe the dataset, the system, the method, settings, workflow or outputs (points 2–3);
- stable identifiers for Properties (point 2);
- how Properties are reviewed, standardized and removed (point 8);
- a vocabulary of software codes and normalized values in general (point 6);
- mappings to other schemas (positioning and collaboration);
- the name `localized-orbital-basis-set` (point 6).

That name is in dft `wavefunction-representation` and in mbpt `dielectric-matrix`. It holds basis functions centred on atoms: Gaussian, local atomic or numerical atomic orbitals. "Localized orbitals" usually means something else, e.g. Wannier functions or localized molecular orbitals, which are built from the results of a calculation rather than used as its basis. In MatCore such orbitals are derived results: a computation of method DP, e.g. with software Wannier90, names the computation whose states it uses as input role Source data, and its derived block describes them.

## Decision
1. **Semantic level.** §1.2 says that MatCore is a reporting standard: it says what the metadata of a dataset must contain and how it is structured. It is not an ontology. Its Properties are defined in words, and they can be aligned with ontologies and richer schemas through mappings.
2. **Layers.** A paragraph in §1.2 says which part of a record holds each kind of metadata:
   - the top-level Properties of the minimal metadata describe the dataset;
   - `structure` describes the modelled system;
   - `computation` describes each computation: its method, task, inputs, imposed conditions and software;
   - the method sections give each computation's settings;
   - the derived section gives the properties obtained from the results.

   The results themselves are in the dataset. No Property gets a layer tag.
3. **Identifiers.** §1.3 says that a Property is identified by its path, e.g. `dft.settings.xc-functional`, and that the definition in one version is cited by its permalink. Resolvable IRIs on matcore.org wait until that domain points to the site.
4. **Governance.** A paragraph in §1.3, after versioning, covers:
   - how a change is proposed: a new, renamed or removed Property, or an `x-` Property to be standardized, proposed as a GitHub issue or pull request;
   - who reviews it: the committee of the section it concerns, with the decision made by the Standard Committee;
   - how renames and removals are treated: they are breaking changes, listed in the Revision History.

   There is no deprecation period below 1.0.
5. **Atom-centred basis set.** dft `wavefunction-representation › localized-orbital-basis-set` and mbpt `dielectric-matrix › localized-orbital-basis-set` are renamed `atom-centered-basis-set`. Their descriptions, the notes that name them, and the example "either … or …" notes are changed to match.
6. **Declined:** a vocabulary of software codes, since there is no community list to adopt and a code is identified by its `identifier`. Also declined: normalized values beside free values in general, since normalization is given where a source exists (LibXC).
7. **Later:** mappings to nomad-simulations, PMDCore and OPTIMADE, as a non-normative annex or a tool (status step 9), taken up with FAIRmat.

## Consequences
- Two pull requests:
  - the Preamble (items 1–4): docs/standard/index.md and tests/test_preamble.py;
  - the rename (item 5): schema/dft.yaml, schema/mbpt.yaml, tests, the regenerated pages and JSON Schema.
- Item 5 breaks 0.7.0 records that use `localized-orbital-basis-set`. No example uses it.
- PROPOSED, NOT DECIDED:
  - a note on `atom-centered-basis-set` saying that Wannier functions and localized molecular orbitals are derived results, given in the derived section;
  - the form of IRIs once matcore.org points to the site.
