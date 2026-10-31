# MatCore Metadata Schema — Change List for Units Handling

A3.3 removed 2026-10-31: referred to a DFT `computation-parameter` that does not exist; the MD entry is covered by A4.1.

**Part A** implements the units design (explicit `unit` on every dimensioned property; schema declares Quantity kind + Recommended unit; no default unit is ever implied).
**Part B** contains independent fixes to existing content. Apply Part B even if Part A is deferred.

Line references are to the draft `MatCore_Dev.docx`; "old" text is quoted so each spot can be found with Find.

Notation: **Quantity kind** and **Recommended unit** replace the current *Standard units* phrase everywhere. Recommended unit is informative only.

---

## PART A — Units implementation

### A1. General rule (§1.3 Format)

**A1.1** Find the bullet:

> When a value has physical units, either the required unit must be specified, or a field provided to define the value units.

Replace with:

> **Units of physical quantities.** Every property whose value is a physical quantity (i.e. whose Quantity kind is neither "dimensionless" nor "inapplicable") SHALL carry a `unit` subproperty in the metadata instance. The value of `unit` SHALL be a symbol from the MatCore Unit Table (Annex U) whose quantity kind is compatible with the property's declared Quantity kind. A property value without a `unit`, or with a unit incompatible with its Quantity kind, is non-conformant; no default unit is ever implied. The Recommended unit listed for each property is informative and does not affect how values are interpreted. Quantities of dimension one use the reserved symbol `dimensionless`; plane angles use an angle unit (`rad` or `degree`). Where the meaning of a value depends on a convention that a unit cannot express (e.g. inclusion of a factor 2π in reciprocal lengths, or components given in a lattice basis), the property has a `convention` or `basis` subproperty, required as stated in its description. Conversion factors to SI for units not exactly defined in SI terms (`bohr`, `hartree`, `Ry`) are those of CODATA 2022, as listed in Annex U.

**A1.2** In the same bullet list, after the "Values:" bullet, add two new bullets:

> - **Quantity kind:** The physical dimension of the Property's value, given as a MatCore quantity-kind name mapped to a QUDT QuantityKind IRI in Annex U (e.g. Energy, Length, InverseLength, Temperature, Pressure). Reserved values: `dimensionless` (ratios, counts), `inapplicable` (strings, identifiers, and the `unit` subproperty itself), `any` (the `value` of a generic name/value/unit parameter, whose quantity kind is then given by the instance `unit`).
> - **Recommended unit:** The unit customarily used for this Property in the community. Informative only; used by templates and tools.

**A1.3** Add to the paragraph beginning "Examples are provided after each Standard specification in XML format":

> In the XML examples, `unit`, `convention` and `basis` are written as attributes of the value element for brevity; an equivalent child-element serialization is also conformant.

### A2. Minimal section (§2.1), simulation-conditions table

**A2.1** Line 129, `simulation-conditions > type`: delete

> **Note 2:** Units for dimensioned variables are to be given in the SI unit system.

and renumber the remaining "Note 1" to "Note".

**A2.2** For each SubSubProperty below, replace the italic *Standard units: …* phrase with the new text.

| Entry | Old phrase | New text |
|---|---|---|
| number-of-particles | *Standard units: dimensionless* | **Quantity kind:** dimensionless |
| volume | *Standard units: cubic meters (m³)* | **Quantity kind:** Volume. **Recommended unit:** angstrom^3. **Subproperties:** `unit` (required) |
| mass-density | *Standard units: kilograms per cubic meter (kg/m³)* | **Quantity kind:** MassDensity. **Recommended unit:** kg/m^3. **Subproperties:** `unit` (required) |
| number-density | *Standard units: inverse cubic meter (1/m³)* | **Quantity kind:** NumberDensity. **Recommended unit:** 1/angstrom^3. **Subproperties:** `unit` (required) |
| cell | *Standard units: meter (m)* | **Quantity kind:** Length. **Recommended unit:** angstrom. **Subproperties:** `unit` (required; applies to all nine components) |
| cell-reference | *Standard units: meter (m)* | Same as cell |
| cell-periodicity | *Standard units: dimensionless* | **Quantity kind:** inapplicable (booleans) |
| temperature | *Standard units: kelvin (K)* | **Quantity kind:** Temperature. **Recommended unit:** K. **Subproperties:** `unit` (required) |
| stress | *Standard units: pascal (Pa)* | **Quantity kind:** Pressure. **Recommended unit:** GPa. **Subproperties:** `unit` (required; applies to all six components) |
| strain | *Standard units: dimensionless* | **Quantity kind:** dimensionless |
| strain-rate | *Standard units: dimensionless* | **Quantity kind:** InverseTime. **Recommended unit:** 1/s. **Subproperties:** `unit` (required). *(See fix B4.)* |
| heat-flux | *Standard units: watts per square meter (W/m²)* | **Quantity kind:** HeatFluxDensity. **Recommended unit:** W/m^2. **Subproperties:** `unit` (required) |
| temperature-gradient | *(see fix B1 first)* | **Quantity kind:** TemperatureGradient. **Recommended unit:** K/m. **Subproperties:** `unit` (required) |

