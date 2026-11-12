# 0063 — How a simulation run in stages is described

Date: 2026-11-12. Status: accepted. Decided by: Ellad Tadmor.

## Context
A reviewer asked how a multi-stage trajectory (e.g. heating, equilibration, a quench, then loading) is documented: as a chain of repeated `computation` entries, as a protocol object listing stages, or as per-field time series; and, if as a chain, how the order of the stages and the carry-over of state (positions, velocities, accumulated strain) are expressed.

0046 already answers most of this, but nowhere in the schema says so. A computation is a group of calculations that share one method and one set of settings; a computation names another in `input` with a role; and §1.2 states that MatCore describes a dataset, not how to reproduce its execution, so the order of the calculations and their control flow belong to a workflow manager's provenance record. A condition that changes within one run is given as entries with a qualifier (0035), as in the `md-quench` example's temperature ramp. The human ruled that the comment needs no new structure, since a sequence of computations is not managed at the minimal level, but that the standard should explain this.

## Decision
1. **minimal `computation`** gains the note: "Note: A simulation run in stages, e.g. heating, equilibration and a quench, is described as one computation for each stage whose method, settings or conditions differ and whose data the dataset contains or depends on. Each stage names the stage it continues from in `input` with the role Initial configuration, which carries over the final state of that stage, e.g. positions, velocities and the cell. These links give the order of the stages; the order of the entries in the record does not. A condition that changes within one stage, e.g. a temperature ramp, is given in that stage's `conditions` as entries with a qualifier. The full protocol, with its control flow and complete inputs, belongs to the provenance record of a workflow manager (§1.2)."
2. **The input role "Initial configuration"** is defined as: "The configurations this computation starts from, with the state carried over from that computation, e.g. velocities." (was: "The configurations this computation starts from").

## Consequences
- One pull request applies items 1 and 2 (schema, a test, the regenerated page). No example changes: `md-quench` is a single stage with a ramp.
- Declined: a `protocol` object listing stages, and an explicit order field, since the `input` links already order the stages that matter to the data.
- Still PROPOSED, NOT DECIDED (0046): whether a series of runs differing only in an imposed condition (e.g. one MD run at each of several temperatures) is one computation or several. Those runs are parallel, not a chain, and this ruling does not settle it.
