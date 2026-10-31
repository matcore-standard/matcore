# 2.2 DFT

\* = required property

### `xc-functional*`

Approximation used to describe the electron exchange and electron correlation energies

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `type*`

The mathematical form of the exchange-correlation functional.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "LDA" – Local Density Approximation "GGA" – Generalized Gradient Approximation "Meta GGA" – Extension to GGA including dependence on Laplacian of electron density "Hybrid" – An approximation for the exchange-correlation (XC) functional that includes a portion of the exact XC from Hartree–Fock theory or machine learning with the rest coming from other sources (ab initio or empirical). "ML" – Machine learning based functional Other user-specified value if none of the above apply.

#### `description`

Explanatory text providing more information about the type of the exchange-correlation method used including any relevant identifying information.

**Repeatable:** False

*Values (legacy text):* A string containing more information about the exchange-correlation type. Examples of possible content by type: LDA: Common parameterizations: VMN, PW92, etc. GGA: Typical choices are PW91, PBE, rPBE, revPBE, BLYP, etc. Meta GGA: Specific named examples include TPSS, SCAN, M06, etc. Hybrid: B3LYP, PBE0, HSE03, HSE06, NeuralXC, DeePKS, … ML: DM21, NNLDA, NNGGA, CIDER, etc. others: BEEF, VdW-corrections (added on top of XC, e.g., D2, D3, D4), etc. LibXC designation: LibXC:LDA_C_GK72 (include source as prefix)

#### `xc-parameter`

A fixed variable associated with the specified exchange-correlation functional method.

**Repeatable:** True

*Values (legacy text):* Contains SubSubProperties as defined in the table below.

##### `name*`

The designation of the exchange-correlation parameter.

**Repeatable:** False

*Values (legacy text):* A string containing the name of an exchange-correlation parameter.

##### `value*`

The data associated with the exchange-correlation parameter.

**Repeatable:** False

*Values (legacy text):* An integer, real, boolean, or string containing the parameter value.

##### `unit*`

A standardized string or identifier that defines the dimension or measurement system of the associated value.

**Repeatable:** False

