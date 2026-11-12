# 0060 — Spin styles a particle interaction model can have

Date: 2026-11-12. Status: accepted. Decided by: Ellad Tadmor.

## Context
pim `magnetic-interactions › spin-style` (moved whole from md by 0046 item 8) lists five baseline values: "Classical spin dynamics", "Coupled spin lattice dynamics", "Ab initio spin dynamics" (magnetism via spin-polarized DFT), "Tight binding spin dynamics" (magnetism from itinerant electrons) and "Quantum spin dynamics" (moments as quantum operators under the time-dependent Schrödinger equation). The list has no "Other user-specified value", unlike every other list in the baseline.

0046 defines a particle interaction model as giving energies and forces as an explicit function of the particles' coordinates, without solving for a wavefunction or an electron density. The last three values fail that test: spin-polarized DFT is a computation of method DFT, tight binding one of method TB (an Electronic method, 0046 item 5), and quantum spin dynamics evolves a wavefunction. Under 0046 a computation that uses another's energies and forces names it as an `input` with the role Interaction model, as AIMD names its DFT computation. The first two values name dynamics; 0046's amendment of 2026-11-09 puts the propagated degree of freedom (spins under LLG dynamics) in pim and its thermostat in md.

## Decision
1. **`spin-style`** keeps its description and becomes a string with open terms "Classical spin" and "Coupled spin lattice". Its note: ""Classical spin" – Spins modeled as classical vectors evolved via the Landau–Lifshitz–Gilbert (LLG) equation defined by a spin Hamiltonian. "Coupled spin lattice" – Classical spins whose spin Hamiltonian depends on the particle positions, so that the spins and the particles evolve together. Magnetism obtained from the electrons, e.g. by spin-polarized DFT or tight binding, is a computation of its own (method DFT or TB), which the computation that uses it names as an `input` with the role Interaction model."
2. **"Ab initio spin dynamics", "Tight binding spin dynamics" and "Quantum spin dynamics" are removed** from pim. Spin-polarized DFT is described by dft (`calculation-physics`); a TB computation by minimal alone, since there is no TB section.
3. **`magnetic-dipole`** becomes a string with the baseline's examples Heisenberg, Multi-spin and Zeeman, and the note: "Note: The strength of an applied field is the condition `magnetic-field` in minimal `conditions`; a Zeeman term names its coupling to the spins."

## Consequences
- One pull request applies items 1–3 (schema, tests, regenerated page) and completes pim. No example has magnetic interactions.
- PROPOSED, NOT DECIDED:
  - a section for tight binding, so a TB computation's settings can be recorded;
  - where quantum spin dynamics is described, since it is neither PIM nor any existing section;
  - a minimal `method` term for spin dynamics on a fixed lattice (e.g. SD under Atomistic, described by md), which is neither MD nor MS; to be taken up with md `algorithm`.
