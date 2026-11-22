# 0078 — A JSON Schema generated from the standard

Date: 2026-11-22. Status: accepted. Decided by: Ellad Tadmor.

## Context
JSON is the first serialization of MatCore records (0044), and step 7 of the work plan calls for a schema generated from the YAML for that serialization, against which the examples are checked in CI. Today a hand-written script, scripts/check_examples.py, walks each example against the YAML. Nothing outside the repository can use that script. An author of a real dataset's record, or a tool that writes records, has no way to check a record against the standard.

[JSON Schema](https://json-schema.org/) is the standard language for describing what a valid JSON document looks like, and validators for it exist in every common language. Every property now has its typed fields filled (status step 5), so the YAML holds everything a schema needs.

## Decision
1. **Generated, committed, published.** A script, scripts/build_json_schema.py, generates one JSON Schema (draft 2020-12) from schema/*.yaml and schema/units.yaml. It is written to docs/standard/matcore.schema.json, a generated file like the section pages:
   - it is never edited by hand;
   - CI fails if the committed copy is stale;
   - the site publishes it with each version, so every release carries the schema of that release;
   - §1.3 links to it.
2. **A whole record.** The schema describes one MatCore record: an object with one member per section, `minimal` required, the method sections optional, and nothing else. Each section's definition sits in `$defs` and can be checked on its own. The single-section examples are checked that way.
3. **What it checks**, following 0044's mapping:
   - every property name, and nothing else at each level;
   - required properties;
   - a repeatable property as an array;
   - a container as an object;
   - a leaf's Type, and the nesting its Extent gives;
   - the bounds, patterns and formats in `values`.
4. **Units by Kind** (0015). The `unit` beside a typed `value` accepts only the Annex U symbols of that value's Kind. It also accepts `dimensionless` where a reduced length or time is allowed (0075).

   A unit the schema does not fix accepts any Annex U symbol, `dimensionless`, or an `x-gnu:` expression (Annex U Rule 4). Such units are:
   - the unit of a generic parameter;
   - a free-form unit;
   - a unit beside a value of Kind any.
5. **Generic parameters** (0044 item 3). The object requires the JSON member `type` (float, int, string or bool), and the value, or each component of it, must have that type.
6. **Not expressed in the schema**, and left to checks of their own or to the instance validator of step 9:
   - open vocabularies (an unlisted term conforms by 0013; near-misses are reported as warnings);
   - whether an `x-gnu:` expression is valid;
   - references by name or label (an input naming a computation in the record, an evolved variable naming a field variable);
   - the grammar of a chemical formula (scripts/check_formula.py);
   - identifier check digits (scripts/check_identifiers.py).
7. **One checker.** scripts/validate_schema.py checks every example against the generated schema. scripts/check_examples.py and its structural tests are removed. The structural cases they covered are tested against the generated schema instead.

## Consequences
- One pull request:
  - the generator;
  - the generated file;
  - the switch in validate_schema.py;
  - the removal of check_examples.py;
  - tests of the generator and of the generated schema, carrying over the structural cases;
  - the link in §1.3;
  - the README's description of the generated files.
- The step 9 validator starts from this schema and adds item 6's checks.
- No change to the standard's properties, so no released record is affected.
- The other part of step 7, the requirements that any serialization must meet, written into the standard, is a separate change.
