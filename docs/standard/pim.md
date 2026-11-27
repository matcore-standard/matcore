# 2.3 Particle Interaction Model (PIM) Metadata

<p class="mc-version" data-version="0.8.0">Version 0.8.0</p>

The metadata for particle interaction models (MatCore-PIM) is tabulated below. A particle interaction model gives the energy and forces of a system of particles as an explicit function of the particles' coordinates, without solving for a wavefunction or an electron density, e.g. an interatomic potential, a machine-learned interatomic potential, a bonded force field, a coarse-grained model or the electron force field. These properties describe a computation whose method is PIM, the evaluation of energies and forces used by another computation, e.g. molecular dynamics. The properties are given in settings blocks, each naming the PIM computations it describes. (Note: This standard inherits the metadata in the minimal MatCore standard, adding the properties below.)

<span class="mc-legend"><span class="mc-key"><span class="mc-star">*</span> required</span><span class="mc-key"><span class="mc-icon mc-i-once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span> appears at most once</span><span class="mc-key"><span class="mc-icon mc-i-rep"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span> repeatable</span></span>

<details class="note mc-property" id="pim.settings" markdown="1">
<summary><span class="mc-name">settings<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

Settings shared by the computations named in it.

| Required | Repeatable |
|---|---|
| yes | yes |

<details class="note mc-property" id="pim.settings.computation-label" markdown="1">
<summary><span class="mc-name">computation-label<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

The label of a computation these settings apply to.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | yes | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="pim.settings.theory-level" markdown="1">
<summary><span class="mc-name">theory-level<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

How the functional form of the model was obtained.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `Physics-based`, `Machine-learned`. Other values are allowed.

**Clarifications:**

- "Physics-based" – A functional form built from a physical model of the interactions, with parameters fitted to data, e.g. EAM, Tersoff, a bonded force field or the electron force field
- "Machine-learned" – A machine learning model trained to take particle positions as input, e.g. GAP or MACE

</details>

<details class="note mc-property" id="pim.settings.model-type" markdown="1">
<summary><span class="mc-name">model-type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The kind of potential used to compute the particle interactions.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Examples: `Lennard-Jones`, `EAM`, `MACE`.

Note: Give the functional form. The specific parameterization, e.g. an OpenKIM model, NIST IPR record, or a published potential file, is identified in the computation's software (role Interaction model).

</details>

<details class="note mc-property" id="pim.settings.architecture-parameter" markdown="1">
<summary><span class="mc-name">architecture-parameter</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A fixed variable that defines the architecture of the interatomic model.

| Required | Repeatable |
|---|---|
| no | yes |

Note: For example, the number of layers, the number of nodes per layer, a cutoff radius or a maximum body order. Training settings are hyperparameter entries of training › training-method.

<details class="note mc-property" id="pim.settings.architecture-parameter.name" markdown="1">
<summary><span class="mc-name">name<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The designation of the architecture parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="pim.settings.architecture-parameter.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The data associated with the architecture parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | any | any | any | — |

</details>

<details class="note mc-property" id="pim.settings.architecture-parameter.unit" markdown="1">
<summary><span class="mc-name">unit</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit in which the associated value is expressed.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning).

Note: Give it when the type of the value is float or int; omit it when it is string or bool.

</details>

<details class="note mc-property" id="pim.settings.architecture-parameter.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

An explanation of the meaning, source, or purpose of the architecture parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

</details>

<details class="note mc-property" id="pim.settings.particle-style" markdown="1">
<summary><span class="mc-name">particle-style<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

The nature of the discrete entities whose interactions the model describes.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | yes | string | [] | inapplicable | — |

Recommended: `Atom`, `Radical`, `United atom`, `Bead`, `Coarse grained`, `Mesoscale`, `Classical electron`, `Nucleus`. Other values are allowed.

**Clarifications:**

