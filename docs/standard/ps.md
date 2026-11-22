# 2.4 Particle Simulation (PS) Metadata

<p class="mc-version" data-version="0.7.0">Version 0.7.0</p>

The metadata for particle simulations (MatCore-PS) is tabulated below. A particle simulation moves or samples a system of particles using the energies and forces supplied by an interaction model, a particle interaction model or, as in ab initio molecular dynamics, an electronic structure computation. This category includes molecular dynamics (MD), molecular statics (MS), Monte Carlo (MC) and their coarse-grained forms: energy and free energy minimization, equilibrium and nonequilibrium MD, accelerated dynamics, enhanced sampling, saddle-point searches and related approaches. The properties are given in settings blocks, each naming the PS computations it describes. (Note: This standard inherits the metadata in the minimal MatCore standard, adding the properties below.)

<span class="mc-legend"><span class="mc-key"><span class="mc-star">*</span> required</span><span class="mc-key"><span class="mc-icon mc-i-once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span> appears at most once</span><span class="mc-key"><span class="mc-icon mc-i-rep"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span> repeatable</span></span>

<details class="note mc-property" id="ps.settings" markdown="1">
<summary><span class="mc-name">settings<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

Settings shared by the computations named in it.

| Required | Repeatable |
|---|---|
| yes | yes |

<details class="note mc-property" id="ps.settings.computation-label" markdown="1">
<summary><span class="mc-name">computation-label<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

The label of a computation these settings apply to.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | yes | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="ps.settings.algorithm" markdown="1">
<summary><span class="mc-name">algorithm<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A procedure by which the computation moves or samples the particles.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | yes | string | [] | inapplicable | — |

Recommended: `Leap frog`, `Runge-Kutta`, `Velocity Verlet`, `Verlet`, `Hyperdynamics`, `Parallel replica dynamics`, `TAD`, `Simplex`, `Damped dynamics`, `FIRE`, `Steepest descent`, `Conjugate gradients`, `BFGS`, `NEB`, `String method`, `Dimer method`, `ART`, `Eigenvector following`, `Simulated annealing`, `SGLD`, `Basin hopping`, `Basin filling`, `Random structure search`, `Evolutionary algorithm`, `Particle swarm optimization`, `Minima hopping`, `Metropolis Monte Carlo`, `Hybrid Monte Carlo`, `Harmonic`, `Metadynamics`, `Thermodynamic integration`, `Umbrella sampling`, `Replica exchange`, `Steered MD`, `Targeted MD`, `aMD`, `Forward flux sampling`, `Transition path sampling`, `Milestoning`. Other values are allowed.

**Clarifications:**

**Molecular dynamics, time integration**

- "Leap frog" – Positions and velocities advanced at times offset by half a time step
- "Runge-Kutta" – The equations of motion integrated by a Runge-Kutta scheme, which evaluates the forces at several points within each time step
- "Velocity Verlet" – Positions, velocities and forces advanced to the same times, the velocities in two half steps
- "Verlet" – Positions advanced from those at the two previous time steps, without explicit velocities

**Molecular dynamics, accelerated**

- "Hyperdynamics" – A bias potential that raises the energy wells but vanishes near the dividing surfaces between states, so that the sequence of transitions is preserved and the simulated time is boosted
- "Parallel replica dynamics" – Copies of the system run in parallel from one state, the first transition found being accepted and the simulated time summed over the copies
- "TAD" – Temperature-Accelerated Dynamics: transitions found at a high temperature and their times extrapolated to the temperature of interest by harmonic transition state theory

**Molecular statics, local minimization**

- "Simplex" – The downhill simplex method of Nelder and Mead, which uses energies only
- "Damped dynamics" – Dynamics with friction or velocity quenching, which removes kinetic energy until the system comes to rest at a minimum
- "FIRE" – Fast Inertial Relaxation Engine: damped dynamics that turns the velocity toward the force and adapts the time step
- "Steepest descent" – Steps along the force
- "Conjugate gradients" – Line minimizations along directions conjugate to the previous ones
- "BFGS" – Broyden-Fletcher-Goldfarb-Shanno: a quasi-Newton method that builds an approximate inverse Hessian from successive forces, including its limited-memory form L-BFGS

**Molecular statics, saddle points and paths**

