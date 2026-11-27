<p class="mc-doc-title">Material Core Metadata (MatCore) Standard</p>

<!-- BEGIN generated: version from schema/releases.yaml by scripts/build_docs.py; do not edit -->
<p class="mc-version" data-version="0.8.1">Version 0.8.1</p>
<!-- END generated -->

# 1. Preamble

## 1.1 Objectives

The *Material Core Metadata (MatCore)* standard for computational materials science (CMS) represents key aspects of a material-focused computation to make it understandable to the broad materials research community. It provides pragmatic and workable guidelines for documentation of materials data. Its goals are to make computational materials data FAIR (findable, accessible, interoperable and reusable) and to contribute to its AI readiness.

The primary goals of the MatCore standard are, by outlining expectations for metadata accompanying a computational dataset, to facilitate: (1) dataset transparency, discoverability, sharing and reuse in theoretical and computational modeling, (2) verification and validation of materials modeling and simulation software, and (3) training physics-based and machine learning (ML) models for material behavior. An additional, more challenging, objective is to promote reproducibility in CMS by providing the information necessary for researchers to regenerate a published dataset.

## 1.2 Scope

The MatCore standard is focused on CMS methods aimed at computing material properties from a microscopic perspective, as opposed to computational methods in which the material is a component (such as engineering finite element analysis). The MatCore standard is designed to be flexible so that it can be extended to any area of CMS and can accommodate future changes in the field. An initial focus is placed on major CMS methods most widely used at the time of the creation of the standard with the aim of adding other methods in the future. The initial methods to be supported are:

- DFT: Density functional theory

- PIM: Particle interaction models

- PS: Particle simulation (molecular dynamics, molecular statics, Monte Carlo and related methods)

- MBPT: Many-body perturbation theory (GW/BSE)

- ML: Machine learning

- PF: Phase field

- DP: Derived properties from CMS calculations

All methods share a common minimal set of metadata defined by the MatCore standard. In addition, each method has its own MatCore extension, e.g. MatCore-DFT, MatCore-PS, etc., that inherits from the minimal MatCore metadata and adds additional method-specific metadata. 

Some methods supply energies and forces (e.g. DFT, or an interatomic potential), others use them to sample or evolve a system (e.g. MD). A dataset is described as one or more computations, each a group of calculations that share a method and its settings. A computation that uses the results of another names it, with the role the other plays: an ab initio molecular dynamics (AIMD) computation names the DFT computation that supplies its energies and forces. Each method-specific section describes the computations of its method. MatCore describes a dataset; it does not record how to reproduce its execution. The order of the calculations, their control flow and complete inputs belong to the provenance record of a workflow manager, to which a MatCore record may point.

The parts of a record hold different kinds of metadata. The top-level Properties of the minimal metadata describe the dataset: its title, creators, license and provenance. `structure` describes the modeled system. `computation` describes each computation: its method, task, inputs, imposed conditions and software. The method-specific sections give the settings of each computation, and the derived section the properties obtained from the results. The results themselves are in the dataset.

MatCore is a reporting standard: it says what the metadata of a dataset must contain and how it is structured. It is not an ontology. Its Properties are defined in words, and they can be aligned with ontologies and richer schemas through mappings.

## 1.3 Format

Each standard consists of a set of Properties with possible SubProperties, SubSubProperties, etc. The term “Property” will be used in the rest of this section to refer collectively to Property, SubProperty, etc. Properties have the following characteristics:

- Each Property has a name consisting of a series of one or more words all in lower case separated by hyphens. 

- Required Properties are indicated by an asterisk (*) appended to the end of the Property name.

