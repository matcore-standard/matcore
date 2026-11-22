"""Computations and structures carry labels, and computations name what they use (decision record 0046)."""
import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'
TASKS = ['Structure generation', 'Single point', 'Optimization', 'Transition path', 'Equilibration', 'Dynamics',
         'Sampling', 'Free energy calculation', 'Training', 'Property calculation']
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
        'label', 'description', 'method-class', 'method', 'task', 'structure-label', 'input', 'conditions',
        'software']
    assert c['description'] == ('A group of calculations in the dataset that share one method and one set of '
                                'settings, e.g. the DFT single points of a training set.')
    assert not sub(c, 'conditions')['required']
    assert sub(c, 'conditions')['description'].endswith(
        'Omitted when no condition is imposed, e.g. for a single point or a training computation.')


def test_a_computation_can_explain_what_its_properties_do_not_capture():
    """A protocol such as a structure search's has parts no property records, so a computation has an optional
    free-text description, a scalar like structure's (0066 item 5)."""
    d = sub(top('minimal', 'computation'), 'description')
    assert shape(d) == (False, False, 'string', [], 'inapplicable', None)
    assert d['values'] is None
    assert d['description'] == ('An explanation of the computation that its other properties do not capture, '
                                'e.g. the protocol of a search.')


STAGES_NOTE = (
    'Note: A simulation run in stages, e.g. heating, equilibration and a quench, is described as one computation '
    'for each stage whose method, settings or conditions differ and whose data the dataset contains or depends on. '
    'Each stage names the stage it continues from in `input` with the role Initial configuration, which carries '
    'over the final state of that stage, e.g. positions, velocities and the cell. These links give the order of '
    'the stages; the order of the entries in the record does not. A condition that changes within one stage, e.g. '
    "a temperature ramp, is given in that stage's `conditions` as entries with a qualifier. The full protocol, "
    'with its control flow and complete inputs, belongs to the provenance record of a workflow manager (§1.2).')


GROUPING_NOTE = (
    'Note: The record explains the dataset; it does not retrace the workflow that produced it (§1.2). Give a '
    'computation for calculations whose results are in the dataset, or whose method or settings a reader needs in '
    'order to understand the data. Steps that serve one purpose with one method are one computation, e.g. the '
    'post-processing steps that give phonon modes and then a Raman spectrum (method DP). A step that only prepares '
    'another computation and adds nothing a reader needs, e.g. a relaxation that fixes the cell for later single '
    'points, may be left out or mentioned in the description of the computation it prepares.')


def test_a_record_groups_calculations_instead_of_retracing_the_workflow():
    """Divided step by step, a record becomes a workflow, which MatCore does not describe; the note says when
    calculations deserve a computation of their own, before 0063's note on stages applies the same test (0077)."""
    assert top('minimal', 'computation')['notes'][0] == GROUPING_NOTE


def test_a_staged_simulation_is_a_chain_of_computations():
    """A reader of a repeatable computation asks how stages are ordered and what carries over between them; the
    answer is the input links, not a protocol object, and the role says the state carries over (0063)."""
    c = top('minimal', 'computation')
    assert c['notes'] == [GROUPING_NOTE, STAGES_NOTE]
    role = sub(sub(c, 'input'), 'role')['values']['note']
    assert ('"Initial configuration" – The configurations this computation starts from, with the state carried '
            'over from that computation, e.g. velocities') in role


def test_task_terms_are_defined():
    """What a computation does is a required open term, each defined in the note (0046 item 2)."""
    t = sub(top('minimal', 'computation'), 'task')
    assert shape(t) == (True, False, 'string', [], 'inapplicable', None)
    assert t['values']['terms'] == TASKS
    assert all(f'"{term}" –' in t['values']['note'] for term in TASKS)


def test_task_names_the_goal_not_the_mechanism():
    """An umbrella-sampling MD run must fit one task, so each task is a goal and the procedure is left to the
    method's section; transitions, generated structures, equilibration and fitted models each get one goal
    (0064 item 3; 0065)."""
    t = sub(top('minimal', 'computation'), 'task')
    note = t['values']['note']
    for definition in (
            '"Structure generation" – The computational creation, modification, or systematic enumeration of '
            'initial atomic, molecular, or crystalline configurations before running physics-based energy or force '
            'evaluations',
            '"Optimization" – Configurations or cells taken to a minimum of the energy, local or global, e.g. a '
            'relaxation or a search for the lowest-energy structure',
            '"Transition path" – Transitions between stable states: saddle points of the energy, minimum energy '
            'paths, or ensembles of reactive trajectories and the rates they give, e.g. by the nudged elastic band, '
            'dimer method or transition path sampling',
            '"Equilibration" – Configurations brought to the conditions of another computation, which takes them '
            'as its Initial configuration; its results are not meant for analysis',
            '"Dynamics" – Configurations evolved in time where the evolution or the kinetics is the result, e.g. '
            'trajectories, transport coefficients or rates, including accelerated dynamics',
            '"Sampling" – Averages over a distribution of configurations, by Monte Carlo or by dynamics, where the '
            'time evolution is not itself the result',
            '"Training" – The parameters of a model fitted to data, e.g. a machine-learned model, a potential fitted '
            'by force matching or Boltzmann inversion, or a cluster expansion'):
        assert definition in note
    assert t['notes'] == ['Note: Give the term for the results the computation is meant to provide; the procedure '
                          'is given in the method\'s section, e.g. ps `algorithm`.']


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


METHOD_DEFINITIONS = (
    '"CC" – Coupled Cluster: wavefunction methods that build electron correlation from excitations of a reference '
    'state; "QMC" – Quantum Monte Carlo: stochastic solutions of the many-electron Schrödinger equation; "DFT" – '
    'Density Functional Theory: electronic structure obtained from the electron density; "MBPT" – Many-Body '
    'Perturbation Theory: excited states obtained from many-body Green\'s functions; "TB" – Tight Binding: '
    'electronic structure in a basis of localized orbitals with parameterized matrix elements; "PIM" – Particle '
    'Interaction Model: energies and forces given as an explicit function of the particles\' coordinates, without '
    'solving for a wavefunction or an electron density; "PS" – Particle Simulation: particles moved or sampled '
    'using the energies and forces of another computation; "DDD" – Discrete Dislocation Dynamics: plastic '
    'deformation from the motion and interaction of dislocation lines; "KMC" – Kinetic Monte Carlo: evolution of a '
    'system as a sequence of thermally activated events chosen by their rates; "PF" – Phase Field: microstructure '
    'evolution described by continuous fields with diffuse interfaces; "ML" – Machine Learning: models trained on '
    'data to predict materials properties or behavior; "DP" – Derived Property: a property obtained from the '
    'results of other computations by a procedure with no physical model of its own, e.g. force constants from '
    'finite-difference forces, an X-ray diffraction pattern from a structure, or a vibrational density of states '
    'from a trajectory.')


def test_method_names_the_section_that_describes_the_computation():
    """MD, MS, MC and CGMD repeat what task, algorithm and method-class say, so one term PS names the section
    that describes them all; tight binding and a particle interaction model keep their terms (0046 items 4, 5;
    0064 items 1, 2)."""
    computation = top('minimal', 'computation')
    m = sub(computation, 'method')
    assert m['description'] == ('The method of the calculations in this computation, which names the section of '
                                'this standard that describes their settings, where one exists.')
    assert {k: c['terms'] for k, c in m['values']['cases'].items()} == {
        'Electronic': ['CC', 'QMC', 'DFT', 'MBPT', 'TB'], 'Atomistic': ['PIM', 'PS'],
        'Mesoscopic': ['DDD', 'KMC', 'PIM', 'PS'], 'Continuum': ['PF'], 'Data-driven': ['ML'],
        'Post-processing': ['DP']}
    assert m['values']['note'] == '\n'.join('- ' + d.rstrip('.') for d in METHOD_DEFINITIONS.split('; '))
    assert sub(computation, 'method-class')['notes'][-1] == (
        'Note: For a PS computation, give the entity of its particles: Atomistic for atoms, Mesoscopic for '
        'coarse-grained particles such as beads.')
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
                     ('dft', 'computation-label'), ('pim', 'computation-label'), ('ps', 'computation-label'),
                     ('mbpt', 'computation-label'), ('ml', 'computation-label'),
                     ('pf', 'computation-label'), ('derived', 'computation-label')}


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
          'pf': '2.7 Phase Field (PF) Metadata', 'derived': '2.8 Derived Property (DP) Metadata'}
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
        'charge-origin', 'charge-style', 'charge-variability', 'electrostatic-summation', 'electric-dipole',
        'electric-dipole-variability']
    assert [c['name'] for c in sub(s, 'magnetic-interactions')['subproperties']] == ['spin-style', 'magnetic-dipole']


