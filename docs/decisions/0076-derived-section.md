# 0076 — The derived section: properties attached to computations, and post-processing as a method

Date: 2026-11-21. Status: accepted. Decided by: Ellad Tadmor.

## Context
The derived section was written before 0046, when a dataset was assumed to come from one method. Its introduction limits derived properties to a single method, with MBPT as the one exception. It is also the only section whose properties name no computation.

Take the section's own example, a Raman spectrum (Materials Cloud 2024.116), and record it as 0046 does:
1. a DFT relaxation (task Optimization);
2. displaced supercells (task Structure generation);
3. DFT forces on them (task Single point);
4. force constants and phonon modes from those forces (task Property calculation, input 3 with role Source data);
5. DFT susceptibilities of structures displaced along each mode (task Single point);
6. the Raman tensor and spectrum (task Property calculation, inputs 4 and 5 with role Source data).

This shows three things:
- 0046's input links already combine methods, so the single-method limit is no longer needed.
- The derived description cannot say that computation 6 produced the spectrum, nor from what.
- Computations 4 and 6 have no `method` term, though `method` is required: they solve no physical model and only process other computations' results. This is part of 0065's open point on computations with no method term.

CWA 17284:2018 (MODA) defines post-processing as "operations on raw output of solvers without altering the physical system state" (§3.12). Its template records a post-processing step as the processed output, the methodologies and the margin of error (Table 7, items 4.1–4.3).

Within the section:
- `type` mixes kinds of property (Electronic, Magnetic, Transport) with techniques (Linear-response, NMR, Microscopy). It lacks mechanical and thermodynamic properties.
- `description` holds both the property's name and its explanation.
- `calculation-method` repeats in order to chain steps, which 0046 records as computations.

## Decision
1. **Settings.** derived's properties sit in a required, repeatable `settings` whose first member is `computation-label` (0046 item 7, 0062). A derived block may name any computation that obtains a property. That may be a computation of method DP (item 3), but also, for example, a DFT computation that computes phonons by density functional perturbation theory, or a PS computation that gives a Green-Kubo thermal conductivity. Such a computation has its own method's block beside the derived block.

2. **Introduction.**
   - The single-method note and the MBPT exception are removed.
   - The introduction says that a property obtained from several computations names them in minimal `computation › input`: with the role Source data for results it processes, and with the role Interaction model for energies and forces it requests (0067).
   - It gains 0054's sentence on settings blocks.

3. **Post-processing in minimal.**
   - `method-class` gains "Post-processing": operations on the results of other computations that do not alter the physical system's state (CWA 17284:2018 §3.12).
   - `method` gains, under it, "DP" – Derived Property: a property obtained from the results of other computations by a procedure with no physical model of its own. Examples: force constants from finite-difference forces, an X-ray diffraction pattern from a structure, a vibrational density of states from a trajectory.
   - DP names the derived section, as DFT names dft (0064).
   - The note on method-class's categories says that Post-processing comes from the CWA's definition, not from its classification of models.
   - This settles 0065's open point for post-processing computations. It remains open for generation without a model and for a fit without a machine-learning model, e.g. force matching.

4. **`derived-property`** keeps its place, one entry for each property. Its members, in order:
   - `type*`;
   - a new `name*`: the specific property, e.g. Raman spectrum or phonon dispersion;
   - `description*`: an explanation of the property;
   - `procedure*`: how the property was obtained from the computation's inputs, explaining each `calculation-parameter` entry, as ps `settings › description` does (0067);
   - `calculation-parameter`: the generic parameter (0016).

   `calculation-method` is removed. Its description becomes `procedure`, and its `calculation-parameter` moves up into `derived-property`. Steps that are separate computations are recorded as computations.

5. **`type`** is the kind of property computed. "Linear-response" is replaced by "Vibrational" (phonon modes and dispersion, interatomic force constants, vibrational density of states). "Mechanical" (e.g. elastic constants) and "Thermodynamic" (e.g. free energies, heat capacities, formation energies) are added. The full list and the definitions are settled in the type pull request.

6. **No accuracy property.** The margin of error (CWA Table 7, item 4.3) is not added. How results and their uncertainty are described is 0039's open question, which concerns every section.

## Consequences
- Applied in a structure pull request, then the property pull requests of status step 5, as for mbpt, ml and pf.
  - The structure pull request:
    - derived's `settings` and `computation-label`;
    - the moves and the removal of item 4;
    - the introduction;
    - minimal's new method-class and method terms, with their definitions and notes;
    - §1.2's list of sections if it needs DP;
    - examples/derived.json in settings, naming a Raman computation.
  - The property pull requests fill the typed fields, add `name` and `procedure`, and settle `type`'s terms.
- No released instance breaks: derived was legacy text in 0.6.0, and minimal gains terms without losing any.
- PROPOSED, NOT DECIDED: the `method` of a computation that generates structures without a model, or that fits a model without machine learning, e.g. force matching (0065).
