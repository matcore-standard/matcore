# 0068 — Electrostatic summation, short-range included

Date: 2026-11-14. Status: accepted. Decided by: Ellad Tadmor.

## Context
A reviewer found that pim `charge-interactions › long-range-electrostatics` has no term for approaches that compute electrostatic interactions only within a cutoff. Examples are a truncated or shifted Coulomb sum, Wolf summation and damped shifted force (DSF). Its terms are None, Direct, Ewald, PME, PPPM and Reaction. "None" is defined as "No electrostatic calculation performed", which does not say what it means for a model that has charges.

With a short-range term among its values, the name `long-range-electrostatics` no longer fits. The name `electrostatic-interactions` was considered and declined. It would parallel the container `charge-interactions`, which corresponds to `magnetic-interactions`, and not this leaf inside it. What the leaf records is how the electrostatic sum is evaluated.

The reviewer also noted that the long-range sum is computed by the simulation code, e.g. LAMMPS, and not by the interaction model. 0046 item 8 (amended 2026-11-09) already settles this. pim describes the interaction as evaluated, including the code's long-range summation, and the code is listed in the PIM computation's `software`.

## Decision
1. **`long-range-electrostatics` is renamed `electrostatic-summation`.** Its description becomes "Method used to compute the electrostatic interactions between the charges."
2. **A term "Short-range" is added**, after Direct: "Electrostatic interactions computed only within a cutoff distance, possibly shifted or damped, e.g. Wolf summation or damped shifted force (DSF)." The terms stay open.
3. **"None" is redefined**: "No electrostatic interactions are computed from the charges." A model whose particles carry no charges, e.g. a local ML potential, omits `charge-interactions`.

## Consequences
- No released instance breaks: pim was created after 0.6.0, and 0.6.0 md instances already break under 0061.
- Applied in one pull request: schema/pim.yaml, tests/test_computations.py and the regenerated pim page. examples/pim.json does not use the property.
