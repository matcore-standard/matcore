# 0038 — The order of an array value, and the cell vectors

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback on minimal `simulation-conditions › cell` and `cell-reference` (extent `[3, 3]`, "Ordered list of three vectors (a, b, c), each with three components"): an XML document cannot tell a 3×3 array from a list of nine numbers, so the value should be either nine numbers (a1, a2, a3, b1, b2, b3, c1, c2, c3) relative to the orthonormal basis (e1, e2, e3), or three subproperties a, b and c.

The decider set the XML point aside, since the standard is independent of serialization (§1.3), but agreed that the note leaves the layout ambiguous. Two things are unstated: whether `value[i]` is the i-th vector or the i-th Cartesian component, and what basis the components are in. They cannot be in the basis (e1, e2, e3) of `stress`, which is itself built from the cell vectors (e1 along a).

Alternatives declined:
- **Nine numbers (extent `[9]`).** The order must still be stated, so the ambiguity remains, and the declared shape is lost. `stress` and `strain` use `[6]` because a symmetric tensor has six independent components in a stated Voigt order; a cell matrix has nine.
- **Subproperties `a`, `b`, `c`.** Each would need its own `value` and `unit` (0015), so the unit would be written three times and could differ, and a `qualifier` (0035) would sit above three quantities.

## Decision
1. **§1.3, the Extent bullet**, gains a sentence on order: "A value with more than one dimension is a list of lists, the first index outermost: a value of extent [n,m] is a list of n entries, each a list of m components. A serialization preserves this nesting." The bullet becomes: "Extent: The shape of the value, in the notation of the Knowledgebase of Interatomic Models (KIM): [] for a scalar, [3,3] for a 3×3 array, [:] for a list of any length, or any when the schema does not fix it. A value with more than one dimension is a list of lists, the first index outermost: a value of extent [n,m] is a list of n entries, each a list of m components. A serialization preserves this nesting."
2. **`cell › value`**'s note gains, after its first sentence: "`value[i][j]` is the j-th Cartesian component, in the frame of the simulation, of the i-th cell vector, so the rows are a, b and c."
3. **`cell-reference › value`**'s note gains, after its first sentence: "`value[i][j]` is the j-th Cartesian component, in the frame of the simulation, of the i-th reference cell vector, so the rows are a<sub>0</sub>, b<sub>0</sub> and c<sub>0</sub>."
4. Both keep extent `[3, 3]`.

## Consequences
- One pull request applies items 1–3 (Preamble, schema, tests, regenerated page). No instance changes meaning: the rule states what the note implied. examples/ give no cell.
- Status step 7 (serialization requirements) takes up item 1's nesting rule for each serialization.
