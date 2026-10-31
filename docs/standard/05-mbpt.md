# 2.4 MBPT

\* = required property

### `mbpt-method*`

The many-body perturbation theory (MBPT) approach used and associated settings.

**Repeatable:** False

*Values (legacy text):* Contains SubProperties as listed below.

#### `type*`

The nature of the MBPT calculation performed.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "GW" "BSE" "GW/BSE" Other user-specified value if none of the above apply.

#### `self-consistency*`

Specifies the level of iterative updating applied to the Green's function (*G*), the screened Coulomb interaction (*W*), or the excitonic Hamiltonian during the calculation. This property identifies whether the MBPT equations are solved in a 'one-shot' perturbative manner or through an iterative cycle where the electronic or excitonic quasiparticle states are updated to reach a self-consistent solution.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values depending on the variant of the GW, BSE, or GW/BSE approach used: "G0W0" – One-shot calculation; the *G* and *W *are constructed using the starting eigenvalues and wavefunctions. "GW0" – Only the Green's function *G* is updated iteratively, while *W *remains fixed at the *W0 *level "G0W" – Only the screened interaction *W *is updated iteratively, while *G *remains fixed at *G0* "scGW" – Fully self-consistent GW; both*G* and *W* are updated iteratively until the quasiparticle energies and/or wavefunctions converge "QSGW" – Quasiparticle self-consistent GW; the starting potential is updated to provide the optimal independent particle basis for the GW expansion "BSE0" – One-shot BSE; the excitonic Hamiltonian is built once using fixed GW quasiparticle energies and screening (*W*) "scBSE" – Self-consistent BSE; internal refinement of the kernel or energies within the BSE process "evGW+BSE" – Eigenvalue-only self-consistent GW (evGW) used as the starting point for a subsequent BSE calculation "scGW+BSE" – The BSE is solved using the results of a fully self-consistent GW calculation Other user-specified value if none of the above apply.

### `starting-point*`

The density functional theory (DFT) exchange-correlation functional used to generate Kohn-Sham wavefunctions and eigenvalues for the Green's function and the screened Coulomb interaction.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "LDA" "GGA" "Meta GGA" "Hybrid GGA" "DFT+U" Other user-specified value if none of the above apply.

### `dielectric-matrix*`

Information on the dielectric matrix used to compute the screened Coulomb interaction *W*.

**Repeatable:** False

*Values (legacy text):* Contains SubProperties as listed below.

#### `planewave-basis-cutoff*`

For a planewave code, the basis set cutoff employed for the dielectric matrix. This is the same as the kinetic energy cutoff.

**Repeatable:** False

*Values (legacy text):* A real number containing the cutoff.

*Standard units (legacy text):* Rydberg (Ry)

> Note:Specify either "planewave-basis-cutoff" or "local-orbital-basis-set", but not both.

#### `local-orbital-basis-set*`

For local orbital codes, the name of the basis set .

**Repeatable:** False

*Values (legacy text):* A string containing the name of the atomic orbital basis. (e.g. "cc-pV6Z").

> Note:Specify either "basis-cutoff-planewave" or "local-orbital-basis-set", but not both.

#### `frequency`

The method used to handle the frequency dependence of the Green's function, the screened Coulomb interaction, and their product.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "Hybertsen-Louie" "Godby-Needs" "Full frequency real axis" "Full frequency imaginary axis" "Contour deformation" "Spacetime" Other user-specified value if none of the above apply.

#### `response-basis-size`

For sum-over-states methods, the number of bands used in the sum. For linear-response methods, the number of dielectric eigenvalues.

**Repeatable:** False

*Values (legacy text):* One integer containing the number of bands or eigenvalues.

*Standard units (legacy text):* dimensionless

#### `q-points*`

Brillouin zone grid used for sampling the dielectric matrix.

**Repeatable:** False

*Values (legacy text):* Ordered list of 3 integer numbers containing the number points along the three reciprocal lattice vector directions.

*Standard units (legacy text):* dimensionless

#### `coulomb-truncation`

Method used to eliminate long-range Coulomb interactions between periodic replicas in supercell calculations.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "Ismail-Beigi" "Rozzi" "Spencer-Alavi" Other user-specified value if none of the above apply.

### `gw-bands`

Number of bands for which the GW correction is evaluated.

**Repeatable:** False

*Values (legacy text):* One integer specifying how many bands are corrected, counting from the bottom of the valence bands.

*Standard units (legacy text):* dimensionless

### `bse-hamiltonian`

A collective descriptor for the parameters defining the construction, dimensionality, and solution method of the effective excitonic Bethe-Salpeter Hamiltonian that is being solved in a BSE calculation. It characterizes the Hilbert space size and the physical constraints (momentum and spin) applied during the diagonalization

**Repeatable:** False

*Values (legacy text):* Contains SubProperties as listed below.

#### `number-valence-bands`

Number of valence bands included in the BSE Hamiltonian.

**Repeatable:** False

*Values (legacy text):* One integer specifying how many valence bands are corrected, counting from the valence band top.

*Standard units (legacy text):* dimensionless

#### `number-conduction-bands`

Number of conduction bands included in the BSE Hamiltonian.

**Repeatable:** False

*Values (legacy text):* One integer specifying how many bands are corrected, counting from the conduction band bottom.

*Standard units (legacy text):* dimensionless

#### `k-point-mesh`

Brillouin zone grid used for building the BSE Hamiltonian.

**Repeatable:** False

*Values (legacy text):* Ordered list of 3 integer numbers containing the number points along the reciprocal lattice vector directions.

*Standard units (legacy text):* dimensionless

#### `exciton-momentum`

Crystal momentum of the exciton in the BSE calculation.

**Repeatable:** False

*Values (legacy text):* Ordered list of 3 real values containing the crystal momentum, e.g. [0.5,0.5,1.0].

*Standard units (legacy text):* Reciprocal lattice units (2π/a)

#### `exciton-multiplicity`

Specification whether the BSE calculation is performed for singlet or triplet excitons.

**Repeatable:** False

*Values (legacy text):* string containing one of the values: "Singlet" "Triplet" Other user-specified value if none of the above apply.

#### `diagonalization`

Approximation method used to diagonalize the BSE Hamiltonian.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "Tamm-Dancoff" "Full diagonalization" Other user-specified value if none of the above apply.

#### `number-lowest-eigenvalues`

Number of lowest eigenvalues computed by solving the BSE Hamiltonian.

**Repeatable:** False

*Values (legacy text):* One integer containing the number of BSE eigenvalues.

*Standard units (legacy text):* dimensionless

### `bse-kernel-truncation`

Method used to eliminate long-range Coulomb interactions between periodic replicas in the BSE Coulomb kernel.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "Ismail-Beigi" "Rozzi" "Spencer-Alavi" Other user-specified value if none of the above apply.
