# 0017 — Name and normalization of an exchange-correlation functional

Date: 2026-11-05. Status: accepted. Decided by: Ellad Tadmor.

Amended 2026-11-07 by 0024: the list of named functionals moves from `description`'s note to `name`'s, with the pointer to `normalization`; `description`'s note states its own use.

## Context
Community feedback on dft `xc-functional` asked for "a canonical normalization layer based on existing community resources such as LibXC", keeping the user-facing value (e.g. "PBE") while also allowing a normalized representation (e.g. the components GGA_X_PBE and GGA_C_PBE, with LibXC as the normalization source).

`xc-functional` › `type` holds the family of the functional (LDA, GGA, Meta GGA, Hybrid, ML). The named functional the feedback calls the user-facing value has no field: it is written as prose in `description`, whose note suggests "LibXC designation: LibXC:LDA_C_GK72 (include source as prefix)". Three alternatives were weighed and rejected:
- writing the normalized components in `type`, with the source in `description`, which puts a family term and a decomposition in one field and the source in free prose;
- a `standard-type` and `standard-type-source` beside `type`, which can contradict `type` and is not the same kind of value;
- a `type-standard-source` that changes what `type` holds, which makes `type`'s meaning depend on another field.

LibXC's list of functionals (Libxc 7.1.0, https://libxc.gitlab.io/functionals/) gives, for example, `GGA_X_PBE` (id 101) and `GGA_C_PBE` (id 130), both "Perdew, Burke & Ernzerhof", and its identifiers begin with family prefixes such as `LDA_`, `HYB_LDA_` and `GGA_`. The pages do not state a naming convention.

## Decision
1. **`type` is unchanged.** It holds the family of the functional.
2. **`name`** (new, optional): a scalar string, the functional as the author names it (e.g. PBE, HSE06). It is the user-facing value and is kept whether or not a normalization is given.
3. **`normalization`** (new, optional, not repeatable): a container holding
   - `components` (required): a list of strings (extent `[:]`), the functional's components in the source's own identifiers (e.g. GGA_X_PBE, GGA_C_PBE);
   - `source` (required): a string with open terms, the first being LibXC.

   Both are required inside the container, so a decomposition never appears without its source, as an identifier's `value` never appears without its `scheme` (0014).
4. **`description`** stays a string. Its note's LibXC hint is replaced by a pointer to `normalization`.
5. The order of `xc-functional`'s subproperties is `type`, `name`, `description`, `normalization`, `xc-parameter`.

## Consequences
- One pull request revises `xc-functional` (schema, tests, regenerated page); examples/dft.xml is reviewed (its description names PW91, which may also be given as `name`).
- PROPOSED, NOT DECIDED: the instance validator (status step 9) may warn when `type` and the family prefix of the components disagree (e.g. `type` LDA with component GGA_X_PBE). LibXC does not document its prefixes as a convention, so the rule needs a source before it is adopted.
- Other normalization sources may be added to `source`'s terms later; a source's identifiers are not checked by the schema.
