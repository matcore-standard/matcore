# 0059 — The cell a k-point mesh samples, and a mesh that varies

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding C8 of the minimal–dft analysis (2026-11-08): dft `k-point-mesh` counts points along "the three reciprocal lattice vector directions" without saying which cell's reciprocal lattice; it is that of minimal `conditions › cell`, periodic in the directions `cell-periodicity` gives. A computation is a group of calculations (0046), and its configurations may have different cells (e.g. the Si GAP dataset), each with a mesh chosen from a k-point spacing; one `number-of-points` cannot describe them. k-point-spacing was removed by 0004 item 47, which is not reopened. dft `comment` holds information the recorded settings do not cover (2026-11-09, finding C4 declined).

## Decision
1. **`k-point-mesh`** gains the note: "Note: The mesh samples the Brillouin zone of the simulation cell (minimal `conditions › cell`), periodic in the directions given by `cell-periodicity`. When the mesh differs between the configurations of a computation, e.g. one chosen from a k-point spacing, omit `number-of-points` and say in `comment` how the mesh was chosen."

## Consequences
- One pull request applies item 1 (schema, a test, regenerated page). Wording only.