def test_ps_keeps_only_the_dynamics():
    """md describes how particles are moved: its algorithm, parameters, initialization and constraints; mode is
    minimal's task, and the model is in pim (0046 item 9)."""
    props = section('ps')['properties']
    assert [p['name'] for p in props] == ['settings']
    assert [c['name'] for c in props[0]['subproperties']] == [
        'computation-label', 'algorithm', 'description', 'computation-parameter', 'initialization',
        'thermodynamic-constraint']
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
    'molecular dynamics (MD), molecular statics (MS), Monte Carlo (MC) and their coarse-grained forms: energy and '
    'free energy minimization, equilibrium and nonequilibrium MD, accelerated dynamics, enhanced sampling, '
    'saddle-point searches and related approaches. The properties are given in settings '
    'blocks, each naming the PS computations it describes. (Note: This standard inherits the metadata in the '
    'minimal MatCore standard, adding the properties below.)')


def test_ps_is_named_for_every_method_it_describes():
    """Section 2.4 serves MD, MS, MC, their coarse-grained forms and ab initio MD, so it is named Particle
    Simulation, not after one method, and the site names it so wherever it named MatCore-MD (0061; 0064 item 5)."""
    assert section('ps')['introduction'].strip() == PS_INTRODUCTION
    assert json.loads((ROOT / 'examples/ps.json').read_text()).keys() == {'ps'}
    preamble = (ROOT / 'docs/standard/index.md').read_text()
    assert ('- PS: Particle simulation (molecular dynamics, molecular statics, Monte Carlo and related methods)\n'
            in preamble)
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
    assert note.startswith('- "Physics-based" – A functional form built from a physical model of the interactions')
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
            'particles, e.g. in the electron force field') in note
    assert 'Give one entry for each kind of particle the model has' in note
    assert not [k for k in t if k.startswith('legacy_')]


BONDING_TYPE_NOTE = ('- "Reactive" – A model without a predetermined bonding topology in which bonds are formed or '
                     'broken on-the-fly based on the particle environment\n- "Bonded fixed" – Bonds defined '
                     '<i>a priori</i> and cannot be broken during a simulation\n- "Bonded mutable" – Bonds defined '
                     '<i>a priori</i> but can be broken and/or formed during a simulation')


def test_pim_bonding_type_says_whether_the_topology_is_given():
    """Reactive covers every model with no predetermined bonding topology, so a pair potential, EAM or a
    machine-learned potential is Reactive, as the example's Finnis-Sinclair model is."""
    t = sub(section('pim')['properties'][0], 'bonding-type')
    assert (t['required'], t['repeatable'], t['type'], t['extent'], t['kind'], t['recommended-unit']) == (
        True, False, 'string', [], 'inapplicable', None)
    assert t['description'] == 'Specifies whether the bonds between particles are immutable or can be broken.'
    assert t['values']['terms'] == ['Reactive', 'Bonded fixed', 'Bonded mutable']
    assert t['values']['note'] == BONDING_TYPE_NOTE
    assert not [k for k in t if k.startswith('legacy_')]


