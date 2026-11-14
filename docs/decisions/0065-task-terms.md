# 0065 — Task terms for transitions, generation, equilibration and fitting

Date: 2026-11-14. Status: accepted. Decided by: Ellad Tadmor.

## Context
Ruling 0064 made minimal computation › `task` name the goal of a computation, never its mechanism. A review of the terms against common workflows raised six cases:
- Transition path sampling (TPS, forward flux, transition interface sampling, milestoning) falls under Dynamics, which 0064 defines as "including accelerated dynamics and path sampling", although its goal is the same as that of the nudged elastic band and the dimer method: a transition between states.
- Structure generation: a generative model, random structure searching, enumeration of inequivalent defect or dopant sites, slab cleaving and grain boundary construction produce configurations without evaluating them. A generative model does not optimize, so no term fits.
- Active learning combines several tasks to build a dataset.
- Coarse-graining fits a lower-resolution model or a classical potential to higher-level data (force matching, Boltzmann inversion, cluster expansions).
- Equilibration is commonly separated from production dynamics, so that users can leave out its data.
- Post-processing derives data from existing data without a new simulation (deduplication, unit conversion, symmetry analysis, featurization).

## Decision
1. **"Transition state search" is renamed "Transition path"**: "Transitions between stable states: saddle points of the energy, minimum energy paths, or ensembles of reactive trajectories and the rates they give, e.g. by the nudged elastic band, dimer method or transition path sampling." Dynamics no longer mentions path sampling: "Configurations evolved in time where the evolution or the kinetics is the result, e.g. trajectories, transport coefficients or rates, including accelerated dynamics."
2. **"Structure generation" is added**: "The computational creation, modification, or systematic enumeration of initial atomic, molecular, or crystalline configurations before running physics-based energy or force evaluations." A search that generates, relaxes and ranks structures is a Structure generation computation and an Optimization computation, the latter naming the former as an input with the role Initial configuration (0063). Rattled, perturbed or strained configurations are generated, not sampled.
3. **"Equilibration" is added**: "Configurations brought to the conditions of another computation, which takes them as its Initial configuration; its results are not meant for analysis."
4. **"Training" is reworded** so that it is not read as machine learning only: "The parameters of a model fitted to data, e.g. a machine-learned model, a potential fitted by force matching or Boltzmann inversion, or a cluster expansion." Coarse-graining is not a term of its own.
5. **Active learning is not a term.** It is a workflow of computations linked by `input`: sampling with the current model (Dynamics or Sampling), labelling (Single point), fitting (Training, with the role Training data), and Structure generation for perturbed or scaled configurations. The criterion that selects configurations (query by committee, an uncertainty threshold) is left to the ML section.
6. **Post-processing is not a term.** Deduplication and unit conversion change the dataset and are `provenance` events; symmetry analysis and featurization derive data from another computation's results and are Property calculation.
7. The terms, in this order: Structure generation, Single point, Optimization, Transition path, Equilibration, Dynamics, Sampling, Free energy calculation, Training, Property calculation. The others' definitions and task's note are unchanged.

## Consequences
- Amends 0064 item 3. No released instance breaks: `task` was added after 0.6.0 (0046).
- One pull request: schema/minimal.yaml (task terms and note), tests/test_computations.py, 02-minimal regenerated.
- PROPOSED, NOT DECIDED: whether a Structure generation is a computation only when its configurations are part of the dataset or the input of another computation, so that a single cleaved slab is described in its structure's `description` instead.
- PROPOSED, NOT DECIDED: the `method` of a computation with no method term: a structure generated without a model (random placement, enumeration, geometric construction), a fit of a model that is not machine-learned (force matching of a PIM), an analysis with no physical method (featurization). Candidates: `method` optional where no section applies, or a term for such procedures.
