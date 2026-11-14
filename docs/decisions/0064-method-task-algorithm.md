# 0064 — Method names the section, task the goal, algorithm the procedure

Date: 2026-11-14. Status: accepted. Decided by: Ellad Tadmor.

## Context
A reviewer found that section 2.4 (Particle Simulation) cannot describe accelerated and rare-event methods: hyperdynamics (bond-boost, strain-boost), parallel replica dynamics, temperature-accelerated dynamics, aMD and GaMD, replica exchange, basin hopping and basin filling, forward flux, transition path and transition interface sampling, milestoning, the string, dimer, ART and ART nouveau and eigenvector-following methods, steered and targeted MD, and kinetic Monte Carlo variants. The baseline's ps `algorithm` lists integrators, minimizers and free energy methods only, keyed to the calculation type that 0046 moved to minimal `task`.

Analysis of minimal `computation` against these methods found two overlaps:
- `task` mixes mechanism (Dynamics; Sampling, "without a time evolution") with goal (Optimization, Free energy calculation, Training, Property calculation), and has no term for saddle-point and path searches. An umbrella-sampling MD run fits Dynamics, Sampling and Free energy calculation as defined.
- `method`'s MD, MS and MC repeat what `task` and `algorithm` say, and CGMD repeats `method-class` Mesoscopic with pim `particle-style` Bead. Placing MD, MS and MC in `method` gives no principle for leaving accelerated MD, metadynamics or path sampling out of it.

Separate properties for the time scale (direct, accelerated) and the sampling bias were considered and declined: the algorithm terms imply them, so they could only contradict them.

Other standards were read for context, not for conformance: MODA (CWA 17284:2018), the Review of Materials Modelling (RoMM, 2017), EMMO and OSMO, the NFDI-MatWerk ontology and knowledge graph, ASMO and CMSO (OCDO), NOMAD MetaInfo and nomad-simulations, QCSchema and QCPortal, OpenKIM, CML CompChem, OPTIMADE, ASE and pyiron, and the FAIRmat Area C feedback to MatCore. All separate the physical model from the procedure run on it (MODA §3.10: "strict separation between the concept of 'Model' and 'Solver'"); QCSchema separates what is computed from the procedure; NOMAD's workflow classes and CML CompChem's task mix goal and procedure; FAIRmat Area C (item 4) asks MatCore to separate method from workflow or task.

## Decision
Each property of a computation answers one question, and none can be derived from another.

1. **minimal `method`** names the method section that describes the computation. Its description becomes "The method of the calculations in this computation, which names the section of this standard that describes their settings, where one exists."
   - **PS** (Particle Simulation) replaces MD, MS, MC and CGMD. Cases: Electronic CC, QMC, DFT, MBPT, TB; Atomistic PIM, PS; Mesoscopic DDD, KMC, PIM, PS; Continuum PF; Data-driven ML.
   - The note defines "PS" as: "Particle Simulation: a system of particles moved or sampled using the energies and forces of another computation, by molecular dynamics, molecular statics, Monte Carlo or related methods; described in the PS section." The definitions of MD, MS, MC and CGMD are removed; the others are unchanged.
   - A term without a section (CC, QMC, TB, DDD, KMC) is described by minimal alone until its section exists.
2. **minimal `method-class`** gains a note: "For a PS computation, give the entity of its particles: Atomistic for atoms, Mesoscopic for coarse-grained particles such as beads."
3. **minimal `task`** names the goal of the computation, never its mechanism. Terms, in this order:
   - "Single point" – unchanged.
   - "Optimization" – "Configurations or cells taken to a minimum of the energy, local or global, e.g. a relaxation or a search for the lowest-energy structure."
   - "Transition state search" (new) – "Saddle points of the energy, or minimum energy paths between given configurations, e.g. by the nudged elastic band or dimer method."
   - "Dynamics" – "Configurations evolved in time where the evolution or the kinetics is the result, e.g. trajectories, transport coefficients or rates, including accelerated dynamics and path sampling."
   - "Sampling" – "Averages over a distribution of configurations, by Monte Carlo or by dynamics, where the time evolution is not itself the result."
   - "Free energy calculation", "Training", "Property calculation" – unchanged.
   - A note: "Give the term for the results the computation is meant to provide; the procedure is given in the method's section, e.g. ps `algorithm`."
4. **ps `algorithm`** names the procedures by which the computation moves or samples the particles: a repeatable string with open terms, required. Its description becomes "A procedure by which the computation moves or samples the particles." Its note groups the terms, as a reading aid only, and defines each:
   - Molecular dynamics, time integration: Leap frog, Runge-Kutta, Velocity Verlet, Verlet.
   - Molecular dynamics, accelerated: Hyperdynamics, Bond-boost hyperdynamics, Strain-boost hyperdynamics, Parallel replica dynamics, TAD.
   - Molecular statics, local minimization: Simplex, Damped dynamics, FIRE, Steepest descent, Conjugate gradients, BFGS.
   - Molecular statics, saddle points and paths: NEB, String method, Dimer method, ART, ART nouveau, Eigenvector following.
   - Global optimization: Simulated annealing, SGLD, Basin hopping, Basin filling.
   - Monte Carlo: Metropolis Monte Carlo, Hybrid Monte Carlo.
   - Enhanced sampling and free energy: Harmonic, Metadynamics, Thermodynamic integration, Umbrella sampling, Replica exchange, Steered MD, Targeted MD, aMD, GaMD.
   - Path sampling: Forward flux sampling, Transition path sampling, Transition interface sampling, Milestoning.
   - The note asks for one entry per procedure, e.g. Velocity Verlet and Hyperdynamics, and states that how a thermodynamic constraint is enforced (thermostat, barostat, GCMC) is given in `thermodynamic-constraint`, not here.
