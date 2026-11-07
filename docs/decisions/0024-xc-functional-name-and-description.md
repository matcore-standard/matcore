# 0024 — Name and description of an exchange-correlation functional

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
In dft `xc-functional`, `name` (added by 0017) holds the functional as the author names it, with examples PBE and HSE06. `description`, from the baseline, is "Explanatory text providing more information about the type of the exchange-correlation method used including any relevant identifying information." Its note lists named functionals by family ("GGA: Typical choices are PW91, PBE, rPBE, revPBE, BLYP, etc."), which are examples of `name`; the note predates `name`. The two fields therefore appear to overlap.

Merging them into a single `name` was weighed and rejected:
- `name` is a short identifier a tool can match; `description` is free prose, as in examples/dft.xml ("PW91 functional (the choice is motivated by the existence of a large-scale simulation of the melting point with this functional)"). Merged, the prose becomes the name.
- `description` exists in 0.5.0 instances; dropping it breaks them.

## Decision
1. **Both fields stay**, unchanged in name, order, type and flags.
2. **`name`'s note** holds the list of named functionals by family, moved from `description` in its baseline wording, with the sentence pointing to `normalization`:

   > Examples of possible content by type: LDA: Common parameterizations: VWN, PW92, etc. GGA: Typical choices are PW91, PBE, rPBE, revPBE, BLYP, etc. Meta GGA: Specific named examples include TPSS, SCAN, M06, etc. Hybrid: B3LYP, PBE0, HSE03, HSE06, NeuralXC, DeePKS, … ML: DM21, NNLDA, NNGGA, CIDER, etc. Others: BEEF, VdW-corrections (added on top of XC, e.g., D2, D3, D4), etc. A decomposition into the components of a community library such as LibXC is given in normalization.
3. **`description`'s note** states its own use: "Free text on what `type` and `name` do not say, e.g. a modification of the functional or the reason for choosing it."
4. **examples/dft.xml** gives `<name>PW91</name>` after `<type>`, keeping its description.

## Consequences
- One pull request applies items 2–4 (schema, tests, regenerated page, example).
- No instance is affected: the structure is unchanged.
- PROPOSED, NOT DECIDED: whether `name`'s note should say that a dispersion correction's name may form part of `name` (e.g. PBE-D3) and that the correction is also recorded as `calculation-physics` "Van der Waals" (0022).
