# 0054 — The dft introduction

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding C1 of the minimal–dft analysis (2026-11-08): the dft introduction names the "core-electron model, and valence-electron model", renamed `core-electron-treatment` and `wavefunction-representation` by 0018. Since 0046 the dft properties sit in `settings` blocks that name the DFT computations they describe, and the introduction does not say so.

## Decision
1. **schema/dft.yaml `introduction`** becomes: "The metadata for density functional theory (DFT) data (MatCore-DFT) is tabulated below. This includes the level of theory (exchange-correlation functional, core-electron treatment and wavefunction representation) and associated parameters. The properties are given in settings blocks, each naming the DFT computations it describes. (Note: This standard inherits the metadata in the minimal MatCore standard, adding the properties below.)"

## Consequences
- One pull request applies item 1 (schema, a test, regenerated page). Wording only.
- The pim and md introductions gain the sentence on settings blocks in their own pull requests.
