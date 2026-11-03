# 0015 — The `unit` subproperty of a typed quantity

Date: 2026-11-03. Status: accepted. Decided by: Ellad Tadmor.

## Context
0001 Part A gives every property whose value is a physical quantity a required `unit` subproperty holding an Annex U symbol whose Kind is compatible with the property's Kind (A1.1). Minimal `computation` › `simulation-conditions` is the first property to need it, with ten such entries (A2.2); about a hundred follow across the standard.

The keys of `values` (0013) cannot state "an Annex U symbol of Kind Temperature". Listing the symbols of each Kind in every `unit` as an `enum` would copy units.yaml into every dimensioned property, and the copies would drift from it whenever a unit is added.

Separately, §1.3 of the Preamble still carries the draft's bullet "When a value has physical units, either the required unit must be specified, or a field provided to define the value units." 0001 A1.1 and A1.2 replace it, but they were not applied: status step 3 handed Part A to the property pull requests of step 5, and §1.3 belongs to no property.

## Decision
1. **Physical Kind.** A Kind is physical when it is a key of units.yaml `kinds` other than `dimensionless`. The reserved Kinds `dimensionless`, `inapplicable` and `any` are not physical.
2. **Fixed form.** A property with a physical Kind has exactly one subproperty named `unit`, and it has this form, identical everywhere:
   ```yaml
   - name: unit
     required: true
     description: The unit of the value, an Annex U symbol whose Kind is the Kind of the property.
     type: string
     extent: []
     kind: inapplicable
     recommended-unit: null
     values: null
     repeatable: false
   ```
   The parent's `kind` carries the information; the symbol's Kind is looked up in units.yaml. The `x-gnu:` escape (Annex U Rule 4) is not permitted here (0001 A1.1).
3. **Check.** validate_schema.py fails when a property with a physical Kind lacks this `unit`, when its `unit` departs from the fixed form, or when a property whose Kind is `dimensionless` or `inapplicable` has a `unit` subproperty. A `unit` under a container (the generic parameters and free-form units of 0001 and 0003) is outside this check; those are settled in their property pull requests.
4. **Instances.** The instance validator (status step 9) checks that the symbol is in Annex U and that its Kind matches the property's Kind.
5. **§1.3.** 0001 A1.1 and A1.2 are applied to §1.3 now, worded with "Kind" (0004 item 14).

## Consequences
- One pull request adds the check of item 3, its tests, and the §1.3 text of item 5. Since only `concentration` (dimensionless) has a Kind today, no existing property changes.
- From then on, each property pull request of status step 5 that fills a physical Kind adds the fixed `unit`; CI fails otherwise.
- The pf properties `grid-spacing` and `time-step-size` (0003, typed, handled like temperature) are currently containers with `value` and `unit` siblings; the pf pull requests decide whether they take this form.
