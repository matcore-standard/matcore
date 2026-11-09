# 0049 — The net charge of the simulated system; the Kind ElectricCharge

Date: 2026-11-09. Status: accepted. Decided by: Ellad Tadmor.

## Context
Finding B1 of the minimal–dft analysis (2026-11-08): a calculation of a charged defect or an ion fixes the number of electrons relative to the neutral system (e.g. Quantum ESPRESSO `tot_charge`, VASP `NELECT`), and MatCore has no place for it. The charge is not specific to DFT: coupled cluster, quantum Monte Carlo and MBPT calculations of charged systems need it, and a classical simulation may hold an electrode at constant charge, the counterpart of the constant-potential condition `electrode-potential` (0041). It is imposed by the simulation as `number-of-particles` is, so it is a condition (0039).

Annex U has no Kind for electric charge. A charge counted in elementary charges is not dimensionless, as angles and moles are not (Annex U).

## Decision
1. **A new Kind, ElectricCharge**, in schema/units.yaml, with the units `e` (the elementary charge) and `C` (the coulomb). Following 0040, each unit is added by its own pull request with every field (Kind, QUDT identifier, GNU Units name, SI factor, source) traced to a primary source named in the pull request; the first adds the Kind.
2. **minimal `conditions` gains `net-charge`** after `number-of-particles`: optional, repeatable, a container of `value*` (float, `[]`, Kind ElectricCharge, recommended unit `e`), `unit*` (the fixed form, 0015) and `qualifier` (0035), as the other conditions with a physical Kind are. Description: "The net electric charge of the simulated system, as imposed by the simulation, e.g. by fixing the number of electrons of a charged defect or an ion, or the charge of an electrode." The value is a float, since a fractional charge may be imposed (e.g. 0.1 e of doping).

## Consequences
- Pull requests: the unit `e` with the Kind ElectricCharge; the unit `C`; then the condition, with tests and the regenerated page. The condition is optional; no example changes.
