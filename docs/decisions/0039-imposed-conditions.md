# 0039 — Simulation conditions are imposed, and say so

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee feedback: `heat-flux` and `temperature-gradient` are framed as simulation conditions only, although both can be measured output. More generally, a simulation condition is an imposed condition, and the definitions do not say so; only the note on `simulation-conditions` does ("Giving a condition means that its value is imposed on the simulation as an external constraint", 0026). The decider asked for every condition's definition to be fixed and reviewed, and for natural definitions where a well-understood term was avoided in its own definition (e.g. temperature as "a measure of the hotness or coldness of an external heat bath").

In a Müller-Plathe simulation the heat flux is imposed and the temperature gradient is measured; with two thermostatted regions the gradient is imposed and the flux is measured. A quantity measured during a run is part of the data the dataset holds, not a condition. §2.7 (derived properties) covers quantities computed from such data in post-processing, so a measured quantity is not sent there.

## Decision
1. **Definitions.** Each says what is imposed, in the property's own terms:
   - `simulation-conditions`: "The conditions imposed on the simulated system during the computation, e.g. by a thermostat, a barostat, a loading device or a fixed simulation cell."
   - `number-of-particles`: "The number of particles (atoms or other discrete entities) in the simulated system, as imposed by the simulation."
   - `volume`: "The volume of the simulated system, as imposed by the simulation."
   - `mass-density`: "The mass density of the simulated system, as imposed by the simulation."
   - `cell`: "The simulation cell, as imposed by the simulation."
   - `cell-reference`: "The simulation cell in the reference configuration, relative to which strain and strain rate are defined."
   - `cell-periodicity`: "Whether periodic boundary conditions are applied along each cell vector, for both cell and cell-reference."
   - `temperature`: "The temperature imposed on the simulated system, e.g. by a thermostat or a heat bath in thermal contact with it."
   - `stress`: "The stress, normal and shear components, imposed on the simulated system, e.g. by a barostat or an external loading device."
   - `strain`: "The strain imposed on the simulation cell relative to cell-reference, as the Lagrangian strain tensor."
   - `strain-rate`: "The strain rate imposed on the simulation cell relative to cell-reference, as the time derivative of the Lagrangian strain tensor."
   - `heat-flux`: "The heat flux imposed on the simulated system, the thermal energy per unit area per unit time driven through it, e.g. by exchanging energy between a heat source and a heat sink."
   - `temperature-gradient`: "The temperature gradient imposed on the simulated system, e.g. by thermostatting two regions at different temperatures."
2. **The note on `simulation-conditions`** becomes: "Note: The conditions below, other than type and description, are given as appropriate to the simulation. Each is imposed on the simulation as an external constraint. A quantity computed from the simulation, e.g. a heat flux measured under an imposed temperature gradient or the temperature of a microcanonical run, is a result, not a condition, and is not given here. A condition that varies is given as several entries, each with a qualifier; the description explains how it varies."
3. **`heat-flux` and `temperature-gradient`** each gain the note "Note: Give heat-flux or temperature-gradient, whichever the simulation imposes; the other is a result."
4. **Basis notes**, reworded alike: `stress` Note 1 becomes "Note 1: Requires cell, which defines the basis of the tensor components."; the notes of `strain` and `strain-rate` become "Note: Requires cell-reference, which defines the basis of the tensor components." (`strain-rate`'s lacked its "Note: " and final period).
5. **Value notes**: `cell`'s "supercell vector lengths" becomes "cell vector lengths"; `heat-flux`'s "heat flux vector q" becomes "heat flux vector <i>q</i>".

## Consequences
- One pull request applies items 1–5 (schema, tests, regenerated page). Wording only: no structure changes and no instance is affected.
- Under item 2, an NPT run gives the imposed `stress`, not an average volume, and a grand-canonical run gives at most the Initial number of particles; a qualifier's Average (0035) applies to an imposed condition that varies.
- PROPOSED, NOT DECIDED: whether the minimal metadata should list the quantities a dataset contains (e.g. energies, forces, a heat flux).
