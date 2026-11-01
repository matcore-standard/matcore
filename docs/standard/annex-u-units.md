# Annex U — MatCore Unit Table

<!-- BEGIN generated: version from schema/releases.yaml by scripts/build_docs.py; do not edit -->
<p class="mc-version" data-version="0.4.0">Version 0.4.0</p>
<!-- END generated -->

*(Normative)*

*Amended 2026-10-31: Rule 4 extended from generic parameters to any subproperty whose Kind the schema declares as `any` (decision record 0001).*

## U.1 Purpose

This annex defines the closed set of unit symbols that MAY appear as the value of a `unit` subproperty in a MatCore metadata instance, the kind of each symbol, and its conversion to coherent SI. It also defines the kind names used in the **Kind** field of the schema and their mapping to the QUDT ontology.

A validator checks that (a) the symbol is in Table U.4 and (b) its kind matches the kind declared for the property in the schema. No unit parsing is required.

## U.2 Rules

1. Symbols are case-sensitive ASCII strings. `eV` and `ev` are not the same symbol.
2. Compound symbols use `/` for division and `^` for integer exponents, exactly as written in Table U.4. Symbols not listed (e.g. `eV/A`, `Å`, `angstrom**3`) are non-conformant.
3. The reserved symbol `dimensionless` is used for quantities of dimension one (ratios, counts, fractional coordinates). It SHALL NOT be used for plane angles (use `rad` or `degree`) or for amount of substance (use `mol`).
4. A `unit` subproperty of a generic parameter or of any other subproperty whose Kind the schema declares as `any` MAY, if and only if no symbol in Table U.4 applies, contain a string of the form `x-gnu:<expression>`, where `<expression>` is a unit expression valid in GNU Units 2.23 with `definitions.units` version 3.19 (February 2024). Such values are accepted with a validation warning and are not guaranteed to be machine-convertible. Later versions of `definitions.units` are not implied; a change of the pinned version is a revision of this annex.
5. Conversion factors marked *exact* follow from the SI definitions. Factors marked *CODATA 2022* are the 2022 CODATA recommended values published by NIST. The factors in Table U.4 are normative for MatCore and take precedence over the values embedded in any external vocabulary (see Note 5). A revision to a later CODATA release is a revision of this annex.
6. This annex is versioned with the standard. Instance files SHALL use symbols from the annex version matching their declared MatCore version. Symbols are only ever added; a symbol, once published, is never removed or redefined.
7. Compatibility between a unit and a kind is decided by the SI dimension vector in Table U.3, not by QUDT's own `hasQuantityKind` links (see Note 4).
8. `Energy` and `MolarEnergy` are distinct kinds and are not interchangeable. A property declared with Kind Energy SHALL NOT carry a MolarEnergy unit, and vice versa (see Note 1).

## U.3 Kinds

QUDT namespace: `http://qudt.org/vocab/quantitykind/`. The dimension vector is QUDT's, in the order A (amount of substance), E (electric current), L (length), I (luminous intensity), M (mass), H (thermodynamic temperature), T (time), D (dimensionless).

<!-- BEGIN generated: Table U.3 from schema/units.yaml by scripts/build_docs.py; do not edit -->
| Kind | QUDT QuantityKind | QUDT dimension vector | SI dimension |
|---|---|---|---|
| Energy | Energy | A0E0L2I0M1H0T-2D0 | kg·m²·s⁻² |
| MolarEnergy | MolarEnergy | A-1E0L2I0M1H0T-2D0 | kg·m²·s⁻²·mol⁻¹ |
| Length | Length | A0E0L1I0M0H0T0D0 | m |
| InverseLength | InverseLength | A0E0L-1I0M0H0T0D0 | m⁻¹ |
| Volume | Volume | A0E0L3I0M0H0T0D0 | m³ |
| Time | Time | A0E0L0I0M0H0T1D0 | s |
| InverseTime | InverseTime | A0E0L0I0M0H0T-1D0 | s⁻¹ |
| Temperature | ThermodynamicTemperature | A0E0L0I0M0H1T0D0 | K |
| TemperatureGradient | TemperatureGradient | A0E0L-1I0M0H1T0D0 | K·m⁻¹ |
| Pressure | Pressure | A0E0L-1I0M1H0T-2D0 | kg·m⁻¹·s⁻² |
| Force | Force | A0E0L1I0M1H0T-2D0 | kg·m·s⁻² |
| Mass | Mass | A0E0L0I0M1H0T0D0 | kg |
| MassDensity | MassDensity | A0E0L-3I0M1H0T0D0 | kg·m⁻³ |
| NumberDensity | NumberDensity | A0E0L-3I0M0H0T0D0 | m⁻³ |
| HeatFluxDensity | HeatFluxDensity | A0E0L0I0M1H0T-3D0 | kg·s⁻³ |
| Angle | PlaneAngle | A0E0L0I0M0H0T0D1 | 1 (rad) |
| AmountOfSubstance | AmountOfSubstance | A1E0L0I0M0H0T0D0 | mol |
| dimensionless | Dimensionless | A0E0L0I0M0H0T0D1 | 1 |
| inapplicable | — | — | — |
| any | — | — | — |
<!-- END generated -->

