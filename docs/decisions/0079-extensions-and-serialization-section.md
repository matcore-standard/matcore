# 0079 — Properties added by a record, and a section on serialization

Date: 2026-11-22. Status: accepted. Decided by: Ellad Tadmor.

## Context
§1.3, in the baseline's wording, allows a record to grow: "In addition to the required and optional Properties, other arbitrary Properties can be added to any MatCore Standard metadata files to support developments in the field." The JSON Schema of 0078 rejects any member the standard does not define (item 3, "nothing else"), so a record that uses this freedom fails the published schema. Accepting any unknown name would bring the opposite fault: a misspelled property, e.g. `temprature`, would pass unnoticed.

Status step 7 also calls for the requirements that any serialization must meet to be written into the standard. JSON's mapping (0044 item 2) is in that decision record only, and decision records are not published (0004). §1.3 defines a serialization in one sentence and, since 0078, links the JSON Schema.

## Decision
1. **Added Properties carry the prefix `x-`.**
   - A record may add Properties of its own, at any level, named with the prefix `x-` followed by words in the form of a Property name, e.g. `x-beamline` or `x-run-notes`.
   - The standard's own Property names never begin with `x-`; the meta-schema enforces this.
   - The JSON Schema accepts any member whose name begins with `x-`, with any value, and still rejects every other name it does not define.
   - §1.3's sentence is reworded to say so; its second sentence, that such Properties may be standardized later, stays.
   - This amends 0078 item 3.
2. **A new §1.4 Serialization** in the Preamble, after §1.3 Format, holds:
   - the definition of a serialization, moved from §1.3;
   - the requirements that any serialization must meet: what a record written in it must preserve, so that it can be read back into the data model without loss;
   - the JSON serialization, as 0044 decided it: RFC 8259, UTF-8, the extension `.json`, and item 2's mapping, with the `type` member of a generic parameter (item 3) and the prefix of item 1;
   - the link to the JSON Schema, moved from §1.3.

   The menu lists it with §1.1–§1.3, from the page's headings (0008).

## Consequences
- One pull request:
  - the meta-schema's name pattern refuses the prefix;
  - the generator accepts `x-` members at every level, and tests check it;
  - the §1.3 sentence;
  - §1.4;
  - the README if it names §1.3's contents.
- Status step 7's requirements part is done with it.
- No released record breaks: a record with unprefixed added Properties was never checkable before 0078, and 0078 is not yet in a release.
