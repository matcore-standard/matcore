# 0074 — The PF section: settings, names, domain and numerical method

Date: 2026-11-19. Status: accepted. Decided by: Ellad Tadmor.

## Context
The PF section is the last method section still in its baseline form. 0046 item 7 puts its properties in a `settings` block, as for dft, pim, ps, mbpt and ml. Review of the section raised these points:
1. `physical-phenomena` lacks fracture and plasticity.
2. `problem-specification › time-dependence` offers "Property prediction", which is not a time-evolution state.
3. The domain has no stated boundary: `boundary-conditions` gives a condition but not where it applies.
4. "NoFlux" is not a boundary condition in itself; a zero-flux condition is a zero Neumann condition on a concentration or a potential.
5. `initial-conditions` has no term for a configuration produced by an algorithm or given as a spatial distribution.
6. `spatial-discretization` has no place for its parameters, e.g. the element degree, the quadrature or the finite-difference stencil.
7. "Implicit" and "Explicit" in `temporal-discretization` are not schemes but classes of schemes.
8. Different governing equations may be solved by different solvers.
9. One `governing-equation › type` per equation cannot describe coupled models, and the terms "Fluid" and "Multi" are too vague to classify anything.
10. An anti-trapping current, or a sharp- or thin-interface formulation, has no property.
11. Electrostatics or mechanics solved with the phase field have no type, and minimal `computation › method` takes one method.
12. `evolved-variable` says the equation "solves for" one variable, though an implicit solve of coupled equations solves for several.
13. "Driving energy" is not a standard term; "driving force" names a forcing term in the equation, not a part of the free energy.
14. A CALPHAD-coupled simulation has no property for its thermodynamic database (TDB file).
15. A 20-component alloy has 20 concentration fields, and the schema does not say whether each is listed.

## Decision
1. **Settings.** pf's properties sit in a required, repeatable `settings` whose first member is `computation-label` (0046 item 7, 0062). The introduction gains 0054's sentence on settings blocks.

2. **`physical-phenomena`** is renamed `physical-phenomenon`, since it repeats (a repeatable property stays singular). It gains the terms Fracture and Plasticity.

3. **`problem-specification`:**
   - `time-dependence` loses the term "Property prediction".
   - `free-energy` is renamed `free-energy-density` and becomes repeatable, one entry per term (e.g. f_chem, f_elastic), since each equation names the terms that drive it.
   - `governing-equation › type` becomes repeatable. An anti-trapping current and a sharp- or thin-interface formulation are given as user-specified terms.
   - In `type`, "Fluid" becomes "Navier-Stokes" (the flow equation; evolved variable the velocity) and "Multi" becomes "Multi-phase-field" (several phase fields constrained to sum to one). "Coupled" and "Diffuse" are removed: coupling is several `governing-equation` entries, and every phase-field interface is diffuse.
   - `type` gains "Mechanical equilibrium" (evolved variable the displacement) and "Poisson" (electrostatics; evolved variable the electric potential). Equations solved together with the phase field belong to the one PF computation, so minimal `method` stays PF; a separately run code is a computation of its own, linked by an input (0046).
   - `governing-equation › evolved-variable` is defined as "The name of the field-variable being evolved by this equation."
   - `governing-equation › driving-energy` is renamed `free-energy-density-term`.
   - No property is added for a thermodynamic database: too detailed. It can be given in `free-energy-density`'s description or as a file of the computation's software.

4. **`domain-and-mesh`** is renamed `domain`, and `mesh-type` moves to `numerical-method`. In `domain`:
   - `domain-size` gets a note: it applies as given to a regular domain; for an irregular geometry, whose mesh is given in `numerical-method`, it may give a characteristic size of the structure.
   - `boundary-conditions`: "NoFlux" becomes "Zero-Neumann". Where each boundary lies is given in the mesh file (item 5).
   - `initial-conditions`: an initial state produced by an algorithm or given as a spatial distribution is a user-specified value; no term is added.

5. **`numerical-method`** gains:
   - `mesh-type`, moved from `domain`;
   - `mesh-file`, a file the record carries or points to (0056: `name`, `description`, `contents`, `encoding`, `link`, `checksum`), holding the mesh and the boundaries on which the boundary conditions apply;
   - `spatial-discretization-parameter`, a repeatable generic parameter (0016) for the parameters of the spatial discretization, e.g. the element degree, the quadrature rule or the stencil;
   - `evolved-variable`, optional and repeatable, naming the equations the entry solves by their evolved variables. It is given when equations are solved by different methods or solvers, one `numerical-method` entry for each group, and omitted when one entry covers every equation.

   `temporal-discretization` loses "Implicit" and "Explicit", since its other terms name implicit and explicit schemes. `solver` gains "Explicit" (no system of equations is solved) and further solvers (see the Consequences).

6. **`variables › field-variable`**: each field variable is a separate entry, e.g. one concentration entry per component of a 20-component alloy. Its documentation says so.

## Consequences
- Applied in a structure pull request and then the property pull requests of status step 5, in file order, as for mbpt and ml:
  - The structure pull request: `settings` and `computation-label`, the renames of items 2, 3 and 4 and the move of `mesh-type`, and the introduction. It fills no typed field. examples/pf.json moves into settings under the new names.
  - Each property pull request fills its typed fields and applies the term changes and new members above.
- examples/pf.json gives `temporal-discretization` "Implicit", which item 5 removes; the numerical-method pull request replaces it with a term that fits the source.
- No released instance breaks: pf's properties were legacy text in 0.6.0.
- PROPOSED, NOT DECIDED:
  - the solver terms beside "Explicit";
  - whether `free-energy-density › unit` drops "(or of the free energy, if `expression` is not a density)" (0001 A7.3), now that the property is a density;
  - "Mixed" in `temporal-discretization`, and the spelling "Crank-Nicholson" (the scheme is Crank–Nicolson);
  - how a boundary condition names its boundary in `mesh-file`, and the overlap of "Fixed" with "Dirichlet" and of "Free" with "Zero-Neumann";
  - how `time-dependence` relates to minimal `conditions › type` (thermodynamic-state, time-dependence; 0036).
