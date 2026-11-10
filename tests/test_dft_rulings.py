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


def test_dispersion_correction_is_named_apart_from_the_functional():
    """Corrections such as D2, D3 and D4 change results with the same functional, so the correction has its own
    property and the functional's name gives the functional alone (0051)."""
    s = settings()
    names = [p['name'] for p in s['subproperties']]
    assert names.index('dispersion-correction') == names.index('calculation-physics') + 1
    d = sub(s, 'dispersion-correction')
    assert shape(d) == (False, False, 'string', [], 'inapplicable', None)
    assert d['values']['terms'] == ['D2', 'D3', 'D3(BJ)', 'D4', 'TS', 'MBD']
    assert all(f'"{t}"' in d['values']['note'] for t in d['values']['terms'])
    assert d['notes'][0].startswith('Note: Give it when `calculation-physics` lists Van der Waals')
    name_note = ' '.join(sub(s, 'xc-functional', 'name')['values']['note'].split())
    assert 'VdW-corrections' not in name_note
    assert name_note.endswith('Give the functional alone, without a dispersion correction (e.g. PBE, not '
                              'PBE-D3); the correction is given in dispersion-correction.')


WIDTH_NOTE = 'Note: Give the width as an energy; for Fermi-Dirac smearing it is k<sub>B</sub>T, where T is the electronic temperature. It is not a temperature imposed on the simulated system, which is given in `conditions`.'


def test_smearing_width_is_not_an_imposed_temperature():
    """A Fermi-Dirac width is an electronic temperature, which a writer could mistake for a thermostat's
    temperature in conditions (0052)."""
    s = settings()
    width = next(w for c in s['subproperties'] if c['name'] in ('k-point-mesh', 'smearing')
                 for w in c['subproperties'] if w['name'] in ('smearing-width', 'width'))
    assert width['notes'] == [WIDTH_NOTE]


def test_smearing_leaves_the_k_point_mesh():
    """Smearing assigns occupations and applies where there is no mesh, so it is its own container after the
    mesh, holding the former smearing-type, smearing-width and smearing-parameter (0053)."""
    s = settings()
    names = [p['name'] for p in s['subproperties']]
    assert names.index('smearing') == names.index('k-point-mesh') + 1
    assert [p['name'] for p in sub(s, 'k-point-mesh')['subproperties']] == ['type', 'number-of-points', 'shift']
    assert [p['name'] for p in sub(s, 'smearing')['subproperties']] == ['type', 'width', 'parameter']
    assert 'smearing-' not in (ROOT / 'schema/dft.yaml').read_text()


def test_dft_introduction_uses_current_names():
    """The introduction names the properties as 0018 renamed them and says how settings blocks work (0054)."""
    intro = yaml.safe_load(open(ROOT / 'schema/dft.yaml'))['introduction'].strip()
    assert intro == 'The metadata for density functional theory (DFT) data (MatCore-DFT) is tabulated below. This includes the level of theory (exchange-correlation functional, core-electron treatment and wavefunction representation) and associated parameters. The properties are given in settings blocks, each naming the DFT computations it describes. (Note: This standard inherits the metadata in the minimal MatCore standard, adding the properties below.)'


def test_lapw_basis_cutoff_is_rkmax():
    """LAPW codes set the basis by the dimensionless RKmax, which cannot be turned into an energy without the
    muffin-tin radius; the energy cutoff serves plane waves, and LAPW only when given as an energy (0057)."""
    w = sub(settings(), 'wavefunction-representation')
    names = [p['name'] for p in w['subproperties']]
    assert names.index('lapw-basis-cutoff') == names.index('kinetic-energy-cutoff') + 1
    c = sub(w, 'lapw-basis-cutoff')
    assert shape(c) == (False, False, 'float', [], 'dimensionless', None) and c['values'] == {'minimum': 0}
    assert 'subproperties' not in c and 'RKmax' in c['description']
    assert sub(w, 'kinetic-energy-cutoff')['description'].startswith(
        'For type "Plane waves", or for "LAPW" when the code takes the cutoff as an energy,')
