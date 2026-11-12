# 0062 — A property that holds a label is named for the label

Date: 2026-11-12. Status: accepted. Decided by: Ellad Tadmor.

## Context
0046 gave every structure and computation a `label` and added three properties whose value is such a label: `settings › computation` in each method section (dft, pim, ps), minimal `computation › input › computation`, and minimal `computation › structure`. Each carries the name of the container it refers to, so the standard has a `computation` that is a container in minimal and a `computation` that is a string in the method sections, and likewise two `structure`s. The committee found this confusing.

The committee's candidates were declined: `computation-origin` and `computation-source` read as provenance, and `source` collides with the input role Source data; `pointer-to-computation` names an implementation, and the value is a label, not a pointer; `parent-computation` implies a hierarchy, and computations already link through `input`. `applies-to` was declined because minimal `license › applies-to` uses the name for free text.

All three properties were added after release 0.6.0, so renaming them breaks no released instance.

## Decision
1. **`settings › computation`** in dft, pim and ps is renamed **`computation-label`**.
2. **minimal `computation › input › computation`** is renamed **`computation-label`**.
3. **minimal `computation › structure`** is renamed **`structure-label`**.
4. Their other fields, descriptions and notes are unchanged.

## Consequences
- One pull request applies items 1–3 to the schema, the examples, the tests and the regenerated pages. Property addresses change accordingly, e.g. `#ps.settings.computation-label`.
- A property added later whose value is the label of a structure or computation follows the same form: the referent's name followed by `-label`.
- Earlier decision records keep the old names.
