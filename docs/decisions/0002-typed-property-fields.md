# 0002 — Replace the prose "Values" field with typed fields

Date: 2026-09-28. Status: accepted (implementation pending).

## Decision
Each property has `type` (string|float|int|bool|file|any), `extent` (KIM notation; `any` for generic parameters), `kind` (Annex U kinds or dimensionless|inapplicable|any), `recommended-unit`, structured `values`, `required`, `repeatable`. "Kind" rather than "Quantity kind". Generic name/value/unit/description parameters: `value` is type any, extent any, kind any; instance supplies type/shape/unit. `repeatable` (property may occur more than once) is distinct from an open extent (shape of one value).

## Rationale
Machine-readable fields allow XSD/JSON Schema and the unit validator to be generated from the YAML. Follows OpenKIM Property Definitions and OPTIMADE property definitions.
