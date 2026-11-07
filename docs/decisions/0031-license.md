# 0031 — License identifiers, custom licenses and several licenses

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on minimal `license`:
- An example, `GPL-3.0-only`, is a license written for code, not data.
- It is unclear how a license not on the SPDX License List is given ("A license not on the list is written `LicenseRef-` followed by an identifier."), what exactly is written from SPDX (full name, short identifier, or both), and how a custom license and its exact terms are given.
- A dataset may have more than one license.
- No SPDX license fits NIST data; the SPDX entries link to repositories and web pages rather than to NIST's canonical statements for [NIST data](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications#data) and [NIST software](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications#software).

The SPDX License List (data of 2026-10-28) holds licenses written for data that link to their canonical texts: CC-BY-4.0, CC0-1.0, ODbL-1.0, ODC-By-1.0, PDDL-1.0 and CDLA-Permissive-2.0. For NIST, `NIST-PD` and `NIST-PD-fallback` link to software repositories on GitHub, `NIST-Software` links to NIST's statement page, and no entry covers NIST's statement for data not covered by the Standard Reference Data Act, or the copyright of Standard Reference Data. SPDX 2.3.1 Annex D defines a user-defined license reference as `LicenseRef-` followed by `idstring = 1*(ALPHA / DIGIT / "-" / ".")`; in an SPDX document its text is given in a section that a MatCore instance does not have.

## Decision
1. **`license`** becomes a required, repeatable container. Description: "A contract defining the terms and conditions under which the dataset can be used." Several entries all apply, each to its part of the dataset; a choice between licenses is one entry with an `OR` expression. Its subproperties, in order:
   - **`identifier`**: required; string, `[]`, inapplicable. Description: "The license as an SPDX license expression built from short identifiers of the SPDX License List, or as `LicenseRef-` followed by an identifier for a license not on the list." Examples: CC-BY-4.0, CC0-1.0, LicenseRef-NIST-data.
   - **`name`**: optional; string. Description: "The full name of the license." Example: "Creative Commons Attribution 4.0 International".
   - **`link`**: optional; string, format uri. Description: "A URI pointing to the full text of the license."
   - **`applies-to`**: optional; string. Description: "The part of the dataset the license covers, when the dataset has more than one license, e.g. the data or the code."
2. **The note on `license`** becomes:

   > Note: A license expression as defined in the [SPDX specification, version 2.3.1](https://spdx.github.io/spdx-spec/v2.3.1/SPDX-license-expressions/), built from current identifiers of the [SPDX License List](https://spdx.org/licenses/): a single identifier (e.g. `CC-BY-4.0`) or a combination (e.g. `CC-BY-4.0 OR CC0-1.0`). Give the SPDX short identifier, not the license's full name, so that the value can be read by tools. A license not on the SPDX License List, including a custom license, is written `LicenseRef-` followed by letters, digits, `-` or `.` (e.g. `LicenseRef-NIST-data`), with its `name` and a `link` to its full text, both required in this case. A license for data is usually one written for data, e.g. `CC-BY-4.0`, `CC0-1.0` or `ODbL-1.0`, rather than one written for software.
3. **examples/minimal.xml** keeps the Si GAP data's license, which its repository page gives as the GNU General Public License v3.0, and writes it as an entry: identifier `GPL-3.0-only`, name "GNU General Public License v3.0 only" (the SPDX List's name), link https://www.gnu.org/licenses/gpl-3.0.en.html (the repository's link).

A NIST data license is written, for example, identifier `LicenseRef-NIST-data` with a name and a link to NIST's data statement. No NIST entry is built into the schema: a LicenseRef with a link covers it, as it covers any custom license.

## Consequences
- One pull request applies items 1–3 (schema, tests, regenerated page, example). No MatCore instances exist yet, so the restructuring breaks none.
- "name and link required for a LicenseRef" and "`applies-to` when there is more than one license" are prose; the validator does not check them.
