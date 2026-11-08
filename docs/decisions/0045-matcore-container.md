# 0045 — The MatCore record information, the standard version and the dataset version

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee feedback on minimal:
- The record does not say which version of the MatCore standard it follows, so a reader cannot tell which schema applies. It should, as a required field, with a pointer to where that version's schema is kept.
- The MatCore-specific properties (`matcore-id`, `matcore-author`, `matcore-date`) should be gathered in one required container.
- How does `provenance` relate to the record's identifier? Some provenance events should change it, assuming it carries the version of the dataset, which it should.

`provenance › event-type` already distinguishes the events: "Initial creation"; "Admin update", an editorial update "not requiring a version update"; "Version update", a change "requiring a new version"; "Metadata update", a change to the metadata only. The example's `matcore-id`, `mc-ad83jsd3-1`, ends in what reads as a version number.

Only mkdocs.yml holds the repository's address (0004), and the organization may move; a schema note does not hard-code it. A DOI per release keeps resolving if the repository moves; releases get one when a GitHub release triggers Zenodo (0010), which has not been done yet.

## Decision
1. **A new required top-level property `matcore`**, not repeatable, a container. Description: "Information about this MatCore metadata record: the standard it follows, the dataset version it describes, and who created it and when." It takes the place of `matcore-id`, `matcore-author` and `matcore-date`, at their position (after `provenance`). Its members, in order:
   - **`standard-version`**: required; string. Description: "The version of the MatCore standard this record follows." Pattern: three non-negative integers separated by dots (MAJOR.MINOR.PATCH, 0010). Example: 0.6.0.
   - **`standard-link`**: optional; string, format uri. Description: "A URI for the schema of that version of the standard." Note: "Note: Give the DOI of the release where it has one; otherwise the address of the release's tag in the MatCore repository."
   - **`id`**: required; string. Description: "An identifier of the dataset, the same for all its versions." Example: mc-ad83jsd3. (Was `matcore-id`. Not `identifier`, which elsewhere names a container of a value and a scheme.)
   - **`dataset-version`**: required; int, `[]`, dimensionless, minimum 1. Description: "The version of the dataset this record describes." Note: "Note: The first version is 1. Each provenance event of type Version update starts a new version: the dataset's new version is described by a new record with the same id, its dataset-version raised by 1. Admin update and Metadata update events keep the version. When provenance is given, dataset-version is 1 more than the number of Version update events."
   - **`record-author`**: required, repeatable; creator's structure (0014), as `matcore-author` had (0033). Description: "An entity (e.g. person, organization, software agent) responsible for creating this metadata record, and their institutional affiliation if relevant." Its members keep `matcore-author`'s descriptions.
   - **`creation-date`**: required; `matcore-date`'s type and values (the pattern and note of the top-level `creation-date`). Description: "The date, or date and time, when this metadata record was created."
2. **`matcore-id`, `matcore-author` and `matcore-date` are removed** as top-level properties.
3. **examples/minimal.json** gives `matcore` with `standard-version` "0.6.0", `standard-link` https://github.com/matcore-standard/matcore/tree/v0.6.0/schema (no DOI exists yet), `id` "mc-ad83jsd3", `dataset-version` 1, the present `matcore-author` as `record-author`, and the present `matcore-date` as `creation-date`.

## Consequences
- One pull request applies items 1–3 (schema, tests, regenerated page, example). It breaks 0.6.0 instances: the three properties move and two required members are new.
- The step 9 instance validator checks item 1's rule between `dataset-version` and `provenance`, and that `standard-version` names a released version.
- The form of `id`, and who issues it, remain PROPOSED, NOT DECIDED (status step 6).
- PROPOSED, NOT DECIDED: GitHub releases with Zenodo, so that each release gets a DOI (0010), and the procedure step that adds; a `.zenodo.json` or `CITATION.cff` giving the record's authors, title and license.
