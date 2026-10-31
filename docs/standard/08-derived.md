# 2.7 Derived Property

\* = required property

### `derived-property*`

Details of a quantity related to material behavior computed based on a computational materials science (CMS) calculation covered by the MatCore standard.

**Repeatable:** True

*Values (legacy text):* Contains SubProperties as listed below.

#### `type*`

Kind of physical quantity being computed.

**Repeatable:** False

*Values (legacy text):* String one of the following values that defines the type of the computed derived property: "Electronic" "Electron-phonon interactions" "Linear-response" "Magnetic" "Microscopy, electron" "Microscopy, scanning probe" "NMR" "Optical" "Spectroscopy, core-level" "Spectroscopy, vibrational" "Transport" "X-ray scattering" Other user-specified value if none of the above apply.

#### `description*`

Explanation of the derived property.

**Repeatable:** False

*Values (legacy text):* A string containing an explanation of the specific derived property that was computed.

#### `calculation-method*`

Details regarding an approach used to obtain the derived property. Multiple approaches may be involved in the computation.

**Repeatable:** True

*Values (legacy text):* Contains SubSubProperties as defined in the table below.

##### `description*`

Description of the method used to obtain the derived property.

**Repeatable:** False

*Values (legacy text):* A string containing a human-readable description of the approach and/or algorithm used to compute the derived property.

##### `calculation-parameter`

A parameter associated with the specified calculation method.

**Repeatable:** True

*Values (legacy text):* Contains SubSubSubProperties as defined in the table below.

###### `name*`

The designation of the parameter associated with the specified derived property calculation method.

**Repeatable:** False

*Values (legacy text):* A string containing the name of the calculation parameter.

###### `value*`

The data associated with the calculation parameter.

**Repeatable:** False

*Values (legacy text):* An integer, real, boolean, or string containing the calculation parameter value.

###### `unit*`

A standardized string or identifier that defines the dimension or measurement system of the associated value.

**Repeatable:** False

*Values (legacy text):* A string containing the units of the value in the [GNU unit convention](https://www.gnu.org/software/units/) (or the text "dimensionless").

###### `description`

An explanation of the meaning, source, or purpose of the calculation parameter.

**Repeatable:** False

*Values (legacy text):* A string explaining the computation parameter (e.g. "The spin-spin coupling constant for an NMR spectroscopy calculation").