- "Atom" – Each particle represents an individual atom
- "Radical" – Each particle represents a free radical
- "United atom" – Each particle represents a fixed grouping of atoms
- "Bead" – Each particle represents a user-tuneable group of atoms
- "Coarse grained" – Each particle represents a higher scale particle obtained by scaling up the atomic representation
- "Mesoscale" – Granular particles used to simulate microstructure at the mesoscopic scale
- "Classical electron" – Antisymmetrized wave packet representation of valence electrons
- "Nucleus" – A nucleus or an ion core as a point charge, with its electrons represented by other particles, e.g. in the electron force field

Give one entry for each kind of particle the model has, e.g. Nucleus and Classical electron for the electron force field.

</details>

<details class="note mc-property" id="pim.settings.bonding-type" markdown="1">
<summary><span class="mc-name">bonding-type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Specifies whether the bonds between particles are immutable or can be broken.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `Reactive`, `Bonded fixed`, `Bonded mutable`. Other values are allowed.

**Clarifications:**

- "Reactive" – A model without a predetermined bonding topology in which bonds are formed or broken on-the-fly based on the particle environment
- "Bonded fixed" – Bonds defined <i>a priori</i> and cannot be broken during a simulation
- "Bonded mutable" – Bonds defined <i>a priori</i> but can be broken and/or formed during a simulation

</details>

<details class="note mc-property" id="pim.settings.charge-interaction" markdown="1">
<summary><span class="mc-name">charge-interaction</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

The model used to describe the interactions between charged particles.

| Required | Repeatable |
|---|---|
| no | yes |

<details class="note mc-property" id="pim.settings.charge-interaction.charge-origin" markdown="1">
<summary><span class="mc-name">charge-origin<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Nature of the particle charges.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `Semi empirical`, `Quantum`, `Electronic population`, `Electronegativity`, `Tabulated`. Other values are allowed.

**Clarifications:**

- "Semi empirical" – Charges obtained from semi-empirical quantum calculations
- "Quantum" – Charges obtained from quantum calculations
- "Electronic population" – Charges obtained from electronic population analysis, e.g. Mulliken
- "Electronegativity" – Charges obtained from electronegativity differences between atoms
- "Tabulated" – Charges obtained from an external source

</details>

<details class="note mc-property" id="pim.settings.charge-interaction.charge-style" markdown="1">
<summary><span class="mc-name">charge-style<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The nature of the charges associated with the particles, such as total or effective charges.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `Coulomb full`, `Coulomb screened`. Other values are allowed.

**Clarifications:**

- "Coulomb full" – The particle charge accounting for all electrons
- "Coulomb screened" – Effective charge due to screening or shielding by other electrons (e.g. Slater)

</details>

<details class="note mc-property" id="pim.settings.charge-interaction.charge-variability" markdown="1">
<summary><span class="mc-name">charge-variability<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Attribute specifying the method for dynamically varying the local electric charge associated with discrete entities.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `Fixed`, `QEq`, `EEM`, `iEL/SCF`, `FlucQ`, `Drude`. Other values are allowed.

**Clarifications:**

- "Fixed" – Charges cannot change during a simulation
- "QEq" – Charge equilibration method
- "EEM" – Electronegativity Equalization Method
- "iEL/SCF" – Extended Lagrangian/self-consistent field scheme
- "FlucQ" – Fluctuating charge potential
- "Drude" – Drude method

</details>

<details class="note mc-property" id="pim.settings.charge-interaction.electrostatic-summation" markdown="1">
<summary><span class="mc-name">electrostatic-summation</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Method used to compute the electrostatic interactions between the charges.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Recommended: `None`, `Direct`, `Short-range`, `Ewald`, `PME`, `PPPM`, `Reaction`. Other values are allowed.

**Clarifications:**

- "None" – No electrostatic interactions are computed from the charges. A model whose particles carry no charges omits charge-interaction
- "Direct" – All Coulomb interactions computed directly
- "Short-range" – Electrostatic interactions computed only within a cutoff distance, possibly shifted or damped, e.g. Wolf summation or damped shifted force (DSF)
- "Ewald" – Ewald summation
- "PME" – Particle mesh Ewald
- "PPPM" – Particle particle particle mesh
- "Reaction" – Reaction field

</details>