5. **The PS introduction** names Monte Carlo: "This category includes molecular dynamics (MD), molecular statics (MS), Monte Carlo (MC) and their coarse-grained forms: energy and free energy minimization, equilibrium and nonequilibrium MD, accelerated dynamics, enhanced sampling, saddle-point searches and related approaches." **§1.2** lists "PS: Particle simulation (molecular dynamics, molecular statics, Monte Carlo and related methods)".
6. **A DFT relaxation** stays one computation (method DFT, task Optimization) with dft's relaxation tolerances (0046, settled 2026-11-09). A relaxation using energies and forces from another computation is a PS computation with task Optimization (was: method MS).

## Departures from other standards
- `method-class` is given for every computation; a PS computation takes the entity of its particles. MODA classifies models, not solvers, and would class ab initio MD by its model, DFT (Electronic).
- MD, MS and MC are not `method` terms, though ASMO's ComputationalMethod has them. Each corresponds to a group of `algorithm` terms, which is how a mapping to ASMO reads.
- Thermostats and barostats stay in ps `thermodynamic-constraint`. RoMM counts them as materials relations, part of the model; ASMO and NOMAD treat them as algorithms or numerical settings.

## Consequences
- Reverses 0061 item 2 (method terms MD and MS unchanged) and rewords 0046's settlement as item 6 states. Settles 0061's open point: PS describes Monte Carlo.
- Breaks 0.6.0 instances whose method is MD, MC or CGMD; MS was added after 0.6.0.
- Two pull requests: (a) items 1, 2, 3, 5 and 6 in minimal, ps's introduction and §1.2, with the tests that list the method terms; (b) item 4 as the status step 5 PR for ps `algorithm`. No example changes: examples/minimal.json's computation is DFT.
- KMC and its variants (BKL, adaptive, self-learning) await a KMC section. Concurrently coupled models (quasicontinuum, bridging scales, QM/MM, hyper-QC) await a Multiscale section, described in MODA's terms (iterative or tight coupling; one-way linking is `input`). Both are PROPOSED, NOT DECIDED.
- PROPOSED, NOT DECIDED, beyond this ruling: marking each property's layer (model, numerical setting, dataset, provenance), as nomad-simulations and FAIRmat Area C (items 2 and 3) suggest; identifiers for terms that map to external vocabularies (ASMO, EMMO); recording what a computation computes (QCSchema's driver), which overlaps 0039's open question.

## Confirmed in review
- `algorithm` is required (the baseline has it optional): with MD, MS and MC gone from `method`, it alone says which procedure was used.
- The baseline term "PMF" is removed from `algorithm`, since a potential of mean force is a result, named in task's Free energy calculation; "Harmonic" is kept, defined as a free energy from the harmonic or quasi-harmonic approximation.
- NEB, Metropolis Monte Carlo and Hybrid Monte Carlo are added beyond the baseline and the reviewer's list.
- aMD and GaMD sit under enhanced sampling, not accelerated dynamics: they bias the potential and reweight, rather than preserve state-to-state dynamics.

*Amended 2026-11-14 (decided by Ellad Tadmor): item 1, the definitions in method's note. They mixed bare expansions with long descriptions that named methods not among the terms (GW, BSE, interatomic potentials, the electron force field, molecular dynamics). Each term is now its expansion followed by a short phrase stating the kind of methods it covers, with no named examples:*
- *"CC" – Coupled Cluster: wavefunction methods that build electron correlation from excitations of a reference state;*
- *"QMC" – Quantum Monte Carlo: stochastic solutions of the many-electron Schrödinger equation;*
- *"DFT" – Density Functional Theory: electronic structure obtained from the electron density;*
- *"MBPT" – Many-Body Perturbation Theory: excited states obtained from many-body Green's functions;*
- *"TB" – Tight Binding: electronic structure in a basis of localized orbitals with parameterized matrix elements;*
- *"PIM" – Particle Interaction Model: energies and forces given as an explicit function of the particles' coordinates, without solving for a wavefunction or an electron density;*
- *"PS" – Particle Simulation: particles moved or sampled using the energies and forces of another computation;*
- *"DDD" – Discrete Dislocation Dynamics: plastic deformation from the motion and interaction of dislocation lines;*
- *"KMC" – Kinetic Monte Carlo: evolution of a system as a sequence of thermally activated events chosen by their rates;*
- *"PF" – Phase Field: microstructure evolution described by continuous fields with diffuse interfaces;*
- *"ML" – Machine Learning: models trained on data to predict materials properties or behavior.*

Still PROPOSED, NOT DECIDED: whether a DFT relaxation may also be described as PS (Optimization) with a DFT computation (Single point) as its interaction model, so that its minimizer can be recorded.
