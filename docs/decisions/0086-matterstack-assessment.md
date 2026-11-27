# 0086 — Quantities, populations, MLIP training, geometric construction and other gaps found in use

Date: 2026-11-27. Status: accepted. Decided by: Ellad Tadmor.

## Context
Matterstack assessed MatCore 0.8.1 by describing the six kinds of dataset its database will hold, each as a record valid against the JSON Schema. Its report lists:
- fourteen gaps in the standard (A1–A14);
- four uses of `x-` Properties (B1–B4);
- ten questions of interpretation (C1–C10).

Each was checked against the v0.8.1 sources and decided one by one; several were revised in review.
- Every gap was confirmed.
- A8 (a k-point spacing) ran into 0004 item 47, which removed `k-point-spacing` because it can contradict `number-of-points`.
- Several gaps answer questions this standard had left PROPOSED, NOT DECIDED: what quantities a dataset holds (0039); how pim records an MLIP's fit and a software role for a trained model (0073); the method of a structure built without a model (0065).

## Decision
**Minimal metadata**
1. **`computation › quantity`** (A1), optional, repeatable: a quantity the dataset holds from this computation. Its values stay in the dataset (§1.2). Members:
   - `name*`, as stored;
   - `description`;
   - `unit`: an Annex U symbol or `dimensionless`, not checked against a Kind, and omitted for a string or boolean quantity;
   - `extent`: a string in §1.3's notation;
   - `type`: open terms Float, Integer, Complex, String, Boolean. These describe the stored data; MatCore's own Types are unchanged;
   - `per`: how many values, one for each Atom, Configuration, …;
   - `normalized-by`: what each value is divided by, e.g. Atom, Formula unit, Cell volume;
   - `convention`: sign, ordering or normalization.
2. **`structure › population`** (A2), optional: many structures of different compositions described together. Members:
   - `count*`;
   - `element`: repeatable, IUPAC symbols;
   - `number-of-elements` and `number-of-sites`: repeated value + qualifier entries, e.g. Minimum and Maximum;
   - `form`.

   `material-component` becomes required unless `population` is given. A structure gives one or the other, never both, and notes on both say when to use each.
3. **`computation › input`** (A5) gains `dataset` (format uri), given instead of a local `computation-label` for an input from outside the record. `computation-label` becomes optional; with `dataset`, it names a computation in that dataset's record.
4. **`computation › selection`** (A12), an optional string: the criterion, how many results were kept out of how many, and whether rejected or failed results are in the dataset. ml `inference › filtering` is unchanged and named in its note.
5. **Orientation** (A13):
   - `material-component › orientation`: `plane` [hkl] and `direction` [uvw], in the component's conventional cell. The direction lies in the interface plane and is parallel to the direction given for the other side.
   - `termination`: repeatable, the atomic layer at the interface, named by composition.
   - `structure › orientation-relationship`: open terms, e.g. Kurdjumov-Sachs and Nishiyama-Wassermann.
   - `material-component › role` gains "Grain".
   - The registry stays in the data.
6. **`access`** (A14), optional, top level. Its terms are the four of COAR Access Rights 1.1 (open access, embargoed access, restricted access, metadata only access), each with its COAR URI in the note, plus an optional `embargo-date`.
7. **Vocabularies.**
   - `software › dependency › role` gains "Container image" (A9), with a note to give the image digest, not a tag.
   - `software › role` gains "Trained model" (A10): a model trained elsewhere, other than an interatomic potential, which stays "Interaction model".
   - `input › role` gains "Guidance" (A11): a model whose outputs steer sampling or generation.
   - "Initial configuration" is reworded to "The configurations this computation starts from or evaluates, with any state carried over, e.g. velocities." (C5).
8. **`Unknown`** (A6). §1.3 reserves the value `Unknown` for a required string Property whose information was not recorded. An optional Property is omitted instead, and numbers have no such form.

**Method sections**

