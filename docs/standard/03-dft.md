# 2.2 Density Functional Theory (DFT) Metadata

<p class="mc-version" data-version="0.5.0">Version 0.5.0</p>

The metadata for density functional theory (DFT) data (MatCore-DFT) is tabulated below. This includes the level of theory (exchange-correlation functional, core-electron model, and valence-electron model) and associated parameters. (Note: This standard inherits the metadata in the minimal MatCore standard, adding the properties below.)

<span class="mc-legend"><span class="mc-key"><span class="mc-star">*</span> required</span><span class="mc-key"><span class="mc-icon mc-i-once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span> appears at most once</span><span class="mc-key"><span class="mc-icon mc-i-rep"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span> repeatable</span></span>

<details class="note mc-property" id="dft.xc-functional" markdown="1">
<summary><span class="mc-name">xc-functional<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

Approximation used to describe the electron exchange and electron correlation energies

| Required | Repeatable |
|---|---|
| yes | yes |

<details class="note mc-property" id="dft.xc-functional.type" markdown="1">
<summary><span class="mc-name">type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The mathematical form of the exchange-correlation functional.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `LDA`, `GGA`, `Meta GGA`, `Hybrid`, `ML`. Other values are allowed. "LDA" – Local Density Approximation. "GGA" – Generalized Gradient Approximation. "Meta GGA" – Extension to GGA including dependence on Laplacian of electron density. "Hybrid" – An approximation for the exchange-correlation (XC) functional that includes a portion of the exact XC from Hartree–Fock theory or machine learning with the rest coming from other sources (ab initio or empirical). "ML" – Machine learning based functional.

</details>

<details class="note mc-property" id="dft.xc-functional.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Explanatory text providing more information about the type of the exchange-correlation method used including any relevant identifying information.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Examples of possible content by type: LDA: Common parameterizations: VWN, PW92, etc. GGA: Typical choices are PW91, PBE, rPBE, revPBE, BLYP, etc. Meta GGA: Specific named examples include TPSS, SCAN, M06, etc. Hybrid: B3LYP, PBE0, HSE03, HSE06, NeuralXC, DeePKS, … ML: DM21, NNLDA, NNGGA, CIDER, etc. Others: BEEF, VdW-corrections (added on top of XC, e.g., D2, D3, D4), etc. LibXC designation: LibXC:LDA_C_GK72 (include source as prefix).

</details>

<details class="note mc-property" id="dft.xc-functional.xc-parameter" markdown="1">
<summary><span class="mc-name">xc-parameter</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A fixed variable associated with the specified exchange-correlation functional method.

| Required | Repeatable |
|---|---|
| no | yes |

Note: For example, the mixing parameter of a hybrid exchange-correlation functional, or another method-specific parameter.

<details class="note mc-property" id="dft.xc-functional.xc-parameter.name" markdown="1">
<summary><span class="mc-name">name<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The designation of the exchange-correlation parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="dft.xc-functional.xc-parameter.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The data associated with the exchange-correlation parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | any | any | any | — |

</details>

<details class="note mc-property" id="dft.xc-functional.xc-parameter.unit" markdown="1">
<summary><span class="mc-name">unit<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit in which the associated value is expressed.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning).

</details>

<details class="note mc-property" id="dft.xc-functional.xc-parameter.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

An explanation of the meaning, source, or purpose of the parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

</details>

</details>

<details class="note mc-property" id="dft.core-electron-model" markdown="1">
<summary><span class="mc-name">core-electron-model<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Model of the electrons used in the calculation.

| Required | Repeatable |
|---|---|
| yes | no |

<details class="note mc-property" id="dft.core-electron-model.type" markdown="1">
<summary><span class="mc-name">type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The method used to model the electrons.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `All Electron`, `LAPW`, `Pseudopotential`, `PAW`. Other values are allowed. "All Electron" – All of the electrons in an atom are modeled explicitly. "LAPW" – Linearized Augmented Plane Wave. "Pseudopotential" – Valence electrons are treated explicitly, and core electrons are modeled by a simplified potential. "PAW" – Projector Augmented Wave.

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential" markdown="1">
<summary><span class="mc-name">pseudopotential</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

For type "Pseudopotential", or type "PAW", additional information about the pseudopotentials.

| Required | Repeatable |
|---|---|
| no | yes |

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.name" markdown="1">
<summary><span class="mc-name">name<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The name of the pseudopotential.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.type" markdown="1">
<summary><span class="mc-name">type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The physical form of the pseudopotential.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `Norm conserving`, `Ultrasoft`. Other values are allowed.

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Explanatory text about the pseudopotential including any relevant identifying information.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.number-of-valence-electrons" markdown="1">
<summary><span class="mc-name">number-of-valence-electrons<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The number of electrons treated explicitly.

