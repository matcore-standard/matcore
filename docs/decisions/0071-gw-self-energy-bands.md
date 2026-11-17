# 0071 — The self-energy's bands: corrected range, sum and terminator

Date: 2026-11-17. Status: accepted. Decided by: Ellad Tadmor.

## Context
mbpt `gw-bands` is one integer, "how many bands are corrected, counting from the bottom of the valence bands". Review on 2026-11-17 raised two points:
- Codes give the corrected bands as a range, e.g. bands 35 to 70.
- A GW calculation also sets the number of bands summed over in the polarizability, which builds *W*, and in the self-energy (*G*), and the two usually differ, e.g. 500 and 600.

`dielectric-matrix › response-basis-size` already holds the polarizability's count. Nothing holds the self-energy's.

The same review asked for "Bruneval-Gonze" as a coulomb-truncation term. It is not a truncation. It is the extrapolar approximation of F. Bruneval and X. Gonze, Phys. Rev. B 78, 085125 (2008), which stands in for the bands left out of a sum over states. Yambo offers it for each sum separately: `XTermKind` for the polarizability and `GTermKind` for the self-energy. Its home was left to this ruling.

In diagonal GW the corrected bands *n* and the summed bands *m* are separate indices: Σ<sub>n</sub> sums over bands *m* = 1 … N. The corrected range is the output; the summed count is a convergence parameter.

## Decision
1. **`gw-bands` is replaced by an optional container `self-energy`** in `settings`, with a note "Give it when `type` is GW or GW/BSE." It holds:
   - `band-range`: int [2], dimensionless, minimum 1. The first and last band whose quasiparticle energies are computed, counted from 1 at the lowest band in the calculation.
   - `number-bands`: int, dimensionless, minimum 1. The number of bands in the self-energy's sum over states, counted the same way. The last band of `band-range` does not exceed it.
   - `band-terminator`: a string with open terms None and Bruneval-Gonze. It names the approximation used for the bands left out of the sum.
2. **`dielectric-matrix` gains the same `band-terminator`** after `response-basis-size`, for the polarizability's sum.
3. **The two sums stay counts, not ranges.** Codes write them as ranges (Yambo `BndsRnXp`, `GbndRnge`), but in practice the ranges start at band 1.
4. **"Bruneval-Gonze" is not a coulomb-truncation term.**

## Consequences
- Applied in the gw-bands pull request (status step 5): schema/mbpt.yaml, tests and the regenerated mbpt page.
- examples/mbpt.json gains the source dataset's values from Yambo input `ppa_48kp.in` (Materials Cloud 2023.92):
  - `self-energy › number-bands` 200 (`GbndRnge 1 | 200`) and `band-terminator` Bruneval-Gonze (`GTermKind "BG"`);
  - `band-range` from `QPkrange` (bands 3 to 4).
- No released instance breaks: mbpt's properties were legacy text in 0.6.0.
- PROPOSED, NOT DECIDED: whether the step 9 validator checks that the last band of `band-range` does not exceed `number-bands`.

## Amendment (2026-11-17, review of the pull request)
- `number-bands` is renamed `number-of-bands`.
- Its description says the sum runs over bands 1 to `number-of-bands`. The phrase "counted from 1 at the lowest band in the calculation" is dropped, because it read as the first band of `band-range`. Band numbering is stated once, in `band-range`.
- The note on `band-terminator` names the extrapolar approximation without citing the paper, as no other term in the schema cites one.