9. **pim** (A3):
   - `settings` gains `training`, for a computation whose task is Training. It holds ml-model's `training-data`, `training-method` and `model-performance` with the same members and notes, kept in step by a test.
   - `settings` gains a generic `architecture-parameter`, after `model-type`.
   - The PIM method term and the input role "Interaction model" widen to "energies, forces and other per-configuration responses (e.g. charges, dipoles, polarizabilities)".
   - A computation that uses the trained model names the training computation as input role Parameters.
10. **Geometric Construction** (A4): a new section 2.9 (GC), key `gc`.
    - `settings*` holds `computation-label*`, `procedure*` and a generic `construction-parameter`. Method parameters stay in their own section.
    - The method term "GC" is added under Atomistic and Mesoscopic: "structures built by rules the author specifies (geometric, combinatorial or random), without evaluating energies or forces and without a model learned from data".
    - Generative models stay ML, and searches that relax candidates stay PS. The ML and PS notes point to GC.
    - The Leadership page gains "Method: Geometric Construction", membership TBD.
11. **dft `k-point-mesh › rule`** (A8). Members:
    - `type*`: Spacing or Density;
    - `value*` and `unit*`;
    - `convention*` for a spacing: "2pi included" or "2pi excluded".

    It is given only when `number-of-points` is omitted, so 0004 item 47 stands. The value's Kind depends on `type`: InverseLength for a spacing, dimensionless for a density. That is the conditional-rule case §1.3 leaves open, settled in its PR.
12. **ml and pim `metric`** gain `normalized-by`, with the terms of item 1 (A7).

**Units** (A7)

13. Annex U gains seven Kinds, with units:
    - energy per area: J/m^2, mJ/m^2, eV/angstrom^2;
    - electric dipole moment: e*angstrom, D, C*m;
    - polarizability: C*m^2/V, e*angstrom^2/V;
    - second-order susceptibility: pm/V, m/V;
    - thermal conductivity: W/(m*K);
    - electric current: A;
    - electrical conductivity: S/m.

    Each unit is added in its own pull request, every field traced to a primary source, the first unit of each Kind adding the Kind. Kind names and QUDT identifiers are fixed in those pull requests. A value per atom is written with `normalized-by`, not as a unit.

**Checks and examples**

14. The generated JSON Schema requires `name` and `link` when a license `identifier` begins with `LicenseRef-`. The link may be any URI, internal included (C8).
15. `examples/minimal.json` states the current standard version and link, and a test compares them with `schema/releases.yaml` (C10).

**Answers without a change to the standard**

16. Interpretation questions:
    - **C1, append-only datasets:** a version is an immutable release snapshot (a Version update), and rows appended in between belong to the next version. The snapshot id goes in `provenance › comment`.
    - **C2, settings by rule:** one computation covers calculations whose settings follow one rule (0077, 0063). Runs at several imposed temperatures are one computation per temperature (0035, 0063).
    - **C3:** a DFT computation whose goal is a property has task Property calculation.
    - **C4:** runs with identical settings differing only in requested output are one computation, their outputs given as quantities.
    - **C6:** a Wannierization is method DP, naming its DFT computation as Source data.
    - **C7:** a temperature or bias used only in post-processing is a `calculation-parameter`.
    - **C9:** a URI form for MatCore ids waits for the decision on how ids are assigned (0084).
17. **B1–B4** are correct uses of `x-`. A computation-level `x-` member should hold keys of the computation, not lists of row ids.

## Consequences
- Pull requests, one per group:
  - minimal (items 1–8);
  - pim (item 9);
  - the GC section (item 10);
  - dft (item 11);
  - ml and pim metric (item 12);
  - the units (item 13, several);
  - checks and examples (items 14, 15).
- No conformant 0.8.0 record breaks:
  - every new Property is optional;
  - `material-component` loses its unconditional requirement;
  - the reworded role definitions keep their terms.

  Records that used user terms where a term now exists (e.g. method "Geometric construction") should switch to it (GC).
- Settles three open points: 0039 (quantities), 0073 (MLIP training, trained-model role) and 0065 (construction).
- The reply to Matterstack gives one entry per finding.