<details class="note mc-property" id="pim.settings.charge-interaction.electric-dipole" markdown="1">
<summary><span class="mc-name">electric-dipole</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Attribute specifying the type of interaction associated with the local electric dipoles associated with particles.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Recommended: `Stockmayer`, `Screened`, `Long range`. Other values are allowed.

**Clarifications:**

- "Stockmayer" – Stockmayer potential
- "Screened" – Screened dipoles
- "Long range" – Long-range dipoles

</details>

<details class="note mc-property" id="pim.settings.charge-interaction.electric-dipole-variability" markdown="1">
<summary><span class="mc-name">electric-dipole-variability</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Attribute specifying the method for dynamically varying the local electric dipoles associated with discrete entities.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Recommended: `Induced`, `Isotropic`, `Anisotropic`. Other values are allowed.

**Clarifications:**

- "Induced" – Induced point dipoles
- "Isotropic" – Isotropic polarizability
- "Anisotropic" – Anisotropic polarizability

</details>

</details>

<details class="note mc-property" id="pim.settings.magnetic-interaction" markdown="1">
<summary><span class="mc-name">magnetic-interaction</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

The model used to describe the interactions between magnetic spins.

| Required | Repeatable |
|---|---|
| no | yes |

<details class="note mc-property" id="pim.settings.magnetic-interaction.spin-style" markdown="1">
<summary><span class="mc-name">spin-style<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The nature of the magnetic spins associated with the particles.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `Classical spin`, `Coupled spin lattice`. Other values are allowed.

**Clarifications:**

- "Classical spin" – Spins modeled as classical vectors evolved via the Landau–Lifshitz–Gilbert (LLG) equation defined by a spin Hamiltonian
- "Coupled spin lattice" – Classical spins whose spin Hamiltonian depends on the particle positions, so that the spins and the particles evolve together

Magnetism obtained from the electrons, e.g. by spin-polarized DFT or tight binding, is a computation of its own (method DFT or TB), which the computation that uses it names as an `input` with the role Interaction model.

</details>

<details class="note mc-property" id="pim.settings.magnetic-interaction.magnetic-dipole" markdown="1">
<summary><span class="mc-name">magnetic-dipole</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Attribute specifying the type of interaction (spin Hamiltonian) between the magnetic dipoles associated with particles.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Examples: `Heisenberg`, `Multi-spin`, `Zeeman`.

Note: The strength of an applied field is the condition `magnetic-field` in minimal `conditions`; a Zeeman term names its coupling to the spins.

</details>

</details>

<details class="note mc-property" id="pim.settings.training" markdown="1">
<summary><span class="mc-name">training</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

How the interatomic model was fitted to data.

| Required | Repeatable |
|---|---|
| no | no |

Note: Give it for a computation whose task is Training. A computation that uses the trained model names this one in `input` with the role Parameters; a model trained elsewhere is given as software.

<details class="note mc-property" id="pim.settings.training.training-data" markdown="1">
<summary><span class="mc-name">training-data</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

The information used for parameterizing the interatomic model.

| Required | Repeatable |
|---|---|
| no | yes |

<details class="note mc-property" id="pim.settings.training.training-data.name" markdown="1">
<summary><span class="mc-name">name<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Name of the training dataset used to train in the interatomic model.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="pim.settings.training.training-data.contents" markdown="1">
<summary><span class="mc-name">contents<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Description of the information included in the training dataset.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

**Clarifications:** E.g. DFT calculations or experiments, and what one item of the data is (a structure, a configuration), since size counts items.

</details>

<details class="note mc-property" id="pim.settings.training.training-data.source" markdown="1">
<summary><span class="mc-name">source</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Location from which the training data was obtained.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** A MatCore ID, web address, DOI, citation, or other description of where the data was obtained. Training data produced by a computation of the record is not given here: the training computation names it in minimal `computation › input` with the role Training data.

</details>

<details class="note mc-property" id="pim.settings.training.training-data.size" markdown="1">
<summary><span class="mc-name">size</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Number of items in the training dataset.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | int | [] | dimensionless | — |

Minimum: 1.

**Clarifications:** The kind of item is stated in contents.

</details>

