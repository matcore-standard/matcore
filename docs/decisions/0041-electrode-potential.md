# 0041 — Electrode potential

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
The feedback of 0040 named an electrostatic potential among the missing conditions. In electrochemistry (constant-potential MD, grand-canonical DFT) the imposed quantity is the potential of an electrode, and it means nothing without the reference it is measured against. A convention that a unit cannot express is a separate required enumerated subproperty, never part of the unit string (CLAUDE.md, Units model; 0001).

Annex U has no Kind for an electric potential. This record adds it (0004).

## Decision
1. **A new Kind** `ElectricPotential` in schema/units.yaml, its fields traced to QUDT 3.3.0 in the pull request that adds its first unit.
2. **A new unit** `V` (ElectricPotential), by its own pull request, every field traced to its primary source (0004).
3. **A new condition `electrode-potential`** in minimal `computation › simulation-conditions`, after `body-force`: a repeatable container of, in order:
   - `value*`: float, `[]`, ElectricPotential, recommended unit `V`, in the fixed form of 0015;
   - `unit*`: in the fixed form of 0015;
   - `reference*`: string, `[]`, inapplicable, open terms SHE, RHE, Vacuum. Description: "The reference against which the potential is given." Note: "One of: "SHE" – The standard hydrogen electrode. "RHE" – The reversible hydrogen electrode, at the pH of the simulation. "Vacuum" – The vacuum level, giving an absolute potential."
   - `qualifier`: as for the other conditions (0035).

   Description: "The potential of the working electrode imposed on the simulated system, e.g. by a potentiostat in a constant-potential simulation, relative to the reference given in `reference`."

   The entries follow the rule of 0035: without a qualifier, one entry. A simulation that imposes the potentials of several electrodes gives the working electrode's here and the others in `description`.

## Consequences
- Pull requests, in order: the unit `V` (adding the Kind), then one applying item 3 (schema, tests, regenerated page), after the 0040 pull requests. No instance is affected.
- PROPOSED, NOT DECIDED: an `electrode` subproperty naming the electrode, so that several electrodes can each have entries, if datasets need it.
