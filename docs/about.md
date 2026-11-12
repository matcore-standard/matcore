# About MatCore

The *Material Core Metadata (MatCore)* standard for computational materials science (CMS) represents key aspects of a material-focused computation to make it understandable to the broad materials research community. It provides pragmatic and workable guidelines for documentation of materials data.

## Goals

The primary goals of the MatCore standard are, by outlining expectations for metadata accompanying a computational dataset, to facilitate:

- Dataset transparency, discoverability, sharing and reuse in theoretical and computational modeling.
- Verification and validation of materials modeling and simulation software.
- Training physics-based and machine learning models for material behavior.
- Promote reproducibility in CMS by providing the information necessary for researchers to regenerate a published dataset.

## Scope

The MatCore standard is focused on CMS methods aimed at computing material properties from a microscopic perspective, as opposed to computational methods in which the material is a component (such as engineering finite element analysis). The MatCore standard is designed to be flexible so that it can be extended to any area of CMS and can accommodate future changes in the field. An initial focus is placed on major CMS methods most widely used at the time of the creation of the standard with the aim of adding other methods in the future. The initial methods to be supported are:

- Density functional theory
- Many-body perturbation theory (GW, BSE)
- Machine learning for materials
- Molecular dynamics
- Phase field
- Derived approaches involving a combination of other methods

## Standard

All methods share a common minimal set of metadata defined by the MatCore standard. The minimal MatCore metadata includes aspects of a dataset deemed important to report for data findability and reuse and are *universal* across all computational methods. In addition, each method has its own MatCore extension, e.g. MatCore-PS, MatCore-DFT, etc., that inherits from the minimal MatCore metadata and adds additional method-specific metadata.

## More Information and Citing

For more information, and to cite, see [Greenberg et al., "Towards MatCore: A Unified Metadata Standard for Materials Science", arXiv:2502.07106, 2025](https://doi.org/10.48550/arXiv.2502.07106).

## Funding

The MatCore effort is funded by the National Science Foundation, Division of Materials Research (DMR) through [Award #2404283](https://www.nsf.gov/awardsearch/show-award?AWD_ID=2404283) and supported through the [KIM Initiative](https://openkim.org).
