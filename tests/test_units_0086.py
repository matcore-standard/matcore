"""Annex U gains the Kinds and units of energy per area, dipole moments, polarizabilities, second-order
susceptibilities, thermal and electrical conductivity and electric current (decision record 0086 item 13)."""
from decimal import Decimal
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
UNITS = yaml.safe_load((ROOT / 'schema/units.yaml').read_text())

# Kind: (QUDT quantity kind or None, QUDT dimension vector)
KINDS = {
    'EnergyPerArea': ('EnergyPerArea', 'A0E0L0I0M1H0T-2D0'),
    'ElectricDipoleMoment': ('ElectricDipoleMoment', 'A0E1L1I0M0H0T1D0'),
    'Polarizability': ('Polarizability', 'A0E2L0I0M-1H0T4D0'),
    'SecondOrderSusceptibility': (None, 'A0E1L-1I0M-1H0T3D0'),
    'ThermalConductivity': ('ThermalConductivity', 'A0E0L1I0M1H-1T-3D0'),
    'ElectricCurrent': ('ElectricCurrent', 'A0E1L0I0M0H0T0D0'),
    'ElectricConductivity': ('ElectricConductivity', 'A0E2L-3I0M-1H0T3D0'),
}
# symbol: (Kind, QUDT unit or None, SI factor)
NEW = {
    'J/m^2': ('EnergyPerArea', 'J-PER-M2', '1'),
    'mJ/m^2': ('EnergyPerArea', 'MilliJ-PER-M2', '1e-3'),
    'eV/angstrom^2': ('EnergyPerArea', None, '1.602176634e1'),
    'e*angstrom': ('ElectricDipoleMoment', None, '1.602176634e-29'),
    'D': ('ElectricDipoleMoment', 'DEBYE', '3.33564095198152e-30'),
    'C*m': ('ElectricDipoleMoment', 'C-M', '1'),
    'C*m^2/V': ('Polarizability', 'C-M2-PER-V', '1'),
    'e*angstrom^2/V': ('Polarizability', None, '1.602176634e-39'),
    'pm/V': ('SecondOrderSusceptibility', None, '1e-12'),
    'm/V': ('SecondOrderSusceptibility', None, '1'),
    'W/(m*K)': ('ThermalConductivity', 'W-PER-M-K', '1'),
    'A': ('ElectricCurrent', 'A', '1'),
    'S/m': ('ElectricConductivity', 'S-PER-M', '1'),
}


def test_new_kinds_carry_their_dimension_and_qudt_anchor():
    """Each new Kind is compatible with its units by its SI dimension vector (Annex U Rule 7); the one with no QUDT
    quantity kind says so rather than borrowing a wrong one."""
    for name, (qudt, dimension) in KINDS.items():
        k = UNITS['kinds'][name]
        assert (k['qudt'], k['dimension']) == (qudt, dimension), name


def test_new_units_have_their_kind_identifier_and_exact_factor():
    """Each unit converts to coherent SI by an exact decimal factor, traced in the pull request (0009, 0086)."""
    for symbol, (kind, qudt, factor) in NEW.items():
        u = UNITS['units'][symbol]
        assert (u['kind'], u['qudt'], u['si_factor']) == (kind, qudt, factor), symbol
    # the debye is 1e-18 statC cm = 1e-21 C m / c, given to 15 significant digits
    assert Decimal(NEW['D'][2]) == round(Decimal('1e-21') / Decimal(299792458), 44)


def test_compound_symbols_may_multiply():
    """A dipole moment is a charge times a length, so a symbol may use * for multiplication, and a denominator of
    several factors is parenthesized (Annex U Rule 2, extended by 0086)."""
    rules = (ROOT / 'docs/standard/annex-u-units.md').read_text()
    assert '`*` for multiplication' in rules and 'in parentheses' in rules
