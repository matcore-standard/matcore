# 0069 — Thermodynamic constraints: the ensemble and how it is enforced

Date: 2026-11-15. Status: accepted. Decided by: Ellad Tadmor.

## Context
ps `thermodynamic-constraint` is the last ps property to be filled. In the baseline it holds `system` (the particles the constraint applies to), `type` (the ensemble), `method` (one enforcing algorithm, its terms listed per ensemble), `description` and `td-parameter`. 0042 item 3 divides the work: minimal `conditions` holds the values (temperature, stress, chemical potential, …), and ps holds the ensemble and how it is enforced, with `td-parameter` holding enforcement parameters only.

Points raised in review on 2026-11-14 and 2026-11-15:
- One ensemble is often enforced by more than one algorithm, e.g. NPT by a Nosé-Hoover thermostat with a Parrinello-Rahman barostat, which a single `method` cannot record. Andersen and Berendsen each name both a thermostat and a barostat.
- `method` (how a constraint is enforced) is not ps `algorithm` (the procedure that moves or samples the particles, 0064); the two are separate properties, and the algorithm's note already points thermostats and barostats to `thermodynamic-constraint`.
- A two-phase melting-point run holds two regions at different temperatures. 0026 declined a region field on the conditions, and 0035 item 4 puts the region a value applies to in `conditions › description`. MatCore conveys the intent and key parameters of a computation, not every detail of it, so no region field is added now.
- The semi-grand-canonical ensemble has had no `type` term since PR #56, although 0042 gave `chemical-potential` a `relative-to` for it.

## Decision
1. **`method` is repeatable: one entry for each thermostat, barostat or particle-exchange scheme used.** Its open terms form one list, grouped in its note in the form of 0007 item 5 (amended 2026-11-14), each defined in a phrase:
   - **Thermostats:** Andersen thermostat, Berendsen thermostat, CSVR, Langevin, Nosé-Hoover, Nosé-Hoover chain, Velocity rescaling.
   - **Barostats:** Andersen barostat, Berendsen barostat, CauchyStat, Nosé-Hoover barostat (the baseline's "Nosé-Hoover style"), Parrinello-Rahman.
   - **Particle exchange:** GCMC, SGCMC.

   The terms do not depend on `type` by `depends-on`, since a repeatable `method` mixes groups. In Monte Carlo, an acceptance rule given in ps `algorithm` (e.g. Metropolis) needs no `method` entry.
2. **`type` gains "ΔμNPT" – Semi-grand canonical**, after μσT.
3. **`type` and `conditions`:** a note on `type` says that the ensemble names the quantities held fixed, and that their values are given in minimal `conditions` (e.g. the temperature for NVT, the chemical potential for μVT, a difference with `relative-to` for ΔμNPT); none is repeated in ps (0042 item 3). The schema does not check the two against each other; whether the instance validator does (status step 9) is open.
4. **The other members:**
   - `system`: a required string naming the particles or degrees of freedom the constraint acts on: "Entire system", a group of atoms, or e.g. Drude particles or spins (0046 item 8, amended 2026-11-09). When constraints on different parts hold different values, the values and the parts they apply to are stated in minimal `conditions › description` (0035 item 4).
   - `description`: an optional string.
   - `td-parameter`: a generic parameter in the form of 0016, holding enforcement parameters only, e.g. a damping time, the length of a Nosé-Hoover chain or a barostat relaxation time.

## Consequences
- One pull request (status step 5): schema/ps.yaml, tests, the regenerated ps page. examples/ps.json's NPT entry gains `method` only if its source gives the algorithm.
- No released instance breaks: `method` and the ensemble terms were legacy text in 0.6.0, and ps was created after 0.6.0 (0061).
- Settles the semi-grand-canonical term (PROPOSED since PR #56) and where a region's temperature goes (raised 2026-11-14): in `conditions › description`, with no new field.
- PROPOSED, NOT DECIDED: whether the step 9 validator checks `type` against `conditions` (the fixed quantities present; μ ensembles with system-openness Open, 0036).
