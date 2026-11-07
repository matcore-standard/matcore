# 0025 — Structure as a top-level container of material components

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on minimal `material-component`: "The material property contains phase+description for describing the crystal structure, molecule, etc. and microstructure subproperty, but there doesn't seem to be anywhere for actual structures. How would one characterize things such as nano structures, free surfaces, thin films?"

`material-component` records what a substance is made of (`constituent`), its state of matter (`phases`), and free text (`description`, `microstructure`). Nothing records the form of the system modelled: a Si slab and a bulk Si supercell get the same metadata. examples/minimal.xml can mention surfaces only in `description`. `simulation-conditions › cell-periodicity` does not fill the gap: a slab is usually periodic in all three directions, with vacuum between its images.

Adding a structure type inside `material-component` was weighed and rejected: the form belongs to the system, which may consist of several materials (a film on a substrate), not to each material.

## Decision
1. **A new top-level property `structure`** takes the place of `material-component` in minimal (after `disclaimer`): required, repeatable, a container. Description: "A system modelled in the dataset, e.g. a bulk crystal or a thin film on a substrate, and the materials that make it up." Its subproperties, in order:
   - **`type`**: required, not repeatable; string, `[]`, inapplicable. Description: "The geometric form of the structure." Open terms (0013): Bulk, Cluster, Monolayer, Nanoparticle, Nanotube, Nanowire, Surface, Thin film. Interface is not a term: it does not fit as a form of a structure. The note defines each term:

     > One of: "Bulk" – A material extending without bound in all three directions, e.g. a periodic crystal or a liquid. "Cluster" – A finite aggregate of atoms or molecules, smaller than a nanoparticle. "Monolayer" – A layer one atom or molecule thick, e.g. graphene. "Nanoparticle" – A solid particle of nanometre size in all three directions. "Nanotube" – A hollow cylinder of nanometre diameter, e.g. a carbon nanotube. "Nanowire" – A solid wire of nanometre diameter, extending without bound along its axis. "Surface" – The free surface of a semi-infinite solid, e.g. modelled as a slab. "Thin film" – A layer of finite thickness, free-standing or on a substrate.
   - **`material-component`**: required, repeatable, moved from the top level with its subproperties. Its description becomes "A description of the chemical composition and phase of a substance making up the structure." (was "… composition and structure of a substance in this dataset."), since "structure" now names the container.
2. **`description` and `microstructure` stay in `material-component`**, unchanged.
3. **`phases` is renamed `phase`** and becomes a repeatable scalar (string, `[]`) instead of a list (extent `[:]`), following the naming rule (a repeatable property stays singular). Same terms. Description: "A phase of the material." The note opens "One of:" instead of "One or more of:".
4. **examples/minimal.xml** gets two `structure` entries for the Si GAP data, one of type Bulk and one of type Surface, each holding the Si `material-component` with `<phase>Crystal</phase>`.

## Consequences
- Breaks 0.5.0 instances: `material-component` moves inside `structure`, and `phases` is renamed `phase`.
- One pull request applies items 1–4 (schema, tests, regenerated page, example). minimal stays complete (`legacy_complete: true`).
- A structure of several materials (a film on a substrate) lists each as a `material-component`; which of them is the film is stated in their `description`.