<details class="note mc-property" id="pim.settings.training.training-data.data-preprocessing" markdown="1">
<summary><span class="mc-name">data-preprocessing</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Approach used for preliminary refining of raw, unformatted, or incomplete information into a structured and clean state suitable for modeling or analysis.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="pim.settings.training.training-data.missing-data" markdown="1">
<summary><span class="mc-name">missing-data</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Documentation of incomplete, null, or unrecorded entries within a feature set that hinder algorithm training.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** E.g. the percentage of missing data, and which fields are missing and why.

</details>

<details class="note mc-property" id="pim.settings.training.training-data.missing-data-strategy" markdown="1">
<summary><span class="mc-name">missing-data-strategy</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Approach used for filling in or removing blank, null, or unknown entries in a dataset.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="pim.settings.training.training-data.outlier-handling" markdown="1">
<summary><span class="mc-name">outlier-handling</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Approach to identifying and addressing extreme observations that deviate significantly from the general distribution to ensure they do not disproportionately skew model training.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="pim.settings.training.training-data.dataset-split" markdown="1">
<summary><span class="mc-name">dataset-split</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

A description of how information used to train the interatomic model was divided into subsets as part of the training process.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** In words, e.g. a random split of 80/10/10 into training, validation and test sets, a split stratified by composition, or k-fold cross-validation.

</details>

</details>

<details class="note mc-property" id="pim.settings.training.training-method" markdown="1">
<summary><span class="mc-name">training-method</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The approach used to determine the interatomic model's free parameters.

| Required | Repeatable |
|---|---|
| no | no |

<details class="note mc-property" id="pim.settings.training.training-method.training-procedure" markdown="1">
<summary><span class="mc-name">training-procedure<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The methodology used to determine the interatomic model's free parameters.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

**Clarifications:** E.g. the optimizer (Adam, L-BFGS, closed-form least squares), the learning-rate schedule, the stopping rule, and any active-learning loop with its selection criterion (e.g. query by committee, an uncertainty threshold). Explain the role of each hyperparameter entry.

</details>

<details class="note mc-property" id="pim.settings.training.training-method.loss-function" markdown="1">
<summary><span class="mc-name">loss-function</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The quantities fitted in training and how they are weighted.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** E.g. the mean squared error of formation energies, or a weighted sum of the errors in energies, forces and stresses with weights 1:100:10.

</details>

<details class="note mc-property" id="pim.settings.training.training-method.hyperparameter" markdown="1">
<summary><span class="mc-name">hyperparameter</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A fixed variable that controls the fitting of the interatomic model.

| Required | Repeatable |
|---|---|
| no | yes |

Note: For example, the learning rate, the batch size, the number of epochs or the early-stopping patience. Numbers that fix the model's architecture are architecture-parameter entries of the settings.

<details class="note mc-property" id="pim.settings.training.training-method.hyperparameter.name" markdown="1">
<summary><span class="mc-name">name<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The designation of the hyperparameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="pim.settings.training.training-method.hyperparameter.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The data associated with the hyperparameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | any | any | any | — |

</details>

<details class="note mc-property" id="pim.settings.training.training-method.hyperparameter.unit" markdown="1">
<summary><span class="mc-name">unit</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit in which the associated value is expressed.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning).

Note: Give it when the type of the value is float or int; omit it when it is string or bool.

</details>

<details class="note mc-property" id="pim.settings.training.training-method.hyperparameter.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

An explanation of the meaning, source, or purpose of the hyperparameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

</details>

<details class="note mc-property" id="pim.settings.training.training-method.transfer-learning" markdown="1">
<summary><span class="mc-name">transfer-learning</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Method used to migrate knowledge from previously mastered objectives to accelerate proficiency for the current training.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** E.g. fine-tuning, domain adaptation, multi-task learning or delta learning, with the details of how it was applied.

</details>

</details>

<details class="note mc-property" id="pim.settings.training.model-performance" markdown="1">
<summary><span class="mc-name">model-performance</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

An assessment of the reliability of the results of the interatomic model.

| Required | Repeatable |
|---|---|
| no | no |

