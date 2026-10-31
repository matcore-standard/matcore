# 2.1 Minimal MatCore Metadata

\* = required property

### `creator*`

An entity (e.g. person, organization, software agent) responsible for generated the dataset and their institutional affiliation if relevant.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `name*`

The name of the entity that generated the dataset.

**Repeatable:** False

*Values (legacy text):* A string containing the entity name. Examples: "Albert Einstein", "Lawrence Livermore National Laboratory", "Claude Opus 5.5".

#### `affiliation`

The affiliation of the entity that generated the dataset if they have one.

**Repeatable:** True

*Values (legacy text):* A string containing the entity affiliation.

#### `creator-identifier`

A unique, persistent URI that globally and unambiguously identifies the entity that created the dataset.

**Repeatable:** True

*Values (legacy text):* For individuals, this includes an ORCID ID ([https://orcid.org](https://orcid.org)), for organizations, an ROR ID ([https://ror.org](https://ror.org)), for software or AI agents, a Digital Object Identifier (DOI) generated specifically for the software code or version (e.g., a Zenodo software DOI) or a Software Heritage ID (SWHID) pointing to the exact software release or state (e.g., swh:1:rel:a0b1c2d3e4f5...).

#### `affiliation-identifier`

A unique, persistent URI that globally and unambiguously identifies the entity's affiliation.

**Repeatable:** True

*Values (legacy text):* An ROR ID ([https://ror.org](https://ror.org)) or other suitable identifier.

### `contributor*`

An entity (e.g. person, organization, software agent) responsible for making contributions to the dataset and their institutional affiliation if relevant.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `name*`

The name of the entity that contributed to the dataset.

**Repeatable:** False

*Values (legacy text):* A string containing the entity name. Examples: "Albert Einstein", "Lawrence Livermore National Laboratory", "Claude Opus 5.5".

#### `affiliation*`

The affiliation of the entity that contributed to the dataset if they have one.

**Repeatable:** True

*Values (legacy text):* A string containing the entity affiliation.

#### `contributor-identifier`

A unique, persistent URI that globally and unambiguously identifies the entity that contributed to the dataset.

**Repeatable:** True

*Values (legacy text):* For individuals, this includes an ORCID ID ([https://orcid.org](https://orcid.org)), for organizations, an ROR ID ([https://ror.org](https://ror.org)), for software or AI agents, a Digital Object Identifier (DOI) generated specifically for the software code or version (e.g., a Zenodo software DOI) or a Software Heritage ID (SWHID) pointing to the exact software release or state (e.g., swh:1:rel:a0b1c2d3e4f5...).

#### `affiliation-identifier`

A unique, persistent URI that globally and unambiguously identifies the entity's affiliation.

**Repeatable:** True

*Values (legacy text):* An ROR ID ([https://ror.org](https://ror.org)) or other suitable identifier.

### `title*`

A single sentence description of the dataset.

**Repeatable:** False

*Values (legacy text):* A string containing the dataset title.

### `creation-date*`

The calendar date and time when the dataset was created.

**Repeatable:** False

*Values (legacy text):* A string containing the creation date in either format YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssz (where "z" indicates UTC time zone) format (following the [ISO 8601 Date and Time Format Standard](https://www.iso.org/iso-8601-date-and-time-format.html)).

### `description*`

A synopsis of the dataset, its contents, and purpose.

**Repeatable:** False

*Values (legacy text):* A string containing a description of the dataset contents. This can optionally include information on the format in which the dataset is stored (e.g. pointer to a relevant schema).

### `disclaimer`

A statement of applicability provided by the creator(s) informing users of the intended use and/or limitations of this dataset.

**Repeatable:** False

*Values (legacy text):* A string containing the dataset disclaimer.

### `material-component*`

A description of the chemical composition and structure of a substance in this dataset.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `constituent*`

A chemical element included in the material component and its concentration.

**Repeatable:** True

*Values (legacy text):* Contains SubSubProperties as defined in the table below.

##### `species*`

A chemical element included in the material.

**Repeatable:** False

*Values (legacy text):* A string containing the chemical designation of the element (e.g. "C").

##### `concentration*`

The fraction of the material composed of this element.

**Repeatable:** False

*Values (legacy text):* A string containing the concentration in percent.

#### `phase*`

The phase of the material included in the dataset.

**Repeatable:** False

*Values (legacy text):* A list of strings containing one or more of the following values: "Amorphous" – A solid material without crystalline order "Crystal" – A solid material characterized by a repeating pattern of atoms. "Quasicrystal" – A crystal-like material with short-range order, but without long-range order. "Molecule" – A finite group of atoms bonded together forming an independent unit. "Liquid" – A fluid structure (e.g. the molten state of a material) "Gas" – A structure where atoms are far apart and only interact during collisions. "Plasma" – A gas comprised of ions and electrons. Other user-specified value if none of the above apply.

#### `description`

An explanation of the nature of the material, e.g. a crystal structure designation, a chemical formula for a molecule, etc.

**Repeatable:** False

*Values (legacy text):* A string containing the material description.

#### `microstructure`

The arrangement of phases, grains and defects in a material.

**Repeatable:** False

*Values (legacy text):* A string containing a description of the microstructure of the material.

### `computation*`

A description of a computer simulation used to generate data in the dataset.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `method-class*`

The general category to which the computational technique belongs.

**Repeatable:** False

*Values (legacy text):* A string containing one of the following values: "Electronic" "Atomistic" "Mesoscopic" "Continuum" "Data-driven" Other user-specified value if none of the above apply.

> Note:The categories listed above are based on the [MODA standard](https://data.europa.eu/doi/10.2777/404734).

#### `method*`

The computational materials science (CMS) approach used in the computation.

**Repeatable:** False

*Values (legacy text):* A string containing one of the following values: For method-class "Electronic": "CC" – Coupled Cluster "QMC" – Quantum Monte Carlo "DFT" – Density Functional Theory "MBPT" – Many-Body Perturbation Theory methods (such as GW and BSE) For method-class "Atomistic": "MC" – Monte Carlo "MD" – Molecular Dynamics For method-class "Mesoscopic": "DDD" – Discrete Dislocation Dynamics "KMC" – Kinetic Monte Carlo "CGMD" – Coarse-grained MD For method-class "Continuum": "PF" – Phase Field For method-class "Data-driven": "ML" – Machine Learning Other user-specified value if none of the above apply.

#### `simulation-conditions*`

The interactions between the system being modeled and the rest of the world maintained during the computation.

**Repeatable:** False

*Values (legacy text):* Contains SubSubProperties as defined in the table below.

##### `type*`

The nature of the simulation being performed, whether equilibrium, nonequilibrium, or nonstandard.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values defining the simulation conditions: "Equilibrium" – Thermodynamic equilibrium "Nonequilibrium" – Conforming to some definition of nonequilibrium thermodynamics "Other" – A simulation not fitting into the equilibrium and nonequilibrium categories. Note 1: The SubSubProperties listed below (aside from description) are provided as appropriate given the nature of the simulation. Providing a SubSubProperty means that its value is imposed on the simulation as an external constraint. Note 2:Units for dimensioned variables are to be given in the SI unit system.

##### `description`

Explanatory text clarifying the simulation type selection.

**Repeatable:** False

*Values (legacy text):* A string containing the simulation type explanation.

##### `number-of-particles`

A count of atoms or other discrete entities comprising the material.

**Repeatable:** False

*Values (legacy text):* An integer containing the number of particles *N*.

*Standard units (legacy text):* dimensionless

##### `volume`

The amount of space occupied by the material.

**Repeatable:** False

*Values (legacy text):* A real number containing the volume *V*.

*Standard units (legacy text):* cubic meters (m^3)

##### `mass-density`

The total mass of the material divided by the volume it occupies.

**Repeatable:** False

*Values (legacy text):* A real number containing the mass density *𝜌*.

*Standard units (legacy text):* kilograms per cubic meter (kg/m^3)

##### `number-density`

The total number of particles comprising the material divided by the volume it occupies.

**Repeatable:** False

*Values (legacy text):* A real number containing the number density *n*.

*Standard units (legacy text):* inverse cubic meter (1/m^3)

##### `cell`

The domain occupied by the material in the simulation (if fixed).

**Repeatable:** False

*Values (legacy text):* Ordered list of three vectors (a, b, c), each with three components, that define the simulation cell. The vectors (a, b, c) need not be orthogonal, and the magnitudes (│a│, │b│, │c│) are the supercell vector lengths.

*Standard units (legacy text):* meter (m)

##### `cell-reference`

The domain occupied by the material in the simulation in configuration relative to which strains are defined.

**Repeatable:** False

*Values (legacy text):* Ordered list of three vectors (a0, b0, c0), each with three components, that define the cell used in the simulation in its reference configuration. The vectors (a0, b0, c0) need not be orthogonal, and the magnitudes (│a0│, │b0│, │c0│) are the reference cell vector lengths.

*Standard units (legacy text):* meter (m)

##### `cell-periodicity`

Specification of whether periodic boundary conditions are applied along the cell vector directions. This applies to both cell and cell-reference.

**Repeatable:** False

*Values (legacy text):* Ordered list of three booleans (*pa*,, *pb*,, *pc*,), which are set to true if periodic boundary conditions are applied along the corresponding cell vectors (a, b, c).

*Standard units (legacy text):* dimensionless

##### `temperature`

A measure of the hotness or coldness of an external heat bath in thermal contact with the material.

**Repeatable:** False

*Values (legacy text):* A real number containing the temperature *T*.

*Standard units (legacy text):* kelvin (K)

##### `stress`

A uniform force per unit current area, including both normal and shear components, applied to the material during the simulation through contact with an external loading device.

**Repeatable:** False

*Values (legacy text):* An array of six real numbers containing the components of the (symmetric) Cauchy stress tensor σ in the following order: [*σ*11, *σ*22, *σ*33, *σ*23, *σ*13, *σ*12]. The stress component are expressed relative to an orthonormal basis (e1, e2, e3), where e1 is in the direction of a, e2 is in the direction of c╳a, and e3= e1╳e2, where (a, b, c) are the vectors defining the cell, which may not be orthogonal. Note 1: Requires the definition of the cell subproperty in order for a basis to be defined relative to which the tensor components are given. Note 2:The adopted sign convention is for tensile normal stresses to be positive, and compressive normal stresses to be negative. This implies that for a material subjected to a positive pressure *p*, the stress tensor components are [-*p*, -*p*, -*p*, 0, 0, 0].

*Standard units (legacy text):* pascal (Pa)

##### `strain`

A deformation relative to a reference configuration imposed on the simulation cell expressed in the referential frame (Lagrangian strain tensor).

**Repeatable:** False

*Values (legacy text):* An array of six real numbers containing the components of the (symmetric) Lagrangian strain tensor Ein the following order: [*E*11, *E*22, *E*33, *E*23, *E*13, *E*12]. The strain component are expressed relative to an orthonormal basis (e1, e2, e3), where e1 is in the direction of a0, e2 is in the direction of c0╳a0, and e3= e1╳e2, where (a0, b0, c0) are the vectors defining the cell in the reference configuration, which may not be orthogonal. Note: Requires the definition of cell-reference in order for the basis to be defined relative to which the tensor components are given.

*Standard units (legacy text):* dimensionless

##### `strain-rate`

The derivative with respect to time of a deformation relative to a reference configuration imposed on the simulation cell expressed in the referential frame (Lagrangian strain rate tensor), which is constant throughout the simulation.

**Repeatable:** False

*Values (legacy text):* An array of six real numbers containing the components of the (symmetric) Lagrangian strain rate tensor E in the following order: [*E11, E22, E33, E23, E13, E12,*]. The strain component are expressed relative to an orthonormal basis (e1, e2, e3), where e1 is in the direction of a0, e2 is in the direction of c0╳a0, and e3= e1╳e2, where (a0, b0, c0) are the vectors defining the cell in the reference configuration, which may not be orthogonal.

*Standard units (legacy text):* dimensionless

> Requires the definition of cell-reference in order for the basis to be defined relative to which the tensor components are given

##### `heat-flux`

The amount of thermal energy transferred to the material per unit area per unit time along a given direction.

**Repeatable:** False

*Values (legacy text):* An array of three real numbers containing the components of the heat flux vector q. The heat flux component are expressed relative to an orthonormal basis (e1, e2, e3), where e1 is in the direction of a, e2 is in the direction of c╳a, and e3= e1╳e2, where (a, b, c) are the vectors defining the cell, which may not be orthogonal.

*Standard units (legacy text):* watts per square meter (W/m^2)

##### `temperature-gradient`

A physical quantity that describes the rate and direction of maximum temperature change per unit distance.

**Repeatable:** False

*Values (legacy text):* An array of three real numbers containing the components of the temperature gradient vector ∇*T*. The temperature gradient component are expressed relative to an orthonormal basis (e1, e2, e3), where e1 is in the direction of a, e2 is in the direction of c╳a, and e3= e1╳e2, where (a, b, c) are the vectors defining cell, which may not be orthogonal.

*Standard units (legacy text):* watts per square meter (K/m)

#### `software*`

Identification of a computer package used to perform the calculations.

**Repeatable:** True

*Values (legacy text):* Contains SubSubProperties as defined in the table below.

##### `name*`

The name of the software package.

**Repeatable:** False

*Values (legacy text):* A string containing the name of the software package (e.g. "VASP").

##### `version`

The version of the software package.

**Repeatable:** False

*Values (legacy text):* A string containing the software version (e.g. "6.3.1")

##### `file`

Input or output file for the software package associated with the computation. This includes the input file used to perform the computation, associated data files, and output generated by the software package. Most important are input files to enable reproduction of the dataset.

**Repeatable:** True

*Values (legacy text):* Contains SubSubSubProperties as defined in the table below.

###### `name*`

The file name.

**Repeatable:** False

*Values (legacy text):* A string containing the name of the included file.

###### `description*`

A brief description of the file and its contents.

**Repeatable:** False

*Values (legacy text):* A string containing the file description.

###### `contents`

The text and/or data contained in the file. Not required in case a link to the file is provided instead.

**Repeatable:** False

*Values (legacy text):* A string containing the file contents.

###### `link`

A URI pointing to a permanent location of the file online.

**Repeatable:** False

*Values (legacy text):* A string containing the file URI.

### `citation`

Information that uniquely identifies a source being acknowledged.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `reference*`

Text that uniquely identifies the source of information being cited.

**Repeatable:** False

*Values (legacy text):* A string containing the reference to the source.

#### `doi`

The digital object identifier (DOI) for the source.

**Repeatable:** False

*Values (legacy text):* A string containing the source DOI.

#### `link`

A URI pointing to a permanent location of the source.

**Repeatable:** False

*Values (legacy text):* A string containing the file URI.

### `funding`

Information about received monetary support or other resources to generate the dataset.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `award-title*`

Name of the grant that provided funding to generate the dataset.

**Repeatable:** False

*Values (legacy text):* A string containing the award title.

#### `funder*`

The name of the funding agency that provided money and/or resources to generate the dataset.

**Repeatable:** False

*Values (legacy text):* A string containing the funding agency using [Crossref Open Funder Registry](https://www.crossref.org/services/funder-registry/) designation.

#### `award-number`

A funder identifier for the grant.

**Repeatable:** False

*Values (legacy text):* A string containing the award number.

### `related-content`

Other datasets that are connected to the current one in some manner.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `links*`

Pointer to one or more related datasets.

**Repeatable:** False

*Values (legacy text):* A list of permanent pointers to related datasets (such as MatCore IDs, DOIs, URIs, etc.)

#### `description`

Explanation of the relationship between the related content and the current dataset.

**Repeatable:** False

*Values (legacy text):* A string containing a description of the related content.

### `provenance`

History of the dataset, detailing its origins and transformations.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `event-type*`

Description of change made to the dataset.

**Repeatable:** False

*Values (legacy text):* A string containing one of the following values: "Initial creation" – Initial creation of the dataset "Admin update" – Editorial update to the dataset not requiring a version update (e.g. spelling correction). "Version update" – Change to the dataset or associated files requiring a new version "Metadata update" – Change to the metadata, but not the dataset itself. Other user-specified value if none of the above apply.

#### `date*`

The date and time when the change was made.

**Repeatable:** False

*Values (legacy text):* A string containing the creation date in either format YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssz (where "z" indicates UTC time zone) format (following the [ISO 8601 Date and Time Format Standard](https://www.iso.org/iso-8601-date-and-time-format.html)).

#### `agent*`

Identity of the entity responsible for the change.

**Repeatable:** False

*Values (legacy text):* A string containing the name or other designation identifying who or what is responsible for the change.

#### `comments`

Explanation for the change in provenance.

**Repeatable:** False

*Values (legacy text):* A string containing an explanation for the nature of the changes leading to the revised provenance.

#### `checksum`

A digital fingerprint for the dataset of associated files.

**Repeatable:** False

*Values (legacy text):* A list containing two strings: The name of a file, and the checksum for the file (e.g. the SHA-256 encoding for file).

### `matcore-id*`

An identifier for the dataset.

**Repeatable:** False

*Values (legacy text):* A string containing the MatCore identifier.

### `matcore-date*`

The calendar date and time when this MatCore document was created.

**Repeatable:** False

*Values (legacy text):* A string containing the creation date in either format YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssz (where "z" indicates UTC time zone) format (following the [ISO 8601 Date and Time Format Standard](https://www.iso.org/iso-8601-date-and-time-format.html)).

### `license*`

A contract defining the terms and conditions under which the dataset can be used.

**Repeatable:** False

*Values (legacy text):* A string containing the dataset license in a format conforming to the [SPDX](https://spdx.org/licenses/)[ Standard](https://spdx.org/licenses/).
