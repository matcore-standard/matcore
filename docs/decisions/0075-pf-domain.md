# 0075 — PF domain: reduced units without a flag, and boundary conditions that name their boundary

Date: 2026-11-20. Status: accepted. Decided by: Ellad Tadmor.

## Context
The cross-check of pf `domain` against the baseline .docx raised three points.

1. **Reduced units.** Phase field simulations often run in reduced units: lengths in units of an interface width, times in units of a relaxation time. In the section's example, the grid spacing is 1.0 and the time step 0.01, both pure numbers. 0003 gives `domain-size`, `grid-spacing` and `time-step-size` a required `scaling` (physical, nondimensional): when nondimensional, `unit` SHALL be `dimensionless`. The flag carries nothing the unit does not. A unit of `dimensionless` already says the value is reduced, and a Length or Time symbol already says it is physical. §1.3 already allows the case: where a `unit` is given for a pure number, "as in ... a nondimensional length", it is `dimensionless`.
2. **Where a boundary condition applies.** `boundary-conditions` is a repeatable string. It cannot say which boundary a condition applies to, nor which field variable it constrains. 0074 puts the boundaries in `numerical-method › mesh-file` and leaves open how a condition names one.
3. **Overlapping terms.** "Fixed" (a prescribed value) is a Dirichlet condition. "Free" (a traction-free surface, the natural condition) is a zero Neumann condition.

## Decision
1. **No `scaling`** (amends 0003). `domain-size`, `grid-spacing` and `time-step-size` are each `value` + `unit`, with Kind Length (Time for `time-step-size`) and recommended unit m (s). A note on each says:
   - `unit` is a Length (Time) symbol from Annex U, or `dimensionless` when the simulation uses reduced units;
   - in that case the characteristic length (time) is given as a `model-parameter` entry, so the values can be converted.

   The step 9 instance validator accepts `dimensionless` for these three properties. No conditional rule is needed, so none is written in §1.3.
2. **`boundary-conditions`** becomes a repeatable container of:
   - `type*`: the kind of condition;
   - `boundary`: the name of a boundary in `numerical-method › mesh-file`, or a description such as "x = 0". It is omitted when the condition applies to every boundary;
   - `field-variable`: the name of the `field-variable` entry the condition constrains. It is omitted when the condition applies to every field variable.
3. **`type`'s terms** are Dirichlet, Neumann, Zero-Neumann and Periodic, each defined. "Fixed" and "Free" are removed: a fixed value is Dirichlet, and a free surface is Zero-Neumann.

## Consequences
- Applied in the pf domain pull request (items 1 for `domain-size`, 2 and 3). `grid-spacing` and `time-step-size` follow in the numerical-method pull request.
- examples/pf.json writes `domain-size` as value + unit (`dimensionless`) and its boundary condition as an entry with `type` Periodic.
- Settles 0074's open points on how a boundary condition names its boundary, and on Fixed and Free.
- Settles, by making it unnecessary, the open point in CLAUDE.md on stating conditional validation rules once in §1.3 for `scaling`.
- No released instance breaks: pf's properties were legacy text in 0.6.0.
