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

## Amended 2026-11-04 (Ellad Tadmor)
Under items 2 and 3, a quantity with a physical Kind had both a value of its own and a `unit` subproperty. The standard's pages render every property with subproperties as a container (0007 item 12), so the Type, Extent, Kind and Recommended unit of such a quantity were not shown. Serializations also handle such a node poorly: a JSON key holds either a number or an object, and XML needs mixed content or an attribute. The amendment replaces items 2 and 3.

1. **Leaf or container.** A property either has a value of its own or has subproperties, never both.
   - A leaf has no subproperties; its type, extent, kind and recommended unit are filled. An instance writes it as its value, e.g. `<title>…</title>`, `<number-of-particles>64</number-of-particles>`.
   - A container has subproperties; its type, extent, kind, recommended unit and values are null (0004 item 37). An instance writes it as its children, e.g. `<creator>`, `<volume>`.
2. **Quantities with a unit.** A quantity with a physical Kind is a container holding two leaves, `value` and `unit`. The container keeps the property's name, required flag, description, repeatable flag and notes. `value` carries the type, extent, kind, recommended unit and values (its note states the symbol, the order of components and the basis). Both leaves have a fixed form, identical everywhere:
   ```yaml
   - name: value
     required: true
     description: The value of the property, in the unit given by `unit`.
     type: float            # and extent, kind, recommended-unit, values: per property
     ...
     repeatable: false
   - name: unit
     required: true
     description: The unit of the value, an Annex U symbol whose Kind is the Kind of `value`.
     type: string
     extent: []
     kind: inapplicable
     recommended-unit: null
     values: null
     repeatable: false
   ```
   An instance: `<volume><value>1280.9</value><unit>angstrom^3</unit></volume>`. A leaf whose Kind is `dimensionless` or `inapplicable` is not wrapped and has no `unit`.
3. **Check.** validate_schema.py fails when a property has subproperties and a non-null type, extent, kind, recommended unit or values; when a leaf with a physical Kind is not named `value` or has no sibling `unit`; when such a `value` or its `unit` departs from the fixed form (required, repeatable and description for `value`; all of item 2 for `unit`); or when a `unit` sits beside a `value` whose Kind is `dimensionless` or `inapplicable`. The generic parameters (whose `value` has Kind `any`) and the free-form units (a `unit` with no `value`) of 0001 and 0003 remain outside this check, as before.

Items 1, 4 and 5 stand; item 4 applies to `value`'s Kind. The minimal computation pull request applies the amendment: check_units.py and its tests, the ten simulation-conditions quantities restructured, and §1.3's units bullet worded for `value` and `unit`.

## Second amendment 2026-11-04 (Ellad Tadmor)
Every numerical value takes one format. The first amendment left a dimensionless value as a bare leaf, so a reader had to know a property's Kind to find its number. The second amendment replaces the first amendment's rule for pure numbers.

1. **Leaves are non-quantities.** A leaf has Kind `inapplicable` (strings, booleans, identifiers). A value whose Kind is physical or `dimensionless` is a container holding `value` and `unit` in the fixed forms of the first amendment's item 2. An instance: `<concentration><value>0.5</value><unit>dimensionless</unit></concentration>`.
2. **The unit of a dimensionless value.** The `unit` form is unchanged. Its rule, an Annex U symbol whose Kind is the Kind of `value`, admits only `dimensionless`, the one symbol of that Kind; the instance validator (0015's original item 4) checks it. `value`'s recommended unit is `dimensionless` (0004 item 46).
3. **Check.** validate_schema.py fails when a leaf whose Kind is physical or `dimensionless` is not a `value` in the fixed form beside exactly one `unit` in the fixed form. The check of a `unit` beside a dimensionless `value` is dropped. Containers, generic parameters (`value` of Kind `any`) and free-form units are checked as in the first amendment.
4. **The unit of a dimensionless value states its one symbol** (settled 2026-11-04). Beside a `value` of Kind `dimensionless`, the `unit` has the fixed form of the first amendment except for `values`, which holds only a `note` reading "The only allowed unit is `dimensionless`.", so a reader sees the rule of item 2 on the property itself. Beside a `value` of any other numerical Kind, `values` stays null. The check of item 3 applies the form that matches the Kind of `value`. A second pull request applies this item: check_units.py and its tests, and the `unit` of minimal `concentration`, `number-of-particles` and `strain`.

One pull request applies it: check_units.py and its tests; minimal `concentration` (a fraction, 0004 item 46), `number-of-particles` and `strain` as containers; examples/minimal.xml; and §1.3's units bullet.

## Third amendment 2026-11-04 (Ellad Tadmor)
The second amendment is reversed. A dimensionless value has no unit to state, so wrapping it in `value` and `unit` made every count and ratio three lines long in an instance for no information; a dimensionless number is written as itself, e.g. `<number-of-points>6 6 6</number-of-points>`.

1. **Leaves.** A leaf has Kind `inapplicable` or `dimensionless`; a dimensionless leaf carries no `unit` and its recommended unit is null (0004 item 48).
2. **Quantities with a unit.** A value whose Kind is physical (a units.yaml kind other than `dimensionless`) is a container of `value` and `unit` in the fixed forms of the first amendment's item 2, unchanged.
3. **Check.** As in the first amendment's item 3: validate_schema.py fails when a container has typed fields, when a leaf with a physical Kind is not a fixed `value` beside exactly one fixed `unit`, or when a `unit` sits beside a `value` whose Kind is `dimensionless` or `inapplicable`. The second amendment's item 4 (the note on a dimensionless value's `unit`) lapses with it. Generic parameters (0016) and free-form units are unaffected; a generic parameter's `unit` may still be `dimensionless`.

One pull request applies it: check_units.py and its tests; minimal `concentration`, `number-of-particles` and `strain` and dft `number-of-valence-electrons`, `number-of-points` and `shift` back to leaves; examples/minimal.xml and examples/dft.xml; and §1.3's units bullet.
