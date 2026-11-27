# 0085 — A version only for a change to the standard

Date: 2026-11-27. Status: accepted. Decided by: Ellad Tadmor. Amends 0010.

## Context
0010 item 1 raises PATCH for "an editorial or non-breaking fix" without saying what has to change. Release 0.8.1 (2026-11-27, tag `v0.8.1`) was cut for changes to the website only: the collapsible rows of the Revision History, the supporters' logos in the bottom bar and a smaller menu logo. Neither the schema nor the text of the standard changed. A version number tells a reader that what a record conforms to has changed, and 0.8.1 did not change it.

## Decision
1. **A version is cut only for a change to the standard.** The standard is:
   - its schema files (`schema/<section>.yaml`, `schema/units.yaml`, `schema/identifier-schemes.yaml`, `schema/meta-schema.yaml`);
   - its normative text (the Preamble, the Annexes, the section introductions).

   Changes to the website's presentation, the tools, the tests and CI never warrant a version. They reach the site through `dev` and appear in a released version's pages only with the next release.
2. **0.8.1 is withdrawn.**
   - Its entry leaves `schema/releases.yaml`, so 0.8.0 is again the current version.
   - The tag `v0.8.1` is deleted.
   - The version 0.8.1 is removed from the site, and `latest` returns to 0.8.0.
3. 0010 item 1 reads, in place of "an editorial or non-breaking fix raises PATCH": "an editorial or non-breaking change to the standard (item 1 of 0085) raises PATCH".

## Consequences
- One commit on `main`:
  - `schema/releases.yaml` loses the 0.8.1 entry;
  - the version line on every standard page, the Revision History and the JSON Schema's title are regenerated for 0.8.0;
  - CLAUDE.md is updated.
- The human then:
  - deletes the tag locally and on GitHub;
  - removes 0.8.1 from `gh-pages` with `mike`, pointing `latest` at 0.8.0;
  - pushes `gh-pages`.
- The website changes merged in PRs #148 and #149 stay on `dev` until the next release.
