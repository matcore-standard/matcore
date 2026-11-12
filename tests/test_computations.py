"""Computations and structures carry labels, and computations name what they use (decision record 0046)."""
import json
import re
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
        'label', 'method-class', 'method', 'task', 'structure-label', 'input', 'conditions', 'software']
    assert c['description'] == ('A group of calculations in the dataset that share one method and one set of '
                                'settings, e.g. the DFT single points of a training set.')
    assert not sub(c, 'conditions')['required']
    assert sub(c, 'conditions')['description'].endswith(
        'Omitted when no condition is imposed, e.g. for a single point or a training computation.')


STAGES_NOTE = (
    'Note: A simulation run in stages, e.g. heating, equilibration and a quench, is described as one computation '
    'for each stage whose method, settings or conditions differ and whose data the dataset contains or depends on. '
    'Each stage names the stage it continues from in `input` with the role Initial configuration, which carries '
    'over the final state of that stage, e.g. positions, velocities and the cell. These links give the order of '
    'the stages; the order of the entries in the record does not. A condition that changes within one stage, e.g. '
    "a temperature ramp, is given in that stage's `conditions` as entries with a qualifier. The full protocol, "
    'with its control flow and complete inputs, belongs to the provenance record of a workflow manager (§1.2).')


def test_a_staged_simulation_is_a_chain_of_computations():
    """A reader of a repeatable computation asks how stages are ordered and what carries over between them; the
    answer is the input links, not a protocol object, and the role says the state carries over (0063)."""
    c = top('minimal', 'computation')
    assert c['notes'] == [STAGES_NOTE]
    role = sub(sub(c, 'input'), 'role')['values']['note']
    assert ('"Initial configuration" – The configurations this computation starts from, with the state carried '
            'over from that computation, e.g. velocities;') in role


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
    assert [s['name'] for s in i['subproperties']] == ['computation-label', 'role']
    assert shape(sub(i, 'computation-label')) == (True, False, 'string', [], 'inapplicable', None)
    role = sub(i, 'role')
    assert shape(role) == (True, False, 'string', [], 'inapplicable', None)
    assert role['values']['terms'] == ROLES
    assert all(f'"{term}" –' in role['values']['note'] for term in ROLES)
    assert i['notes'] == ['Note: Give an input only where the data of this computation cannot be understood '
                          'without it. A record describes the dataset; it does not record the order of the '
                          'calculations or how to repeat them.']
    s = sub(top('minimal', 'computation'), 'structure-label')
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
        'computation-label', 'xc-functional', 'core-electron-treatment', 'wavefunction-representation',
        'calculation-physics', 'initial-magnetic-moment', 'dispersion-correction', 'k-point-mesh', 'smearing',
        'self-consistent-field-convergence', 'relaxation-tolerance-energy',
        'relaxation-tolerance-forces', 'relaxation-tolerance-stress', 'comment']
    c = sub(s, 'computation-label')
    assert shape(c) == (True, True, 'string', [], 'inapplicable', None)
    assert c['description'] == 'The label of a computation these settings apply to.'


def test_a_property_holding_a_label_is_named_for_it():
    """A property whose value is the label of a structure or computation is named for that label, so it is never
    mistaken for the container it refers to (0062)."""
    def walk(props):
        """Yield every property entry below and including props.

        props (list): property entries of a section file.
        """
        for p in props:
            yield p
            yield from walk(p.get('subproperties') or [])
    found = {(k, p['name']) for k in ['minimal', 'dft', 'pim', 'ps', 'mbpt', 'ml', 'pf', 'derived']
             for p in walk(section(k)['properties'])
             if p['description'].startswith(('The label of a structure', 'The label of a computation',
                                             'The label of that computation'))}
    assert found == {('minimal', 'structure-label'), ('minimal', 'computation-label'),
                     ('dft', 'computation-label'), ('pim', 'computation-label'), ('ps', 'computation-label')}


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
        assert set(c.get('structure-label', [])) <= set(structures)
        assert {i['computation-label'] for i in c.get('input', [])} <= set(computations)
    named = [label for block in dft['settings'] for label in block['computation-label']]
    assert named and all(computations[n]['method'] == 'DFT' for n in named)


TITLES = {'minimal': '2.1 Minimal MatCore Metadata', 'dft': '2.2 Density Functional Theory (DFT) Metadata',
          'pim': '2.3 Particle Interaction Model (PIM) Metadata', 'ps': '2.4 Particle Simulation (PS) Metadata',
          'mbpt': '2.5 Many-Body Perturbation Theory (MBPT) Metadata', 'ml': '2.6 Machine Learning (ML) Metadata',
          'pf': '2.7 Phase Field (PF) Metadata', 'derived': '2.8 Derived Property Metadata'}
