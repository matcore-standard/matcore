# 0026 — Simulation conditions and composition that vary

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback:
- "What about semi-grand-canonical where the concentration varies (same for other "concentration" fields)?"
- "The current schema appears to be optimized for spatially and temporally homogeneous simulations: a single ensemble applied to the entire simulation cell, with constant temperature, stress, strain rate, etc., for the whole run. This is a workable starting point, but most modern atomistic simulations in materials science deviate from it in one of these two directions, and the schema currently has no structural place for the corresponding metadata."

In minimal, `computation › simulation-conditions` is a single entry whose conditions each hold one value, imposed on the simulation; `structure › material-component` fixes the composition. Neither says what a value means when it changes during the run or across the system.

The metadata documents the essence of a simulation, not every detail of its input files. Alternatives weighed and rejected on that ground:
- **A repeatable `simulation-conditions` with a stage, a region, a duration, and a final value beside each value** (for ramps). It records the protocol the input files already hold, and the final value amends the fixed value + unit form of 0015.
- **A `description` beside each condition's value and unit.** It amends 0015, and cannot reach the conditions that are leaves (`number-of-particles`, `strain`; 0015, third amendment), although `number-of-particles` is the value that varies in a grand-canonical run.
- **A `chemical-potential` condition in minimal.** The imposed chemical potentials of a grand-canonical or semi-grand-canonical simulation go in the description below, and in md's `thermodynamic-constraint`, whose generic `td-parameter` can hold them with their unit.

## Decision
1. **`simulation-conditions › description`** becomes: "Explanatory text clarifying the simulation type, and how any condition varies in space or time, e.g. a temperature ramp, a thermostat applied to part of the system, or a composition set by chemical potentials. For a condition that varies, it states what the given value represents, e.g. the initial, mean or final value, or the value in one region." (was "Explanatory text clarifying the simulation type selection.")
2. **The note on `simulation-conditions`** is reworded, since it named the conditions "SubSubProperties", a term from the baseline's tables that does not fit the nested tree: "Note: The conditions below, other than type, description, spatially-varying and time-varying, are given as appropriate to the simulation. Giving a condition means that its value is imposed on the simulation as an external constraint. A condition that varies in space or time gives a single representative value, which the description explains." (was "Note: The SubSubProperties listed below (aside from type and description) are provided as appropriate given the nature of the simulation. Providing a SubSubProperty means that its value is imposed on the simulation as an external constraint.")
3. **`strain-rate`**'s description drops "which is constant throughout the simulation", which item 2 would contradict.
4. **`stress`**'s first note, for the same reason, says "cell" instead of "the cell subproperty": "Note 1: Requires the definition of cell in order for a basis to be defined relative to which the tensor components are given." No other text in minimal or dft uses "SubProperty" or "SubSubProperty".
5. **Two optional flags** follow `description`, so that a search can find simulations whose conditions vary; both bool, `[]`, inapplicable, values null, not repeatable:
   - **`spatially-varying`**: "Whether any imposed condition varies across the system, e.g. a thermostat applied to part of it."
   - **`time-varying`**: "Whether any imposed condition changes during the simulation, e.g. a temperature ramp or a change of ensemble."

   Each carries the note "Note: If true, describe the details in `description`." The prefix `simulation-is-` was declined (the parent names the simulation), as was "inhomogeneous" (unclear for time) and `time-dependent` (pf's `time-dependence` describes the governing equation). An omitted flag means not stated; required flags were declined, so that a uniform equilibrium run needs no "false" entries.
6. **`concentration`** and **`fraction`** each gain a sentence in their values note: "When the composition changes during the simulation (e.g. semi-grand-canonical Monte Carlo), give the composition as set up." These are the only composition fields in the schema.

## Consequences
- One pull request applies items 1–6 (schema, tests, regenerated page). The flags are optional: no instance is affected, and examples/minimal.xml needs no change.
- Which conditions vary, and how, is prose; the validator does not check it.
- PROPOSED, NOT DECIDED (md, status step 5): a `thermodynamic-constraint` type term for the semi-grand-canonical ensemble, and whether its `system` field states the region a constraint applies to in the same way as the description of item 1.
