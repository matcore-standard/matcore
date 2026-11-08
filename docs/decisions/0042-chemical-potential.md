# 0042 — Chemical potential, and md's alignment with the simulation conditions

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
0026 declined a `chemical-potential` condition in minimal and pointed to md's `thermodynamic-constraint`; 0040 deferred the question to the md work. Since then:
- 0036 lets a simulation be Open (`type › system-openness`), but minimal cannot say what it is open to.
- md's `thermodynamic-constraint` lists the ensembles μVT and μPT, but a chemical potential could only be a generic `td-parameter`: no species, a free unit of Kind `any`, and only for MD. Grand-canonical and semi-grand-canonical Monte Carlo, the most common users of an imposed chemical potential, are not MD; phase-field models impose chemical potentials too.
- A chemical potential is held fixed by a reservoir, as a temperature is by a thermostat: an imposed condition in the sense of 0039.

## Decision
1. **A new condition `chemical-potential`** in minimal `computation › simulation-conditions`, after `electrode-potential`. Description: "The chemical potential of a species imposed on the simulated system by a reservoir, e.g. in a grand-canonical or semi-grand-canonical simulation." A repeatable container of, in order (value and unit first, as in `electrode-potential`):
   - **`value`**: required; float, `[]`, Kind Energy, recommended unit `eV`, in the fixed form of 0015. Note: "The chemical potential <i>μ</i> per particle, or the difference <i>μ</i>(species) − <i>μ</i>(relative-to). An absolute value is relative to the energy zero of the model given in `interaction-model`, so absolute values from different models do not compare. A value in a molar unit (e.g. kJ/mol) is converted to an energy per particle before it is given."
   - **`unit`**: required, in the fixed form of 0015.
   - **`species`**: required; string, `[]`, inapplicable. Description: "The species whose chemical potential is given, as an element symbol, a user-defined species or a group of a material component's formula." Example: Cu, H2O, Ja.
   - **`relative-to`**: optional; string, `[]`, inapplicable. Description: "A second species, when the value is the difference between the chemical potentials of species and of this one." Note: "Note: Give relative-to when the simulation imposes a difference of chemical potentials, as a semi-grand-canonical simulation does."
   - **`qualifier`**: optional, in the fixed form of 0035. Since there is one entry per species (or pair), its note reads as for the other conditions but with "the only one for the species" in place of "the only one for the condition" (0035 lets the note depend on where the qualifier sits).
2. **Out of scope**: the electron chemical potential (the Fermi level in grand-canonical DFT) is not a species of `formula`; an imposed electrode potential is given by `electrode-potential` (0041).
3. **md is aligned with the simulation conditions.** md does not repeat a quantity that `simulation-conditions` holds (temperature, stress, chemical potential, …). It adds only what is specific to MD: how a condition is enforced (e.g. the thermostat or barostat and its parameters) and the ensemble. The md pull requests apply this, starting with `thermodynamic-constraint`, whose `td-parameter` then holds enforcement parameters only.

## Consequences
- One pull request applies items 1 and 2 (schema, tests, regenerated page). No instance is affected: the condition is new and optional.
- That `species` and `relative-to` name a symbol or group of a material component's formula, and that the qualifier rule holds per species, are checked by the step 9 instance validator.
- Supersedes the part of 0026 that declined a `chemical-potential` condition in minimal.
