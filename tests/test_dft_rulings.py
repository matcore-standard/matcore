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


def test_relaxation_has_a_stress_tolerance_and_the_tolerances_serve_optimization():
    """A cell relaxation stops when the stress is near its target, the stress imposed in conditions; the
    three tolerances mean something only for a computation whose task is Optimization (0048)."""
    s = settings()
    names = [p['name'] for p in s['subproperties']]
    assert names.index('relaxation-tolerance-stress') == names.index('relaxation-tolerance-forces') + 1
    stress = sub(s, 'relaxation-tolerance-stress')
    assert (stress['required'], stress['repeatable']) == (False, False)
    assert stress['description'] == ('Maximum stress convergence criterion for cell relaxation, relative to the '
                                     'stress imposed in `conditions`.')
    v = sub(stress, 'value')
    assert (v['type'], v['extent'], v['kind'], v['recommended-unit'], v['values']) == (
        'float', [], 'Pressure', 'GPa', {'minimum': 0})
    for name in ('relaxation-tolerance-energy', 'relaxation-tolerance-forces', 'relaxation-tolerance-stress'):
        assert sub(s, name)['notes'][-1] == "Note: Give it when the computation's task is Optimization.", name
