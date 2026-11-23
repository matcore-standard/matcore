# 0082 — Constraints on and potentials applied to groups of particles

Date: 2026-11-22. Status: accepted. Decided by: Ellad Tadmor.

## Context
A reviewer's written feedback on MatCore-MD 0.3.0 (committee review of 2026-09-23) notes that a particle simulation often treats groups of particles in the cell differently:

> fixed slabs supporting a free surface, tethered atoms holding a reference frame, rigid blocks driven as indenters or pistons; per-group SHAKE / RATTLE / LINCS holonomic constraints, rigid-body integrators, centre-of-mass constraints; 2D- or 1D-restricted atoms in slab and wire geometries.

The feedback also names flexible (Green's-function and lattice-Green's-function) boundary conditions and externally applied potentials such as harmonic walls, indenter potentials and synthetic grain-boundary driving forces. It observes that PF has a boundary-conditions vocabulary and MD has none.

Much of that feedback is met by later rulings: stages and carry-over of state (0063), varying conditions (0035, 0026), a thermostat on a group (0069 `system`), rare-event algorithms (0064, 0066) and their variants (0067). But ps still has no place for a constraint on, or a potential applied to, a group of particles. `thermodynamic-constraint › system` names a group only for an ensemble's thermostat or barostat.

## Decision
1. **ps `settings` gains `particle-constraint`**, optional and repeatable, after `thermodynamic-constraint`. Its description: "A constraint on, or a potential applied to, a group of particles." One entry per group and constraint. Members:
   - `system*`: a string naming the particles in words, as `thermodynamic-constraint › system` does, e.g. "Bottom three atomic layers of the slab", "Indenter block", "Water molecules (O–H bonds and H–O–H angle)". No atom indices or code group names: they belong to one input file, which the record does not carry (§1.2).
   - `type*`: a string with open terms in two groups, each defined in a note (0007 item 5):
     - Motion constraints: Fixed, Tethered, Restricted (to a plane or a line), Rigid body, Holonomic (e.g. SHAKE, RATTLE, LINCS), Centre of mass, Prescribed motion, Flexible boundary (boundary particles moved by the elastic, Green's-function response to the forces on them);
     - Applied potentials: Wall, Indenter, Driving potential (e.g. a synthetic grain-boundary driving force).
   - `description`: the form and variant, and the role of each `computation-parameter` entry it uses (spring constants, an indenter's radius and speed), as 0067 does for algorithms.
2. **No ps boundary-conditions property.** A particle simulation's boundaries are minimal `conditions › cell-periodicity` together with `particle-constraint` entries (Fixed, Flexible boundary, Wall). This is the counterpart of PF's `boundary-conditions`, which constrain continuous fields.
3. **SLLOD shear needs no change.** The imposed shear rate is minimal `conditions › strain-rate`, and a rate history is given as its qualified entries (0035). SLLOD is a user-specified ps `algorithm` term, with the Lees–Edwards boundary stated in `settings › description`.

## Consequences
- One pull request: schema/ps.yaml (the container, its term definitions drafted in the PR), tests and the regenerated ps page and JSON Schema. Each example is reviewed (0012); examples/ps.json, which has no constraint, is expected to stay unchanged.
- An optional property is added, so no released record breaks.
