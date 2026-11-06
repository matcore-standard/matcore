# 0019 — The self-consistent field tolerance

Date: 2026-11-06. Status: accepted. Decided by: Ellad Tadmor.

## Context
dft `self-consistent-field-convergence` › `tolerance*` is "a real number containing the convergence tolerance" in eV in the baseline. Codes converge on the total energy, the charge density or the potential, and the unit depends on which. 0001 B6 (accepted) adds a required `criterion`; 0001 A3.1 gives the tolerance Kind `any` and a required `unit`. Until now only B6's stopgap was applied: the description says "(on total energy)".

Under 0015 a quantity with a unit is a container of `value` and `unit`. 0016 item 2 recognises a generic parameter by "a `value` of Kind `any`", so a tolerance written in that form would be checked, and rejected, as a generic parameter. 0016 also limits the `x-gnu:` escape to generic parameters and free-form units, while Annex U Rule 4, as amended 2026-10-31, permits it for any subproperty whose Kind the schema declares as `any`. CLAUDE.md lists "no recommended unit when kind is `any`" as proposed, not decided.

A check that the unit's Kind matches the criterion was weighed and rejected: for the charge density, the potential and any other criterion, codes measure different quantities (residual norms, squared residuals, changes in a density matrix), whose Kinds differ, so only the energy criterion could be checked.

## Decision
1. **`tolerance`** (required, not repeatable) is a container of, in this order:
   - `criterion` (required): a scalar string, open terms Energy, Charge density, Potential. The note: '"Energy" – The change in the total energy between successive iterations. "Charge density" – The change or residual of the electron density. "Potential" – The change or residual of the Kohn-Sham potential.'
   - `value` (required): float, extent `[]`, Kind `any`, recommended unit null, minimum 0, with 0015's fixed `value` description.
   - `unit` (required): the `unit` of a generic parameter (0016 item 1), with its fixed description and note.

   Its description returns to the baseline's: "Convergence criterion for the self-consistent loop."
2. **No check of the unit's Kind.** The schema does not relate `unit` to `criterion`.
3. **Generic parameters are recognised by Type and Kind** (amends 0016 item 2). A container is a generic parameter when one of its subproperties is a `value` whose Type and Kind are both `any`. A `value` of fixed Type and Kind `any`, as here, is not a generic parameter.
4. **`x-gnu:`** follows Annex U Rule 4 (amends 0016's last consequence): it is permitted in the `unit` of any `value` whose Kind the schema declares as `any`, and in free-form units.
5. **No recommended unit for Kind `any`.** A value of Kind `any` has recommended unit null.

## Consequences
- The pull request that fills `self-consistent-field-convergence` (with 0020) applies item 1, changes scripts/check_generic.py for item 3, and adds tests.
- CLAUDE.md: the `x-gnu:` sentence, the recognition of group 1 and the recommended-unit item are corrected.
