# 0009 — schema/units.yaml is the single source of Annex U's tables

Date: 2026-11-01. Status: accepted. Decided by: Ellad Tadmor.

## Context
Annex U's two tables, U.3 (kinds) and U.4 (unit symbols), existed twice: typed by hand in `docs/standard/annex-u-units.md`, and as data in `schema/units.yaml`, which `scripts/validate_schema.py` reads. Both called themselves normative, and no record said which prevails. A third copy, the generated page "Annex U. Unit Table (generated)", repeated U.4 again. The hand-typed tables showed things `units.yaml` did not hold: the SI unit after each factor and the SI dimension of each kind, CODATA's significant trailing zeros (Ry, hartree), "π/180 rad" for degree, and the note "(= E_h/2)" for Ry. Ten factors in `units.yaml` (e.g. `1.0e10`) were read as text, not numbers, because a YAML exponent without a sign is not a float.

## Decision
1. **`schema/units.yaml` is the single, normative source of Tables U.3 and U.4.** If the annex and the YAML ever differ, the YAML prevails. The tables in `annex-u-units.md` are generated from it by `scripts/build_docs.py` between marker comments and are never edited by hand; the rest of the annex (purpose, rules, notes, references) stays hand-written.
2. **The separate generated page `annex-u-table.md` is removed**, with its menu entry.
3. **`units.yaml` gains what the tables show**, copied from the annex as verified (0001 A9):
   - each kind: `si_unit` (the coherent SI unit written after factors, e.g. `J`, `Pa`, `m⁻¹`) and `si_dimension` (Table U.3's SI dimension, e.g. `kg·m²·s⁻²`);
   - each unit: `si_factor` as exact decimal text in the annex's mantissa and exponent, e.g. `"2.1798723611030e-18"`, `"1e3"`, `"1"`, so significant digits are kept; `null` for `dimensionless`;
   - `degree`: `exact: π/180`, shown instead of the decimal factor;
   - `Ry`: source `CODATA 2022 (= E_h/2)`.
4. **validate_schema.py checks `units.yaml`**: every `si_factor` is decimal text (or null for `dimensionless`) that parses as a number; every kind has `si_unit` and `si_dimension`.

## Consequences
The generated tables are tested to reproduce the annex tables as they stood before this change, character for character, so no published value or wording changes. Tools read factors with `float(si_factor)`. CLAUDE.md and record 0008 (menu) are updated; the Annex U menu entry is "Annex U. MatCore Unit Table".