PAGES = {'minimal': '02-minimal.md', 'dft': '03-dft.md', 'pim': 'pim.md', 'ps': 'ps.md', 'mbpt': '05-mbpt.md',
         'ml': '06-ml.md', 'pf': '07-pf.md', 'derived': '08-derived.md'}


def test_sections_are_numbered_with_pim_before_ps():
    """pim serves ps, so it comes first; the other sections move down one (0046, settled 2026-11-09); 2.4 is
    Particle Simulation (0061)."""
    assert {k: section(k)['title'] for k in TITLES} == TITLES


def test_pages_keep_their_addresses():
    """Renumbered pages keep their file names, so links to them still work; pim's page is pim.md, ps's ps.md
    (0061), and the menu lists the sections in their numbered order (0046, settled 2026-11-09)."""
    import sys
    sys.path.insert(0, str(ROOT / 'scripts'))
    import build_docs
    assert build_docs.PAGES == PAGES and list(build_docs.PAGES) == list(TITLES)
    nav = (ROOT / 'mkdocs.yml').read_text()
    positions = [nav.index(f'standard/{page}') for page in PAGES.values()]
    assert positions == sorted(positions)


def test_pim_holds_the_model_properties_moved_from_md():
    """The particle model's properties describe the interaction as evaluated, so they leave md for pim, with
    particle-style repeatable for models with two kinds of particle (0046 item 8, amended 2026-11-09)."""
    props = section('pim')['properties']
    assert [p['name'] for p in props] == ['settings']
    s = props[0]
    assert (s['required'], s['repeatable']) == (True, True)
    assert [(c['name'], c['required'], c['repeatable']) for c in s['subproperties']] == [
        ('computation-label', True, True), ('theory-level', True, False), ('model-type', True, False),
        ('particle-style', True, True), ('bonding-type', True, False), ('charge-interactions', False, True),
        ('magnetic-interactions', False, True)]
    assert [c['name'] for c in sub(s, 'charge-interactions')['subproperties']] == [
        'charge-origin', 'charge-style', 'charge-variability', 'long-range-electrostatics', 'electric-dipole',
        'electric-dipole-variability']
    assert [c['name'] for c in sub(s, 'magnetic-interactions')['subproperties']] == ['spin-style', 'magnetic-dipole']


def test_ps_keeps_only_the_dynamics():
    """md describes how particles are moved: its algorithm, parameters, initialization and constraints; mode is
    minimal's task, and the model is in pim (0046 item 9)."""
    props = section('ps')['properties']
    assert [p['name'] for p in props] == ['settings']
    assert [c['name'] for c in props[0]['subproperties']] == [
        'computation-label', 'algorithm', 'computation-parameter', 'initialization', 'thermodynamic-constraint']
    text = (ROOT / 'schema/ps.yaml').read_text()
    for gone in ('name: mode', 'particle-style', 'particle-interactions', 'charge-interactions',
                 'magnetic-interactions'):
        assert gone not in text, gone


def test_preamble_lists_pim_among_the_methods():
    """§1.2 lists each method that has a section, in the order of the sections."""
    text = (ROOT / 'docs/standard/index.md').read_text()
    assert '- DFT: Density functional theory\n\n- PIM: Particle interaction models\n\n- PS:' in text


PS_INTRODUCTION = (
    'The metadata for particle simulations (MatCore-PS) is tabulated below. A particle simulation moves or samples '
    'a system of particles using the energies and forces supplied by an interaction model, a particle interaction '
    'model or, as in ab initio molecular dynamics, an electronic structure computation. This category includes '
    'molecular dynamics (MD), molecular statics (MS) and coarse-grained MD (CGMD): energy and free energy '
    'minimization, equilibrium and nonequilibrium MD, and related approaches. The properties are given in settings '
    'blocks, each naming the PS computations it describes. (Note: This standard inherits the metadata in the '
    'minimal MatCore standard, adding the properties below.)')


def test_ps_is_named_for_every_method_it_describes():
    """Section 2.4 serves MD, MS, CGMD and ab initio MD, so it is named Particle Simulation, not after one method,
    and the site names it so wherever it named MatCore-MD (0061)."""
    assert section('ps')['introduction'].strip() == PS_INTRODUCTION
    assert json.loads((ROOT / 'examples/ps.json').read_text()).keys() == {'ps'}
    preamble = (ROOT / 'docs/standard/index.md').read_text()
    assert '- PS: Particle simulation (molecular dynamics, molecular statics and related methods)\n' in preamble
    for page in (preamble, (ROOT / 'docs/about.md').read_text()):
        assert 'MatCore-PS' in page and 'MatCore-MD' not in page


