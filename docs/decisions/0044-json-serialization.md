# 0044 — JSON is the first serialization of MatCore instances

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
The standard is agnostic to serialization (§1.3), and its examples are written in XML, which the baseline used and the standard calls illustrative. Status step 7 opens with a decision record choosing the first serialization, which the MatCore tools (status step 9) then read and write (CLAUDE.md, Instance serialization). The decider asked whether XML is the best choice, given that it is dense to read, and whether JSON or YAML would serve better. The chosen serialization is used for the examples and by the tools that generate MatCore metadata.

Compared against MatCore's data model:
- **XML** has no types (every value is text) and no arrays: a value of extent `[3]` or `[3,3]` needs a convention of its own, and 0038's list of lists another. Validation would need a third schema language (XSD). Every name is written twice.
- **YAML** reads best and allows comments, but infers types from how values look. In MatCore data, `No` (nobelium) becomes `false` under YAML 1.1 (schema/minimal.yaml already quotes `'No'`), a version `6.10` becomes the number 6.1, and `2021-02-22` becomes a date. A value written without quotes can change type silently.
- **JSON** (RFC 8259) has native strings, numbers, booleans, objects and arrays, so properties, containers, repeatable properties and nested extents map directly. The standard already validates values with JSON Schema 2020-12 (0013), so the schema of status step 7 is generated in the same language. JSON is read natively in Python and in the browser (the Pyodide tools of 0000 and 0006). It has no comments; an example's explanation is already given beside it in the section's caption and notes.

## Decision
1. **JSON (RFC 8259) is the first serialization** of MatCore instances. The examples in examples/ are written in it, and the MatCore tools read and write it. The standard itself stays independent of serialization (§1.3); another serialization may be defined later by its own record.
2. **Mapping** from the data model to JSON:
   - An instance is a JSON object with one member per section it uses, named by the section key (`minimal`, `dft`, `md`, `mbpt`, `ml`, `pf`, `derived`), each an object holding that section's top-level properties. Sections are kept apart because a property name may recur in two sections (e.g. `computation` in minimal and in md).
   - A property is a member named by the property's name. A container is an object; a leaf is a JSON value of its Type: string → string, bool → `true`/`false`, float and int → number (an int property's value has no fraction or exponent).
   - A repeatable property is always an array of entries, even with one entry; a property that is not repeatable is never an array of entries.
   - A value whose Extent lists dimensions is nested arrays, first index outermost (0038): extent `[3]` is an array of 3, `[3,3]` an array of 3 arrays of 3, `[":"]` an array of any length.
   - An optional property that is not given is omitted; `null` is not written.
   - Members may appear in any order; writers should follow the order of the schema.
3. **Generic parameters.** A generic parameter's instance type (float, int, string or bool) is stated in the instance, not inferred from how the value is written (§1.3; 0016). JSON does not distinguish an int from a float, so in JSON a generic parameter's object carries one more member, `type`, holding `float`, `int`, `string` or `bool`. It belongs to the JSON serialization, not to the property tree.
4. **Encoding and naming.** A MatCore JSON file is encoded in UTF-8 (RFC 8259 §8.1) and named with the extension `.json`.
5. **Examples.** The seven example files are converted from XML to JSON by script, keeping their content. `scripts/check_examples.py` reads JSON, `scripts/check_formula.py` reads the material components from it, `scripts/build_docs.py` shows the examples as JSON, and the section files' `examples › file` names the `.json` files. The meta-schema's `file` pattern requires `.json`.
6. **§1.3**, where it names XML: "Examples are provided after each Standard specification in XML format." becomes "Examples are provided after each Standard specification in JSON, the first serialization adopted for MatCore instances." (JSON needs no expansion; 0004 item 51.) The rest of the paragraph, which states that the examples are for clarification only and that the standard is implementation-agnostic, is unchanged.

## Consequences
- One pull request applies items 4–6 (examples, scripts, meta-schema, Preamble, tests, regenerated pages).
- Status step 7 continues with the serialization-requirements section of the standard, which states item 2's rules for any serialization, and with a JSON Schema generated from the YAML against which CI validates the examples.
- md and the later sections write their examples in JSON from their pull requests on.
