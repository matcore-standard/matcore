# 0016 — Generic parameters

Date: 2026-11-04. Status: accepted. Decided by: Ellad Tadmor.

Amended 2026-11-06 by 0019: item 2 recognises a generic parameter by a `value` whose Type and Kind are both `any`; the `x-gnu:` escape follows Annex U Rule 4.

## Context
Five properties of the standard hold a parameter whose meaning the schema does not fix: dft `xc-functional` › `xc-parameter`, md `computation-parameter` and `td-parameter`, pf `model-parameter`, and derived `calculation-parameter`. Each has the same four subproperties in the baseline: `name*`, `value*`, `unit*` and `description`. 0001 A3.2 (and A7.4 for pf) gives the `value` Kind `any` and the `unit` its allowed forms; 0004 item 16 states that the instance gives the value's type (float, int, string or bool) and that the value need not be a scalar. CLAUDE.md proposed defining the pattern once and checking every such entry against one canonical definition, but left it undecided. dft `xc-parameter` is the first of the five to be filled (status step 5).

0001 B9, also undecided, proposed replacing the baseline's definition of every generic `unit`, "A standardized string or identifier that defines the dimension or measurement system of the associated value.", with "The unit in which the associated value is expressed."

## Decision
1. **Generic parameter.** A *generic parameter* is a container with exactly these subproperties, in this order:
   - `name` (required): a scalar string, Kind `inapplicable`, values null.
   - `value` (required): type, extent and Kind `any`, recommended unit null, values null. The instance states the type and gives the unit (0004 item 16).
   - `unit` (required): a scalar string, Kind `inapplicable`, recommended unit null, with the fixed description "The unit in which the associated value is expressed." (0001 B9) and the fixed values note "A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning)." (0001 A3.2).
   - `description` (optional): a scalar string, Kind `inapplicable`, values null.

   None of the four is repeatable; the generic parameter itself may be. The descriptions of `name`, `value` and `description` stay specific to each parameter (e.g. "The designation of the exchange-correlation parameter.").
2. **Recognised by structure.** A container is a generic parameter when one of its subproperties is a `value` of Kind `any`. No tag is added to the meta-schema.
3. **Check.** validate_schema.py fails when a generic parameter departs from item 1: a missing, extra or reordered subproperty, or a different type, extent, Kind, recommended unit, required flag, repeatable flag, or (for `unit`) description or values.
4. **§1.3.** The Preamble defines the term "generic parameter" once, in the words of item 1; the five properties follow it.

## Consequences
- The pull request that fills dft `xc-functional` adds the check and its tests and the §1.3 text, and fills `xc-parameter`. The other four take the form in their own property pull requests; CI fails otherwise.
- 0001 B9 is decided by item 1 for the five generic `unit` rows. Other `unit` definitions are governed by 0015.
- The `x-gnu:` escape stays limited to the groups of 0001 A1.1 (generic parameters and free-form units).