def test_leadership_lists_a_committee_per_method_section():
    """Each method section has a committee heading, in alphabetical order with Derived Properties last; the PIM
    committee is still to be named (0061)."""
    text = (ROOT / 'docs/leadership.md').read_text()
    methods = re.findall(r'^### Method: (.+)$', text, re.M)
    assert methods == ['Density Functional Theory', 'Machine Learning for Materials',
                       'Many-Body Perturbation Theory', 'Particle Interaction Model', 'Particle Simulation',
                       'Phase Field', 'Derived Properties']
    pim = text.split('### Method: Particle Interaction Model\n\n')[1].split('\n\n')[0]
    assert pim == '- TBD'
    ps = text.split('### Method: Particle Simulation\n\n')[1].split('\n\n')[0]
    assert ps.count('\n- ') == 3 and 'Aidan Thompson' in ps


THEORY_LEVELS = ['Physics-based', 'Machine-learned']


def test_pim_theory_level_is_the_origin_of_the_functional_form():
    """Of the baseline's five theory levels, three name electronic methods, which are computations of their own
    since 0046; what remains is whether the form is physical or learned, with eFF counted as physical (0046
    item 8)."""
    t = sub(section('pim')['properties'][0], 'theory-level')
    assert (t['required'], t['repeatable'], t['type'], t['extent'], t['kind'], t['recommended-unit']) == (
        True, False, 'string', [], 'inapplicable', None)
    assert t['description'] == 'How the functional form of the model was obtained.'
    assert t['values']['terms'] == THEORY_LEVELS
    note = ' '.join(t['values']['note'].split())
    assert note.startswith('"Physics-based" – A functional form built from a physical model of the interactions')
    assert 'electron force field' in note and '"Machine-learned" – A machine learning model trained to take' in note
    assert not [k for k in t if k.startswith('legacy_')]


MODEL_TYPE_NOTE = ("Note: Give the functional form. The specific parameterization, e.g. an OpenKIM model, NIST IPR "
                   "record, or a published potential file, is identified in the computation's software (role "
                   "Interaction model).")


def test_pim_model_type_names_the_functional_form():
    """model-type names the form (EAM, MACE); the specific potential is the PIM computation's software (0046 item
    6), so writers do not put a potential's name here."""
    t = sub(section('pim')['properties'][0], 'model-type')
    assert (t['required'], t['repeatable'], t['type'], t['extent'], t['kind'], t['recommended-unit']) == (
        True, False, 'string', [], 'inapplicable', None)
    assert t['description'] == 'The kind of potential used to compute the particle interactions.'
    assert t['values'] == {'examples': ['Lennard-Jones', 'EAM', 'MACE']}
    assert t['notes'] == [MODEL_TYPE_NOTE]
    assert not [k for k in t if k.startswith('legacy_')]


PARTICLE_STYLES = ['Atom', 'Radical', 'United atom', 'Bead', 'Coarse grained', 'Mesoscale', 'Classical electron',
                   'Nucleus']


def test_pim_particle_style_names_each_kind_of_particle():
    """The baseline's seven styles, plus Nucleus so that the electron force field is Nucleus and Classical electron
    rather than Atom, which would count its electrons twice (0046, settled 2026-11-10). The property repeats, one
    entry per kind of particle (0046 item 8)."""
    t = sub(section('pim')['properties'][0], 'particle-style')
    assert (t['required'], t['repeatable'], t['type'], t['extent'], t['kind'], t['recommended-unit']) == (
        True, True, 'string', [], 'inapplicable', None)
    assert t['description'] == 'The nature of the discrete entities whose interactions the model describes.'
    assert t['values']['terms'] == PARTICLE_STYLES
    note = ' '.join(t['values']['note'].split())
    assert '"Atom" – Each particle represents an individual atom' in note
    assert ('"Nucleus" – A nucleus or an ion core as a point charge, with its electrons represented by other '
            'particles, e.g. in the electron force field.') in note
    assert 'Give one entry for each kind of particle the model has' in note
    assert not [k for k in t if k.startswith('legacy_')]


BONDING_TYPE_NOTE = ('"Reactive" – A model without a predetermined bonding topology in which bonds are formed or '
                     'broken on-the-fly based on the particle environment. "Bonded fixed" – Bonds defined '
                     '<i>a priori</i> and cannot be broken during a simulation. "Bonded mutable" – Bonds defined '
                     '<i>a priori</i> but can be broken and/or formed during a simulation.')


