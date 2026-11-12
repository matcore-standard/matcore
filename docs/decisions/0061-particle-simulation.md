# 0061 — Particle Simulation replaces Molecular Dynamics as the name of section 2.4

Date: 2026-11-12. Status: accepted. Decided by: Ellad Tadmor.

## Context
Section 2.4 is titled "Molecular Dynamics (MD) Metadata", its introduction speaks of "classical molecular dynamics", and §1.2 lists "MD: Classical molecular dynamics". Since 0046 the section describes the computations that move or sample particles using energies and forces supplied by another computation: molecular dynamics, molecular statics (energy minimization), free energy calculations, and ab initio MD, whose forces come from DFT rather than from a classical model. "MD" names one of these methods, not all of them.

"Atomistic Simulation" was considered and declined. minimal `method-class` already uses the term `Atomistic`, for MC, MD, MS and PIM. The section also serves coarse-grained MD (CGMD, under `Mesoscopic`) and models whose particles are beads, mesoscale grains or classical electrons (pim `particle-style`), and does not describe PIM, which has its own section. "Particle Simulation" pairs with 2.3 Particle Interaction Model: the model supplies the energies and forces, the simulation uses them.

## Decision
1. **Section 2.4 is titled "2.4 Particle Simulation (PS) Metadata"**, its extension is MatCore-PS, and its section key is `ps`: schema/ps.yaml, examples/ps.json, the instance member `ps`, the page docs/standard/ps.md, and property addresses `#ps.…`. Released versions keep their old addresses.
2. **The `method` terms MD and MS are unchanged.** They name methods; the section describes the computations whose method is MD, MS or CGMD.
3. **The introduction** becomes: "The metadata for particle simulations (MatCore-PS) is tabulated below. A particle simulation moves or samples a system of particles using the energies and forces supplied by an interaction model, a particle interaction model or, as in ab initio molecular dynamics, an electronic structure computation. This category includes molecular dynamics (MD), molecular statics (MS) and coarse-grained MD (CGMD): energy and free energy minimization, equilibrium and nonequilibrium MD, and related approaches. The properties are given in settings blocks, each naming the PS computations it describes. (Note: This standard inherits the metadata in the minimal MatCore standard, adding the properties below.)" It drops "classical" and carries 0054's sentence on settings blocks.
4. **§1.2** lists "PS: Particle simulation (molecular dynamics, molecular statics and related methods)" in place of "MD: Classical molecular dynamics", and its example extensions read "MatCore-DFT, MatCore-PS, etc.". The About page's "MatCore-MD" becomes "MatCore-PS"; its list of methods is unchanged.
5. **The Leadership page** renames "Method: Molecular Dynamics" to "Method: Particle Simulation", with the same members, and adds "Method: Particle Interaction Model" with the single entry "TBD". The method headings stay in alphabetical order, Derived Properties last.

## Consequences
- One pull request applies items 1–5 (schema, example, scripts and tests that list the sections, mkdocs.yml, the Preamble, About, Leadership, regenerated pages). It breaks 0.6.0 md instances, whose member `md` becomes `ps`.
- The fill of the section's properties (status step 5) continues under the new name, starting with `algorithm`.
- Earlier decision records and status entries keep the name md.
- PROPOSED, NOT DECIDED: whether PS also describes Monte Carlo sampling (method MC), which no property of the section addresses yet; the members of the Particle Interaction Model committee.
