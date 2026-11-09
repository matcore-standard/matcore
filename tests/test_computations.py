"""Computations and structures carry labels, and computations name what they use (decision record 0046)."""
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'
TASKS = ['Single point', 'Optimization', 'Dynamics', 'Sampling', 'Free energy calculation', 'Training',
         'Property calculation']
ROLES = ['Interaction model', 'Initial configuration', 'Starting point', 'Training data', 'Parameters',
         'Source data']
UNIQUE = 'Note: A label is unique among all labels of structures and computations in the record.'


def section(key):
    """Return the parsed section file.

    key (str): the section key, e.g. 'minimal'.
    """
    return yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))


def top(key, name):
    """Return a top-level property of a section.

    key (str): the section key; name (str): the property's name.
    """
    return next(p for p in section(key)['properties'] if p['name'] == name)


def sub(p, name):
    """Return the subproperty of p with the given name.

    p (dict): property entry; name (str): the subproperty's name.
    """
    return next(s for s in p['subproperties'] if s['name'] == name)


def shape(p):
    """Return the fields that fix a leaf's form.

    p (dict): property entry.
    """
    return (p['required'], p['repeatable'], p['type'], p['extent'], p['kind'], p['recommended-unit'])


@pytest.mark.parametrize('owner', ['structure', 'computation'])
def test_structures_and_computations_have_a_label_first(owner):
    """A label lets a computation, or a method section added later, refer to a structure or computation, so it
    is required, written like a property name, and unique in the record (0046 items 1, 2)."""
    label = top('minimal', owner)['subproperties'][0]
    assert label['name'] == 'label'
    assert shape(label) == (True, False, 'string', [], 'inapplicable', None)
    assert label['values']['pattern'] == NAME_PATTERN
    assert label['notes'] == [UNIQUE]


def test_computation_members_and_order():
    """A computation says what its calculations do, which structures they model and which other computations
    they use; conditions are optional and interaction-model is gone (0046 items 2-4)."""
    c = top('minimal', 'computation')
    assert [s['name'] for s in c['subproperties']] == [
        'label', 'method-class', 'method', 'task', 'structure', 'input', 'conditions', 'software']
    assert c['description'] == ('A group of calculations in the dataset that share one method and one set of '
                                'settings, e.g. the DFT single points of a training set.')
    assert not sub(c, 'conditions')['required']
    assert sub(c, 'conditions')['description'].endswith(
        'Omitted when no condition is imposed, e.g. for a single point or a training computation.')


def test_task_terms_are_defined():
    """What a computation does is a required open term, each defined in the note (0046 item 2)."""
    t = sub(top('minimal', 'computation'), 'task')
    assert shape(t) == (True, False, 'string', [], 'inapplicable', None)
    assert t['values']['terms'] == TASKS
    assert all(f'"{term}" –' in t['values']['note'] for term in TASKS)


def test_input_names_a_computation_and_its_role():
    """The role sits on the link, since one computation can be both published data and another's interaction
    model (0046 item 2)."""
    i = sub(top('minimal', 'computation'), 'input')
    assert (i['required'], i['repeatable'], i['type']) == (False, True, None)
    assert [s['name'] for s in i['subproperties']] == ['computation', 'role']
    assert shape(sub(i, 'computation')) == (True, False, 'string', [], 'inapplicable', None)
    role = sub(i, 'role')
    assert shape(role) == (True, False, 'string', [], 'inapplicable', None)
    assert role['values']['terms'] == ROLES
    assert all(f'"{term}" –' in role['values']['note'] for term in ROLES)
    assert i['notes'] == ['Note: Give an input only where the data of this computation cannot be understood '
                          'without it. A record describes the dataset; it does not record the order of the '
                          'calculations or how to repeat them.']
    s = sub(top('minimal', 'computation'), 'structure')
    assert shape(s) == (False, True, 'string', [], 'inapplicable', None)


def test_method_terms_include_tb_ms_and_pim():
    """Tight binding solves for electrons; molecular statics relaxes particles with another computation's
    forces; a particle interaction model supplies energies and forces without solving for a wavefunction or
    density (0046 items 4, 5)."""
    m = sub(top('minimal', 'computation'), 'method')
    assert {k: c['terms'] for k, c in m['values']['cases'].items()} == {
        'Electronic': ['CC', 'QMC', 'DFT', 'MBPT', 'TB'], 'Atomistic': ['MC', 'MD', 'MS', 'PIM'],
        'Mesoscopic': ['DDD', 'KMC', 'CGMD', 'PIM'], 'Continuum': ['PF'], 'Data-driven': ['ML']}
    note = m['values']['note']
    assert '"TB" – Tight Binding' in note and '"MS" – Molecular Statics' in note
    assert 'without solving for a wavefunction or an electron density' in note
    assert m['notes'] == ['Note: Give the method of the calculations in this computation. When they use energies '
                          'and forces from another method, describe that method as a computation of its own and '
                          'name it in `input` with the role Interaction model.']
    assert 'interaction-model' not in open(ROOT / 'schema/minimal.yaml').read()


def test_software_can_be_an_interaction_model():
    """A KIM model or potential file is the software of a PIM computation (0046 item 6)."""
    role = sub(sub(top('minimal', 'computation'), 'software'), 'role')['values']
    assert role['terms'] == ['Calculation method', 'Interaction model', 'Script', 'Simulation code',
                             'Workflow framework']
    assert '"Interaction model" –' in role['note']


def test_dft_properties_sit_in_settings_naming_computations():
    """A dft block names the DFT computations it describes, so several computations can have their own
    settings (0046 item 7)."""
    props = section('dft')['properties']
    assert [p['name'] for p in props] == ['settings']
    s = props[0]
    assert (s['required'], s['repeatable'], s['type']) == (True, True, None)
    assert s['description'] == 'Settings shared by the computations named in it.'
    assert [c['name'] for c in s['subproperties']] == [
        'computation', 'xc-functional', 'core-electron-treatment', 'wavefunction-representation',
        'calculation-physics', 'k-point-mesh', 'self-consistent-field-convergence', 'relaxation-tolerance-energy',
        'relaxation-tolerance-forces', 'comment']
    c = sub(s, 'computation')
    assert shape(c) == (True, True, 'string', [], 'inapplicable', None)
    assert c['description'] == 'The label of a computation these settings apply to.'


def test_example_labels_are_unique_and_every_reference_resolves():
    """Every label in the minimal example is unique, every structure, input and dft settings block names a
    label of the right kind, and the dft block names a DFT computation (0046 items 1, 2, 7)."""
    load = lambda k: json.loads((ROOT / f'examples/{k}.json').read_text(encoding='utf-8'))[k]
    minimal, dft = load('minimal'), load('dft')
    structures = [s['label'] for s in minimal['structure']]
    computations = {c['label']: c for c in minimal['computation']}
    every = structures + list(computations)
    assert len(every) == len(set(every))
    for c in computations.values():
        assert set(c.get('structure', [])) <= set(structures)
        assert {i['computation'] for i in c.get('input', [])} <= set(computations)
    named = [label for block in dft['settings'] for label in block['computation']]
    assert named and all(computations[n]['method'] == 'DFT' for n in named)