<details class="note mc-property" id="pim.settings.training.model-performance.evaluation-method" markdown="1">
<summary><span class="mc-name">evaluation-method<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A description of the approach used to determine the reliability of the obtained results of the interatomic model.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | yes | string | [] | inapplicable | — |

**Clarifications:** E.g. a hold-out test set or k-fold cross-validation. Validation data serve to tune the model's hyperparameters or stop its training; test data, used for neither, assess it. The scores are metric entries.

</details>

<details class="note mc-property" id="pim.settings.training.model-performance.metric" markdown="1">
<summary><span class="mc-name">metric</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A score of the interatomic model on one subset of the data.

| Required | Repeatable |
|---|---|
| no | yes |

<details class="note mc-property" id="pim.settings.training.model-performance.metric.subset" markdown="1">
<summary><span class="mc-name">subset<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The data on which the score was measured.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `Training`, `Validation`, `Test`. Other values are allowed.

**Clarifications:**

- "Training" – The data the model's parameters were fitted to
- "Validation" – Data used to tune hyperparameters or to stop training
- "Test" – Data used in neither, which assesses the model

</details>

<details class="note mc-property" id="pim.settings.training.model-performance.metric.quantity" markdown="1">
<summary><span class="mc-name">quantity<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The target variable the score is for.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Examples: `Formation energy`, `Forces`.

</details>

<details class="note mc-property" id="pim.settings.training.model-performance.metric.measure" markdown="1">
<summary><span class="mc-name">measure<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The statistic used as the score.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `MAE`, `RMSE`, `R²`, `Accuracy`. Other values are allowed.

**Clarifications:**

- "MAE" – Mean absolute error
- "RMSE" – Root-mean-square error
- "R²" – Coefficient of determination
- "Accuracy" – Fraction of correct predictions, for a classification

</details>

<details class="note mc-property" id="pim.settings.training.model-performance.metric.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The value of the property, in the unit given by `unit`.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | float | [] | any | — |

</details>

<details class="note mc-property" id="pim.settings.training.model-performance.metric.unit" markdown="1">
<summary><span class="mc-name">unit<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit in which the associated value is expressed.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

**Clarifications:** A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning).

</details>

<details class="note mc-property" id="pim.settings.training.model-performance.metric.normalized-by" markdown="1">
<summary><span class="mc-name">normalized-by</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

What each value is divided by.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Recommended: `Atom`, `Formula unit`, `Cell volume`. Other values are allowed.

**Clarifications:**

- "Atom" – Divided by the number of atoms in the configuration
- "Formula unit" – Divided by the number of formula units in the configuration
- "Cell volume" – Divided by the volume of the cell

Note: Omit it for a value not divided by anything. The unit is that of the undivided quantity, e.g. eV for a total energy divided by the number of atoms.

</details>

</details>

<details class="note mc-property" id="pim.settings.training.model-performance.uncertainty-quantification" markdown="1">
<summary><span class="mc-name">uncertainty-quantification</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The method or process used to identify and measure the range of possible outcomes to assess the reliability of interatomic model predictions.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** E.g. Bayesian methods, dropout, ensemble methods or a Gaussian process. Say whether an uncertainty for each item is part of the dataset.

</details>

<details class="note mc-property" id="pim.settings.training.model-performance.applicability-domain" markdown="1">
<summary><span class="mc-name">applicability-domain</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Where the inputs the model is applied to lie relative to its training data.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

**Clarifications:** E.g. the elements, structure types or range of compositions the training data cover, and how inputs outside them were identified (a distance in feature space, an uncertainty threshold).

</details>

</details>

</details>

</details>

## Example: PIM Method-Specific Metadata

Dataset source: [https://doi.org/10.6084/m9.figshare.6273170](https://doi.org/10.6084/m9.figshare.6273170)

```json
{
  "pim": {
    "settings": [
      {
        "computation-label": [
          "finnis-sinclair"
        ],
        "theory-level": "Physics-based",
        "model-type": "Finnis-Sinclair potential",
        "particle-style": [
          "Atom"
        ],
        "bonding-type": "Reactive"
      }
    ]
  }
}
```

