# 0000 — Move the standard to a Git repository; YAML as source of truth

Date: 2026-10-31. Status: accepted.

## Context
The standard was a Google Doc, manually edited, converted to HTML by a script from a .docx export. Not programmatically accessible; two sources of truth.

## Decision
- Public GitHub organization `matcore-standard` and single repository `matcore` (schema + docs + tools; split later if needed).
- Standard expressed in regular MatCore YAML (one file per section) validated by a JSON-Schema meta-schema written in YAML. No LinkML dependency (may be revisited; keep YAML regular so a translation stays mechanical).
- Baseline migration first, tagged; every subsequent change (units, typed fields, community feedback) as separate PRs referencing decision records.
- Static site (MkDocs Material, GitHub Pages, mike for versions). Tools as one Python package, run in-browser via Pyodide.
- Licenses CC BY 4.0 (text/schema), Apache-2.0 (code). Releases get Zenodo DOIs.
- Google Doc frozen on tagging the baseline.

## Consequences
Committee reviews changes as PRs; decisions live in docs/decisions/. Generated chapters are never hand-edited.
