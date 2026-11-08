# 2.7 Derived Property Metadata

<p class="mc-version" data-version="0.6.0">Version 0.6.0</p>

The metadata for derived properties (MatCore-Der) is tabulated below. This refers to properties computed from data generated using a CMS method documented elsewhere in this section (e.g. spectroscopy computations based on DFT data). (Notes: (1) This standard inherits the metadata in the minimal MatCore standard and one of the associated methods metadata, adding the properties below. (2) Derived properties in this category are limited to properties based on a single method. Derived properties involving a combination of multiple methods (e.g. MD and ML) are not supported. An exception is MBPT, which itself is based on DFT.)

Examples of derived properties include:

- Electronic (band structure, density of states (DOS), projected DOS, dielectric function, charge and bonding analysis, etc.)
- Electron-phonon interactions (superconducting properties, line widths, etc.)
- Linear-response (phonon modes, dispersion, interatomic force constants, vibrational DOS, etc.)
- Magnetic (magnetics, magnetization, magnons, etc.)
- Microscopy, electron (S/TEM, 4D-STEM, SAED, etc.)
- Microscopy, scanning probe (STM, AFM, etc.)
- NMR (chemical shifts)
- Optical (electronic excitation spectra, low-loss EELS, etc.)
- Spectroscopy, core-level (XAS, XES, core-loss EELS, XPS, etc.)
- Spectroscopy, vibrational (Raman, Infrared spectroscopy, etc.)
- Transport (electronic conductivity, thermal conductivity, etc.)
- X-ray scattering (diffraction, reflectivity, pair-distribution function, etc.)

<span class="mc-legend"><span class="mc-key"><span class="mc-star">*</span> required</span><span class="mc-key"><span class="mc-icon mc-i-once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span> appears at most once</span><span class="mc-key"><span class="mc-icon mc-i-rep"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span> repeatable</span></span>

<details class="note mc-property" id="derived.derived-property" markdown="1">
<summary><span class="mc-name">derived-property<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

Details of a quantity related to material behavior computed based on a computational materials science (CMS) calculation covered by the MatCore standard.

| Required | Repeatable |
|---|---|
| yes | yes |

<details class="note mc-property" id="derived.derived-property.type" markdown="1">
<summary><span class="mc-name">type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Kind of physical quantity being computed.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | — | — | — | — |

<span class='legacy'>Legacy: String one of the following values that defines the type of the computed derived property: "Electronic" "Electron-phonon interactions" "Linear-response" "Magnetic" "Microscopy, electron" "Microscopy, scanning probe" "NMR" "Optical" "Spectroscopy, core-level" "Spectroscopy, vibrational" "Transport" "X-ray scattering" Other user-specified value if none of the above apply.</span>

</details>

<details class="note mc-property" id="derived.derived-property.description" markdown="1">
<summary><span class="mc-name">description<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Explanation of the derived property.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | — | — | — | — |

<span class='legacy'>Legacy: A string containing an explanation of the specific derived property that was computed.</span>

</details>

<details class="note mc-property" id="derived.derived-property.calculation-method" markdown="1">
<summary><span class="mc-name">calculation-method<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

Details regarding an approach used to obtain the derived property. Multiple approaches may be involved in the computation.

| Required | Repeatable |
|---|---|
| yes | yes |

<details class="note mc-property" id="derived.derived-property.calculation-method.description" markdown="1">
<summary><span class="mc-name">description<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Description of the method used to obtain the derived property.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | — | — | — | — |

<span class='legacy'>Legacy: A string containing a human-readable description of the approach and/or algorithm used to compute the derived property.</span>

</details>

<details class="note mc-property" id="derived.derived-property.calculation-method.calculation-parameter" markdown="1">
<summary><span class="mc-name">calculation-parameter</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A parameter associated with the specified calculation method.

| Required | Repeatable |
|---|---|
| no | yes |

<details class="note mc-property" id="derived.derived-property.calculation-method.calculation-parameter.name" markdown="1">
<summary><span class="mc-name">name<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The designation of the parameter associated with the specified derived property calculation method.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | — | — | — | — |

<span class='legacy'>Legacy: A string containing the name of the calculation parameter.</span>

</details>

<details class="note mc-property" id="derived.derived-property.calculation-method.calculation-parameter.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The data associated with the calculation parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | — | — | — | — |

<span class='legacy'>Legacy: An integer, real, boolean, or string containing the calculation parameter value.</span>

</details>

<details class="note mc-property" id="derived.derived-property.calculation-method.calculation-parameter.unit" markdown="1">
<summary><span class="mc-name">unit<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

A standardized string or identifier that defines the dimension or measurement system of the associated value.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | — | — | — | — |

<span class='legacy'>Legacy: A string containing the units of the value in the [GNU unit convention](https://www.gnu.org/software/units/) (or the text "dimensionless").</span>

</details>

<details class="note mc-property" id="derived.derived-property.calculation-method.calculation-parameter.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

An explanation of the meaning, source, or purpose of the calculation parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: A string explaining the computation parameter (e.g. "The spin-spin coupling constant for an NMR spectroscopy calculation").</span>

</details>

</details>

</details>

</details>

## Example: Derived Property Metadata

Dataset source: [https://archive.materialscloud.org/record/2024.116](https://archive.materialscloud.org/record/2024.116)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <derived-property>
    <type>Spectroscopy, vibrational</type>
    <description>Raman spectra plots of intensity versus wavenumber (frequency) representing inelastic light scattering (Raman effect) from a sample.</description>
    <calculation-method>
      <description>The Raman spectra is obtained in two steps: (1) Phonon eigenmodes and frequencies are computed for a given crystalline material within the harmonic approximation using force constants derived from density functional theory (DFT). (2) The Raman tensor is obtained by numerically differentiating the electronic susceptibility with respect to atomic displacements along each vibrational mode and using these tensors to compute Raman scattering intensities for all Raman-active modes, ultimately yielding a full Raman spectrum after appropriate averaging and broadening.</description>
    </calculation-method>
  </derived-property>
</root>
```

