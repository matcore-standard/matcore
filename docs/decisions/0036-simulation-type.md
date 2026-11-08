# 0036 — The simulation type is classified along four axes

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on minimal `computation › simulation-conditions › type` (terms Equilibrium, Nonequilibrium, Other): "What about a steady-state simulation? What about a time-evolving simulation trending toward equilibrium?"

The decider proposed making `type` a container of four classifications (thermodynamic state, system openness, time dependence, spatial uniformity), with a note pointing to `description`, and removing the bool flags `spatially-varying` and `time-varying` (0026 item 5), which two of the classifications capture.

Review of the proposed terms:
- For the thermodynamic state, Nonequilibrium covers both Steady state and Transient, and Driven cuts across them (a sheared liquid is driven and steady; the first cycles of fatigue loading are driven and transient). Three mutually exclusive terms remain. A driving shows in the conditions given (`strain-rate`, `heat-flux`, `temperature-gradient`).
- Time dependence and spatial uniformity could describe the imposed conditions or the simulated system (Static could mean a single-point calculation). Only a classification of the imposed conditions replaces the flags, which also told whether a Minimum and Maximum (0035) range over space or over time. The terms are chosen so that they cannot be read as describing the system.

## Decision
1. **`simulation-conditions › type`** becomes a container, required and not repeatable as now. Description: "The nature of the simulation being performed." Note: "Note: Detailed explanations of the simulation conditions are given in `description`." Its subproperties, in order, each a string, `[]`, inapplicable, not repeatable, with open terms defined in its values note:
   - **`thermodynamic-state`**: required. Description: "Whether the simulated system is at equilibrium, in a steady state, or evolving in time." Terms:
     - "Equilibrium" – The system samples thermodynamic equilibrium.
     - "Steady state" – A nonequilibrium state whose averages do not change in time, maintained by a driving such as a strain rate or a heat flux.
     - "Transient" – A state whose averages change in time, e.g. relaxation toward equilibrium or a steady state, or a quench.
   - **`system-openness`**: optional. Description: "What the system exchanges with its surroundings." Terms:
     - "Isolated" – Exchanges neither energy nor particles, e.g. the microcanonical ensemble.
     - "Closed" – Exchanges energy but not particles, e.g. the canonical or isothermal-isobaric ensemble.
     - "Open" – Exchanges particles, or their species, with a reservoir, e.g. the grand-canonical or semi-grand-canonical ensemble.
   - **`time-dependence`**: optional. Description: "How the imposed conditions change during the simulation." Terms:
     - "Constant" – No imposed condition changes.
     - "Varying" – An imposed condition changes, e.g. a temperature ramp or a change of ensemble.
     - "Cyclic" – An imposed condition changes periodically, e.g. cyclic loading.
   - **`spatial-uniformity`**: optional. Description: "How the imposed conditions vary across the system." Terms:
     - "Uniform" – Every imposed condition is the same throughout the system.
     - "Nonuniform" – An imposed condition differs between parts of the system, e.g. a thermostat applied to part of it.
     - "Periodic" – An imposed condition varies periodically across the system, e.g. sinusoidal heating. Not to be confused with `cell-periodicity`.
2. **The terms Equilibrium, Nonequilibrium and Other** of the present `type` are removed; Equilibrium moves to `thermodynamic-state`.
3. **`spatially-varying` and `time-varying` are removed** (reverses 0026 item 5; 0035 item 4 kept them). `spatial-uniformity` and `time-dependence` say what they said, with more detail.
4. **The note on `simulation-conditions`** begins "Note: The conditions below, other than type and description, are given as appropriate to the simulation." in place of "Note: The conditions below, other than type, description, spatially-varying and time-varying, are given as appropriate to the simulation."
5. **examples/minimal.xml** writes `<type><thermodynamic-state>Equilibrium</thermodynamic-state></type>`.

## Consequences
- One pull request applies items 1–5 (schema, tests, regenerated page, example). It breaks 0.5.0 instances: `type` becomes a container, and the flags are gone.
- md's `thermodynamic-constraint` (the ensemble) overlaps `system-openness`; how they relate is taken up in the md pull requests.