> **Team decision:** the recommended units above for volume, number-density and cell use Å, matching OPTIMADE/ASE practice. Keeping the draft's SI recommendations (m, m³, 1/m³) is a one-word change per row and does not affect conformance.

### A3. DFT section (§2.2)

**A3.1** Replace *Standard units* phrases:

| Entry | New text |
|---|---|
| kinetic-energy-cutoff | **Quantity kind:** Energy. **Recommended unit:** eV. **Subproperties:** `unit` (required) |
| charge-density-cutoff | Same as kinetic-energy-cutoff |
| number-of-points | **Quantity kind:** dimensionless |
| k-point-spacing | **Quantity kind:** InverseLength. **Recommended unit:** 1/angstrom. **Subproperties:** `unit` (required); `convention` (required; one of "2pi-included", "2pi-excluded"). **Note:** Codes differ on whether the factor 2π is included in the reciprocal length; the convention must be stated. |
| shift | *(see fix B5 first)* **Quantity kind:** dimensionless. **Note:** Shifts are given as fractions of the mesh spacing along each reciprocal lattice vector. |
| smearing-width | **Quantity kind:** Energy. **Recommended unit:** eV. **Subproperties:** `unit` (required) |
| methfessel-paxton-order | **Quantity kind:** dimensionless |
| tolerance (SCF) | *(see fix B6 first)* **Quantity kind:** any. **Subproperties:** `unit` (required); `criterion` (required; one of "energy", "charge-density", "potential", "other") |
| relaxation-tolerance-energy | **Quantity kind:** Energy. **Recommended unit:** eV. **Subproperties:** `unit` (required) |
| relaxation-tolerance-forces | **Quantity kind:** Force. **Recommended unit:** eV/angstrom. **Subproperties:** `unit` (required) |
| number-of-valence-electrons | **Quantity kind:** dimensionless |

**A3.2** Generic quadruple `xc-parameter` (line ~300). In the `value*` row append: **Quantity kind:** any. In the `unit*` row replace:

> A string containing the units of the value in the GNU unit convention (or the text "dimensionless").

with:

> A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning). **Quantity kind:** inapplicable.

### A4. MD section (§2.3)

**A4.1** Apply A3.2 to `computation-parameter` (line ~422) and `td-parameter` (line ~439).

### A5. MBPT section (§2.4)

| Entry | New text |
|---|---|
| planewave-basis-cutoff | **Quantity kind:** Energy. **Recommended unit:** eV. **Subproperties:** `unit` (required). *(See fix B2.)* |
| response-basis-size, q-points, gw-bands, number-valence-bands, number-conduction-bands, k-point-mesh, number-lowest-eigenvalues | **Quantity kind:** dimensionless |
| exciton-momentum | *(see fix B3 first)* **Quantity kind:** InverseLength or dimensionless, depending on basis. **Subproperties:** `basis` (required; one of "cartesian", "reciprocal-lattice-fractional"); `unit` (required; when basis = "reciprocal-lattice-fractional" the unit SHALL be `dimensionless`; when "cartesian", an InverseLength unit, recommended 1/angstrom, plus `convention` as for k-point-spacing) |

### A6. ML section (§2.5)

**A6.1** No unit changes are required. The ML section contains no properties with physical dimensions and no `unit` rows; `training-hyperparameters` (line ~569) is a single free-text string. Optionally, for consistency with the other sections, consider converting `training-hyperparameters` to the name/value/unit/description form used elsewhere (with `value` of Quantity kind `any` and `unit` per A3.2); this is a separate design decision, not part of the units change.

### A7. PF section (§2.6)

**A7.1** `domain-size` (line ~636): replace

> An ordered list of real numbers containing the domain dimensions in meters (m).

with:

> An ordered list of real numbers containing the domain extents along each coordinate direction. **Quantity kind:** Length. **Recommended unit:** m. **Subproperties:** `unit` (required).

**A7.2** `spatial-accuracy-order`, `temporal-accuracy-order`: replace *Standard units: dimensionless* with **Quantity kind:** dimensionless.

**A7.3** `free-energy > unit` (line ~666): replace the GNU-units sentence with the A3.2 wording. Change the Definition to "The physical unit of the free energy density (or of the free energy, if `expression` is not a density)".

**A7.4** Apply A3.2 to the `unit*` rows of `grid-spacing`, `time-step-size`, `model-parameter`, `field-variable`. In the `value*` rows add: `grid-spacing` → **Quantity kind:** Length; `time-step-size` → **Quantity kind:** Time; `model-parameter` and `field-variable` → **Quantity kind:** any.

### A8. Derived property section (§2.7)

**A8.1** Apply A3.2 to `calculation-parameter > unit*` (line ~844); add **Quantity kind:** any to its `value*` row.

### A9. New Annex U — MatCore Unit Table