def test_pim_bonding_type_says_whether_the_topology_is_given():
    """Reactive covers every model with no predetermined bonding topology, so a pair potential, EAM or a
    machine-learned potential is Reactive, as the example's Finnis-Sinclair model is."""
    t = sub(section('pim')['properties'][0], 'bonding-type')
    assert (t['required'], t['repeatable'], t['type'], t['extent'], t['kind'], t['recommended-unit']) == (
        True, False, 'string', [], 'inapplicable', None)
    assert t['description'] == 'Specifies whether the bonds between particles are immutable or can be broken.'
    assert t['values']['terms'] == ['Reactive', 'Bonded fixed', 'Bonded mutable']
    assert ' '.join(t['values']['note'].split()) == BONDING_TYPE_NOTE
    assert not [k for k in t if k.startswith('legacy_')]


CHARGE_TERMS = {
    'charge-origin': ['Semi empirical', 'Quantum', 'Electronic population', 'Electronegativity', 'Tabulated'],
    'charge-style': ['Coulomb full', 'Coulomb screened'],
    'charge-variability': ['Fixed', 'QEq', 'EEM', 'iEL/SCF', 'FlucQ', 'Drude'],
    'long-range-electrostatics': ['None', 'Direct', 'Ewald', 'PME', 'PPPM', 'Reaction'],
    'electric-dipole': ['Stockmayer', 'Screened', 'Long range'],
    'electric-dipole-variability': ['Induced', 'Isotropic', 'Anisotropic'],
}


def test_pim_charge_interactions_keeps_the_baseline_vocabularies():
    """charge-interactions moves whole from md (0046 item 8): a repeatable container of six string properties,
    each with the baseline's open terms, defined in its note."""
    c = sub(section('pim')['properties'][0], 'charge-interactions')
    assert (c['required'], c['repeatable'], c['type'], c['values']) == (False, True, None, None)
    assert [s['name'] for s in c['subproperties']] == list(CHARGE_TERMS)
    for s in c['subproperties']:
        assert (s['required'], s['repeatable'], s['type'], s['extent'], s['kind']) == (
            s['name'] in ('charge-origin', 'charge-style', 'charge-variability'), False, 'string', [], 'inapplicable')
        assert s['values']['terms'] == CHARGE_TERMS[s['name']]
        note = ' '.join(s['values']['note'].split())
        assert all(f'"{t}" – ' in note for t in CHARGE_TERMS[s['name']])
    assert not [k for s in [c, *c['subproperties']] for k in s if k.startswith('legacy_')]


def test_pim_dipole_variability_is_about_dipoles():
    """The baseline copied charge-variability's description onto electric-dipole-variability; its values are
    about dipoles, so the description says so (decided in review)."""
    c = sub(section('pim')['properties'][0], 'charge-interactions')
    assert 'local electric dipoles' in sub(c, 'electric-dipole-variability')['description']
    note = ' '.join(sub(c, 'charge-variability')['values']['note'].split())
    assert '"Fixed" – Charges cannot change during a simulation.' in note


def test_pim_spin_style_keeps_only_particle_models():
    """Spin dynamics driven by spin-polarized DFT, tight binding or a wavefunction is not a particle interaction
    model (0046); such a computation is named as an input instead, so only the classical spin styles remain
    (0060)."""
    m = sub(section('pim')['properties'][0], 'magnetic-interactions')
    assert (m['required'], m['repeatable'], m['type'], m['values']) == (False, True, None, None)
    assert [s['name'] for s in m['subproperties']] == ['spin-style', 'magnetic-dipole']
    s = sub(m, 'spin-style')
    assert (s['required'], s['repeatable'], s['type'], s['extent'], s['kind']) == (
        True, False, 'string', [], 'inapplicable')
    assert s['values']['terms'] == ['Classical spin', 'Coupled spin lattice']
    note = ' '.join(s['values']['note'].split())
    assert 'Landau–Lifshitz–Gilbert (LLG)' in note
    assert 'names as an `input` with the role Interaction model' in note
    d = sub(m, 'magnetic-dipole')
    assert (d['required'], d['repeatable'], d['type'], d['extent'], d['kind']) == (
        False, False, 'string', [], 'inapplicable')
    assert d['values'] == {'examples': ['Heisenberg', 'Multi-spin', 'Zeeman']}
    assert d['notes'] == ['Note: The strength of an applied field is the condition `magnetic-field` in minimal '
                          '`conditions`; a Zeeman term names its coupling to the spins.']
    assert not [k for p in [m, s, d] for k in p if k.startswith('legacy_')]


def test_pim_is_complete():
    """Every pim property is filled, so the section declares legacy_complete (0004 item 36)."""
    assert section('pim').get('legacy_complete') is True


def test_pim_introduction_names_settings_blocks():
    """pim's introduction says where its properties sit, as dft's does (0054)."""
    assert ('The properties are given in settings blocks, each naming the PIM computations it describes.'
            in section('pim')['introduction'])
