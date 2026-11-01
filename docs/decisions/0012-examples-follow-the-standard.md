# 0012 — Examples always conform to the current standard

Date: 2026-11-01. Status: accepted. Decided by: Ellad Tadmor.

## Context
The section examples (examples/*.xml, 0004 items 23 and 33) are what readers copy. A check of all seven against version 0.4.0 found two that did not conform, because of contradictions in the standard (0011). Nothing kept examples and standard in step.

## Decision
1. **Rule.** Every change to the standard (schema/*.yaml, including renames, required and repeatable flags, subproperties, and later the typed fields) includes reviewing every example and updating any that no longer conform, in the same change. A change that leaves an example non-conformant is incomplete.
2. **Automatic check.** `scripts/check_examples.py`, run by `scripts/validate_schema.py` and so by CI, fails when an example uses an element the standard does not define at that place, omits a required property, repeats a non-repeatable one, or nests elements under a property without subproperties.
3. The check covers structure only. Values, types and units are checked once the typed fields are filled (status step 5) and the format-specific schema of status step 7 exists. Rules the schema cannot yet express, such as "exactly one of" (0011 item 3), are reviewed by hand.

## Consequences
CLAUDE.md (working rules) and CONTRIBUTING.md state the rule; tests/test_examples.py tests the check and runs it over every example.
