# 0084 — No unit for string or bool parameters, singular repeatable names, and the matcore container first

Date: 2026-11-23. Status: accepted. Decided by: Ellad Tadmor.

## Context
A reviewer's written comments on the minimal metadata (committee review of 2026-09-23, by email) raise three points that the standard has not yet met.

1. **Units on generic parameters.** A generic parameter (0016) has a required `unit`. Its value may be a float, an int, a string or a bool, so a parameter whose value is a string (e.g. the optimizer "Adam") or a bool must carry the unit `dimensionless`. The reviewer calls this overkill. A unit says what a number is measured in, and a string or bool is not measured.
2. **Singular names.** The naming rule states that a name is plural only when its value is a list, and that a repeatable Property stays singular. Four repeatable Properties are plural:
   - pf `domain › boundary-conditions` and `domain › initial-conditions`;
   - pim `charge-interactions` and `magnetic-interactions`.

   `settings`, repeatable in every method section, reads as a mass noun for one block of settings.
3. **Position of `matcore`.** The required `matcore` container identifies the record: its standard version, id, dataset version, author and date. It is the second-to-last top-level Property of minimal, after the dataset's own metadata.

The reviewer also asks where a MatCore id comes from. That question is about the process by which ids are assigned, e.g. minted by a central service through a software tool. It is not decided here.

## Decision
1. **A generic parameter whose value is a string or a bool has no `unit`.** `unit` is required when the value's type is float or int, and absent when it is string or bool. This amends 0016's `unit*`. It applies to:
   - §1.3's definition of the generic parameter;
   - scripts/check_generic.py;
   - the JSON Schema, through a condition on the JSON member `type` (0044 item 3).

   In the schema, `unit` stays listed with its fixed form and becomes not required. Its note says when it is given.
2. **The four Properties take the singular:** `boundary-condition`, `initial-condition`, `charge-interaction`, `magnetic-interaction`. Their descriptions and the notes that name them change to match. `settings` keeps its name.
3. **`matcore` becomes the first top-level Property of minimal.** Its members and their order are unchanged.

## Consequences
- One pull request: schema/minimal.yaml, pf.yaml, pim.yaml and the generic parameters' `unit` in every section; docs/standard/index.md §1.3; scripts/check_generic.py and scripts/build_json_schema.py; examples/pf.json (boundary and initial conditions) and any example whose order follows minimal; tests; the regenerated pages and JSON Schema.
- Breaking changes:
  - item 1 breaks 0.7.0 records that give a unit to a string or bool parameter (no example does);
  - item 2 breaks records that use the four old names.
- Item 3 breaks none, since order has no meaning in JSON.
- PROPOSED, NOT DECIDED: how MatCore ids are assigned, e.g. by a central service that mints them through a software tool, or another way. `matcore › id` stays as it is until then.
