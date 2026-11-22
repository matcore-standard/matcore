# 0081 — Derived property families: examples, transport, and transition paths

Date: 2026-11-22. Status: accepted. Decided by: Ellad Tadmor.

## Context
Reviewer feedback, 2026-11-22, on the families of derived properties (the derived introduction's list, which mirrors `derived-property › type`):

> Additional types (if they classify as derived properties)
> - "Mechanical" (tensile, yield, fracture stresses and strengths, hardness, etc.)
> - "Thermodynamic" (thermodynamic integration, melting temperature, etc.)
> - "Transformation-pathway" (nudged-elastic band, energy maps, minimum-energy-paths, etc.)
> - Are diffusion and viscosity considered transport? What about defect mobilities (point defects, dislocations, grain boundaries)?

Mechanical and Thermodynamic are already families (0076 item 5); the examples are new. Thermodynamic integration is a procedure, a ps `algorithm` used in a computation of task Free energy calculation. The free energy it gives is already an example of Thermodynamic.

A transition path and its barrier are found by a PS computation of task Transition path, e.g. by the nudged elastic band, a ps `algorithm`. The task and the PS settings already say what the computation found and how. A derived entry naming that computation would repeat them, which 0077 rules out.

Transport is defined as "the transport of charge, heat or mass". Diffusion is in; viscosity, the transport of momentum, and the mobility of a dislocation or a grain boundary are not.

## Decision
1. **Mechanical**: "The response to a mechanical load, e.g. elastic constants, a stress-strain response, a tensile, yield or fracture strength, or a hardness". The introduction's examples: elastic constants, stress-strain response, tensile, yield and fracture strengths, hardness.
2. **Thermodynamic**: "Thermodynamic quantities, e.g. free energies, heat capacities, formation energies or a melting temperature". The introduction's examples gain melting temperature. Thermodynamic integration is not listed: it is a procedure, recorded in ps.
3. **Transport**: "The transport of charge, heat, mass or momentum, or the motion of defects under a driving force, e.g. an electrical or thermal conductivity, a diffusion coefficient, a viscosity, or the mobility of a dislocation or a grain boundary". The introduction's examples: electronic and thermal conductivity, diffusion, viscosity, defect mobilities.
4. **No transition-path family.** The introduction says that a result its computation already names needs no derived entry. For example, a transition path and its energy barrier, e.g. a point defect's migration barrier, are found by the nudged elastic band (ps `algorithm`, minimal task Transition path). A property obtained from such results, e.g. a rate from barriers and attempt frequencies, is a derived entry.

## Consequences
- One pull request: schema/derived.yaml (three definitions and the introduction), tests and the regenerated page.
- `type`'s terms do not change, so no record breaks.