- Properties have the following features:

    - Definition: A short explanation of the nature of the Property. Best-practice is to not use words from the Property name in the definition to prevent circular definitions, except in cases where confusion is unlikely.

    - Type: The data type of the Property's value: string, float, int, bool, file, or any (the instance states the type). A Property that only contains SubProperties has no type.

    - Extent: The shape of the value, in the notation of the Knowledgebase of Interatomic Models (KIM): [] for a scalar, [3,3] for a 3×3 array, [:] for a list of any length, or any when the schema does not fix it. A value with more than one dimension is a list of lists, the first index outermost: a value of extent [n,m] is a list of n entries, each a list of m components. A serialization preserves this nesting.

    - Values: The values the Property can take on, such as a controlled vocabulary, bounds, a format or a pattern, with examples.

        - When appropriate a controlled vocabulary can be defined. In this case sentence case format is adopted (i.e. for a phrase containing several words, the first letter of the first word is capitalized and all others are lower case except for proper names or acronyms). An option should always be added for users to add terms not included in the controlled vocabulary to allow the standard to support future developments. New terms may eventually be standardized and added to the controlled vocabulary.

        - When a controlled vocabulary is used, adoption of existing standards is recommended whenever possible. 

        - A Property either has a value of its own or has SubProperties, never both. A physical quantity (a value whose Kind is neither "dimensionless" nor "inapplicable") is therefore a Property with two SubProperties, `value` and `unit`. In the Standard, `value` defines the Type, Extent, Kind and Recommended unit of the quantity. In a metadata instance, `value` holds the quantity and `unit` holds the unit in which it is expressed; `unit` SHALL be given, and SHALL be a symbol from the MatCore Unit Table (Annex U) whose Kind is compatible with the Kind of `value`. A property value without a `unit`, or with a unit incompatible with its Kind, is non-conformant; no default unit is ever implied. The Recommended unit listed for each property is informative and does not affect how values are interpreted. A pure number (a ratio, a fraction or a count) has the Kind `dimensionless`; it is a Property with a value of its own and carries no `unit`. Where a `unit` is given for a pure number, as in a generic parameter or a nondimensional length, it is the reserved symbol `dimensionless`. Plane angles use an angle unit (`rad` or `degree`). Where the meaning of a value depends on a convention that a unit cannot express (e.g. inclusion of a factor 2π in reciprocal lengths, or components given in a lattice basis), the property has a `convention` or `basis` subproperty, required as stated in its description. Some units (`bohr`, `hartree`, `Ry`) are defined through measured physical constants, so their values in SI units change slightly each time the Committee on Data of the International Science Council (CODATA) revises those constants; MatCore uses the CODATA 2022 values listed in Annex U.

        - A *generic parameter* holds a parameter whose meaning the Standard does not fix, such as a parameter of an exchange-correlation functional. It is a Property with four SubProperties, in this order: `name` (required), the designation of the parameter; `value` (required), whose Type, Extent and Kind are `any`, the metadata instance stating its type (float, int, string or bool) and its unit; `unit`, given when the value's type is float or int and omitted when it is string or bool, a symbol from the MatCore Unit Table (Annex U), the reserved symbol `dimensionless`, or, if and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning); and `description` (optional), an explanation of the parameter.

        - A Property that contains SubProperties shows them nested within it.

    - Kind: The physical dimension of the Property's value, given as a MatCore Kind name (e.g. Energy, Length, InverseLength, Temperature, Pressure) mapped in Annex U to a QuantityKind Internationalized Resource Identifier (IRI) of QUDT, an ontology of quantities, quantity kinds, units, dimensions and data types. Reserved values: `dimensionless` (ratios, counts), `inapplicable` (strings, identifiers, and the `unit` subproperty itself), `any` (a `value` whose Kind is given by the instance `unit`, as in a generic parameter).

    - Recommended unit: The unit customarily used for this Property in the community. Informative only; used by templates and tools.

    - Repeatable: A boolean variable that is “True” for Properties that may appear multiple times inside the metadata file. For example, for a dataset created by more than one person, the creator Property can be repeated as many times as needed, each with its own SubProperties.

    - Note(s): Additional clarifying information regarding a Property.