| Required | Repeatable |
|---|---|
| yes | no |

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.number-of-valence-electrons.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The value of the property, in the unit given by `unit`.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | int | [] | dimensionless | dimensionless |

Minimum: 1.

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.number-of-valence-electrons.unit" markdown="1">
<summary><span class="mc-name">unit<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit of the value, an Annex U symbol whose Kind is the Kind of `value`.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

The only allowed unit is `dimensionless`.

</details>

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.repository" markdown="1">
<summary><span class="mc-name">repository</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The database from which the pseudopotential was obtained.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.version" markdown="1">
<summary><span class="mc-name">version</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The version of the pseudopotential.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Examples: `6.3.1`.

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.doi" markdown="1">
<summary><span class="mc-name">doi</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The digital object identifier (DOI) for the pseudopotential.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Pattern: `https://doi\.org/10\.[^/]+/.+`.

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.checksum" markdown="1">
<summary><span class="mc-name">checksum</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

A digital fingerprint of the pseudopotential file, computed by a named algorithm.

| Required | Repeatable |
|---|---|
| no | no |

Note: Use checksum when the pseudopotential is identified by a checksum of its file (e.g. the SHA256 hash of a VASP POTCAR file). For any other designation, use unique-identifier.

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.checksum.file" markdown="1">
<summary><span class="mc-name">file<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The name of the file.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.checksum.algorithm" markdown="1">
<summary><span class="mc-name">algorithm<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The algorithm that computed the checksum.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `SHA1`, `SHA224`, `SHA256`, `SHA384`, `SHA512`, `SHA3-256`, `SHA3-384`, `SHA3-512`, `BLAKE2b-256`, `BLAKE2b-384`, `BLAKE2b-512`, `BLAKE3`, `MD2`, `MD4`, `MD5`, `MD6`, `ADLER32`. Other values are allowed. The algorithm names of [SPDX 2.3.1 §8.4](https://spdx.github.io/spdx-spec/v2.3.1/file-information/) (File checksum field).

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.checksum.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The checksum of the file, in lowercase hexadecimal digits.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Pattern: `[0-9a-f]+`.

</details>

</details>

<details class="note mc-property" id="dft.core-electron-model.pseudopotential.unique-identifier" markdown="1">
<summary><span class="mc-name">unique-identifier</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

A token other than a checksum that identifies the pseudopotential, such as a label or code assigned by the library that distributes it.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Note: For a checksum of the pseudopotential file, use checksum instead.

</details>

</details>

</details>

<details class="note mc-property" id="dft.valence-electron-model" markdown="1">
<summary><span class="mc-name">valence-electron-model<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The elementary functions used for expanding electronic wave functions.

| Required | Repeatable |
|---|---|
| yes | no |

<details class="note mc-property" id="dft.valence-electron-model.type" markdown="1">
<summary><span class="mc-name">type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

The choice of a basis set to expand electronic wave functions.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | yes | string | [] | inapplicable | — |

Recommended: `Plane waves`, `LAPW`, `Localized orbitals`, `PAW`. Other values are allowed. "LAPW" – Linearized Augmented Plane Wave.

</details>

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set" markdown="1">
<summary><span class="mc-name">localized-orbital-basis-set</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

For type "Localized orbitals", additional information about the localized orbital basis set.

| Required | Repeatable |
|---|---|
| no | yes |

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.type" markdown="1">
<summary><span class="mc-name">type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The designation of the set of orbital functions used for expanding electronic wave functions.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Examples: `6-31G`, `DZP`.

</details>

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.repository" markdown="1">
<summary><span class="mc-name">repository</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The database from which the localized-orbital basis set was obtained.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.version" markdown="1">
<summary><span class="mc-name">version</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The version of the localized-orbital basis set.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.doi" markdown="1">
<summary><span class="mc-name">doi</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The digital object identifier (DOI) for the localized-orbital basis set.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Pattern: `https://doi\.org/10\.[^/]+/.+`.

</details>

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.checksum" markdown="1">
<summary><span class="mc-name">checksum</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

A digital fingerprint of the localized-orbital basis set file, computed by a named algorithm.

| Required | Repeatable |
|---|---|
| no | no |

Note: Use checksum when the basis set is identified by a checksum of its file. For any other designation, use unique-identifier.

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.checksum.file" markdown="1">
<summary><span class="mc-name">file<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The name of the file.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.checksum.algorithm" markdown="1">
<summary><span class="mc-name">algorithm<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The algorithm that computed the checksum.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `SHA1`, `SHA224`, `SHA256`, `SHA384`, `SHA512`, `SHA3-256`, `SHA3-384`, `SHA3-512`, `BLAKE2b-256`, `BLAKE2b-384`, `BLAKE2b-512`, `BLAKE3`, `MD2`, `MD4`, `MD5`, `MD6`, `ADLER32`. Other values are allowed. The algorithm names of [SPDX 2.3.1 §8.4](https://spdx.github.io/spdx-spec/v2.3.1/file-information/) (File checksum field).

</details>

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.checksum.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The checksum of the file, in lowercase hexadecimal digits.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Pattern: `[0-9a-f]+`.

</details>

</details>

<details class="note mc-property" id="dft.valence-electron-model.localized-orbital-basis-set.unique-identifier" markdown="1">
<summary><span class="mc-name">unique-identifier</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

A token other than a checksum that identifies the localized-orbital basis set, such as a label or code assigned by the library that distributes it.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Note: For a checksum of the basis set file, use checksum instead.

</details>

</details>

<details class="note mc-property" id="dft.valence-electron-model.kinetic-energy-cutoff" markdown="1">
<summary><span class="mc-name">kinetic-energy-cutoff</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

For type not "Localized orbitals", the maximum kinetic energy of the plane waves included in the calculation of wave functions.

| Required | Repeatable |
|---|---|
| no | no |

<details class="note mc-property" id="dft.valence-electron-model.kinetic-energy-cutoff.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The value of the property, in the unit given by `unit`.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | float | [] | Energy | eV |

Minimum: 0.

</details>

<details class="note mc-property" id="dft.valence-electron-model.kinetic-energy-cutoff.unit" markdown="1">
<summary><span class="mc-name">unit<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit of the value, an Annex U symbol whose Kind is the Kind of `value`.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

</details>

<details class="note mc-property" id="dft.valence-electron-model.charge-density-cutoff" markdown="1">
<summary><span class="mc-name">charge-density-cutoff</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

For type not "Localized orbitals", the energy value used to truncate the plane wave expansion of the electron charge density.

| Required | Repeatable |
|---|---|
| no | no |

<details class="note mc-property" id="dft.valence-electron-model.charge-density-cutoff.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The value of the property, in the unit given by `unit`.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | float | [] | Energy | eV |

Minimum: 0.

</details>

<details class="note mc-property" id="dft.valence-electron-model.charge-density-cutoff.unit" markdown="1">
<summary><span class="mc-name">unit<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit of the value, an Annex U symbol whose Kind is the Kind of `value`.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

</details>

</details>

<details class="note mc-property" id="dft.calculation-physics" markdown="1">
<summary><span class="mc-name">calculation-physics</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

Additional phenomena included beyond the standard DFT calculation.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | yes | — | — | — | — |

<span class='legacy'>Legacy: String containing one of the following values: "Relativistic effects" "Spin polarization" "Noncollinear spin polarization" "On-site correlation" (e.g. DFT+U) "Van der Waals" Other user-specified value if none of the above apply.</span>

</details>

<details class="note mc-property" id="dft.k-point-mesh" markdown="1">
<summary><span class="mc-name">k-point-mesh</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

For periodic systems, a grid of points sampled within the Brillouin zone, used to approximate integrals and calculate electronic properties by discretizing the wavefunction across reciprocal space.

| Required | Repeatable |
|---|---|
| no | no |

<details class="note mc-property" id="dft.k-point-mesh.type" markdown="1">
<summary><span class="mc-name">type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The choice of how k-points are distributed on the mesh.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | — | — | — | — |

<span class='legacy'>Legacy: String containing one of the following values: "Monkhorst-Pack" "Gamma centered" "Irregular" Other user-specified value if none of the above apply.</span>

</details>

<details class="note mc-property" id="dft.k-point-mesh.number-of-points" markdown="1">
<summary><span class="mc-name">number-of-points</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

How many k-points are included along each reciprocal lattice vector.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: Ordered list of three integer numbers containing the number k-points along the three reciprocal lattice vector directions.</span> <span class='legacy'>Legacy unit: dimensionless</span>

</details>

<details class="note mc-property" id="dft.k-point-mesh.k-point-spacing" markdown="1">
<summary><span class="mc-name">k-point-spacing</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Separation between k-points along each reciprocal lattice vector direction.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: Real number containing the k-point spacing.</span> <span class='legacy'>Legacy unit: 1/angstrom (1/Å)</span>

State whether the factor 2π is included in the reciprocal length.

</details>

<details class="note mc-property" id="dft.k-point-mesh.shift" markdown="1">
<summary><span class="mc-name">shift</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Translation of the k-point mesh along the reciprocal lattice vector directions.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: Ordered list of three real numbers containing the shifts along the three reciprocal lattice vector directions.</span> <span class='legacy'>Legacy unit: 1/angstrom (1/Å)</span>

</details>

<details class="note mc-property" id="dft.k-point-mesh.smearing-type" markdown="1">
<summary><span class="mc-name">smearing-type</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The choice of method for assigning fractional occupancies of electronic states and/or facilitating reciprocal space integrations.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: String containing one of the following values: "None" "None - tetrahedron" "None - Blöchl-corrected tetrahedron" "Gaussian" "Fermi" "Methfessel-Paxton" Other user-specified value if none of the above apply.</span>

</details>

<details class="note mc-property" id="dft.k-point-mesh.smearing-width" markdown="1">
<summary><span class="mc-name">smearing-width</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

A parameter that controls the broadening of the electron energy levels near the Fermi level.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: Real number containing the smearing width.</span> <span class='legacy'>Legacy unit: electron Volt (eV)</span>

</details>

<details class="note mc-property" id="dft.k-point-mesh.methfessel-paxton-order" markdown="1">
<summary><span class="mc-name">methfessel-paxton-order</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

For smearing-type "Methfessel-Paxton", level of polynomial approximation used in the Methfessel-Paxton smearing method

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: Integer containing the Methfessel-Paxton order.</span> <span class='legacy'>Legacy unit: dimensionless</span>

</details>

</details>

<details class="note mc-property" id="dft.self-consistent-field-convergence" markdown="1">
<summary><span class="mc-name">self-consistent-field-convergence</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Method and termination criteria defining the precision of self-consistent solution of the Kohn-Sham equations.

| Required | Repeatable |
|---|---|
| no | no |

<details class="note mc-property" id="dft.self-consistent-field-convergence.method" markdown="1">
<summary><span class="mc-name">method</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The self-consistent field mixing and/or extrapolation scheme for the iterative solution of the Kohn-Sham equations.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: String containing one of the following values: "Simple mixing" "Pulay mixing" "Blocked Davidson" "DIIS" – Direct Inversion in the Iterative Subspace "BFGS" – Broyden–Fletcher–Goldfarb–Shanno algorithm Other user-specified value if none of the above apply.</span>

</details>

<details class="note mc-property" id="dft.self-consistent-field-convergence.tolerance" markdown="1">
<summary><span class="mc-name">tolerance<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Convergence criterion (on total energy) for the self-consistent loop.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | — | — | — | — |

<span class='legacy'>Legacy: Real number containing the convergence tolerance</span> <span class='legacy'>Legacy unit: electron Volt (eV)</span>

</details>

</details>

<details class="note mc-property" id="dft.relaxation-tolerance-energy" markdown="1">
<summary><span class="mc-name">relaxation-tolerance-energy</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Total energy convergence criterion for atomic relaxation.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: Real number containing the convergence tolerance</span> <span class='legacy'>Legacy unit: electron Volt (eV)</span>

</details>

<details class="note mc-property" id="dft.relaxation-tolerance-forces" markdown="1">
<summary><span class="mc-name">relaxation-tolerance-forces</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Maximum force convergence criterion for atomic relaxation.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | — | — | — | — |

<span class='legacy'>Legacy: Real number containing the convergence tolerance</span> <span class='legacy'>Legacy unit: electron Volt (eV/Å)</span>

</details>

<details class="note mc-property" id="dft.comment" markdown="1">
<summary><span class="mc-name">comment</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

Additional information on the DFT calculation. For example, non-self-consistent constraints, such as details about imposed state occupation or moment freezing.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | yes | — | — | — | — |

<span class='legacy'>Legacy: String containing the calculation comments.</span>

</details>

## Example: DFT Method-Specific Metadata

Dataset source: [https://doi.org/10.60732/8e9bc5b0](https://doi.org/10.60732/8e9bc5b0)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <xc-functional>
    <type>GGA</type>
    <description>PW91 functional (the choice is motivated by the existence of a large-scale simulation of the melting point with this functional)</description>
  </xc-functional>
  <core-electron-model>
    <type>Pseudopotential</type>
    <pseudopotential>
      <name>Ultrasoft Pseudopotentials (USP)</name>
      <type>Ultrasoft</type>
      <number-of-valence-electrons>
        <value>4</value>
        <unit>dimensionless</unit>
      </number-of-valence-electrons>
    </pseudopotential>
  </core-electron-model>
  <valence-electron-model>
    <type>Plane waves</type>
    <kinetic-energy-cutoff>
      <value>250.0</value>
      <unit>eV</unit>
    </kinetic-energy-cutoff>
  </valence-electron-model>
  <k-point-mesh>
    <type>Monkhorst-Pack</type>
    <k-point-spacing>0.03</k-point-spacing>
    <smearing-width>0.05</smearing-width>
  </k-point-mesh>
</root>
```

