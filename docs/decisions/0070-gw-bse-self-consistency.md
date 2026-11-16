# 0070 — GW and BSE in one computation, a self-consistency property for each

Date: 2026-11-16. Status: accepted. Decided by: Ellad Tadmor.

## Context
mbpt `mbpt-method` holds `type` (GW, BSE, GW/BSE) and one `self-consistency` whose terms mix the two stages: G0W0, GW0, G0W, scGW and QSGW for GW, BSE0 and scBSE for BSE, and the combinations evGW+BSE and scGW+BSE. The commonest combination, G₀W₀ followed by BSE, has no term, and covering every GW variant with every BSE variant would take one combined term per pair.

Review on 2026-11-16 raised two more points: eigenvalue-only self-consistent GW (evGW) has no term of its own, and the digit zero in G0W0, GW0, G0W and BSE0 looks like the letter O in the site's fonts. The .docx wrote the definitions with subscripts (G₀, W₀), which the migration lost.

Three structures were compared: the baseline; GW followed by BSE as two computations, the BSE naming the GW as input role Starting point (0046); and one computation with a self-consistency property for each stage. The last was chosen: a GW + BSE calculation stays one computation, as in the baseline, and needs no combined terms.

## Decision
1. **`self-consistency` is replaced by two optional properties of `mbpt-method`:**
   - `gw-self-consistency`, open terms G0W0, GW0, G0W, evGW, scGW, QSGW;
   - `bse-self-consistency`, open terms BSE0, scBSE.

   The combined terms evGW+BSE and scGW+BSE are removed.
2. **"evGW" – Eigenvalue-only self-consistent GW** is added.
3. **`type` keeps GW, BSE and GW/BSE.** GW followed by BSE is one computation of type GW/BSE; a computation of type GW or BSE does only that stage, e.g. a BSE built on DFT energies, which names the DFT computation as input role Starting point. This qualifies 0063 for MBPT: the GW and BSE stages of one calculation are not separate computations.
4. **Which property is given follows `type`:** `gw-self-consistency` for GW and GW/BSE, `bse-self-consistency` for BSE and GW/BSE. A note states the rule; 0013's `depends-on` constrains values, not presence, so the schema does not check it.
5. **The terms stay ASCII** (G0W0, as codes write them), and each definition writes the notation with subscript zero (G₀W₀), restoring the .docx subscripts.

## Consequences
- Applied in the mbpt-method pull request (status step 5): schema/mbpt.yaml, tests, the regenerated mbpt page; examples/mbpt.json writes `gw-self-consistency`.
- No released instance breaks: mbpt's properties were legacy text in 0.6.0.
- Settles the open question of GW + BSE as one computation or two (raised 2026-11-15).
- PROPOSED, NOT DECIDED: whether the step 9 validator checks the presence rule of item 4.