A Property is identified by its path: the key of its section followed by the names leading down to it, joined by full stops, e.g. `dft.settings.xc-functional`. The path is the Property's address on the page of its section, and the permalink of a Property cites its definition in one version of the Standard.

In addition to the required and optional Properties, a metadata file may add Properties of its own, at any level, to support developments in the field. Their names begin with the prefix `x-`, e.g. `x-beamline`, which no Property of the Standard uses, so that they cannot be mistaken for the Standard's. Such Properties may eventually be standardized and added to the MatCore Standard.

Examples are provided after each Standard specification in JSON, the first serialization adopted for MatCore instances. However, this is for clarification purposes only. The MatCore Standard serves as a conceptual and logical framework. It defines the schema for Properties required to ensure data consistency and interoperability. Critically, the MatCore Standard is implementation-agnostic. It dictates what information must be captured and how it should be structured logically, but it does not mandate a specific substrate, file format, or programming language.

MatCore adopts [Semantic Versioning](https://semver.org/) (SemVer) three-part versioning system (major, minor, patch) to indicate Standard changes.

A change to the Standard, such as a new, renamed or removed Property, or the adoption of a Property added with the prefix `x-`, is proposed as an issue or pull request in the MatCore repository on GitHub. It is reviewed by the members of the [Standard Committee](../leadership.md) responsible for the section it concerns, and decided by the Committee. Renaming or removing a Property is a breaking change and is listed in the Revision History.


## 1.4 Serialization

A *serialization* is a file format (for example XML or JSON) together with the rules that map the MatCore data model onto it. The Standard defines the data model; a serialization says how a record of it is written in a file.

A serialization conforms to the Standard when a record written in it can be read back into the data model without loss. To that end it SHALL:

- keep the Properties of each section apart from those of the others, since a Property name may recur in two sections;
- name each Property by its name, and keep its SubProperties nested within it;
- tell a Property given once from a repeatable Property given as entries, even when there is a single entry;
- write each value in its Type, and a value whose Extent lists dimensions as nested lists, the first index outermost;
- state the type of a generic parameter's value (float, int, string or bool) where the format does not show it;
- leave out an optional Property that is not given, rather than write an empty value.

JSON is the first serialization adopted for MatCore records. It is defined by Request for Comments (RFC) 8259 of the Internet Engineering Task Force. A MatCore record in JSON is a file encoded in UTF-8, with the extension `.json`, that maps the data model as follows:

- The record is an object with one member for each section it uses, named by the key of its section: `minimal`, `dft`, `pim`, `ps`, `mbpt`, `ml`, `pf`, `derived`. Each member holds the Properties of its section. The member `minimal` is always present.
- A Property is a member named by the Property's name. A Property with SubProperties is an object. A value is a string, `true` or `false`, or a number, as its Type is string, bool, or float or int; an int is written without a fraction or an exponent.
- A repeatable Property is always an array of entries, even with one entry. A Property that is not repeatable is never an array of entries.
- A value whose Extent lists dimensions is nested arrays, the first index outermost: Extent [3] is an array of 3 numbers, and Extent [3,3] an array of 3 arrays of 3 numbers.
- An optional Property that is not given is omitted; `null` is not written.
- A generic parameter's object has one more member, `type`, holding `float`, `int`, `string` or `bool`, since JSON writes 4 and 4.0 alike.
- A Property added by the record is a member whose name begins with `x-`, holding any value.
- Members may appear in any order; a writer should follow the order of the Standard.

A [JSON Schema](https://json-schema.org/) generated from this version of the Standard, [matcore.schema.json](matcore.schema.json), describes a valid MatCore record in JSON. Any JSON Schema validator can check a record against it: its structure, the Type and Extent of each value, and that each unit fits its Kind. It does not check what lies beyond a JSON Schema, such as the spelling of a chemical formula or whether a label refers to a computation in the record.
