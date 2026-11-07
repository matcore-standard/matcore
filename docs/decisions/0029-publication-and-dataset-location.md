# 0029 — Publications describing a dataset and where it is stored

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on minimal `citation`: "Are these citations of papers describing the dataset (e.g. Science, Nature, ...)? Or of the DOI of the dataset itself, i.e. where it's hosted? (e.g. Zenodo, Materials Cloud Archive, ...)"

`citation` ("Information that uniquely identifies a source being acknowledged") does not say which. No property says where the dataset itself is stored: The schema's own example for `related-content › link` is the Si GAP data's deposit (https://doi.org/10.17863/CAM.65004), although `related-content` is "Another dataset that is connected to the current one in some manner" and examples/minimal.xml describes the Si GAP data itself. The two belong in separate entries.

No MatCore instances exist yet, so renaming a property breaks none.

## Decision
1. **`citation` is renamed `publication`**, with the description "A publication that describes the dataset or the work that produced it, e.g. a journal article or preprint, to be cited when the dataset is used." It gains the note "Note: The location where the dataset itself is stored is given in `dataset-location`." Its subproperties (`reference`, `doi`, `link`) are unchanged.
2. **A new top-level property `dataset-location`**, after `publication`: optional, repeatable (a dataset may be mirrored), a container. Description: "A repository where the dataset itself is stored and can be obtained." Note: "Note: Omit when the metadata accompanies the dataset itself." Its subproperties, in order:
   - **`repository`**: optional; string, `[]`, inapplicable. Description: "The name of the repository." Examples: Zenodo, Materials Cloud Archive.
   - **`doi`**: optional; the dataset's DOI in Annex I's https URI form, with `publication › doi`'s pattern (0014, settled 2026-11-04). Description: "The digital object identifier (DOI) of the dataset in the repository."
   - **`link`**: required; string, `[]`, inapplicable, format uri. Description: "A URI pointing to the dataset in the repository."
3. **Examples.** The Cambridge deposit moves from `related-content › link`'s example to `dataset-location`'s: `doi` https://doi.org/10.17863/CAM.65004 and `link` https://www.repository.cam.ac.uk/handle/1810/317974, the repository's permanent URI. `related-content › link` keeps no example. examples/minimal.xml, which has no `citation` or `related-content`, gains a `dataset-location` for the Si GAP data: repository "Apollo - University of Cambridge Repository" (the repository's own name), with that doi and link.

## Consequences
- One pull request applies items 1–3 (schema, tests, regenerated page, example).
- `dataset-location` is optional: metadata that accompanies its dataset needs no location.
- `matcore-id` is unchanged; whether it has a URI form stays open (status step 6).
