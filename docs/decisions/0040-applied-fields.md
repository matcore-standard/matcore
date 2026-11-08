# 0040 — Applied electric and magnetic fields, and body force

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee feedback: "What about other simulation conditions? Magnetic field, gravity, electrostatic potential, ..."

Reviewed candidates, and where each goes:
- **Electric field, magnetic field, body force**: imposed in many datasets (field-driven ion transport and dielectric response in MD; finite-field DFT; Zeeman fields in DFT, spin dynamics and micromagnetics; gravity in mesoscale and continuum models; a constant force driving flow in MD). Added here.
- **Electrode potential**: added by 0041, since it needs a reference.
- **Chemical potential**: 0026 declined it for minimal, pointing to md's `thermodynamic-constraint`. Since 0036 a simulation can be Open, but minimal cannot say what it is open to. It is decided together with md's `thermodynamic-constraint` (PROPOSED, NOT DECIDED in CLAUDE.md).
- **Irradiation, time-dependent fields (e.g. laser pulses), electric current density, deposition flux, walls and confinement**: specialized or method-specific; they stay in `description` until one proves common.

Annex U has none of the Kinds these conditions need. A new Kind needs a decision record (0004); this is that record for three.

## Decision
1. **Three new Kinds** in schema/units.yaml: `ElectricFieldStrength`, `MagneticFluxDensity` and `Acceleration`. Each entry's fields (QUDT QuantityKind, dimension vector, SI unit and dimension) are traced to QUDT 3.3.0 in the pull request that adds the Kind's first unit.
2. **New units**, one pull request each, every field traced to its primary source as 0004 requires: `V/m` and `V/angstrom` (ElectricFieldStrength), `T` (MagneticFluxDensity), `m/s^2` (Acceleration).
3. **Three new conditions** in minimal `computation › simulation-conditions`, after `temperature-gradient`, in the form of the other vector conditions: repeatable containers of `value*` (float, `[3]`), `unit*` and `qualifier` (0015, 0035), defined as imposed (0039). The value note gives the components in the orthonormal basis (e<sub>1</sub>, e<sub>2</sub>, e<sub>3</sub>) built from the cell, as `heat-flux`'s does; each property notes that it requires cell.
   - **`electric-field`**: Kind ElectricFieldStrength, recommended unit `V/m`. Description: "The electric field imposed on the simulated system, e.g. a uniform applied field." Value note: "The components of the electric field vector <i>E</i>." followed by the basis sentence.
   - **`magnetic-field`**: Kind MagneticFluxDensity, recommended unit `T`. Description: "The magnetic field imposed on the simulated system, given as the magnetic flux density <i>B</i>." Value note: "The components of the magnetic flux density vector <i>B</i>." followed by the basis sentence. It is given as <i>B</i>, not the magnetic field strength <i>H</i>, so values from different codes compare.
   - **`body-force`**: Kind Acceleration, recommended unit `m/s^2`. Description: "The body force per unit mass imposed on the simulated system, e.g. gravity or a constant force driving a flow." Value note: "The components of the body force per unit mass <i>g</i>." followed by the basis sentence. One property per unit mass covers gravity and flow-driving forces alike.

## Consequences
- Pull requests, in order: one per unit of item 2 (the first of each Kind also adds the Kind), then one applying item 3 (schema, tests, regenerated page). No instance is affected: the conditions are new and optional.
- Annex U's Tables U.3 and U.4 are regenerated from units.yaml with each unit pull request.