Reserved kinds: `dimensionless`; `inapplicable` (the value is not a physical quantity: strings, booleans, identifiers, and the `unit` subproperty itself); `any` (the kind is determined by the instance `unit`; used only for the `value` of generic name/value/unit parameters).

## U.4 Unit symbols

QUDT namespace: `http://qudt.org/vocab/unit/`. "—" in the QUDT column means the unit has no IRI in QUDT (see Note 7).

<!-- BEGIN generated: Table U.4 from schema/units.yaml by scripts/build_docs.py; do not edit -->
| Symbol | Kind | QUDT Unit | GNU Units expression | Factor to coherent SI | Source |
|---|---|---|---|---|---|
| `eV` | Energy | EV | eV | 1.602 176 634 × 10⁻¹⁹ J | exact |
| `meV` | Energy | — | meV | 1.602 176 634 × 10⁻²² J | exact |
| `Ry` | Energy | — | rydberg | 2.179 872 361 103 0 × 10⁻¹⁸ J | CODATA 2022 (= E_h/2) |
| `hartree` | Energy | E_h | hartree | 4.359 744 722 206 0 × 10⁻¹⁸ J | CODATA 2022 |
| `J` | Energy | J | J | 1 | exact |
| `kJ/mol` | MolarEnergy | KiloJ-PER-MOL | kJ/mol | 1 × 10³ J·mol⁻¹ | exact |
| `kcal/mol` | MolarEnergy | KiloCAL-PER-MOL | kcal/mol | 4.184 × 10³ J·mol⁻¹ | exact (thermochemical calorie) |
| `J/mol` | MolarEnergy | J-PER-MOL | J/mol | 1 | exact |
| `angstrom` | Length | ANGSTROM | angstrom | 1 × 10⁻¹⁰ m | exact |
| `bohr` | Length | — | bohrradius | 5.291 772 105 44 × 10⁻¹¹ m | CODATA 2022 |
| `nm` | Length | NanoM | nm | 1 × 10⁻⁹ m | exact |
| `um` | Length | MicroM | um | 1 × 10⁻⁶ m | exact |
| `m` | Length | M | m | 1 | exact |
| `1/angstrom` | InverseLength | PER-ANGSTROM | 1/angstrom | 1 × 10¹⁰ m⁻¹ | exact |
| `1/bohr` | InverseLength | — | 1/bohrradius | 1.889 726 125 91 × 10¹⁰ m⁻¹ | CODATA 2022 |
| `1/nm` | InverseLength | PER-NanoM | 1/nm | 1 × 10⁹ m⁻¹ | exact |
| `1/m` | InverseLength | PER-M | 1/m | 1 | exact |
| `angstrom^3` | Volume | ANGSTROM3 | angstrom^3 | 1 × 10⁻³⁰ m³ | exact |
| `bohr^3` | Volume | — | bohrradius^3 | 1.481 847 111 7 × 10⁻³¹ m³ | CODATA 2022 |
| `nm^3` | Volume | — | nm^3 | 1 × 10⁻²⁷ m³ | exact |
| `m^3` | Volume | M3 | m^3 | 1 | exact |
| `fs` | Time | FemtoSEC | fs | 1 × 10⁻¹⁵ s | exact |
| `ps` | Time | PicoSEC | ps | 1 × 10⁻¹² s | exact |
| `ns` | Time | NanoSEC | ns | 1 × 10⁻⁹ s | exact |
| `s` | Time | SEC | s | 1 | exact |
| `1/s` | InverseTime | PER-SEC | 1/s | 1 | exact |
| `1/ps` | InverseTime | — | 1/ps | 1 × 10¹² s⁻¹ | exact |
| `K` | Temperature | K | K | 1 | exact |
| `K/m` | TemperatureGradient | K-PER-M | K/m | 1 | exact |
| `K/angstrom` | TemperatureGradient | — | K/angstrom | 1 × 10¹⁰ K·m⁻¹ | exact |
| `Pa` | Pressure | PA | Pa | 1 | exact |
| `GPa` | Pressure | GigaPA | GPa | 1 × 10⁹ Pa | exact |
| `kbar` | Pressure | KiloBAR | kbar | 1 × 10⁸ Pa | exact |
| `bar` | Pressure | BAR | bar | 1 × 10⁵ Pa | exact |
| `eV/angstrom^3` | Pressure | — | eV/angstrom^3 | 1.602 176 634 × 10¹¹ Pa | exact |
| `eV/angstrom` | Force | EV-PER-ANGSTROM | eV/angstrom | 1.602 176 634 × 10⁻⁹ N | exact |
| `hartree/bohr` | Force | — | hartree/bohrradius | 8.238 723 503 8 × 10⁻⁸ N | CODATA 2022 |
| `N` | Force | N | N | 1 | exact |
| `amu` | Mass | AMU | amu | 1.660 539 068 92 × 10⁻²⁷ kg | CODATA 2022 |
| `kg` | Mass | KiloGM | kg | 1 | exact |
| `kg/m^3` | MassDensity | KiloGM-PER-M3 | kg/m^3 | 1 | exact |
| `g/cm^3` | MassDensity | GM-PER-CentiM3 | g/cm^3 | 1 × 10³ kg·m⁻³ | exact |
| `1/angstrom^3` | NumberDensity | — | 1/angstrom^3 | 1 × 10³⁰ m⁻³ | exact |
| `1/m^3` | NumberDensity | PER-M3 | 1/m^3 | 1 | exact |
| `W/m^2` | HeatFluxDensity | W-PER-M2 | W/m^2 | 1 | exact |
| `rad` | Angle | RAD | radian | 1 | exact |
| `degree` | Angle | DEG | degree | π/180 rad | exact |
| `mol` | AmountOfSubstance | MOL | mol | 1 | exact |
| `dimensionless` | dimensionless | UNITLESS | — | — | reserved |
<!-- END generated -->

