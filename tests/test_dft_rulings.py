"""The dft rulings that followed the minimal-dft analysis (decision records 0047-0059)."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def settings():
    """Return the dft settings block."""
    return yaml.safe_load(open(ROOT / 'schema/dft.yaml'))['properties'][0]


def sub(p, *names):
    """Return the property reached from p through the named subproperties.

    p (dict): property entry; names (str): subproperty names, outermost first.
    """
    for name in names:
        p = next(s for s in p['subproperties'] if s['name'] == name)
    return p


def shape(p):
    """Return the fields that fix a leaf's form.

    p (dict): property entry.
    """
    return (p['required'], p['repeatable'], p['type'], p['extent'], p['kind'], p['recommended-unit'])


def test_pseudopotential_and_basis_set_name_their_species():
    """A pseudopotential or PAW dataset is made for one element, and basis sets are often chosen per element,
    so each says which species of the formula it serves; a basis set named once for all species omits it
    (0047)."""
    pp = sub(settings(), 'core-electron-treatment', 'pseudopotential-or-paw', 'species')
    assert shape(pp) == (True, False, 'string', [], 'inapplicable', None)
    assert pp['values']['examples'] == ['Si', 'Ja']
    basis = sub(settings(), 'wavefunction-representation', 'localized-orbital-basis-set', 'species')
    assert shape(basis) == (False, True, 'string', [], 'inapplicable', None)
    assert basis['notes'] == ['Note: Give the species this basis set is used for. Omit it when one basis set is '
                              'used for every species.']
