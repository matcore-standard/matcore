# 0034 — A material component's composition is a chemical formula

Date: 2026-11-08. Status: accepted. Decided by: Ellad Tadmor.

## Context
Committee feedback on minimal `structure › material-component › constituent` (an element `species` with an atomic-fraction `concentration`):
- It does not work for molecular systems. Atomic fractions give only the empirical formula: HO and H₂O₂ are both H 0.5, O 0.5, and isomers (ethanol, dimethyl ether: C₂H₆O) cannot be told apart.
- It does not work for compounds that share elements, e.g. a silicon dioxide film on a silicon substrate.
- The composition could instead be a chemical formula, like A_x B_{1−x} with A, B and x specified, and should allow mixtures of compounds such as [Si_x Ge_{1−x}]_y [SiO₂]_{1−y}.
- Data that is not of a real material (e.g. a Lennard-Jones glass with non-physical parameters) needs user-defined species.

Sources compared:
- OPTIMADE (specification v1.4.0~develop): `chemical_formula_reduced` and `chemical_formula_hill` have whole-number counts in a fixed order, while `chemical_formula_descriptive` allows decimal counts and any order. `elements_ratios` sum to 1. A species symbol may be "X" for "a non-chemical element".
- OpenKIM `crystal-structure-npt`: `stoichiometric-species` maps element symbols onto the letters of an AFLOW prototype label (e.g. `['Mo','S']` for AB2). The KIM API reserves species `user01`…`user20` for toy models that "do not model a real material".
- CIF core dictionary (`_chemical_formula.sum`): only recognized element symbols, each followed by a count. Clusters are separated by spaces, and elements are in Hill order. A group's multiplier follows its closing parenthesis (rule 4).
- IUPAC, *Nomenclature of Inorganic Chemistry, Recommendations 2005* (Red Book), §IR-11.3.2 "Phases with variable composition" (pp. 237–238): a notation in which there are variables which define composition should be used, with the range of the variable stated, e.g. Cu_x Ni_{1−x} (0 ≤ x ≤ 1), Li_{2−2x} Mg_x Cl_2, Fe_{3x} Li_{4−x} Ti_{2(1−x)} O_6. A specific value may be written into the formula instead: x = 0.35 gives Fe1.05Li3.65Ti1.30O6.
- InChI (IUPAC and the InChI Trust; software v1.07.5, MIT licence): a canonical identifier. Its FAQ says it covers "well-defined, covalently-bonded organic molecules and, with some limitations, organometallic compounds". Polymers and mixtures are not covered.
- OpenSMILES (v1.0, 2016): a line notation that can write any element, but canonical SMILES "should *not* be considered a universal, global identifier". An IUPAC SMILES+ project (2019-002-2-024) is open.

## Decision
1. **`constituent` is removed.** A material component's composition is one chemical formula, with no constituent level. A single phase whose composition mixes substances (a liquid mixture, a glass, a solid solution) is one formula. Separate phases (e.g. SiGe particles in an SiO₂ matrix, an SiO₂ film on an Si substrate) are separate material components, each with its own `role` (0025).
2. **`material-component`** gains three subproperties at the start, in this order, before `form`:
   - **`formula`**: required; string, `[]`, inapplicable. Description: "The chemical formula of the material component." A `pattern` checks the allowed characters. The note gives the grammar of item 3.
   - **`variable`**: optional, repeatable, a container. Description: "A value of a variable used in `formula`." Its subproperties:
     - `name*`: string, pattern one lowercase letter. Description: "The name of the variable, as written in `formula`."
     - `value*`: float, dimensionless. Description: "A value of the variable."
     - `type`: string, open terms Average, Initial, Maximum, Minimum. Description: "What the value represents." The note says that without a `type`, the value holds throughout. It also says that the entries of one variable share its name, with at most one entry per type.
   - **`molecule`**: optional, repeatable, a container. Description: "A molecule in the material component, identified by its structure, e.g. to distinguish isomers." Its subproperties:
     - `formula*`: string. Description: "The molecular formula of the molecule, written as a group of the material component's formula or as the whole formula."
     - `identifier*`: repeatable, a container of `value*` and `scheme*` as in creator's identifier, with scheme terms InChI and SMILES. The note says InChI is preferred where it can represent the molecule, and SMILES otherwise or in addition.
3. **Formula grammar** (the note on `formula`):
   - A formula is a sequence of terms. A term is an element symbol, a user-defined species or a group in parentheses, each followed by an optional count.
   - An element symbol is one of the 118 symbols of the IUPAC Periodic Table (as `species` listed them).
   - A user-defined species is `J` followed by lowercase letters (e.g. `Ja`, `Jlj`), for particles that are not chemical elements. No element symbol begins with J, and the lowercase name ends at the next uppercase letter, digit, brace or parenthesis.
   - A count is a positive number, whole or decimal, written bare (`H2O`, `Si0.7Ge0.3`), or an expression in braces (`Si{x}Ge{1-x}`). A count of 1 is omitted.
   - An expression contains at least one variable. It is built from numbers, one-letter variables, `+`, `-`, implied multiplication and parentheses (e.g. `x`, `1-x`, `3x`, `2(1-x)`), and is linear in its variables. Inside braces, parentheses are arithmetic; outside, they mark groups.
   - A variable is used only when the composition varies, so it has a range or values of several types. A fixed composition is written with its numbers, e.g. `Si0.3Ge0.7`, not `Si{x}Ge{1-x}` with x = 0.3.
   - When a formula is a sequence of two or more groups, as in a mixture of substances, the groups' counts are their mole fractions and sum to 1, e.g. `(H2O)0.9(C2H6O)0.1` or `(SiO2){y}(GeO2){1-y}`.
   - Elements may appear in any order.
   - A molecule is written with its molecular formula (`H2O2`, not `HO`).
4. **Validation**: a formula parser (`scripts/check_formula.py`), called by validate_schema.py, checks every formula in the schema's examples and in examples/. The step 9 instance validator reuses it. It checks:
   - the grammar;
   - the element symbols;
   - that every variable in `formula` has at least one `variable` entry, and every `variable` entry names a variable of the formula;
   - that counts stay at or above 0, and that the counts of a mixture of groups sum to 1, at each value given for the variables (for a linear expression, Minimum and Maximum bound the range);
   - that each `molecule › formula` is a group of the component's formula or the whole formula.

   The 118 symbols, now the parser's list, keep their source: the CIAAW Standard Atomic Weights table.
5. **Annex I** gains rows for InChI and SMILES (identifies: molecule), each field traced to the scheme's own documentation in the pull request. Their checks are a pattern on the form only, with no checksum.
6. **examples/minimal.xml**: each Si constituent becomes `<formula>Si</formula>`.

## Consequences
- One pull request applies items 1–6 (schema, parser, Annex I rows, tests, regenerated pages, example). It breaks 0.5.0 instances: `constituent`, `species` and `concentration` are gone.
- `fraction`'s note still says to give the composition as set up when it changes. The follow-up on simulation conditions takes this up: a value with a `type` (minimum, maximum, average, initial) for `temperature`, `stress` and the rest, which would amend 0026.