CHARGE_TERMS = {
    'charge-origin': ['Semi empirical', 'Quantum', 'Electronic population', 'Electronegativity', 'Tabulated'],
    'charge-style': ['Coulomb full', 'Coulomb screened'],
    'charge-variability': ['Fixed', 'QEq', 'EEM', 'iEL/SCF', 'FlucQ', 'Drude'],
    'electrostatic-summation': ['None', 'Direct', 'Short-range', 'Ewald', 'PME', 'PPPM', 'Reaction'],
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
    assert '"Fixed" – Charges cannot change during a simulation' in note


def test_pim_electrostatic_summation_covers_short_range_sums():
    """A sum truncated at a cutoff is neither the absence of electrostatics nor a long-range method, and a
    model without charges has no charge-interactions at all (0068)."""
    e = sub(sub(section('pim')['properties'][0], 'charge-interactions'), 'electrostatic-summation')
    assert e['description'] == 'Method used to compute the electrostatic interactions between the charges.'
    note = ' '.join(e['values']['note'].split())
    assert ('"Short-range" – Electrostatic interactions computed only within a cutoff distance, possibly shifted '
            'or damped, e.g. Wolf summation or damped shifted force (DSF)') in note
    assert '"None" – No electrostatic interactions are computed from the charges.' in note


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


ALGORITHM_GROUPS = {
    'Molecular dynamics, time integration': ['Leap frog', 'Runge-Kutta', 'Velocity Verlet', 'Verlet'],
    'Molecular dynamics, accelerated': ['Hyperdynamics', 'Parallel replica dynamics', 'TAD'],
    'Molecular statics, local minimization': ['Simplex', 'Damped dynamics', 'FIRE', 'Steepest descent',
                                              'Conjugate gradients', 'BFGS'],
    'Molecular statics, saddle points and paths': ['NEB', 'String method', 'Dimer method', 'ART',
                                                   'Eigenvector following'],
    'Global optimization': ['Simulated annealing', 'SGLD', 'Basin hopping', 'Basin filling',
                            'Random structure search', 'Evolutionary algorithm', 'Particle swarm optimization',
                            'Minima hopping'],
    'Monte Carlo': ['Metropolis Monte Carlo', 'Hybrid Monte Carlo'],
    'Enhanced sampling and free energy': ['Harmonic', 'Metadynamics', 'Thermodynamic integration',
                                          'Umbrella sampling', 'Replica exchange', 'Steered MD', 'Targeted MD',
                                          'aMD'],
    'Path sampling': ['Forward flux sampling', 'Transition path sampling', 'Milestoning'],
}


def test_ps_algorithm_names_every_procedure_by_group():
    """With MD, MS and MC gone from method, algorithm alone says how the particles were moved or sampled, so it
    is required, repeats for combined procedures, and defines every term, grouped as a reading aid (0064 item 4;
    0066 items 1, 3)."""
    a = sub(top('ps', 'settings'), 'algorithm')
    assert shape(a) == (True, True, 'string', [], 'inapplicable', None)
    assert a['description'] == 'A procedure by which the computation moves or samples the particles.'
    assert a['values']['terms'] == [t for terms in ALGORITHM_GROUPS.values() for t in terms]
    note = a['values']['note']
    blocks = note.split('\n\n')  # a bold group label, then its list, one item per term (0007 item 5, amended)
    assert blocks[0::2] == [f'**{group}**' for group in ALGORITHM_GROUPS]
    for terms, block in zip(ALGORITHM_GROUPS.values(), blocks[1::2]):
        assert [line.split(' – ')[0] for line in block.split('\n')] == [f'- "{t}"' for t in terms]
    for definition in (
            '"Harmonic" – A free energy from the harmonic or quasi-harmonic approximation',
            '"Random structure search" – Candidates generated at random within given constraints, each relaxed to '
            'a local minimum',
            '"Evolutionary algorithm" – Candidates produced from earlier ones by heredity and mutation and selected '
            'by their energies, each relaxed to a local minimum',
            '"Particle swarm optimization" – Candidates moved through configuration space toward the best '
            'structures found by each candidate and by the swarm, each relaxed to a local minimum',
            '"Minima hopping" – A walk from one local minimum to the next by short molecular dynamics escapes, with '
            'an energy threshold for accepting a new minimum and a record of the minima already visited'):
        assert definition in note
    assert 'PMF' not in note
    assert a['notes'] == [
        'Note: Give one entry for each procedure used, e.g. Velocity Verlet and Hyperdynamics, or Random structure '
        'search and BFGS for a search that relaxes its candidates. How a thermodynamic constraint is enforced, e.g. '
        'a thermostat, a barostat or grand canonical Monte Carlo moves, is given in `thermodynamic-constraint`, not '
        'here.',
        'Note: Numerical parameters of a procedure, e.g. the time step of Velocity Verlet or the number of images '
        'of NEB, are given as `computation-parameter` entries; its variant, e.g. well-tempered metadynamics, and '
        'other specifics are given in `description`.']
    assert not any(k.startswith('legacy_') for k in a)
    assert len(a['values']['terms']) == 39  # major classes only; variants go in description (0067 item 1)


def test_ps_settings_describe_algorithm_specifics():
    """The terms name only major classes, so a variant and the meaning of the parameters need free text beside
    them (0067 item 2)."""
    d = sub(top('ps', 'settings'), 'description')
    assert shape(d) == (False, False, 'string', [], 'inapplicable', None)
    assert d['values'] is None
    assert d['description'] == ('Further information on the algorithms of these settings, e.g. the variant used, '
                                'and an explanation of their computation-parameter entries.')


def test_ps_example_names_its_algorithm():
    """algorithm is required, so every settings block of the example gives it (0012)."""
    example = json.loads((ROOT / 'examples/ps.json').read_text())
    assert all(s['algorithm'] for s in example['ps']['settings'])


def test_ps_computation_parameter_is_a_generic_parameter():
    """An algorithm's numerical parameters vary with the algorithm, so the instance names each one and gives
    its type and unit: the generic-parameter form (0016), with the baseline's examples and a structure search's
    settings in its note (0066 item 4)."""
    import sys
    sys.path.insert(0, str(ROOT / 'scripts'))
    import check_generic
    p = sub(top('ps', 'settings'), 'computation-parameter')
    assert (p['required'], p['repeatable'], p['type']) == (False, True, None)
    assert check_generic.generic_errors(p) == []
    assert [s['name'] for s in p['subproperties']] == list(check_generic.FORM)
    assert p['notes'] == [
        'Note: For example, the time step of Velocity Verlet, the simulation time of a dynamics run, the '
        'convergence tolerance of an energy minimization, the number of images of NEB, or, for a structure '
        'search, the number of candidates, the number of atoms per cell, the allowed space groups, the volume '
        'range and the force and energy tolerances of the local relaxations.']
    assert not any(k.startswith('legacy_') for s in [p] + p['subproperties'] for k in s)


INITIALIZATION_NOTE = (
    'Note: Give what the computation sets up itself, e.g. velocities drawn from a Maxwell-Boltzmann distribution '
    'at 300 K with a stated random seed, or randomly oriented spins. A configuration carried over from another '
    'computation is named in minimal `computation › input` with the role Initial configuration, and the imposed '
    'conditions, e.g. the temperature, are given in minimal `conditions`.')


def test_ps_initialization_gives_only_what_the_computation_sets_up():
    """A carried-over state is an input link (0063) and an imposed value a condition (0042 item 3), so
    initialization holds the rest, as free text."""
    p = sub(top('ps', 'settings'), 'initialization')
    assert (p['required'], p['repeatable'], p['type'], p['extent'], p['kind'], p['values']) == (
        False, False, 'string', [], 'inapplicable', None)
    assert p['description'] == 'Information on the conditions set at the start of the simulation.'
    assert p['notes'] == [INITIALIZATION_NOTE]
    assert not any(k.startswith('legacy_') for k in p)


CONSTRAINT_METHODS = {
    'Thermostats': ['Andersen thermostat', 'Berendsen thermostat', 'CSVR', 'Langevin', 'Nosé-Hoover',
                    'Nosé-Hoover chain', 'Velocity rescaling'],
    'Barostats': ['Andersen barostat', 'Berendsen barostat', 'CauchyStat', 'Nosé-Hoover barostat',
                  'Parrinello-Rahman'],
    'Particle exchange': ['GCMC', 'SGCMC'],
}
ENSEMBLES = ['NVE', 'NVT', 'μVT', 'NPT', 'NσT', 'μPT', 'μσT', 'ΔμNPT', 'NPH', 'NσH']


def test_ps_thermodynamic_constraint_names_the_ensemble_and_its_enforcement():
    """The ensemble and how it is enforced are ps's; the values held fixed are minimal conditions' (0042 item 3).
    One ensemble may be enforced by a thermostat and a barostat together, so method repeats, and Andersen and
    Berendsen say which of the two they are (0069)."""
    import sys
    sys.path.insert(0, str(ROOT / 'scripts'))
    import check_generic
    c = sub(top('ps', 'settings'), 'thermodynamic-constraint')
    assert [(s['name'], s['required'], s['repeatable']) for s in c['subproperties']] == [
        ('system', True, False), ('type', True, False), ('method', False, True), ('description', False, False),
        ('td-parameter', False, True)]
    t = sub(c, 'type')
    assert t['values']['terms'] == ENSEMBLES
    assert '"ΔμNPT" – Semi-grand canonical' in ' '.join(t['values']['note'].split())
    assert 'minimal `conditions`' in t['notes'][0]
    m = sub(c, 'method')
    assert m['values']['terms'] == [x for g in CONSTRAINT_METHODS.values() for x in g]
    assert 'depends-on' not in m['values']
    blocks = m['values']['note'].split('\n\n')  # a bold label, a blank line, then the list (0007 item 5)
    assert blocks[0::2] == [f'**{k}**' for k in CONSTRAINT_METHODS]
    assert [[line.split(' – ')[0] for line in b.split('\n')] for b in blocks[1::2]] == [
        [f'- "{t}"' for t in g] for g in CONSTRAINT_METHODS.values()]
    assert '`algorithm`' in m['notes'][0]
    p = sub(c, 'td-parameter')
    assert check_generic.generic_errors(p) == []
    assert 'minimal `conditions`' in p['notes'][0]
    assert 'conditions › description' in sub(c, 'system')['notes'][0]
    assert not any(k.startswith('legacy_') for s in [c, *c['subproperties'], *p['subproperties']] for k in s)


def test_ps_is_complete():
    """Every ps property is filled, so the section declares it (0004 item 36)."""
    assert section('ps')['legacy_complete'] is True


def test_mbpt_properties_sit_in_settings_naming_computations():
    """An mbpt block names the MBPT computations it describes, and the DFT ground state a GW or BSE calculation
    starts from is that computation's input with the role Starting point, not an mbpt property (0046 items 7,
    10)."""
    props = section('mbpt')['properties']
    assert [p['name'] for p in props] == ['settings']
    s = props[0]
    assert (s['required'], s['repeatable'], s['type']) == (True, True, None)
    assert s['description'] == 'Settings shared by the computations named in it.'
    assert [c['name'] for c in s['subproperties']] == [
        'computation-label', 'mbpt-method', 'dielectric-matrix', 'self-energy', 'bse-hamiltonian',
        'bse-kernel-truncation']
    c = sub(s, 'computation-label')
    assert shape(c) == (True, True, 'string', [], 'inapplicable', None)
    assert c['description'] == 'The label of a computation these settings apply to.'
    intro = section('mbpt')['introduction']
    assert 'starting point,' not in intro
    assert 'The properties are given in settings blocks, each naming the MBPT computations it describes.' in intro
    assert 'role Starting point' in intro
    example = json.loads((ROOT / 'examples/mbpt.json').read_text(encoding='utf-8'))['mbpt']
    assert [list(b)[0] for b in example['settings']] == ['computation-label']


GW_VARIANTS = ['G0W0', 'GW0', 'G0W', 'evGW', 'scGW', 'QSGW']
BSE_VARIANTS = ['BSE0', 'scBSE']


def test_mbpt_method_gives_each_stage_its_own_self_consistency():
    """A GW + BSE calculation is one computation, so the GW and BSE variants are two properties instead of one list
    of combined terms, which could not name G0W0 followed by BSE (0070). Terms stay typable ASCII; definitions
    write the zero as a subscript, since the digit reads as the letter O on the site."""
    m = sub(top('mbpt', 'settings'), 'mbpt-method')
    assert (m['type'], m['extent'], m['kind'], m['values']) == (None, None, None, None)
    assert [(s['name'], s['required'], s['repeatable']) for s in m['subproperties']] == [
        ('type', True, False), ('gw-self-consistency', False, False), ('bse-self-consistency', False, False)]
    assert sub(m, 'type')['values']['terms'] == ['GW', 'BSE', 'GW/BSE']
    for name, terms in [('gw-self-consistency', GW_VARIANTS), ('bse-self-consistency', BSE_VARIANTS)]:
        s = sub(m, name)
        assert shape(s) == (False, False, 'string', [], 'inapplicable', None)
        assert s['values']['terms'] == terms
        assert all(t.isascii() for t in terms)
        note = ' '.join(s['values']['note'].split())
        definitions = dict(re.findall(r'"([^"]+)" – (.*?)(?= "[^"]+" – |$)', note))
        assert list(definitions) == terms
        assert [t for t in terms if '0' in t and '₀' not in definitions[t]] == []
        assert s['notes'][0] == f"Note: Give it when `type` is {'GW' if name[0] == 'g' else 'BSE'} or GW/BSE."
    assert sub(m, 'gw-self-consistency')['values']['note'].count('Eigenvalue-only self-consistent GW') == 1
    assert not any(k.startswith('legacy_') for s in [m, *m['subproperties']] for k in s)
    example = json.loads((ROOT / 'examples/mbpt.json').read_text(encoding='utf-8'))['mbpt']
    assert example['settings'][0]['mbpt-method'] == {'type': 'GW', 'gw-self-consistency': 'G0W0'}


FREQUENCY_TREATMENTS = ['Hybertsen-Louie', 'Godby-Needs', 'Full frequency real axis', 'Full frequency imaginary axis',
                        'Contour deformation', 'Spacetime']
COULOMB_TRUNCATIONS = ['Ismail-Beigi', 'Rozzi', 'Spencer-Alavi']


def test_mbpt_dielectric_matrix_is_typed():
    """The dielectric cutoff is an Energy with a unit like any other cutoff (0001 A5), and it is not the wavefunction
    cutoff: codes set it apart and lower (VASP ENCUTGW, ABINIT ecuteps, Yambo NGsBlkXp), so a reader must not copy
    dft kinetic-energy-cutoff into it. Exactly one of the two basis properties is given (0011 item 3)."""
    d = sub(top('mbpt', 'settings'), 'dielectric-matrix')
    assert (d['type'], d['required'], d['repeatable']) == (None, True, False)
    assert [(s['name'], s['required']) for s in d['subproperties']] == [
        ('planewave-basis-cutoff', False), ('localized-orbital-basis-set', False), ('frequency', False),
        ('response-basis-size', False), ('band-terminator', False), ('q-points', True),
        ('coulomb-truncation', False)]
    cutoff = sub(d, 'planewave-basis-cutoff')
    value = sub(cutoff, 'value')
    assert (value['type'], value['kind'], value['recommended-unit'], value['values']) == (
        'float', 'Energy', 'eV', {'minimum': 0})
    assert 'same as the kinetic energy cutoff' not in cutoff['description']
    assert 'kinetic-energy-cutoff' in cutoff['description']
    exclusive = 'Note: Specify either "planewave-basis-cutoff" or "localized-orbital-basis-set", but not both.'
    assert cutoff['notes'] == [exclusive]
    basis = sub(d, 'localized-orbital-basis-set')
    assert shape(basis) == (False, False, 'string', [], 'inapplicable', None)
    assert basis['notes'] == [exclusive]
    for name, terms in [('frequency', FREQUENCY_TREATMENTS), ('coulomb-truncation', COULOMB_TRUNCATIONS)]:
        s = sub(d, name)
        assert shape(s) == (False, False, 'string', [], 'inapplicable', None)
        assert s['values']['terms'] == terms
        note = ' '.join(s['values']['note'].split())
        assert list(dict(re.findall(r'"([^"]+)" – (.*?)(?= "[^"]+" – |$)', note))) == terms
    for name, extent in [('response-basis-size', []), ('q-points', [3])]:
        s = sub(d, name)
        assert (s['type'], s['extent'], s['kind'], s['values']['minimum']) == ('int', extent, 'dimensionless', 1)
    assert not any(k.startswith('legacy_') for s in [d, *d['subproperties']] for k in s)
    example = json.loads((ROOT / 'examples/mbpt.json').read_text(encoding='utf-8'))['mbpt']
    assert example['settings'][0]['dielectric-matrix']['planewave-basis-cutoff'] == {'value': 12.0, 'unit': 'Ry'}
    assert example['settings'][0]['dielectric-matrix']['q-points'] == [48, 48, 1]


def test_mbpt_self_energy_separates_corrected_bands_from_summed_bands():
    """The bands whose energies are corrected are a range, an output; the bands summed over in G and in W are
    separate convergence parameters, each with its own terminator for the bands left out (0071)."""
    settings = top('mbpt', 'settings')
    names = [s['name'] for s in settings['subproperties']]
    assert 'gw-bands' not in names
    assert names.index('self-energy') == names.index('dielectric-matrix') + 1
    se = sub(settings, 'self-energy')
    assert (se['type'], se['required'], se['repeatable']) == (None, False, False)
    assert se['notes'] == ['Note: Give it when `type` is GW or GW/BSE.']
    assert [s['name'] for s in se['subproperties']] == ['band-range', 'number-of-bands', 'band-terminator']
    band_range = sub(se, 'band-range')
    assert (band_range['type'], band_range['extent'], band_range['kind'], band_range['values']['minimum']) == (
        'int', [2], 'dimensionless', 1)
    count = sub(se, 'number-of-bands')
    assert (count['type'], count['extent']) == ('int', [])
    assert 'bands 1 to number-of-bands' in ' '.join(count['description'].split())
    assert 'lowest band' not in count['description']
    d = sub(settings, 'dielectric-matrix')
    dnames = [s['name'] for s in d['subproperties']]
    assert dnames.index('band-terminator') == dnames.index('response-basis-size') + 1
    for t in [sub(se, 'band-terminator'), sub(d, 'band-terminator')]:
        assert shape(t) == (False, False, 'string', [], 'inapplicable', None)
        assert t['values']['terms'] == ['None', 'Bruneval-Gonze']
        assert 'extrapolar approximation' in t['values']['note'] and 'Phys. Rev.' not in t['values']['note']
    assert 'Bruneval-Gonze' not in sub(d, 'coulomb-truncation')['values']['terms']
    example = json.loads((ROOT / 'examples/mbpt.json').read_text(encoding='utf-8'))['mbpt']['settings'][0]
    assert example['self-energy'] == {'band-range': [3, 4], 'number-of-bands': 200, 'band-terminator': 'Bruneval-Gonze'}


def test_mbpt_bse_hamiltonian_is_typed():
    """The BSE Hamiltonian's band counts start at the gap edges, its exciton momentum is fractional so it needs
    no unit or 2π convention (0072), and diagonalization names the approximation, not the solver."""
    settings = top('mbpt', 'settings')
    h = sub(settings, 'bse-hamiltonian')
    assert h['notes'] == ['Note: Give it when `type` is BSE or GW/BSE.']
    assert h['description'].endswith('diagonalization.')
    for name, edge in [('number-valence-bands', 'valence band top'),
                       ('number-conduction-bands', 'conduction band bottom')]:
        p = sub(h, name)
        assert shape(p) == (False, False, 'int', [], 'dimensionless', None)
        assert p['values']['minimum'] == 1
        assert edge in ' '.join(p['values']['note'].split()) and 'corrected' not in p['values']['note']
    mesh = sub(h, 'k-point-mesh')
    assert shape(mesh) == (False, False, 'int', [3], 'dimensionless', None)
    q = sub(h, 'exciton-momentum')
    assert shape(q) == (False, False, 'float', [3], 'dimensionless', None)
    assert 'subproperties' not in q
    note = ' '.join(q['values']['note'].split())
    assert 'conditions › cell' in note and 'Q₁b₁ + Q₂b₂ + Q₃b₃' in note
    multiplicity = sub(h, 'exciton-multiplicity')
    assert shape(multiplicity) == (False, False, 'string', [], 'inapplicable', None)
    assert multiplicity['values']['terms'] == ['Singlet', 'Triplet']
    diag = sub(h, 'diagonalization')
    assert diag['values']['terms'] == ['Tamm-Dancoff', 'Full diagonalization']
    assert 'coupling' in diag['values']['note']
    n = sub(h, 'number-lowest-eigenvalues')
    assert shape(n) == (False, False, 'int', [], 'dimensionless', None)
    assert not any(k.startswith('legacy_') for p in [h, *h['subproperties']] for k in p)


def test_mbpt_bse_kernel_truncation_matches_the_dielectric_truncation():
    """The BSE kernel and the dielectric matrix truncate the same Coulomb interaction, so they share terms and
    definitions; with it filled, mbpt holds no legacy text (0004 item 36)."""
    settings = top('mbpt', 'settings')
    k = sub(settings, 'bse-kernel-truncation')
    c = sub(sub(settings, 'dielectric-matrix'), 'coulomb-truncation')
    assert shape(k) == (False, False, 'string', [], 'inapplicable', None)
    assert k['values'] == c['values']
    assert k['notes'] == ['Note: Give it when `type` is BSE or GW/BSE.']
    assert section('mbpt')['legacy_complete'] is True


def test_ml_properties_sit_in_settings_with_the_model_holding_how_it_was_built():
    """An ml block names the ML computations it describes; the model holds what it is, how it was built and how
    good it is, and ml-task does not repeat since its type does (0073 items 1-3, 5, 6, 8)."""
    props = section('ml')['properties']
    assert [p['name'] for p in props] == ['settings']
    s = props[0]
    assert (s['required'], s['repeatable'], s['type']) == (True, True, None)
    assert [c['name'] for c in s['subproperties']] == [
        'computation-label', 'ml-task', 'ml-model', 'inference']
    assert shape(sub(s, 'computation-label')) == (True, True, 'string', [], 'inapplicable', None)
    task = sub(s, 'ml-task')
    assert (task['required'], task['repeatable']) == (True, False)
    model = sub(s, 'ml-model')
    assert [c['name'] for c in model['subproperties']] == [
        'algorithm', 'target-variable', 'input-feature', 'model-architecture', 'architecture-parameter',
        'model-size', 'training-data',
        'training-method', 'model-performance', 'interpretability-method']
    method = sub(model, 'training-method')
    assert [c['name'] for c in method['subproperties']] == [
        'training-procedure', 'loss-function', 'hyperparameter', 'transfer-learning']
    performance = sub(model, 'model-performance')
    assert [c['name'] for c in performance['subproperties']] == [
        'evaluation-method', 'metric', 'uncertainty-quantification', 'applicability-domain']
    assert ('The properties are given in settings blocks, each naming the ML computations it describes.'
            in section('ml')['introduction'])
    example = json.loads((ROOT / 'examples/ml.json').read_text(encoding='utf-8'))['ml']
    block = example['settings'][0]
    assert list(block)[0] == 'computation-label'
    assert block['ml-task']['type'] == ['Structure generation']
    assert 'training-data' in block['ml-model']


ML_TASK_TYPES = ['Property prediction', 'Structure generation', 'Synthesis prediction', 'Ranking', 'Clustering',
                 'Embedding']


def test_ml_task_names_the_kind_of_result_and_leaves_potentials_to_pim():
    """The task type names what the model produces for the dataset; structure prediction is generation with a
    fixed composition, and a machine-learned interatomic potential is a pim model, not an ML result (0073
    item 2)."""
    task = sub(top('ml', 'settings'), 'ml-task')
    t = sub(task, 'type')
    assert shape(t) == (True, True, 'string', [], 'inapplicable', None)
    assert t['values']['terms'] == ML_TASK_TYPES
    note = ' '.join(t['values']['note'].split())
    assert all(f'"{term}" –' in note for term in ML_TASK_TYPES)
    assert 'Structure prediction' not in t['values']['terms'] and 'composition' in note
    assert any('pim' in n and 'interatomic potential' in n for n in t['notes'])
    assert shape(sub(task, 'description')) == (False, False, 'string', [], 'inapplicable', None)
    assert not any(k.startswith('legacy_') for p in [task, *task['subproperties']] for k in p)


def test_ml_model_identifies_the_model_and_its_architecture_numbers_carry_units():
    """The model's own members say what it is; numbers that fix the architecture, such as a cutoff radius with
    its unit, are generic parameters explained by model-architecture, and model-size counts trainable
    parameters (0073 item 3)."""
    model = sub(top('ml', 'settings'), 'ml-model')
    names = [c['name'] for c in model['subproperties']]
    assert names[:6] == ['algorithm', 'target-variable', 'input-feature', 'model-architecture',
                         'architecture-parameter', 'model-size']
    assert any('only algorithm and target-variable' in n for n in model['notes'])
    assert shape(sub(model, 'algorithm')) == (True, False, 'string', [], 'inapplicable', None)
    assert shape(sub(model, 'target-variable')) == (True, True, 'string', [], 'inapplicable', None)
    assert shape(sub(model, 'input-feature')) == (False, True, 'string', [], 'inapplicable', None)
    arch = sub(model, 'model-architecture')
    assert shape(arch) == (False, False, 'string', [], 'inapplicable', None)
    assert 'architecture-parameter' in arch['values']['note']
    param = sub(model, 'architecture-parameter')
    assert (param['required'], param['repeatable']) == (False, True)
    assert [c['name'] for c in param['subproperties']] == ['name', 'value', 'unit', 'description']
    assert 'cutoff radius' in ' '.join(param['notes'][0].split())
    size = sub(model, 'model-size')
    assert shape(size) == (False, False, 'int', [], 'dimensionless', None)
    assert 'trainable parameters' in size['description']
    assert not any(k.startswith('legacy_') for p in [model, *model['subproperties'][:6]] for k in p)


def test_ml_training_data_points_to_the_record_and_counts_its_items():
    """Training data in the record is an input link, so source is for data from elsewhere; the split is
    described in words; size is a count whose item contents names (0073 item 4)."""
    data = sub(sub(top('ml', 'settings'), 'ml-model'), 'training-data')
    assert (data['required'], data['repeatable']) == (False, True)
    strings = ['name', 'contents', 'source', 'data-preprocessing', 'missing-data', 'missing-data-strategy',
               'outlier-handling', 'dataset-split']
    for name in strings:
        p = sub(data, name)
        assert (p['type'], p['extent'], p['kind'], p['repeatable']) == ('string', [], 'inapplicable', False), name
    assert sub(data, 'name')['required'] and sub(data, 'contents')['required']
    assert 'role Training data' in ' '.join(sub(data, 'source')['values']['note'].split())
    assert 'In words' in sub(data, 'dataset-split')['values']['note']
    size = sub(data, 'size')
    assert shape(size) == (False, False, 'int', [], 'dimensionless', None)
    assert size['values']['minimum'] == 1 and 'contents' in size['values']['note']
    assert not any(k.startswith('legacy_') for p in [data, *data['subproperties']] for k in p)
    example = json.loads((ROOT / 'examples/ml.json').read_text(encoding='utf-8'))
    assert example['ml']['settings'][0]['ml-model']['training-data'][0]['size'] == 45231


def test_ml_training_method_explains_its_hyperparameters_and_states_the_loss():
    """The procedure describes the fit and the role of each hyperparameter, which carries a value and a unit;
    the loss says what is fitted and how it is weighted (0073 item 5)."""
    method = sub(sub(top('ml', 'settings'), 'ml-model'), 'training-method')
    assert [c['name'] for c in method['subproperties']] == [
        'training-procedure', 'loss-function', 'hyperparameter', 'transfer-learning']
    procedure = sub(method, 'training-procedure')
    assert shape(procedure) == (True, False, 'string', [], 'inapplicable', None)
    note = ' '.join(procedure['values']['note'].split())
    assert 'hyperparameter entry' in note and 'active-learning' in note
    loss = sub(method, 'loss-function')
    assert shape(loss) == (False, False, 'string', [], 'inapplicable', None)
    assert 'forces' in loss['values']['note']
    hyper = sub(method, 'hyperparameter')
    assert (hyper['required'], hyper['repeatable']) == (False, True)
    assert [c['name'] for c in hyper['subproperties']] == ['name', 'value', 'unit', 'description']
    assert 'architecture-parameter' in hyper['notes'][0]
    assert shape(sub(method, 'transfer-learning')) == (False, False, 'string', [], 'inapplicable', None)
    assert not any(k.startswith('legacy_') for p in [method, *method['subproperties']] for k in p)


def test_ml_model_performance_keeps_validation_apart_from_testing():
    """How the model was assessed is separate from its scores; each score names the subset it was measured
    on, validation data tuning the model and test data assessing it, and carries its unit (0073 item 6)."""
    perf = sub(sub(top('ml', 'settings'), 'ml-model'), 'model-performance')
    assert [c['name'] for c in perf['subproperties']] == [
        'evaluation-method', 'metric', 'uncertainty-quantification', 'applicability-domain']
    method = sub(perf, 'evaluation-method')
    assert shape(method) == (True, True, 'string', [], 'inapplicable', None)
    metric = sub(perf, 'metric')
    assert (metric['required'], metric['repeatable'], metric['type']) == (False, True, None)
    assert [c['name'] for c in metric['subproperties']] == ['subset', 'quantity', 'measure', 'value', 'unit']
    subset = sub(metric, 'subset')
    assert subset['values']['terms'] == ['Training', 'Validation', 'Test']
    note = ' '.join(subset['values']['note'].split())
    assert 'tune' in note and 'neither' in note
    assert sub(metric, 'measure')['values']['terms'][:3] == ['MAE', 'RMSE', 'R²']
    value = sub(metric, 'value')
    assert (value['type'], value['kind']) == ('float', 'any')
    assert sub(metric, 'unit')['description'] == 'The unit in which the associated value is expressed.'
    uq = sub(perf, 'uncertainty-quantification')
    assert 'part of the dataset' in ' '.join(uq['values']['note'].split())
    assert shape(sub(perf, 'applicability-domain')) == (False, False, 'string', [], 'inapplicable', None)
    assert not any(k.startswith('legacy_') for p in [perf, *perf['subproperties']] for k in p)


INFERENCE_MEMBERS = ['input-data', 'conditioning', 'sampling-procedure', 'inference-parameter', 'number-generated',
                     'filtering']


def test_ml_inference_says_how_the_dataset_came_from_the_model():
    """A dataset produced by a model is described by what the model was applied to, how its outputs were drawn,
    how many were kept and what was removed, the sampling settings explained by the procedure (0073 item 7)."""
    settings = top('ml', 'settings')
    names = [c['name'] for c in settings['subproperties']]
    assert names.index('inference') == names.index('ml-model') + 1
    inference = sub(settings, 'inference')
    assert (inference['required'], inference['repeatable'], inference['type']) == (False, False, None)
    assert [c['name'] for c in inference['subproperties']] == INFERENCE_MEMBERS
    for name in ['input-data', 'conditioning', 'sampling-procedure', 'filtering']:
        assert shape(sub(inference, name)) == (False, False, 'string', [], 'inapplicable', None), name
    assert 'inference-parameter entry' in ' '.join(sub(inference, 'sampling-procedure')['values']['note'].split())
    assert 'role Source data' in ' '.join(sub(inference, 'input-data')['values']['note'].split())
    param = sub(inference, 'inference-parameter')
    assert param['repeatable'] and [c['name'] for c in param['subproperties']] == [
        'name', 'value', 'unit', 'description']
    count = sub(inference, 'number-generated')
    assert shape(count) == (False, False, 'int', [], 'dimensionless', None)
    assert 'novel' in sub(inference, 'filtering')['values']['note']
    example = json.loads((ROOT / 'examples/ml.json').read_text(encoding='utf-8'))['ml']['settings'][0]
    assert example['inference']['number-generated'] == 10000


def test_ml_interpretability_explains_the_model_and_ml_is_complete():
    """Interpretability explains how the model works, so it sits with the model (0073 amendment); with it filled,
    ml holds no legacy text (0004 item 36)."""
    settings = top('ml', 'settings')
    assert 'interpretability-method' not in [c['name'] for c in settings['subproperties']]
    model = sub(settings, 'ml-model')
    names = [c['name'] for c in model['subproperties']]
    assert names[-1] == 'interpretability-method' and names[-2] == 'model-performance'
    p = sub(model, 'interpretability-method')
    assert shape(p) == (False, False, 'string', [], 'inapplicable', None)
    assert 'SHAP' in p['values']['note']
    assert section('ml')['legacy_complete'] is True


def test_pf_properties_sit_in_settings_under_names_that_match_their_meaning():
    """A pf block names the PF computations it describes; a repeating property is singular, the free energy is a
    density given term by term, coupled models repeat the equation type, and the mesh belongs to the numerical
    method rather than the domain (0074 items 1-5)."""
    props = section('pf')['properties']
    assert [p['name'] for p in props] == ['settings']
    s = props[0]
    assert (s['required'], s['repeatable'], s['type']) == (True, True, None)
    assert [c['name'] for c in s['subproperties']] == [
        'computation-label', 'physical-phenomenon', 'problem-specification', 'domain', 'numerical-method',
        'variables']
    assert shape(sub(s, 'computation-label')) == (True, True, 'string', [], 'inapplicable', None)
    problem = sub(s, 'problem-specification')
    assert [c['name'] for c in problem['subproperties']] == ['governing-equation', 'free-energy-density']
    assert sub(problem, 'free-energy-density')['repeatable'] is True
    equation = sub(problem, 'governing-equation')
    assert [c['name'] for c in equation['subproperties']] == ['type', 'evolved-variable', 'free-energy-density-term']
    assert sub(equation, 'type')['repeatable'] is True
    assert [c['name'] for c in sub(s, 'domain')['subproperties']] == [
        'dimensionality', 'coordinate-system', 'domain-size', 'boundary-conditions', 'initial-conditions']
    assert [c['name'] for c in sub(s, 'numerical-method')['subproperties']] == PF_NUMERICAL_MEMBERS
    assert ('The properties are given in settings blocks, each naming the PF computations it describes.'
            in section('pf')['introduction'])
    block = json.loads((ROOT / 'examples/pf.json').read_text(encoding='utf-8'))['pf']['settings'][0]
    assert list(block) == ['computation-label', 'physical-phenomenon', 'problem-specification', 'domain',
                           'numerical-method', 'variables']
    assert block['problem-specification']['governing-equation'][0]['free-energy-density-term'] == ['f_total']


PF_PHENOMENA = ['Isothermal solidification', 'Directional solidification', 'Isothermal annealing', 'Sintering',
                'Twinning', 'Grain growth', 'Spinodal decomposition', 'Fracture', 'Plasticity']


def test_pf_physical_phenomenon_names_each_process_modeled_with_fracture_and_plasticity():
    """A phase field record names the material process it models, one entry per process, from an open list that
    covers fracture and plasticity as well as the baseline's processes (0074 item 2)."""
    p = sub(top('pf', 'settings'), 'physical-phenomenon')
    assert shape(p) == (True, True, 'string', [], 'inapplicable', None)
    assert p['values']['terms'] == PF_PHENOMENA
    note = ' '.join(p['values']['note'].split())
    assert all(f'"{term}" –' in note for term in PF_PHENOMENA)
    assert p['notes'] == ['Note: Give one entry for each process modeled.']
    assert not any(k.startswith('legacy_') for k in p)


def no_legacy(props):
    """Assert that no property in the tree keeps legacy text.

    props (list[dict]): properties, with nested subproperties.
    """
    for p in props:
        assert not any(k.startswith('legacy_') for k in p), p['name']
        no_legacy(p.get('subproperties') or [])


PF_EQUATIONS = ['CH', 'AC', 'GP', 'FID', 'PFC', 'Navier-Stokes', 'Multi-phase-field', 'Mechanical equilibrium',
                'Poisson']
PF_CONTRIBUTIONS = ['Chemical', 'Interfacial', 'Elastic', 'Plastic', 'Electrical', 'Magnetic', 'Fluid-solid interaction',
                    'Solid-solid interaction']
PF_FREE_ENERGY_MODELS = ['Ideal', 'Regular', 'Flory', 'Calphad', 'Poly', 'Non-polynomial']


def test_pf_problem_specification_gives_each_equation_and_free_energy_term_once():
    """A phase field model is its equations and the free energy terms that drive them. Each equation and each term is
    its own entry, so a coupled model lists them all; the system's time-evolution state is given once, in minimal
    conditions, and a term names the physical contribution it represents instead of a separate list (0074 item 3
    and its amendment)."""
    problem = sub(top('pf', 'settings'), 'problem-specification')
    assert 'time-evolution' not in problem['description'] + section('pf')['introduction']
    equation = sub(problem, 'governing-equation')
    t = sub(equation, 'type')
    assert shape(t) == (True, True, 'string', [], 'inapplicable', None)
    assert t['values']['terms'] == PF_EQUATIONS
    note = ' '.join(t['values']['note'].split())
    assert all(f'"{term}" –' in note for term in PF_EQUATIONS)
    assert any('anti-trapping' in n for n in t['notes'])
    v = sub(equation, 'evolved-variable')
    assert shape(v) == (True, False, 'string', [], 'inapplicable', None)
    assert v['description'] == 'The name of the field-variable being evolved by this equation.'
    assert shape(sub(equation, 'free-energy-density-term')) == (False, True, 'string', [], 'inapplicable', None)
    assert '`variables › field-variable`' in v['values']['note']
    assert '`problem-specification › free-energy-density`' in sub(equation, 'free-energy-density-term')['values']['note']
    density = sub(problem, 'free-energy-density')
    assert [c['name'] for c in density['subproperties']] == ['name', 'contribution', 'description', 'expression', 'unit']
    c = sub(density, 'contribution')
    assert shape(c) == (False, True, 'string', [], 'inapplicable', None)
    assert c['values']['terms'] == PF_CONTRIBUTIONS
    assert all(f'"{term}" –' in ' '.join(c['values']['note'].split()) for term in PF_CONTRIBUTIONS)
    d = sub(density, 'description')
    assert d['values']['terms'] == PF_FREE_ENERGY_MODELS
    assert sub(density, 'expression')['description'] == 'The mathematical expression of the free energy density.'
    u = sub(density, 'unit')
    assert u['description'] == 'The physical unit of the free energy density.'
    assert shape(u) == (False, False, 'string', [], 'inapplicable', None)
    assert 'x-gnu:' in u['values']['note']
    no_legacy([problem])
    block = json.loads((ROOT / 'examples/pf.json').read_text(encoding='utf-8'))['pf']['settings'][0]
    assert 'time-dependence' not in block['problem-specification']


PF_BOUNDARY_CONDITIONS = ['Dirichlet', 'Neumann', 'Zero-Neumann', 'Periodic']


def test_pf_domain_takes_reduced_units_and_names_where_each_boundary_condition_applies():
    """A phase field domain is often given in reduced units, which unit dimensionless says without a flag; a boundary
    condition says what it imposes, on which boundary and on which field, with no two terms for one condition (0074
    item 4, 0075)."""
    domain = sub(top('pf', 'settings'), 'domain')
    assert shape(sub(domain, 'dimensionality')) == (True, False, 'string', [], 'inapplicable', None)
    assert sub(domain, 'dimensionality')['values']['terms'] == ['1D', '2D', '3D']
    assert sub(domain, 'coordinate-system')['values']['terms'] == ['Cartesian', 'Cylindrical', 'Spherical']
    size = sub(domain, 'domain-size')
    assert [c['name'] for c in size['subproperties']] == ['value', 'unit']
    assert shape(sub(size, 'value')) == (True, False, 'float', [':'], 'Length', 'm')
    notes = ' '.join(size['notes'])
    assert '`dimensionless`' in notes and '`variables › model-parameter`' in notes and 'irregular' in notes
    bc = sub(domain, 'boundary-conditions')
    assert (bc['required'], bc['repeatable'], bc['type']) == (False, True, None)
    assert [c['name'] for c in bc['subproperties']] == ['type', 'boundary', 'field-variable']
    t = sub(bc, 'type')
    assert shape(t) == (True, False, 'string', [], 'inapplicable', None)
    assert t['values']['terms'] == PF_BOUNDARY_CONDITIONS
    assert all(f'"{term}" –' in ' '.join(t['values']['note'].split()) for term in PF_BOUNDARY_CONDITIONS)
    for name in ('boundary', 'field-variable'):
        assert shape(sub(bc, name)) == (False, False, 'string', [], 'inapplicable', None)
    # a reference names where the referenced property is defined, not just its name
    assert '`numerical-method › mesh-file`' in sub(bc, 'boundary')['values']['note']
    assert '`variables › field-variable`' in sub(bc, 'field-variable')['values']['note']
    assert shape(sub(domain, 'initial-conditions')) == (False, True, 'string', [], 'inapplicable', None)
    assert not any(k.startswith('legacy_') for p in [domain, *domain['subproperties']] for k in p)
    block = json.loads((ROOT / 'examples/pf.json').read_text(encoding='utf-8'))['pf']['settings'][0]
    assert block['domain']['domain-size'] == {'value': [100.0, 100.0], 'unit': 'dimensionless'}
    assert block['domain']['boundary-conditions'] == [{'type': 'Periodic'}]


PF_NUMERICAL_MEMBERS = ['evolved-variable', 'spatial-discretization', 'spatial-discretization-parameter',
                        'spatial-accuracy-order', 'mesh-type', 'mesh-file', 'temporal-discretization',
                        'temporal-accuracy-order', 'grid-spacing', 'time-step-size', 'solver']
PF_SPATIAL = ['FDM', 'FEM', 'FVM', 'LBM', 'Particle', 'Spectral']
PF_MESHES = ['Regular', 'Rectilinear', 'Skewed', 'Curvilinear', 'Unstructured', 'Adaptive mesh refinement', 'Meshless']
PF_TEMPORAL = ['Forward Euler', 'Backward Euler', 'Adams-Bashforth', 'Crank-Nicolson', 'Runge-Kutta', 'IMEX']
PF_SOLVERS = ['Explicit', 'Direct', 'Conjugate gradient', 'BiCGSTAB', 'GMRES', 'Multigrid', 'Newton', 'Newton-Krylov',
              'Picard']


def test_pf_numerical_method_says_how_each_group_of_equations_is_discretized_and_solved():
    """A numerical-method entry says how the equations it names are discretized in space and time and solved, so
    equations solved differently get entries of their own; a mesh that the grid spacing does not fix is a file whose
    boundaries the boundary conditions name; reduced lengths and times need no flag; each term names one scheme
    (0074 item 5 and second amendment, 0075)."""
    nm = sub(top('pf', 'settings'), 'numerical-method')
    assert [c['name'] for c in nm['subproperties']] == PF_NUMERICAL_MEMBERS

    def defined(p, terms):
        """Assert that p has exactly these open terms, each defined in its note.

        p (dict): property entry; terms (list[str]): the expected terms.
        """
        assert p['values']['terms'] == terms
        note = ' '.join(p['values']['note'].split())
        assert all(f'"{t}" –' in note for t in terms), p['name']
    ev = sub(nm, 'evolved-variable')
    assert shape(ev) == (False, True, 'string', [], 'inapplicable', None)
    assert '`variables › field-variable`' in ev['values']['note']
    assert 'one `numerical-method` entry for each group' in ' '.join(ev['notes'][0].split())
    defined(sub(nm, 'spatial-discretization'), PF_SPATIAL)
    param = sub(nm, 'spatial-discretization-parameter')
    assert (param['required'], param['repeatable']) == (False, True)
    assert [c['name'] for c in param['subproperties']] == ['name', 'value', 'unit', 'description']
    for name in ('spatial-accuracy-order', 'temporal-accuracy-order'):
        assert shape(sub(nm, name)) == (False, False, 'int', [], 'dimensionless', None)
    defined(sub(nm, 'mesh-type'), PF_MESHES)
    mesh = sub(nm, 'mesh-file')
    # a mesh may be split over several files, e.g. its structure and its boundaries
    assert (mesh['required'], mesh['repeatable']) == (False, True)
    assert 'one entry for each file' in ' '.join(' '.join(mesh['notes']).split())
    assert mesh['subproperties'] == sub(sub(top('minimal', 'computation'), 'software'), 'file')['subproperties']
    assert '`domain › boundary-conditions › boundary`' in ' '.join(mesh['notes'][0].split())
    temporal = sub(nm, 'temporal-discretization')
    defined(temporal, PF_TEMPORAL)
    assert any('stationary' in n for n in temporal['notes'])
    for name, kind, unit in (('grid-spacing', 'Length', 'm'), ('time-step-size', 'Time', 's')):
        p = sub(nm, name)
        assert [c['name'] for c in p['subproperties']] == ['name', 'value', 'unit', 'description']
        assert shape(sub(p, 'value')) == (True, False, 'float', [], kind, unit)
        notes = ' '.join(' '.join(p['notes']).split())
        assert '`dimensionless`' in notes and '`variables › model-parameter`' in notes
    solver = sub(nm, 'solver')
    assert shape(solver) == (False, True, 'string', [], 'inapplicable', None)
    defined(solver, PF_SOLVERS)
    assert 'software' in ' '.join(solver['notes'][0].split())
    no_legacy([nm])
    block = json.loads((ROOT / 'examples/pf.json').read_text(encoding='utf-8'))['pf']['settings'][0]
    entry = block['numerical-method'][0]
    assert entry['temporal-discretization'] == 'Backward Euler'
    assert [g['value'] for g in entry['grid-spacing']] == [0.4, 0.4]
    assert entry['time-step-size'][0]['value'] == 0.01


def test_pf_variables_give_each_field_its_own_entry_and_pf_is_complete():
    """A model parameter's value takes any type, shape and unit, so it is a generic parameter; a field variable is
    the field one equation evolves, so each field (each component's concentration, each grain's order parameter) is
    its own entry, named as the equations and boundary conditions refer to it (0016, 0074 item 6)."""
    variables = sub(top('pf', 'settings'), 'variables')
    param = sub(variables, 'model-parameter')
    assert [c['name'] for c in param['subproperties']] == ['name', 'value', 'unit', 'description']
    assert (sub(param, 'value')['type'], sub(param, 'value')['kind']) == ('any', 'any')
    assert 'reduced units' in ' '.join(' '.join(param['notes']).split())
    field = sub(variables, 'field-variable')
    assert (field['required'], field['repeatable']) == (False, True)
    assert [c['name'] for c in field['subproperties']] == ['name', 'type', 'unit', 'description']
    assert 'one concentration entry for each component' in ' '.join(' '.join(field['notes']).split())
    t = sub(field, 'type')
    assert shape(t) == (True, False, 'string', [], 'inapplicable', None)
    assert t['values']['terms'] == ['Scalar', 'Vector', 'Tensor']
    assert all(f'"{term}" –' in ' '.join(t['values']['note'].split()) for term in t['values']['terms'])
    unit = sub(field, 'unit')
    assert shape(unit) == (True, False, 'string', [], 'inapplicable', None)
    assert 'x-gnu:' in unit['values']['note']
    no_legacy([variables])
    assert section('pf')['legacy_complete'] is True
    block = json.loads((ROOT / 'examples/pf.json').read_text(encoding='utf-8'))['pf']['settings'][0]
    params = block['variables']['model-parameter']
    assert [(p['value'], p['type']) for p in params] == [(0.04714045, 'float'), (5.05, 'float')]


def test_post_processing_is_a_method_class_whose_method_names_the_derived_section():
    """A computation that only processes other computations' results solves no physical model, yet `method` is
    required; MODA's post-processing (CWA 17284:2018 §3.12) is its class, and DP names the section that describes
    it (0076 item 3)."""
    mc = sub(top('minimal', 'computation'), 'method-class')
    assert mc['values']['terms'][-1] == 'Post-processing'
    note = ' '.join(mc['notes'][0].split())
    assert 'CWA 17284:2018 §3.12' in note and 'do not alter the physical system' in note


def test_derived_properties_sit_in_settings_naming_the_computation_that_obtains_them():
    """A derived property names the computation that obtained it, of any method, and a property built from several
    computations names them as inputs rather than being limited to one method; steps that are computations are not
    chained inside the property (0076 items 1, 2, 4)."""
    props = section('derived')['properties']
    assert [p['name'] for p in props] == ['settings']
    s = props[0]
    assert (s['required'], s['repeatable'], s['type']) == (True, True, None)
    assert [c['name'] for c in s['subproperties']] == ['computation-label', 'derived-property']
    assert shape(sub(s, 'computation-label')) == (True, True, 'string', [], 'inapplicable', None)
    prop = sub(s, 'derived-property')
    assert (prop['required'], prop['repeatable']) == (True, True)
    assert [c['name'] for c in prop['subproperties']] == ['type', 'name', 'description', 'procedure',
                                                       'calculation-parameter']
    intro = ' '.join(section('derived')['introduction'].split())
    assert 'single method' not in intro and 'MBPT' not in intro
    assert 'Source data' in intro and 'Interaction model' in intro and 'DP' in intro
    assert 'The properties are given in settings blocks, each naming the computations it describes.' in intro
    # the record explains the dataset, not its workflow: steps are grouped, and how a property was obtained, with its
    # parameters, sits in the derived entry as a method's settings sit in its section (review 2026-11-22)
    assert 'one for each step' not in intro
    assert 'finite-difference' in intro and '`calculation-parameter`' in intro
    # the introduction stays short: what a derived property is, then the usual record, one DP computation whose
    # block gives an entry per property (review 2026-11-22)
    prose = section('derived')['introduction'].split('Examples of derived properties include:')[0]
    assert len([p for p in prose.split('\n\n') if p.strip()]) == 2
    assert 'one computation' in intro and 'one `derived-property` entry for each property' in intro
    # the introduction lists the property families of `type` as 0076 item 5 states them
    assert 'Linear-response' not in intro
    assert all(f'- {family} (' in section('derived')['introduction'] for family in ('Vibrational', 'Mechanical',
                                                                                   'Thermodynamic'))
    block = json.loads((ROOT / 'examples/derived.json').read_text(encoding='utf-8'))['derived']['settings'][0]
    assert block['computation-label'] == ['raman']
    assert list(block['derived-property'][0]) == ['type', 'name', 'description', 'procedure']


DERIVED_TYPES = ['Electronic', 'Electron-phonon interactions', 'Magnetic', 'Mechanical', 'Microscopy, electron',
                 'Microscopy, scanning probe', 'NMR', 'Optical', 'Scattering', 'Spectroscopy, core-level',
                 'Spectroscopy, vibrational', 'Thermodynamic', 'Transport', 'Vibrational']


def test_derived_property_names_the_property_and_how_it_was_obtained_and_derived_is_complete():
    """A derived entry says what kind of property it is and which one, then how it was obtained, with the parameters
    of that procedure as generic parameters; the kinds are those the introduction lists, scattering covering neutrons
    as well as X-rays (0076 items 4, 5; review 2026-11-22)."""
    prop = sub(top('derived', 'settings'), 'derived-property')
    t = sub(prop, 'type')
    assert shape(t) == (True, False, 'string', [], 'inapplicable', None)
    assert t['values']['terms'] == DERIVED_TYPES
    note = ' '.join(t['values']['note'].split())
    assert all(f'"{term}" –' in note for term in DERIVED_TYPES)
    families = re.findall(r'^- (.+?) \(', section('derived')['introduction'], re.M)
    assert families == DERIVED_TYPES
    for name in ('name', 'description', 'procedure'):
        assert shape(sub(prop, name)) == (True, False, 'string', [], 'inapplicable', None)
    assert 'finite-difference' in ' '.join(' '.join(sub(prop, 'procedure')['notes']).split())
    param = sub(prop, 'calculation-parameter')
    assert (param['required'], param['repeatable']) == (False, True)
    assert [c['name'] for c in param['subproperties']] == ['name', 'value', 'unit', 'description']
    assert (sub(param, 'value')['type'], sub(param, 'value')['kind']) == ('any', 'any')
    no_legacy(section('derived')['properties'])
    assert section('derived')['legacy_complete'] is True