- "NEB" – Nudged Elastic Band: a chain of images between two minima, joined by springs and relaxed to the minimum energy path, including its climbing-image form
- "String method" – A path between two minima represented as a curve, moved along the force perpendicular to it and reparameterized until it is the minimum energy path
- "Dimer method" – A saddle point reached from a minimum by following the lowest curvature mode, estimated from a pair of nearby images using forces only
- "ART" – Activation-Relaxation Technique: a saddle point reached by pushing the system out of its basin, followed by relaxation into a new minimum
- "Eigenvector following" – Steps along the eigenvectors of the Hessian, uphill along one and downhill along the others, to a saddle point

**Global optimization**

- "Simulated annealing" – A temperature lowered gradually during dynamics or Monte Carlo, so that the system settles in a low minimum
- "SGLD" – Stochastic Gradient Langevin Dynamics: Langevin dynamics with stochastically estimated gradients, used to explore and minimize
- "Basin hopping" – Random moves, each followed by a local minimization, accepted by a Metropolis criterion on the minimized energies
- "Basin filling" – Penalty functions added to the energy around the current minimum until the system escapes over the lowest saddle point, mapping minima and the barriers between them
- "Random structure search" – Candidates generated at random within given constraints, each relaxed to a local minimum
- "Evolutionary algorithm" – Candidates produced from earlier ones by heredity and mutation and selected by their energies, each relaxed to a local minimum
- "Particle swarm optimization" – Candidates moved through configuration space toward the best structures found by each candidate and by the swarm, each relaxed to a local minimum
- "Minima hopping" – A walk from one local minimum to the next by short molecular dynamics escapes, with an energy threshold for accepting a new minimum and a record of the minima already visited

**Monte Carlo**

- "Metropolis Monte Carlo" – Random trial moves accepted with the Metropolis probability, which samples the Boltzmann distribution
- "Hybrid Monte Carlo" – Trial moves made by short molecular dynamics trajectories, accepted by a Metropolis criterion on the total energy

**Enhanced sampling and free energy**

- "Harmonic" – A free energy from the harmonic or quasi-harmonic approximation
- "Metadynamics" – A history-dependent bias, built from Gaussians deposited along chosen collective variables, that drives the system away from states already visited and gives the free energy
- "Thermodynamic integration" – A free energy difference from the integral of the average derivative of the energy along a coupling parameter
- "Umbrella sampling" – Sampling in windows along a collective variable, each restrained by a bias potential, combined by reweighting into a free energy profile
- "Replica exchange" – Copies of the system at different temperatures or Hamiltonians, whose configurations are exchanged by a Metropolis criterion
- "Steered MD" – An external force or moving restraint applied along a collective variable to drive a transition
- "Targeted MD" – A time-dependent constraint that drives the system toward a target configuration
- "aMD" – Accelerated Molecular Dynamics: a boost added to the potential where the energy is below a threshold, averages being recovered by reweighting

**Path sampling**

- "Forward flux sampling" – Trajectories fired from a series of interfaces between two states, the rate being the product of the probabilities of reaching each next interface
- "Transition path sampling" – Monte Carlo sampling of the ensemble of trajectories that connect two states, e.g. by shooting and shifting moves
- "Milestoning" – Short trajectories between milestones along a reaction coordinate, combined to give the kinetics of the whole transition

Note: Give one entry for each procedure used, e.g. Velocity Verlet and Hyperdynamics, or Random structure search and BFGS for a search that relaxes its candidates. How a thermodynamic constraint is enforced, e.g. a thermostat, a barostat or grand canonical Monte Carlo moves, is given in `thermodynamic-constraint`, not here.

Note: Numerical parameters of a procedure, e.g. the time step of Velocity Verlet or the number of images of NEB, are given as `computation-parameter` entries; its variant, e.g. well-tempered metadynamics, and other specifics are given in `description`.

</details>

<details class="note mc-property" id="ps.settings.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Further information on the algorithms of these settings, e.g. the variant used, and an explanation of their computation-parameter entries.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="ps.settings.computation-parameter" markdown="1">
<summary><span class="mc-name">computation-parameter</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A fixed variable associated with the specified computation algorithm.

| Required | Repeatable |
|---|---|
| no | yes |

Note: For example, the time step of Velocity Verlet, the simulation time of a dynamics run, the convergence tolerance of an energy minimization, the number of images of NEB, or, for a structure search, the number of candidates, the number of atoms per cell, the allowed space groups, the volume range and the force and energy tolerances of the local relaxations.