**Note 1 (molar energies).** `kJ/mol`, `kcal/mol` and `J/mol` are units of energy per amount of substance and belong to the kind MolarEnergy, consistent with QUDT, which links these units to `quantitykind:MolarEnergy`. They are the customary energy units of classical force fields, and properties in the MD section that are conventionally reported per mole are declared with Kind MolarEnergy. Conversion between Energy and MolarEnergy is a division or multiplication by the Avogadro constant (6.022 140 76 × 10²³ mol⁻¹, exact) and is a task for tooling, not for a `unit` value.

**Note 2 (2π convention).** InverseLength symbols do not encode whether a factor 2π is included. Properties for which this matters (e.g. `k-point-spacing`) carry a separate required `convention` subproperty.

**Note 3 (mole vs. dimensionless).** Following OPTIMADE, `dimensionless` SHALL NOT be used for amounts of substance or plane angles.

**Note 4 (QUDT quantity-kind links are not a validation basis).** QUDT attaches its own quantity kinds to units, and these are often narrower or differently named than MatCore's: `PER-SEC` is linked to Frequency and DecayConstant (not InverseTime); `PER-M3` to InverseVolume (not NumberDensity); `W-PER-M2` to PowerPerArea (not HeatFluxDensity); `GigaPA`, `KiloBAR` and `BAR` to ForcePerArea (not Pressure); `EV-PER-ANGSTROM` to TotalLinearStoppingPower (not Force). In every case the dimension vector agrees with the MatCore kind, so compatibility is validated by dimension vector (Rule 7), and the QUDT unit IRI serves only as a stable identifier.

**Note 5 (stale constants in reference vocabularies).** QUDT's own conversion multipliers for `E_h` (4.359 743 94 × 10⁻¹⁸ J) and `AMU` (1.660 538 782 83 × 10⁻²⁷ kg) are CODATA 2006 values, and GNU Units 2.23 uses CODATA 2018 values (hartree 4.359 744 722 2071 × 10⁻¹⁸ J, bohrradius 5.291 772 109 02 × 10⁻¹¹ m, amu 1.660 539 066 6 × 10⁻²⁷ kg). The factors in Table U.4 are therefore normative in MatCore (Rule 5) and take precedence over the values embedded in either reference vocabulary.

**Note 6 (GNU spelling of bohr).** GNU Units does not define `bohr`; the GNU name is `bohrradius`. The MatCore symbol remains `bohr`; the mapping is given in the GNU column.

**Note 7 (units absent from QUDT).** `Ry`, `bohr`, `meV`, `nm^3`, `1/ps`, `1/bohr`, `bohr^3`, `K/angstrom`, `eV/angstrom^3`, `hartree/bohr` and `1/angstrom^3` have no unit IRI in QUDT Units v3.3.0. For these, the MatCore symbol is the identifier and the quantity-kind IRI in Table U.3 supplies the semantic anchor. QUDT accepts contributions through its public repository, and IRIs will be added to this table if and when they are published.

## U.5 References

- QUDT Units Vocabulary v3.3.0 and QUDT Quantity Kinds Vocabulary, `https://qudt.org/vocab/unit/` and `https://qudt.org/vocab/quantitykind/` (source: `https://github.com/qudt/qudt-public-repo`), consulted 2026-09-27.
- GNU Units 2.23, `definitions.units` version 3.19 (February 2024), Free Software Foundation, `https://www.gnu.org/software/units/`.
- CODATA Recommended Values of the Fundamental Physical Constants: 2022. NIST Reference on Constants, Units, and Uncertainty, `https://physics.nist.gov/cuu/Constants/`; energy-equivalents sheet `https://physics.nist.gov/cuu/pdf/factors_2022.pdf`.
- BIPM, *The International System of Units (SI)*, 9th edition (2019), for exact definitions of the second, kelvin, mole, joule and electronvolt.
- OPTIMADE API specification v1.3.0, section on unit definitions, `https://www.optimade.org/specification/latest/`, for the treatment of `dimensionless` versus angles and amounts of substance.
