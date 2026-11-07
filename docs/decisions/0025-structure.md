# 0025 — Structure as a top-level container of material components

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on minimal `material-component`: "The material property contains phase+description for describing the crystal structure, molecule, etc. and microstructure subproperty, but there doesn't seem to be anywhere for actual structures. How would one characterize things such as nano structures, free surfaces, thin films?"

`material-component` records what a substance is made of (`constituent`), its state of matter (`phases`), and free text (`description`, `microstructure`). Nothing records the form of the system modelled: a Si slab and a bulk Si supercell get the same metadata. examples/minimal.xml can mention surfaces only in `description`. `simulation-conditions › cell-periodicity` does not fill the gap: a slab is usually periodic in all three directions, with vacuum between its images.

Adding a structure type inside `material-component` was weighed and rejected: the form belongs to the system, which may consist of several materials (a film on a substrate), not to each material.

## Decision
1. **A new top-level property `structure`** takes the place of `material-component` in minimal (after `disclaimer`): required, repeatable, a container. Description: "A system modelled in the dataset, e.g. a bulk crystal or a thin film on a substrate, and the materials that make it up." Its subproperties, in order:
   - **`type`**: required, not repeatable; string, `[]`, inapplicable. Description: "The geometric form of the structure." Open terms (0013): 2D heterostructure, 2D material, Bulk, Chain, Cluster, Heterostructure, Molecule, Monolayer, Nanoparticle, Nanoribbon, Nanotube, Nanowire, Slab, Superlattice, Thin film. Interface and Surface are not terms: each is a feature of a structure (e.g. of a slab), not a structure. The note defines each term:

     > One of: "2D heterostructure" – A stack of 2D materials. "2D material" – A crystalline solid that is a single unit cell thick (typically a few nanometers or less), while extending infinitely or to large dimensions in the lateral plane, e.g. graphene. "Bulk" – A material extending without bound in all three directions, e.g. a periodic crystal or a liquid. "Chain" – A one-dimensional sequence of atoms or monomers, e.g. an isolated polymer chain or a monatomic chain. "Cluster" – A finite aggregate of atoms or molecules, smaller than a nanoparticle. "Heterostructure" – A composite structure made of two or more different solid materials (such as semiconductors, metals, or insulators) joined together. "Molecule" – A single molecule, isolated from its surroundings. "Monolayer" – A single layer of atoms or molecules deposited on another material. "Nanoparticle" – A solid particle of nanometre size in all three directions. "Nanoribbon" – A strip of a 2D material of nanometre width, extending without bound along its length. "Nanotube" – A hollow cylinder of nanometre diameter, e.g. a carbon nanotube. "Nanowire" – A solid wire of nanometre diameter, extending without bound along its axis. "Slab" – A truncated bulk structure that can be used, for example, to model surfaces. "Superlattice" – A periodic structure of alternating ultra-thin layers of different materials with a period longer than the lattice period of each. "Thin film" – A layer of finite thickness, free-standing or on a substrate.
   - **`material-component`**: required, repeatable, moved from the top level with its subproperties. Its description becomes "A description of the chemical composition and phase of a substance making up the structure." (was "… composition and structure of a substance in this dataset."), since "structure" now names the container.
2. **`description` and `microstructure` stay in `material-component`**, unchanged.
3. **`phases` is renamed `phase`** and becomes a repeatable scalar (string, `[]`) instead of a list (extent `[:]`), following the naming rule (a repeatable property stays singular). Description: "A phase of the material." The note opens "One of:" instead of "One or more of:". The terms change from the baseline's (Amorphous, Crystal, Quasicrystal, Molecule, Liquid, Gas, Plasma) to Amorphous, Single crystal, Polycrystal, Quasicrystal, Liquid, Gas, Plasma:
   - Crystal is replaced by Single crystal and Polycrystal, in its place.
   - Molecule is removed: a single molecule is a structure of type Molecule, and its phase is Gas.

   In the note, the definitions of Crystal and Molecule are removed, Gas is redefined, the new terms are defined, and a closing sentence covers single molecules:

   > "Single crystal" – A solid material characterized by a repeating pattern of atoms that extends throughout it without interruption. "Polycrystal" – A solid material made of many crystalline grains of differing orientation. "Gas" – A state where molecules or atoms are far apart and only interact during collisions. For a single molecule, give the phase Gas.

   An instance that gives Crystal or Molecule still conforms (the terms are open) and is reported as user-specified.
4. **examples/minimal.xml** gets two `structure` entries for the Si GAP data, one of type Bulk and one of type Slab, each holding the Si `material-component` with `<phase>Single crystal</phase>`.

## Consequences
- Breaks 0.5.0 instances: `material-component` moves inside `structure`, and `phases` is renamed `phase`. A 0.5.0 instance's Crystal and Molecule are reported as user-specified.
- One pull request applies items 1–4 (schema, tests, regenerated page, example). minimal stays complete (`legacy_complete: true`).
- A structure of several materials (a film on a substrate) lists each as a `material-component`; which of them is the film is stated in their `description`.
