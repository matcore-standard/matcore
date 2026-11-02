# 0013 — Structured values

Date: 2026-11-01. Status: accepted. Decided by: Ellad Tadmor.

## Context
Decision 0002 replaced the prose "Values" of each property with a structured `values` field but left its keys open. Status step 5 fills `values` for every property, starting with minimal.yaml, so the keys are needed now. In the baseline, 48 of the 50 controlled vocabularies end with "Other user-specified value if none of the above apply": MatCore is extensible, and a term that users add often is meant to be taken into the standard later.

## Decision
1. **Keys.** `values` is null or a mapping with any of these keys. All keys present apply together.
   - `terms`: an open vocabulary (list of strings). A listed term conforms. Any other string also conforms and is reported as user-specified, so that terms users add can be collected for the committee. A user-specified value close to a listed term (for example differing only in case, spacing or hyphenation, or by a small spelling difference) is reported as a possible typo. The method of comparison is fixed by the validator (status step 9).
   - `enum`: a closed list (list of strings). Any other value is non-conformant. Used only where an unlisted value would make the data meaningless, such as the required convention subproperties of 0001 Part A.
   - `minimum`, `maximum`: inclusive numeric bounds.
   - `format`: the name of a format defined in JSON Schema 2020-12 (Validation, §7.3), for example `date`, `date-time`, `uri`, `email`. The format means what the RFC cited there defines.
   - `pattern`: a regular expression the whole value must match, for a layout that no named format covers.
   - `examples`: sample values, shown to readers. They are data: each must itself satisfy the property's type and values.
   - `note`: prose for any rule that the other keys cannot express.
2. **Combinations.** `terms`, `enum`, `format` and `pattern` apply only to type `string`; `minimum` and `maximum` only to `int` and `float`; `examples` and `note` to any type. A property has at most one of `terms` and `enum`, and at most one of `format` and `pattern`. `minimum` does not exceed `maximum`. `validate_schema.py` checks these rules and that every example satisfies its property. Rules beyond typing are added if a case needs them.
3. **Formats are checked.** JSON Schema 2020-12 treats `format` as an annotation by default and leaves checking optional (§7.2.1). MatCore requires it: a MatCore validator checks every `format` in full, as JSON Schema's Format-Assertion vocabulary describes (§7.2.2). The rules for each format are not stored in MatCore; they are the RFCs that JSON Schema cites, implemented by the validator's libraries.
4. **Deferred** until a property first needs them:
   - terms that carry a definition (e.g. md `mode`: "Static" – snapshot(s) of an arbitrary particle configuration);
   - values that depend on another property's value (e.g. md `computation` › `algorithm`, whose terms depend on `mode`). Proposal, to be decided when the first such property comes up (the md section), together with the conditional rules proposed for §1.3 (`convention`, `basis`, `scaling`):
     ```yaml
     values:
       depends-on: mode        # a sibling under the same parent
       cases:
         Minimization: {terms: [Simplex, Damped dynamics, FIRE, ...]}
         Free energy:  {terms: [Harmonic, Metadynamics, ...]}
     ```
     Each case holds the `values` that apply when the sibling has that value. When the sibling holds a user-specified value, no case applies and any term is accepted.

## Consequences
- meta-schema.yaml gains `terms`. validate_schema.py gains the checks of item 2, with format checking on. build_docs.py renders every key. These come in one pull request before the first property pull request of status step 5.
- With the Python `jsonschema` package, only some formats are checked unless its optional format dependencies are installed; without them, `uri` accepts any string. The pull request above installs them and tests that a malformed value of each format used is rejected.
- Found while counting: md `spin-style` has a controlled list with no "Other" option, and pf `driving-energy` must match a name defined elsewhere in the same instance. Their property pull requests ask how to treat them.

## Settled 2026-11-02 (Ellad Tadmor)
1. **Terms that carry a definition** (item 4, first needed by minimal `material-component` › `phase`). The definitions are written as prose in `note`, one per term, in the baseline's wording. `terms` and `enum` stay plain lists of strings, and no key is added for definitions.