<details class="note mc-property" id="ps.settings.computation-parameter.name" markdown="1">
<summary><span class="mc-name">name<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The designation of the parameter associated with the specified computation algorithm.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="ps.settings.computation-parameter.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The data associated with the computation parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | any | any | any | — |

</details>

<details class="note mc-property" id="ps.settings.computation-parameter.unit" markdown="1">
<summary><span class="mc-name">unit<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit in which the associated value is expressed.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

**Clarifications:** A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning).

</details>

<details class="note mc-property" id="ps.settings.computation-parameter.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

An explanation of the meaning, source, or purpose of the computation parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

</details>

<details class="note mc-property" id="ps.settings.initialization" markdown="1">
<summary><span class="mc-name">initialization</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Information on the conditions set at the start of the simulation.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

Note: Give what the computation sets up itself, e.g. velocities drawn from a Maxwell-Boltzmann distribution at 300 K with a stated random seed, or randomly oriented spins. A configuration carried over from another computation is named in minimal `computation › input` with the role Initial configuration, and the imposed conditions, e.g. the temperature, are given in minimal `conditions`.

</details>

<details class="note mc-property" id="ps.settings.thermodynamic-constraint" markdown="1">
<summary><span class="mc-name">thermodynamic-constraint</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

Macroscopic physical restriction imposed on the simulation, such as a statistical mechanics ensemble.

| Required | Repeatable |
|---|---|
| no | yes |

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.system" markdown="1">
<summary><span class="mc-name">system<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The collection of particles to which the constraint is applied.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Examples: `Entire system`.

Note: Give "Entire system" when the constraint acts on all particles; otherwise name the subset of atoms or the degrees of freedom it acts on, e.g. Drude particles or spins. When constraints on different parts hold different values, the values and the parts they apply to are stated in minimal `conditions › description`.

</details>

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.type" markdown="1">
<summary><span class="mc-name">type<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The nature of the imposed thermodynamic constraint.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

Recommended: `NVE`, `NVT`, `μVT`, `NPT`, `NσT`, `μPT`, `μσT`, `ΔμNPT`, `NPH`, `NσH`. Other values are allowed.

**Clarifications:**

- "NVE" – Microcanonical
- "NVT" – Canonical
- "μVT" – Grand canonical
- "NPT" – Isothermal-isobaric
- "NσT" – Isothermal-isostress
- "μPT" – Grand isothermal-isobaric
- "μσT" – Grand isothermal-isostress
- "ΔμNPT" – Semi-grand canonical
- "NPH" – Isoenthalpic-isobaric
- "NσH" – Isoenthalpic-isostress

Note: The ensemble names the quantities held fixed. Their values are given in minimal `conditions`, e.g. the temperature for NVT, the chemical potential for μVT, or a difference of chemical potentials with `relative-to` for ΔμNPT, and are not repeated here.

</details>

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.method" markdown="1">
<summary><span class="mc-name">method</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

The name of the approach used to impose the constraint.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | yes | string | [] | inapplicable | — |

Recommended: `Andersen thermostat`, `Berendsen thermostat`, `CSVR`, `Langevin`, `Nosé-Hoover`, `Nosé-Hoover chain`, `Velocity rescaling`, `Andersen barostat`, `Berendsen barostat`, `CauchyStat`, `Nosé-Hoover barostat`, `Parrinello-Rahman`, `GCMC`, `SGCMC`. Other values are allowed.

**Clarifications:**

**Thermostats**

- "Andersen thermostat" – Stochastic collisions that redraw particle velocities from the Maxwell-Boltzmann distribution
- "Berendsen thermostat" – Velocities scaled so that the temperature relaxes exponentially toward its target
- "CSVR" – Canonical sampling through velocity rescaling: velocity scaling with a stochastic term that samples the canonical ensemble
- "Langevin" – A friction force and a random force on each particle
- "Nosé-Hoover" – Deterministic coupling of the particles to an extended-system thermostat variable
- "Nosé-Hoover chain" – A Nosé-Hoover thermostat coupled in turn to a chain of further thermostat variables
- "Velocity rescaling" – Velocities scaled to give the target temperature exactly

**Barostats**

