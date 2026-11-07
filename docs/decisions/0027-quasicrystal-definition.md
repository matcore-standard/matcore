# 0027 — Definition of a quasicrystal

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on the `phase` term Quasicrystal: "I don't agree with the definition of "Quasicrystal" in the phase key. To me, the quintessential example of a quasicrystal is an aperiodic tiling, and Wikipedia seems to agree: https://en.wikipedia.org/wiki/Quasicrystal. Therefore, a quasicrystal DOES have long-range order, it just doesn't have translational periodicity."

The note of minimal `structure › material-component › phase` defines the term, in the baseline's wording, as "A crystal-like material with short-range order, but without long-range order." That is the definition of an amorphous solid, and the reverse of the accepted one. The cited article opens: "A quasiperiodic crystal, or quasicrystal, is a structure that is ordered but not periodic." Its diffraction pattern has sharp Bragg peaks, often with a rotational symmetry (e.g. five-fold) that no periodic crystal can have. The same article reports that the International Union of Crystallography redefined "crystal" to include quasicrystals, so "crystal-like" is also out of date (the IUCr's own dictionary could not be read for this record).

## Decision
1. **The definition of "Quasicrystal"** in the `phase` note becomes: "A solid material with long-range order but without translational periodicity, e.g. one whose diffraction pattern shows five-fold rotational symmetry." (was "A crystal-like material with short-range order, but without long-range order.")
2. **Single crystal and Polycrystal** are unchanged: "a repeating pattern of atoms" already means a periodic crystal, so a quasicrystalline grain is a Quasicrystal.

## Consequences
- One pull request applies item 1 (schema, test, regenerated page). No instance is affected.