*Values (legacy text):* A string containing the units of the value in the [GNU unit convention](https://www.gnu.org/software/units/) (or the text "dimensionless").

##### `description`

An explanation of the meaning, source, or purpose of the parameter.

**Repeatable:** False

*Values (legacy text):* A string explaining the exchange-correlation parameter. This can be the mixing parameter for a hybrid exchange-correlation, or other method-specific parameters.

### `core-electron-model*`

Model of the electrons used in the calculation.

**Repeatable:** False

*Values (legacy text):* Contains SubProperties as listed below.

#### `type*`

The method used to model the electrons.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "All Electron" – All of the electrons in an atom are modeled explicitly. "LAPW" – "Linearized Augmented Plane Wave" "Pseudopotential" – Valence electrons are treated explicitly, and core electrons are modeled by a simplified potential. "PAW" – Projector Augmented Wave Other user-specified value if none of the above apply.

#### `pseudopotential`

For type "Pseudopotential", or type "PAW", additional information about the pseudopotentials.

**Repeatable:** True

*Values (legacy text):* Contains SubSubProperties as defined in the table below.

##### `name*`

The name of the pseudopotential.

**Repeatable:** False

*Values (legacy text):* A string containing the pseudopotential name.

##### `type*`

The physical form of the pseudopotential.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "Norm conserving" "Ultrasoft" Other user-specified value if none of the above apply.

##### `description`

Explanatory text about the pseudopotential including any relevant identifying information.

**Repeatable:** False

*Values (legacy text):* A string containing the pseudopotential description.

##### `number-of-valence-electrons*`

The number of electrons treated explicitly.

**Repeatable:** False

*Values (legacy text):* An integer containing the number of valence electrons.

*Standard units (legacy text):* dimensionless

##### `repository`

The database from which the pseudopotential was obtained.

**Repeatable:** False

*Values (legacy text):* String containing the name of the repository.

##### `version`

The version of the pseudopotential.

**Repeatable:** False

*Values (legacy text):* A string containing the pseudopotential version (e.g. "6.3.1")

##### `doi`

The digital object identifier (DOI) for the pseudopotential.

**Repeatable:** False

*Values (legacy text):* A string containing the pseudopotential DOI.

##### `unique-identifier`

A hash or other token providing a digital signature for the pseudopotential.

**Repeatable:** False

*Values (legacy text):* A string containing the pseudopotential identifier (e.g. a SHA256 hash for a VASP pseudopotential).

### `valence-electron-model*`

The elementary functions used for expanding electronic wave functions.

**Repeatable:** False

*Values (legacy text):* Contains SubProperties as listed below.

#### `type*`

The choice of a basis set to expand electronic wave functions.

**Repeatable:** True

*Values (legacy text):* String containing one of the following values: "Plane waves" "LAPW" – "Linearized Augmented Plane Wave" "Localized orbitals" "PAW" Other user-specified value if none of the above apply.

#### `localized-orbital-basis-set`

For type "Localized orbitals", additional information about the localized orbital basis set.

**Repeatable:** True

*Values (legacy text):* Contains SubSubProperties as defined in the table below.

##### `type*`

The designation of the set of orbital functions used for expanding electronic wave functions.

**Repeatable:** False

*Values (legacy text):* String containing the basis set name (e.g. "6-31G", "DZP", etc.).

##### `repository`

The database from which the localized-orbital basis set was obtained.

**Repeatable:** False

*Values (legacy text):* String containing the name of the repository.

##### `version`

The version of the localized-orbital basis set.

**Repeatable:** False

*Values (legacy text):* A string containing the localized-orbital basis set version.

##### `doi`

The digital object identifier (DOI) for the localized-orbital basis set.

**Repeatable:** False

*Values (legacy text):* A string containing the pseudopotential DOI.

##### `unique-identifier`

A hash or other token providing a digital signature for the localized-orbital basis set .

**Repeatable:** False

*Values (legacy text):* A string containing the localized-orbital basis set identifier.

#### `kinetic-energy-cutoff`

For type not "Localized orbitals", the maximum kinetic energy of the plane waves included in the calculation of wave functions.

**Repeatable:** False

*Values (legacy text):* Real number containing the kinetic energy cutoff.

*Standard units (legacy text):* electron Volt (eV)

#### `charge-density-cutoff`

For type not "Localized orbitals", the energy value used to truncate the plane wave expansion of the electron charge density,

**Repeatable:** False

*Values (legacy text):* Real number containing the charge density cutoff.

*Standard units (legacy text):* electron Volt (eV)

### `calculation-physics`

Additional phenomena included beyond the standard DFT calculation.

**Repeatable:** True

*Values (legacy text):* String containing one of the following values: "Relativistic effects" "Spin polarization" "Noncollinear spin polarization" "On-site correlation" (e.g. DFT+U) "Van der Waals" Other user-specified value if none of the above apply.

### `k-point-mesh`

For periodic systems, a grid of points sampled within the Brillouin zone, used to approximate integrals and calculate electronic properties by discretizing the wavefunction across reciprocal space.

**Repeatable:** False

*Values (legacy text):* Contains SubProperties as listed below.

#### `type*`

The choice of how k-points are distributed on the mesh.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "Monkhorst-Pack" "Gamma centered" "Irregular" Other user-specified value if none of the above apply.

#### `number-of-points`

How many k-points are included along each reciprocal lattice vector.

**Repeatable:** False

*Values (legacy text):* Ordered list of three integer numbers containing the number k-points along the three reciprocal lattice vector directions.

*Standard units (legacy text):* dimensionless

#### `k-point-spacing`

Separation between k-points along each reciprocal lattice vector direction.

**Repeatable:** False

*Values (legacy text):* Real number containing the k-point spacing.

*Standard units (legacy text):* 1/angstrom (1/Å)

#### `shift`

Translation of the k-point mesh along the reciprocal lattice vector directions.

**Repeatable:** False

*Values (legacy text):* Ordered list of three real numbers containing the shifts along the three reciprocal lattice vector directions.

*Standard units (legacy text):* 1/angstrom (1/Å)

#### `smearing-type`

The choice of method for assigning fractional occupancies of electronic states and/or facilitating reciprocal space integrations.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "None" "None - tetrahedron" "None - Blöchl-corrected tetrahedron" "Gaussian" "Fermi" "Methfessel-Paxton" Other user-specified value if none of the above apply.

#### `smearing-width`

A parameter that controls the broadening of the electron energy levels near the Fermi level.

**Repeatable:** False

*Values (legacy text):* Real number containing the smearing width.

*Standard units (legacy text):* electron Volt (eV)

#### `methfessel-paxton-order`

For smearing-type "Methfessel-Paxton", level of polynomial approximation used in the Methfessel-Paxton smearing method

**Repeatable:** False

*Values (legacy text):* Integer containing the Methfessel-Paxton order.

*Standard units (legacy text):* Dimensionless

### `self-consistent-field-convergence`

Method and termination criteria defining the precision of self-consistent solution of the Kohn-Sham equations.

**Repeatable:** False

*Values (legacy text):* Contains SubProperties as listed below.

#### `method`

The self-consistent field mixing and/or extrapolation scheme for the iterative solution of the Kohn-Sham equations.

**Repeatable:** False

*Values (legacy text):* String containing one of the following values: "Simple mixing" "Pulay mixing" "Blocked Davidson" "DIIS" – Direct Inversion in the Iterative Subspace "BFGS" – Broyden–Fletcher–Goldfarb–Shanno algorithm Other user-specified value if none of the above apply.

#### `tolerance*`

Convergence criterion for the self-consistent loop.

**Repeatable:** False

*Values (legacy text):* Real number containing the convergence tolerance

*Standard units (legacy text):* electron Volt (eV)

### `relaxation-tolerance-energy`

Total energy convergence criterion for atomic relaxation.

**Repeatable:** False

*Values (legacy text):* Real number containing the convergence tolerance

*Standard units (legacy text):* electron Volt (eV)

### `relaxation-tolerance-forces`

Maximum force convergence criterion for atomic relaxation.

**Repeatable:** False

*Values (legacy text):* Real number containing the convergence tolerance

*Standard units (legacy text):* electron Volt (eV/Å)

### `comment`

Additional information on the DFT calculation. For example, non-self-consistent constraints, such as details about imposed state occupation or moment freezing.

**Repeatable:** True

*Values (legacy text):* String containing the calculation comments.