- "Andersen barostat" – Extended-system barostat with the volume as a dynamical variable, for isotropic pressure
- "Berendsen barostat" – Coordinates and cell scaled so that the pressure relaxes exponentially toward its target
- "CauchyStat" – Extended-system barostat that imposes the Cauchy (true) stress, for large deformations of the cell
- "Nosé-Hoover barostat" – Extended-system barostat in the Nosé-Hoover form, e.g. the Martyna-Tobias-Klein equations
- "Parrinello-Rahman" – Extended-system barostat with the cell vectors as dynamical variables, so the cell can change shape

**Particle exchange**

- "GCMC" – Grand canonical Monte Carlo: insertions and deletions of particles accepted according to the chemical potential
- "SGCMC" – Semi-grand canonical Monte Carlo: changes of species accepted according to differences of chemical potential

Note: Give one entry for each thermostat, barostat or particle-exchange scheme used, e.g. Nosé-Hoover and Parrinello-Rahman for NPT. An acceptance rule of Monte Carlo, e.g. Metropolis, is given in `algorithm`, not here.

</details>

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

Explanatory text about the constraint and method used to impose it.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.td-parameter" markdown="1">
<summary><span class="mc-name">td-parameter</span><span class="mc-icon mc-i-rep" title="repeatable: may appear more than once" aria-label="repeatable: may appear more than once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 6v3l4-4-4-4v3a8 8 0 0 0-8 8c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12a6 6 0 0 1 6-6m6.76 1.74L17.3 9.2c.44.84.7 1.8.7 2.8a6 6 0 0 1-6 6v-3l-4 4 4 4v-3a8 8 0 0 0 8-8c0-1.57-.46-3.03-1.24-4.26"/></svg></span></summary>

A fixed variable associated with the specified thermodynamic constraint.

| Required | Repeatable |
|---|---|
| no | yes |

Note: Parameters of the method only, e.g. the damping time of a Langevin thermostat, the length of a Nosé-Hoover chain or the relaxation time of a barostat. The values held fixed, e.g. the temperature, are given in minimal `conditions`.

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.td-parameter.name" markdown="1">
<summary><span class="mc-name">name<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The designation of the parameter associated with the specified thermodynamic constraint.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

</details>

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.td-parameter.value" markdown="1">
<summary><span class="mc-name">value<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The data associated with the thermodynamic constraint parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | any | any | any | — |

</details>

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.td-parameter.unit" markdown="1">
<summary><span class="mc-name">unit<span class="mc-star" title="required" aria-label="required">*</span></span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

The unit in which the associated value is expressed.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| yes | no | string | [] | inapplicable | — |

**Clarifications:** A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a validation warning).

</details>

<details class="note mc-property" id="ps.settings.thermodynamic-constraint.td-parameter.description" markdown="1">
<summary><span class="mc-name">description</span><span class="mc-icon mc-i-once" title="appears at most once" aria-label="appears at most once"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 12c0-1-.26-1.96-.7-2.8l1.46-1.46A7.93 7.93 0 0 1 20 12c0 1.39-.36 2.68-1 3.82l-1.5-1.5c.32-.72.5-1.49.5-2.32M2.39 1.73 1.11 3 5.5 7.37C4.55 8.68 4 10.27 4 12c0 1.57.46 3.03 1.24 4.26L6.7 14.8A5.9 5.9 0 0 1 6 12c0-1.17.34-2.26.92-3.19l8.27 8.27c-.93.58-2.02.92-3.19.92v-3l-4 4 4 4v-3c1.73 0 3.32-.55 4.63-1.5l4.21 4.23 1.27-1.27zM12 6v2.8l.1.1L16 5l-4-4v3c-1.38 0-2.68.36-3.82 1l1.5 1.5c.72-.32 1.5-.5 2.32-.5"/></svg></span></summary>

An explanation of the meaning, source, or purpose of the thermodynamic constraint parameter.

| Required | Repeatable | Type | Extent | Kind | Rec. unit |
|---|---|---|---|---|---|
| no | no | string | [] | inapplicable | — |

</details>

</details>

</details>

</details>

## Example: PS Method-Specific Metadata

Dataset source: [https://doi.org/10.6084/m9.figshare.6273170](https://doi.org/10.6084/m9.figshare.6273170)

```json
{
  "ps": {
    "settings": [
      {
        "computation-label": [
          "md-quench"
        ],
        "algorithm": [
          "Velocity Verlet"
        ],
        "thermodynamic-constraint": [
          {
            "system": "Entire system",
            "type": "NPT",
            "description": "Amorphous samples were produced by quenching the molten metal from 2300 to 300 K."
          }
        ]
      }
    ]
  }
}
```

