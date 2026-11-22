# 0077 — How many computations a record gives

Date: 2026-11-22. Status: accepted. Decided by: Ellad Tadmor.

## Context
A computation is "a group of calculations in the dataset that share one method and one set of settings" (0046). Nothing says how finely a record should divide the work into computations. §1.2 states that MatCore describes a dataset and does not reproduce its execution, and 0063 records the stages of a simulation only when the dataset contains or depends on their data. Even so, it is easy to write one computation per step, and the record then becomes a workflow.

A worked Raman example (review of 0076, 2026-11-22) showed this. It had six computations:
- a DFT relaxation;
- DFT forces on displaced cells;
- a phonon post-processing;
- DFT susceptibilities;
- a Raman post-processing.

It also had a derived block for each post-processing computation, and those blocks repeated what the computations already said. The dataset is explained as well by two computations:
- `dft` (DFT, Single point), holding the displaced-cell forces and the susceptibilities;
- `raman` (DP, Property calculation), naming `dft` in `input` with role Source data, with one derived block for both properties.

The human adopted this grouping for derived in the review of the derived structure pull request: the derived introduction states it. The same over-division threatens every section. For example, a DFT relaxation that only fixes the cell for later single points need not be a computation of its own.

## Decision
1. **minimal `computation`** gains a note, placed before 0063's note on staged simulations:

   "Note: The record explains the dataset; it does not retrace the workflow that produced it (§1.2). Give a computation for calculations whose results are in the dataset, or whose method or settings a reader needs in order to understand the data. Steps that serve one purpose with one method are one computation, e.g. the post-processing steps that give phonon modes and then a Raman spectrum (method DP). A step that only prepares another computation and adds nothing a reader needs, e.g. a relaxation that fixes the cell for later single points, may be left out or mentioned in the description of the computation it prepares."

2. **0063 stands.** Its note applies the same test to a simulation run in stages: a stage is a computation when the dataset contains or depends on its data.

3. **Settings follow the property.** The parameters of a procedure are given with the procedure, in the section that describes it, even when the procedure applies them in calculations of another computation. For example, the finite-difference displacement of a Raman calculation is given in its derived entry, not in the description of the DFT computation. The derived introduction states this (0076, review of 2026-11-22). This ruling makes it the rule for every section.

## Consequences
- One pull request adds the note of item 1 to schema/minimal.yaml, with a test and the regenerated page. No example changes: each example's computations already hold data in its dataset.
- The derived structure pull request (0076) already carries the derived introduction's statement of items 1 and 3.
- No released instance breaks: the note is guidance and changes no property.
- Still PROPOSED, NOT DECIDED (0046): whether a series of runs that differ only in an imposed condition is one computation or several.
