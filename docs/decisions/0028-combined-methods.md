# 0028 — Methods that supply energies and forces to other methods

Date: 2026-11-07. Status: accepted. Decided by: Ellad Tadmor.

## Context
Community feedback:
1. On §1.2: "supported "methods" (in scope) mixes up categorically different things. DFT is a way of calculating single point properties. MD is something you do with energies and forces."
2. On `computation › method-class`: "this whole classification needs to be rethought - if you're using DFT as a black box for atomic energies/forces (AIMD), is that "atomistic" or "electronic"?"
3. On `computation › method`: "same issue as comment on `method-class` above. What if it's a combined approach? For example AIMD or MLIPs?"

Response to 1: the methods in scope are distinct computational materials science techniques, each with a community arranged around it, and §1.2 allows them to be combined ("an ab initio molecular dynamics (AIMD) dataset could include both MatCore-DFT and MatCore-MD metadata files"). The comment also points to a real distinction: some methods supply energies and forces (DFT, CC, QMC, a machine-learned or empirical potential), others use them to sample or evolve a system (MD, MC). md's `particle-interactions` already records the source of the forces apart from the dynamics; minimal's `method` lists both kinds as alternatives, and holds one value, so a combined computation has no rule for which to give.

Alternatives weighed and rejected:
- **A repeatable `method` (and `method-class`).** It loses which method is primary, and a list of classes cannot be paired with a list of methods by `depends-on`.
- **A new classification scheme.** The present categories (cited to the MODA classification) stay; the rule below says which method they classify. Whether the rule matches MODA's own principle was not checked against the source for this record.

## Decision
1. **§1.2** gains a sentence at the start of its paragraph on combined methods: "Some methods supply energies and forces (e.g. DFT), others use them to sample or evolve a system (e.g. MD)." The paragraph's existing AIMD example follows it.
2. **`computation › method`** gains a note: "Note: Give the method that produces the configurations or properties of the dataset. When another method supplies its energies and forces, give that one in `interaction-model`." `method-class` is the class of that method.
3. **A new property `computation › interaction-model`**, after `method`: optional, repeatable; string, `[]`, inapplicable. Description: "The model that supplies the energies and forces used by `method`, when it is a different method." Open terms (0013): CC, DFT, Empirical potential, ML potential, QMC, Tight binding. Note:

   > "CC" – Coupled Cluster; "DFT" – Density Functional Theory; "Empirical potential" – An interatomic potential with a fixed functional form fitted to data, e.g. Lennard-Jones or EAM; "ML potential" – A machine-learned interatomic potential, e.g. GAP or MACE; "QMC" – Quantum Monte Carlo; "Tight binding" – A semi-empirical electronic-structure model, e.g. DFTB. Give one entry per model, e.g. DFT and Empirical potential for a QM/MM simulation.

Worked cases: a DFT single point or relaxation is Electronic / DFT, with no interaction-model; AIMD is Atomistic / MD with DFT; MD with an MLIP is Atomistic / MD with ML potential; classical MD or MC is Atomistic / MD or MC with Empirical potential; training an MLIP is Data-driven / ML. A dataset of separate calculations (e.g. DFT single points and MD trajectories) repeats `computation`, as before.

## Consequences
- One pull request applies items 1–3 (preamble, schema, tests, regenerated page). The new property is optional and the note adds guidance: no instance is affected, and examples/minimal.xml (a DFT computation) needs no change.
- PROPOSED, NOT DECIDED (md, status step 5): how md's `particle-interactions › model-type` relates to `interaction-model` (the detail of the same model, or its own vocabulary).
- PROPOSED, NOT DECIDED: whether the rule of item 2 matches the classification principle of MODA, which `method-class` cites; to be checked against the MODA source.
