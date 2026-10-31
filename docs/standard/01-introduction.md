# Material Core Metadata (MatCore) Standard

## 1. Preamble

## 1.1 Objectives

The *Material Core Metadata (MatCore)** *standard for computational materials science (CMS) represents key aspects of a material-focused computation to make it understandable to the broad materials research community. It provides pragmatic and workable guidelines for  documentation of materials data. 

The primary goals of the MatCore standard are, by outlining expectations for metadata accompanying a computational dataset, to facilitate: (1) dataset transparency, discoverability, sharing and reuse in theoretical and computational modeling, (2) verification and validation of materials modeling and simulation software, and (3) training physics-based and machine learning (ML) models for material behavior. An additional, more challenging, objective is to promote reproducibility in CMS by providing the information necessary for researchers to regenerate a published dataset.

## 1.2 Scope

The MatCore standard is focused on CMS methods aimed at computing material properties from a microscopic perspective, as opposed to computational methods in which the material is a component (such as engineering finite element analysis). The MatCore standard is designed to be flexible so that it can be extended to any area of CMS and can accommodate future changes in the field. An initial focus is placed on major CMS methods most widely used at the time of the creation of the standard with the aim of adding other methods in the future. The initial methods to be supported are:

- DFT: Density functional theory

- MD: Classical molecular dynamics

- MBPT: Many-body perturbation theory (GW/BSE)

- ML: Machine learning

- PF: Phase field

- DER: Derived properties from CMS calculations

All methods share a common minimal set of metadata defined by the MatCore standard. In addition, each method has its own MatCore extension, e.g. MatCore-DFT, MatCore-MD, etc., that inherits from the minimal MatCore metadata and adds additional method-specific metadata. 

It is allowable to include multiple method-specific metadata if used in concert. For example, an ab initio molecular dynamics (AIMD) dataset could include both MatCore-DFT and MatCore-MD metadata files to document both aspects of the computation.

## 1.3 Format

Each standard consists of a set of Properties with possible SubProperties, SubSubProperties, etc. The term “Property” will be used in the rest of this section to refer collectively to Property, SubProperty, etc. Properties have the following characteristics:

- Each Property has a name consisting of a series of one or more words all in lower case separated by hyphens. 

- Required Properties are indicated by an asterisk (*) appended to the end of the Property name.

- Properties have the following features:

- Definition: A short explanation of the nature of the Property. Best-practice is to not use words from the Property name in the definition to prevent circular definitions, except in cases where confusion is unlikely.

- Values: A description of the type of variable (string, integer, real), form (scalar, list, array), and possible values that the Property can take on. 

- When appropriate a controlled vocabulary can be defined. In this case sentence case format is adopted (i.e. for a phrase containing several words, the first letter of the first word is capitalized and all others are lower case except for proper names or acronyms). An option should always be added for users to add terms not included in the controlled vocabulary to allow the standard to support future developments. New terms may eventually be standardized and added to the controlled vocabulary.

- When a controlled vocabulary is used, adoption of existing standards is recommended whenever possible. 

- When a value has physical units, either the required unit must be specified, or a field provided to define the value units.

- For Properties that contain SubProperties, this is indicated with the phrase “Contains SubProperties as defined in the table below” (where “table below” points to the specification for the SubProperty standard).

- Repeatable: A boolean variable that is “True” for Properties that may appear multiple times inside the metadata file. For example, for a dataset created by more than one person, the creator Property can be repeated as many times as needed, each with its own SubProperties.

- Note(s): Additional clarifying information regarding a Property.

In addition to the required and optional Properties, other arbitrary Properties can be added to any MatCore Standard metadata files to support developments in the field. Such Properties may eventually be standardized and added to the MatCore Standard.

Examples are provided after each Standard specification in XML format. However, this is for clarification purposes only. The MatCore Standard serves as a conceptual and logical framework. It defines the schema for Properties required to ensure data consistency and interoperability. Critically, the MatCore Standard is implementation-agnostic. It dictates what information must be captured and how it should be structured logically, but it does not mandate a specific substrate, file format, or programming language.

A *serialization* is a file format (for example XML or JSON) together with the rules that map the MatCore data model onto it.

MatCore adopts [Semantic Versioning](https://semver.org/) (SemVer) three-part versioning system (major, minor, patch) to indicate Standard changes.