Insert the contents of the separate file `MatCore_Annex_U_Unit_Table.md` as a new section after §2.7 (or as an appendix), keeping its heading "Annex U — MatCore Unit Table (Normative)". It contains the rules, the quantity-kind table, the unit-symbol table, seven explanatory notes and a references list, and all identifiers and factors in it have been verified against the QUDT v3.3.0 source, GNU Units 2.23 (`definitions.units` v3.19) and NIST CODATA 2022.

Two consequences for other entries in this list:

- Annex U defines `MolarEnergy` as a quantity kind distinct from `Energy` (Rule 8). Any typed MD property that is conventionally reported per mole should be declared with Quantity kind MolarEnergy and recommended unit kJ/mol or kcal/mol, not Energy.
- Annex U Rule 4 pins `x-gnu:` expressions to GNU Units 2.23 / `definitions.units` v3.19; the wording in A3.2 needs no change since it refers to Annex U.

### A10. Update the XML examples

**A10.1** In every example, add `unit="…"` to each dimensioned value, e.g.

```xml
<temperature unit="K">300</temperature>
<kinetic-energy-cutoff unit="eV">520</kinetic-energy-cutoff>
<k-point-spacing unit="1/angstrom" convention="2pi-included">0.25</k-point-spacing>
```

**A10.2** In the existing generic-parameter examples (lines ~720–780), `<unit>dimensionless</unit>` is already conformant; leave as is. Check that any non-dimensionless examples use an Annex U symbol.

### A11. Version note

Add to the preamble or a changelog:

> From version X, `unit` is required on all dimensioned properties. Files declaring an earlier MatCore version are interpreted using the fixed units of that version (Annex U, legacy table).

If a legacy table is kept, populate it from the *Standard units* values removed in A2–A8.

---

## PART B — Fixes to existing content

These are corrections independent of the units design.

**B1. temperature-gradient (line 143).** Old: *Standard units: watts per square meter (K/m)*. The name is wrong; the symbol is right. Under Part A this row is replaced by A2.2; if applying B1 alone, change to *kelvin per meter (K/m)*.

**B2. planewave-basis-cutoff vs kinetic-energy-cutoff (line 495 vs 276).** The MBPT entry says the quantity "is the same as the kinetic energy cutoff" but gives Ry while the DFT entry gives eV. Under Part A both become explicit-unit Energy properties (A3.1, A5); if applying B2 alone, align on one unit. Consider adding: "Note: If the DFT `kinetic-energy-cutoff` is given, this value should agree with it."

**B3. exciton-momentum (line 506).** Old: *Standard units: Reciprocal lattice units (2π/a)*. This is a convention, not a unit, and "2π/a" presumes a cubic cell. Replace with the `basis` subproperty wording in A5. If applying B3 alone, at minimum change to "Values: components in fractions of the reciprocal lattice vectors (dimensionless)".

**B4. strain-rate (line 141).** Old: *Standard units: dimensionless*. A rate has dimension 1/time. Replace per A2.2; if applying alone, change to *inverse seconds (1/s)*. Also, the Values sentence uses the symbol E for the strain-rate tensor, the same symbol the strain entry (line 140) uses for the strain tensor; suggest Ė (or dE/dt) for the strain rate.

**B5. shift (line 283).** Old: *Standard units: 1/angstrom (1/Å)*. A mesh shift is customarily a fraction of the mesh spacing (e.g. 0.5 for a half-shift), which is dimensionless. Confirm with the entry's author; if fractional, apply A3.1; if it is an absolute offset in reciprocal length, keep InverseLength and add the same `convention` subproperty as k-point-spacing.

**B6. SCF tolerance (line 289).** Old: "Convergence criterion for the self-consistent loop … *Standard units: electron Volt (eV)*". Codes converge on energy, charge density, or potential, and the unit depends on which. Add the `criterion` subproperty per A3.1; if applying alone, at least say "Convergence criterion (on total energy) for the self-consistent loop".

**B7. k-point-spacing (line 282).** The entry states *1/angstrom (1/Å)* but does not say whether the factor 2π is included, and codes differ. Under Part A this is handled by the required `convention` subproperty in A3.1; if applying alone, add a note: "State whether the factor 2π is included in the reciprocal length."

**B8. Naming consistency.** The draft uses `unit` (singular) throughout; keep it that way in all new text and avoid "units" as a field name. Normalize "Dimensionless." (capital D, line 286) to "dimensionless" wherever it remains.

**B9. Generic quadruple definitions.** All `unit*` rows share the definition "A standardized string or identifier that defines the dimension or measurement system of the associated value." Suggest: "The unit in which the associated value is expressed."

**B10. cell-periodicity (line 137).** Marked *Standard units: dimensionless* but the values are booleans; under Part A becomes `inapplicable` (A2.2). If applying alone, delete the units phrase.

**B11. free-energy > unit (line 666).** Definition says "free energy density" but `expression` may be a total free energy; reworded in A7.3.

**B12. Annex U CODATA version.** Superseded: the published Annex U states CODATA 2022 explicitly and its factors have been verified; no action needed.
