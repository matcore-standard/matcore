# 0066 — Global structure searches

Date: 2026-11-14. Status: accepted. Decided by: Ellad Tadmor.

## Context
A reviewer generates structures by sampling possible inputs and minimizes thousands of them to find the global minimum, and finds no place to say how the phase space was sampled.

What the standard records today:
- the computation, with task Optimization, which 0064 defines as "local or global, e.g. a relaxation or a search for the lowest-energy structure";
- the search code, as the computation's `software`;
- anything else, only as free text in the dataset's `description`.

What it cannot record:
- the search procedure (random, evolutionary, particle swarm, minima hopping);
- its constraints (symmetry, atoms per cell, volume range) and size (number of candidates, generations);
- the convergence criteria of the local relaxations, when the energy code is not the one optimizing;
- how the candidates were ranked and how often the lowest was found.

Ruling 0065 item 2 splits a search into a Structure generation computation and an Optimization computation. That split fails for an evolutionary or particle-swarm search: each generation of candidates depends on the energies of the last, so the two computations would be inputs of each other. Structure generation also has no `method` term (0065, open point), so no section can hold its settings.

A search driver moves configurations using the energies and forces of another computation. That is the definition of PS (0064 item 1).

## Decision
1. **A global structure search run by its own driver is one PS computation with task Optimization.** It names the computation that gives the energies and forces (DFT, PIM, or another method) as an input with the role Interaction model; that computation's task is Single point. The candidates the driver creates are part of the search, not a Structure generation computation. The local relaxation of each candidate is part of the search too, whichever code performs it: its minimizer is a second `algorithm` entry, e.g. Random structure search and BFGS.
2. **0065 item 2 is amended**: a search is split into Structure generation and Optimization only when its candidates are created apart from the search and recorded as a computation of their own, e.g. by a generative model (method ML) or an enumeration of defect sites. The search names that computation as an input with the role Initial configuration.
3. **ps `algorithm`'s Global optimization group gains four terms**, with these definitions in its note:
   - "Random structure search" – candidates generated at random within given constraints, each relaxed to a local minimum.
   - "Evolutionary algorithm" – candidates produced from earlier ones by heredity and mutation and selected by their energies, each relaxed to a local minimum.
   - "Particle swarm optimization" – candidates moved through configuration space toward the best structures found by each candidate and by the swarm, each relaxed to a local minimum.
   - "Minima hopping" – a walk from one local minimum to the next by short molecular dynamics escapes, with an energy threshold for accepting a new minimum and a record of the minima already visited.
4. **The settings of a search are ps `computation-parameter` entries**, e.g. the number of candidates, the number of generations, the atoms per cell, the allowed space groups, the volume range, and the force and energy tolerances of the local relaxations. Its note gives these as examples. dft's relaxation tolerances are not used for a search, since its DFT computation is a Single point.
5. **minimal `computation` gains an optional `description`**, after `label`: "An explanation of the computation that its other properties do not capture, e.g. the protocol of a search." A string, scalar, kind inapplicable, values null.
6. **The results of a search are not settings.** The structures it finds are `structure` entries of the dataset, named in its `structure-label`. How candidates were ranked (energy, enthalpy at a pressure, free energy), the energies found and how often the lowest recurred are results, left to 0039's open question on recording what a dataset contains.

## Consequences
- Amends 0064 item 4 (the Global optimization terms) and 0065 item 2 (when a search is split). Settles 0064's open point on recording a DFT relaxation's minimizer for searches only: a single relaxation stays a DFT computation with task Optimization (0064 item 6).
- No released instance breaks: `description` is optional and the other properties were added after 0.6.0.
- Pull requests: item 3 joins 0064 PR (b), ps `algorithm`; item 4 goes in the status step 5 PR for ps `computation-parameter`; item 5 is one PR (schema/minimal.yaml, tests/test_computations.py, 02-minimal regenerated).
- PROPOSED, NOT DECIDED: whether a single DFT relaxation may also be described as PS with a DFT Single point, for consistency with item 1 (0064's open point, now narrowed).
