# 0010 — Versioning and releases of the standard

Date: 2026-11-01. Status: accepted. Decided by: Ellad Tadmor.

## Context
The last release on matcore.org is 0.3.0 (06-Apr-2026). The baseline .docx carries no version. The repository labelled every section file `matcore_version: 0.9-draft-baseline` and tagged the baseline commit `v0.9-baseline`; no record backs that number, it skips 0.4–0.8, and it is not a semantic version. The site deployed one version, `dev`, with the alias `latest` pointing at it, so "latest" meant whatever was on `main`. Readers had no way to tell which version a page or a cited property belonged to.

## Decision
1. **Semantic versioning**, MAJOR.MINOR.PATCH. Below 1.0, a breaking change or a set of new properties raises MINOR ("Minor (Breaking)" in the history), and an editorial or non-breaking fix raises PATCH. 1.0.0 is the first version the committee declares stable.
2. **Release cadence.** A release is cut when a related set of tasks is complete (a status step, or a batch of committee decisions), never per change.
3. **Single source.** `schema/releases.yaml` lists every release, newest first: version, date, change type, sections, description, approved by. The current version is its newest entry. The Revision History page is generated from it by `scripts/build_docs.py`. The section files no longer carry `matcore_version`.
4. **A release** is one commit on `main` that adds the new entry to `schema/releases.yaml`, followed by the git tag `vX.Y.Z` on that commit; CI refuses a tag that differs from the newest entry. Tagged releases get a Zenodo DOI (0000).
5. **Website.** A push to `main` deploys the `dev` version, marked on every standard page as an unreleased development version. A tag `vX.Y.Z` deploys `X.Y.Z` and moves the alias `latest` to it; the theme's version selector lists all releases. Every standard page states its version under the title.
6. **Versioned property addresses.** The permalink button copies an address that names the concrete version, e.g. `…/matcore/0.4.0/standard/02-minimal/#minimal.creator`, also when the page is read through `latest`. On `dev` pages it copies the `dev` address with a tooltip warning that the address is not stable or citable.
7. **First release: 0.4.0**, "Minor (Breaking)", across the document: `main` as of this change (the migrated baseline with its presentation on the site). The tag `v0.9-baseline` stays as a historical marker of the baseline commit; it is not a release.

## Consequences
New `schema/releases.yaml`; `matcore_version` removed from the meta-schema and the section files; `docs/revision-history.md` becomes generated; `layout.js` shows the version and builds versioned addresses; CI deploys `dev` on `main` and `X.Y.Z` + `latest` on tags, and checks generated pages outside `docs/standard/` too. The 0.4.0 tag is pushed by the human after this change is merged.
