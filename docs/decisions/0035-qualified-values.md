# 0035 — Values that vary are given as qualified entries

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee proposal, raised with 0034: give a value that varies as several entries, each with a value and a word saying what it represents (minimum, maximum, average, initial, final). This would serve the simulation conditions (`temperature`, `stress`, …) and the composition, where today a varying condition gives a single representative value explained in prose (0026), and `fraction` gives the composition "as set up".

0026 weighed "a final value beside each value" and declined it, partly because it changes the fixed value + unit form of 0015. This record takes up that question again at the decider's request, so it amends 0015 and 0026.

0034 already gives a formula `variable` a `type` with the terms Average, Final, Initial, Maximum, Minimum. `simulation-conditions` already has a `type` (Equilibrium, …). A second `type` under each condition would repeat the confusion that 0034's third amendment removed for `formula`.

## Decision
1. **`qualifier`** is the name, throughout the standard, of the subproperty that says what a value represents. It is a leaf in one fixed form: string, `[]`, inapplicable, not repeatable, description "What the value represents.", with open terms Average, Final, Initial, Maximum, Minimum. Its `required` flag and its note depend on where it sits. `variable › type` (0034) is renamed `qualifier` and stays required there; a fixed composition is still written as a number in the formula.
2. **Each simulation condition with a numerical value** in minimal `computation › simulation-conditions` becomes repeatable and gains an optional `qualifier` after its value (and unit): `number-of-particles`, `volume`, `mass-density`, `number-density`, `cell`, `cell-reference`, `temperature`, `stress`, `strain`, `strain-rate`, `heat-flux`, `temperature-gradient`. `cell-periodicity` (a bool), `type`, `description`, `spatially-varying` and `time-varying` are unchanged.
   - The quantities with a unit become containers of `value*`, `unit*` and `qualifier`.
   - `number-of-particles` and `strain`, leaves today (0015, third amendment), become containers of `value*` and `qualifier`, with no unit. Their `value` keeps the type, extent, Kind and values of the present leaf, with the description "The value of the property."
   - The `qualifier` note in a condition: "Without a qualifier, the value holds throughout the simulation and across the system, and the entry is the only one for the condition. Otherwise give one entry for each qualifier that applies, e.g. Initial and Final for a ramp, Minimum and Maximum for a range. For a vector or tensor, Minimum and Maximum are taken component by component."
3. **The note on `simulation-conditions`** ends "A condition that varies is given as several entries, each with a qualifier; the description explains how it varies." in place of "A condition that varies in space or time gives a single representative value, which the description explains." (0026 item 2).
4. **`simulation-conditions › description`**'s second sentence becomes "For a condition that varies, it states how, e.g. the shape of a ramp or the region a value applies to." in place of "For a condition that varies, it states what the given value represents, e.g. the initial, mean or final value, or the value in one region." (0026 item 1). The flags `spatially-varying` and `time-varying` stay: a Minimum or Maximum does not say whether the variation is in space or in time.
5. **`material-component › fraction`** becomes a repeatable container of `value*` (float, `[]`, dimensionless, 0–1, description "The value of the property.") and `qualifier`, with the same `qualifier` note as item 2. Its description is kept. Its values note becomes "The fractions of a structure's components sum to 1, for the entries without a qualifier and for each of Initial, Final and Average." The sentence "When the composition changes during the simulation (e.g. semi-grand-canonical Monte Carlo), give the composition as set up." (0026 item 6) is removed.
6. **0015 is amended**: a quantity's container may hold a `qualifier` leaf in the form of item 1 beside `value` and `unit`; a dimensionless `value` may sit in a container with a `qualifier` and no `unit`. scripts/check_units.py checks the `qualifier` form wherever one appears.

## Consequences
- One pull request applies items 1–6 (schema, check_units.py, check_formula.py's reading of `variable`, tests, regenerated page). It breaks 0.5.0 instances: `number-of-particles`, `strain` and `fraction` become containers, and `variable › type` is renamed.
- examples/minimal.xml gives only the simulation `type` and no fraction or variable, so it needs no change.
- That an entry without a qualifier stands alone, and that no qualifier repeats, is stated in the note; the step 9 instance validator checks it.
- Properties in later sections (md, mbpt, ml, pf, derived) that give a varying value use the same `qualifier` in their own pull requests.
