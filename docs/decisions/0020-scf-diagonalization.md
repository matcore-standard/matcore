# 0020 — Electronic diagonalization method

Date: 2026-11-06. Status: accepted. Decided by: Ellad Tadmor (committee decision).

## Context
Community feedback: "The standard currently appears to omit information about the electronic diagonalization approach used during calculations. Including this metadata would improve reproducibility. Examples include conjugate-gradient diagonalization, Davidson methods, RMM-DIIS, and related approaches."

dft `self-consistent-field-convergence` › `method` lists Simple mixing, Pulay mixing, Blocked Davidson, DIIS and BFGS. Blocked Davidson is a diagonalization method, not a density mixing scheme; BFGS is a quasi-Newton optimizer, while the quasi-Newton density mixing scheme in common use is Broyden mixing.

Committee decision: rename `method` to `method-density`; create a new property `method-diagonalization` with conjugate gradient, Davidson method, RMM-DIIS, Car-Parrinello and Lanczos, adding other important methods if missing.

## Decision
1. **`method-density`** (renamed from `method`; optional, not repeatable, description unchanged): open terms Simple mixing, Pulay mixing, DIIS, Broyden mixing. Blocked Davidson moves to `method-diagonalization` (as Davidson method); BFGS is replaced by Broyden mixing. The note keeps the baseline's definition of DIIS.
2. **`method-diagonalization`** (new; optional, repeatable, since codes combine methods): a scalar string, description "The method used to obtain the Kohn-Sham orbitals at each step of the self-consistent loop.", open terms in alphabetical order: Car-Parrinello, Chebyshev filtering, Conjugate gradient, Davidson method, Direct diagonalization, Lanczos, LOBPCG, RMM-DIIS. Chebyshev filtering, Direct diagonalization and LOBPCG are added to the committee's list. The note: '"Car-Parrinello" – Fictitious dynamics of the electronic orbitals, which replaces diagonalization. "Chebyshev filtering" – Subspace iteration with Chebyshev polynomial filters. "Davidson method" – Including blocked variants. "Direct diagonalization" – A dense eigensolver applied to the full Hamiltonian matrix (e.g. LAPACK, ScaLAPACK). "LOBPCG" – Locally Optimal Block Preconditioned Conjugate Gradient. "RMM-DIIS" – Residual Minimization Method with Direct Inversion in the Iterative Subspace.'
3. **Order** of `self-consistent-field-convergence`'s subproperties: `method-density`, `method-diagonalization`, `tolerance`.

## Consequences
- One pull request fills `self-consistent-field-convergence` with 0019. examples/dft.xml has no such element and needs no change.
- The rename breaks instances written against 0.5.0 that give `method`.
