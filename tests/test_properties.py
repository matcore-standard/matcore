"""Properties whose structure a decision record fixes keep that structure."""
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_values import value_schema  # noqa: E402
from check_generic import UNIT_DESCRIPTION, UNIT_NOTE  # noqa: E402


def tree(p):
    """Return a property's structure as nested tuples: name, required, repeatable, type, scheme terms, children.

    p (dict): property entry, with nested subproperties.
    """
    terms = tuple((p.get('values') or {}).get('terms', ()))
    return (p['name'], p['required'], p['repeatable'], p['type'], terms,
            tuple(tree(s) for s in p.get('subproperties') or []))


def legacy_fields(p):
    """Return the legacy_* fields left in a property and its subproperties.

    p (dict): property entry.
    """
    return [k for k in p if k.startswith('legacy_')] + [k for s in p.get('subproperties') or [] for k in legacy_fields(s)]


def minimal(name):
    """Return a top-level property of schema/minimal.yaml.

    name (str): the property's name.
    """
    return next(p for p in yaml.safe_load(open(ROOT / 'schema/minimal.yaml'))['properties'] if p['name'] == name)


@pytest.mark.parametrize('name, required', [('title', True), ('description', True), ('disclaimer', False)])
def test_at_most_one_string(name, required):
    """A dataset has at most one of each of these, a plain string, not a physical quantity; title and
    description are required, while a disclaimer is given only when the creators have one.

    name (str): the property's name; required (bool): whether a dataset must have it.
    """
    p = minimal(name)
    assert (p['required'], p['repeatable'], p['type'], p['extent'], p['kind'], p['recommended-unit']) == (
        required, False, 'string', [], 'inapplicable', None)
    assert legacy_fields(p) == []


@pytest.mark.parametrize('value, ok', [
    ('2021-02-22', True), ('2021-02-22T14:30:00Z', True),
    ('2021-13-01', False), ('2021-02-32', False), ('2021-02-22T24:00:00Z', False),
    ('2021-02-22T14:30:00+01:00', False), ('2021-02-22T14:30:00', False), ('22/02/2021', False)])
def test_creation_date_takes_a_date_or_a_utc_date_time(value, ok):
    """creation-date accepts the baseline's two ISO 8601 forms, a date or a date and time in UTC, and
    nothing else, so dates from different sources compare without time-zone conversion.

    value (str): a candidate creation date; ok (bool): whether it conforms.
    """
    p = minimal('creation-date')
    assert (p['required'], p['repeatable'], p['type'], p['extent'], p['kind']) == (
        True, False, 'string', [], 'inapplicable')
    assert legacy_fields(p) == []
    assert Draft202012Validator(value_schema(p)).is_valid(value) == ok


@pytest.mark.parametrize('entity, required', [('creator', True), ('contributor', False),
                                              ('matcore/record-author', True)])
def test_creator_and_contributor_follow_0014(entity, required):
    """creator and contributor carry scheme-tagged identifiers and affiliations that hold their own
    identifier (0014 item 1); each keeps its own required flag (contributor is optional, 0011).

    An affiliation and its identifier sit in one container, so they cannot come apart; each identifier
    names its scheme, so a validator knows which rule its value follows.

    entity (str): the property's name; required (bool): whether a dataset must have one.
    """
    first, *rest = entity.split('/')
    prop = minimal(first)
    for n in rest:
        prop = sub(prop, n)
    name = ('name', True, False, 'string', (), ())
    value = ('value', True, False, 'string', (), ())
    entity_scheme = ('scheme', True, False, 'string', ('ORCID', 'ROR', 'DOI', 'SWHID', 'ISNI'), ())
    affiliation_scheme = ('scheme', True, False, 'string', ('ROR', 'ISNI'), ())
    identifier = ('identifier', False, True, None, (), (value, entity_scheme))
    affiliation = ('affiliation', False, True, None, (), (
        name, ('identifier', False, False, None, (), (value, affiliation_scheme))))
    assert tree(prop) == (entity.split('/')[-1], required, True, None, (), (name, identifier, affiliation))
    assert legacy_fields(prop) == []


def sub(p, name):
    """Return the subproperty of p with the given name.

    p (dict): property entry; name (str): the subproperty's name.
    """
    return next(s for s in p['subproperties'] if s['name'] == name)


FORMS = ('2D material', 'Bulk', 'Chain', 'Cluster', 'Molecule', 'Monolayer', 'Nanoparticle', 'Nanoribbon',
         'Nanotube', 'Nanowire', 'Slab', 'Thin film')
ROLES = ('Adsorbate', 'Core', 'Film', 'Inclusion', 'Layer', 'Matrix', 'Shell', 'Solute', 'Solvent', 'Substrate')
PHASES = ('Amorphous', 'Single crystal', 'Polycrystal', 'Quasicrystal', 'Liquid', 'Gas', 'Plasma')


def material_component():
    """Return minimal structure › material-component."""
    return sub(minimal('structure'), 'material-component')


# 0034: a component's composition is one formula, with the variables it uses and, where the formula is
# ambiguous, the topology of its isomers or polymorphs.
COMPOSITION = (
    ('formula', True, False, 'string', (), ()),
    ('variable', False, True, None, (), (
        ('name', True, False, 'string', (), ()), ('value', True, False, 'float', (), ()),
        ('qualifier', True, False, 'string', ('Average', 'Final', 'Initial', 'Maximum', 'Minimum'), ()))),
    ('topology', False, True, None, (), (
        ('substance', True, False, 'string', (), ()),
        ('identifier', True, True, None, (), (
            ('value', True, False, 'string', (), ()), ('scheme', True, False, 'string', ('AFLOW', 'InChI', 'SMILES'), ()))))))


def test_structure_is_made_of_components_with_a_form_and_a_role():
    """A dataset models one or more structures, each made of material components; a composite has no single
    form, so each component carries its own form, and its role says how it combines with the others (a
    film on a substrate, an inclusion in a matrix). A component may have several phases, each a separate
    entry, so phase is singular (0025)."""
    p = minimal('structure')
    component = ('material-component', True, True, None, (), (
        *COMPOSITION, ('form', True, False, 'string', FORMS, ()), ('role', False, False, 'string', ROLES, ()),
        ('fraction', False, True, None, (), (
            ('value', True, False, 'float', (), ()), ('qualifier', False, False, 'string', QUALIFIERS, ()))),
        ('phase', False, True, 'string', PHASES, ()),
        ('description', False, False, 'string', (), ()), ('microstructure', False, False, 'string', (), ())))
    assert tree(p) == ('structure', True, True, None, (), (
        ('label', True, False, 'string', (), ()), ('description', False, False, 'string', (), ()), component))
    assert sub(material_component(), 'phase')['extent'] == []
    assert legacy_fields(p) == []
    assert not any(q['name'] == 'material-component'
                   for q in yaml.safe_load(open(ROOT / 'schema/minimal.yaml'))['properties'])


def test_structure_notes_define_every_term_and_state_the_rules():
    """Every form, role and phase is defined in its note; a structure of layers is described by roles, not
    by form terms, and a molecule has no phase (0025)."""
    form = sub(material_component(), 'form')['values']['note']
    role = sub(material_component(), 'role')['values']['note']
    phase = sub(material_component(), 'phase')['values']['note']
    assert all(f'"{t}" –' in form for t in FORMS) and form.endswith('a substrate modeled as a slab is a Slab.')
    assert not any(f'"{t}"' in form for t in ('Surface', 'Interface', 'Heterostructure', 'Superlattice'))
    assert all(f'"{t}" –' in role for t in ROLES)
    assert role.endswith('Give a role for each component when the structure has more than one.')
    assert all(f'"{t}" –' in phase for t in PHASES)
    assert '"Crystal"' not in phase and '"Molecule"' not in phase
    assert '"Gas" – A state where' in phase and phase.endswith('Omit for a component whose form is Molecule.')
    assert ('"Quasicrystal" – A solid material with long-range order but without translational periodicity, e.g. '
            'one whose diffraction pattern shows five-fold rotational symmetry.') in phase
    assert 'short-range order' not in phase


@pytest.mark.parametrize('value, ok', [(0, True), (0.05, True), (1, True), (-0.1, False), (5, False)])
def test_fraction_is_an_atomic_fraction_of_the_structure(value, ok):
    """fraction is the share of the structure's atoms in one component, a pure number from 0 to 1 with no
    unit, given as qualified entries when it changes; the fractions of a structure sum to 1, for the
    unqualified entries and for each of Initial, Final and Average (0025; 0035 item 5).

    value (float): a candidate fraction; ok (bool): whether it conforms.
    """
    f = sub(material_component(), 'fraction')
    assert tree(f) == ('fraction', False, True, None, (), (
        ('value', True, False, 'float', (), ()), ('qualifier', False, False, 'string', QUALIFIERS, ())))
    v = datum(f)
    assert (v['kind'], v['extent'], v['recommended-unit']) == ('dimensionless', [], None)
    assert 'atomic fraction' in f['description']
    assert v['values']['note'] == ("The fractions of a structure's components sum to 1, for the entries without a "
                                   'qualifier and for each of Initial, Final and Average.')
    assert Draft202012Validator(value_schema(v)).is_valid(value) == ok


def test_formula_note_states_the_grammar_and_its_examples_parse():
    """The note gives the rules a writer must follow (0034 item 3), and every example in the schema parses,
    so the page shows only formulas a validator accepts."""
    from check_formula import formula_errors
    f = sub(material_component(), 'formula')
    assert (f['type'], f['extent'], f['kind'], f['recommended-unit']) == ('string', [], 'inapplicable', None)
    note = f['values']['note']
    for rule in ('`J` followed by lowercase letters', 'A count of 1 is omitted.', 'sum to 1',
                 'only when the composition varies', 'any order', 'molecular formula'):
        assert rule in note, rule
    assert {'Si0.7Ge0.3', 'Si{x}Ge{1-x}', '(H2O)0.9(C2H6O)0.1', 'Ja0.8Jb0.2'} <= set(f['values']['examples'])
    assert all(formula_errors(e) == [] for e in f['values']['examples'])


@pytest.mark.parametrize('value, ok', [('x', True), ('y', True), ('X', False), ('xy', False), ('1', False)])
def test_a_variable_is_one_lowercase_letter(value, ok):
    """A variable's name is one lowercase letter, as the formula writes it in braces (0034 item 2).

    value (str): a candidate name; ok (bool): whether it conforms.
    """
    n = sub(sub(material_component(), 'variable'), 'name')
    assert Draft202012Validator(value_schema(n)).is_valid(value) == ok
    val = sub(sub(material_component(), 'variable'), 'value')
    assert (val['kind'], val['extent'], val['recommended-unit']) == ('dimensionless', [], None)


def test_formula_is_named_once():
    """Only the component's composition is called formula; topology names its substance (0034, third
    amendment)."""
    def names(p):
        """Return the names of p and all its subproperties, at every depth.

        p (dict): property entry.
        """
        return [p['name']] + [n for s in p.get('subproperties') or [] for n in names(s)]
    assert names(material_component()).count('formula') == 1


def test_topology_says_when_to_give_it():
    """topology is given only when the formula alone is ambiguous, for molecular isomers and crystal
    polymorphs alike (0034, second amendment)."""
    t = sub(material_component(), 'topology')
    assert t['notes'] == ['Note: Give topology only when the formula matches more than one isomer or polymorph '
                          'and the data must say which, e.g. ethanol and dimethyl ether (C2H6O), or calcite and '
                          'aragonite (CaCO3).']
    note = sub(sub(t, 'identifier'), 'scheme')['values']['note']
    assert 'InChI is preferred' in note and 'AFLOW prototype label' in note


def test_constituent_is_gone():
    """The element-and-fraction constituent is replaced by the formula (0034 item 1)."""
    assert 'constituent' not in [s['name'] for s in material_component()['subproperties']]


QUALIFIERS = ('Average', 'Final', 'Initial', 'Maximum', 'Minimum')
QUALIFIER_NOTE = ('Without a qualifier, the value holds throughout the simulation and across the system, and the '
                  'entry is the only one for the condition. Otherwise give one entry for each qualifier that '
                  'applies, e.g. Initial and Final for a ramp, Minimum and Maximum for a range. For a vector or '
                  'tensor, Minimum and Maximum are taken component by component.')


# 0001 Part A, A2.2: the Kind and recommended unit of each simulation condition, with the shape its
# baseline values text gives (three cell vectors of three components, six tensor components, ...).
SIMULATION_CONDITIONS = {
    'number-of-particles': ('int', [], 'dimensionless', None),
    'net-charge': ('float', [], 'ElectricCharge', 'e'),
    'volume': ('float', [], 'Volume', 'angstrom^3'),
    'mass-density': ('float', [], 'MassDensity', 'kg/m^3'),
    'cell': ('float', [3, 3], 'Length', 'angstrom'),
    'cell-reference': ('float', [3, 3], 'Length', 'angstrom'),
    'cell-periodicity': ('bool', [3], 'inapplicable', None),
    'temperature': ('float', [], 'Temperature', 'K'),
    'stress': ('float', [6], 'Pressure', 'GPa'),
    'strain': ('float', [6], 'dimensionless', None),
    'strain-rate': ('float', [6], 'InverseTime', '1/s'),
    'heat-flux': ('float', [3], 'HeatFluxDensity', 'W/m^2'),
    'temperature-gradient': ('float', [3], 'TemperatureGradient', 'K/m'),
    'electric-field': ('float', [3], 'ElectricFieldStrength', 'V/m'),
    'magnetic-field': ('float', [3], 'MagneticFluxDensity', 'T'),
    'body-force': ('float', [3], 'Acceleration', 'm/s^2'),
    'electrode-potential': ('float', [], 'ElectricPotential', 'V'),
    'chemical-potential': ('float', [], 'Energy', 'eV'),
}


def datum(p):
    """Return the leaf that holds a property's value: the property itself, or its `value` (0015, amended).

    p (dict): property entry.
    """
    return sub(p, 'value') if p.get('subproperties') else p


def test_simulation_conditions_follow_0001_part_a():
    """Each imposed condition has the Kind, recommended unit and shape 0001 A2.2 gives it, so a value
    can be read without a default unit; type and description are plain strings. A condition with a
    physical Kind holds them in its `value`, beside a `unit`; a pure number is a leaf (0015, amended)."""
    sc = sub(minimal('computation'), 'conditions')
    got = {s['name']: (d['type'], d['extent'], d['kind'], d['recommended-unit'])
           for s in sc['subproperties'] if s['name'] != 'type' for d in [datum(s)]}
    assert got == SIMULATION_CONDITIONS | {'description': ('string', [], 'inapplicable', None)}


def test_computation_restores_the_docx_notation():
    """The tensor and vector notation of the .docx survives: subscripts, the dot of the strain rate Ė,
    and ASCII bars for vector lengths (the migration had flattened them)."""
    sc = sub(minimal('computation'), 'conditions')
    note = lambda n: datum(sub(sc, n))['values']['note']
    assert '<i>σ</i><sub>11</sub>' in note('stress') and '<i>E</i><sub>11</sub>' in note('strain')
    assert '<i>Ė</i><sub>11</sub>' in note('strain-rate') and 'Ė' in note('strain-rate')
    assert '|a|' in note('cell') and '│' not in note('cell') + note('cell-reference')
    assert 'a<sub>0</sub>' in note('cell-reference')
    assert legacy_fields(minimal('computation')) == []


def test_publication_structure():
    """A publication describing the dataset is a repeatable container of a required reference and an optional
    doi and link, all plain strings; the link is a URI. The dataset's own location is a separate property
    (0029)."""
    c = minimal('publication')
    assert 'citation' not in [p['name'] for p in yaml.safe_load(open(ROOT / 'schema/minimal.yaml'))['properties']]
    assert c['notes'] == ['Note: The location where the dataset itself is stored is given in `dataset-location`.']
    assert tree(c) == ('publication', False, True, None, (), (
        ('reference', True, False, 'string', (), ()),
        ('doi', False, False, 'string', (), ()),
        ('link', False, False, 'string', (), ())))
    assert sub(c, 'link')['values']['format'] == 'uri'
    assert legacy_fields(c) == []


def doi_properties():
    """Return every property named doi in the section files, with its location.

    Returns list[tuple[str, dict]]: the section/path and the property entry.
    """
    out = []
    for f in sorted((ROOT / 'schema').glob('*.yaml')):
        doc = yaml.safe_load(f.read_text())
        stack = [(f.stem, p) for p in doc.get('properties') or []] if 'section' in doc else []
        while stack:
            path, p = stack.pop()
            here = f"{path}/{p['name']}"
            if p['name'] == 'doi':
                out.append((here, p))
            stack += [(here, s) for s in p.get('subproperties') or []]
    return out


def test_every_typed_doi_uses_the_annex_i_pattern():
    """A DOI is written one way everywhere: the pattern of Annex I's DOI entry, copied exactly, so no
    copy drifts from the table (0014, settled 2026-11-04)."""
    pattern = yaml.safe_load((ROOT / 'schema/identifier-schemes.yaml').read_text())['schemes']['DOI']['pattern']
    dois = doi_properties()
    assert len(dois) == 4 and {'minimal/publication/doi', 'minimal/dataset-location/doi'} <= {h for h, _ in dois}
    for here, p in dois:
        if p['type'] is not None:
            assert (p['type'], p['extent'], p['kind']) == ('string', [], 'inapplicable'), here
            assert p['values']['pattern'] == pattern, here


@pytest.mark.parametrize('value, ok', [('https://doi.org/10.1000/182', True),
                                       ('https://doi.org/10.1103/PhysRevX.8.041048', True),
                                       ('10.1000/182', False), ('doi:10.1000/182', False),
                                       ('http://dx.doi.org/10.1000/182', False)])
def test_publication_doi_is_the_https_uri(value, ok):
    """Only the https URI form at doi.org conforms; the bare and legacy forms do not."""
    check = Draft202012Validator(value_schema(sub(minimal('publication'), 'doi')))
    assert check.is_valid(value) == ok


def test_funding_structure():
    """A funding entry names its award and its funder; the funder has the structure of an affiliation, a
    name with at most one ROR or ISNI identifier, since the Crossref Open Funder Registry moves into ROR
    (0014, settled 2026-11-04)."""
    f = minimal('funding')
    value = ('value', True, False, 'string', (), ())
    identifier = ('identifier', False, False, None, (), (value, ('scheme', True, False, 'string', ('ROR', 'ISNI'), ())))
    assert tree(f) == ('funding', False, True, None, (), (
        ('award-title', False, False, 'string', (), ()),
        ('funder', True, False, None, (), (('name', True, False, 'string', (), ()), identifier)),
        ('award-number', False, False, 'string', (), ())))
    affiliation = sub(minimal('creator'), 'affiliation')
    assert tree(sub(sub(f, 'funder'), 'identifier')) == tree(sub(affiliation, 'identifier'))
    assert legacy_fields(f) == []


def test_funder_identifier_example_is_a_valid_ror_id():
    """The example funder identifier passes Annex I's ROR pattern and check digits, so it shows a value a
    validator accepts."""
    from check_identifiers import identifier_errors
    v = sub(sub(sub(minimal('funding'), 'funder'), 'identifier'), 'value')
    assert v['values']['examples'] == ['https://ror.org/021nxhr62']
    assert identifier_errors('ROR', v['values']['examples'][0]) == []


def test_related_content_structure():
    """Each related-content entry points to one related dataset, since the entry itself repeats: a
    required link in the form of publication's link (a URI), and an optional description."""
    r = minimal('related-content')
    assert tree(r) == ('related-content', False, True, None, (), (
        ('link', True, False, 'string', (), ()),
        ('description', False, False, 'string', (), ())))
    link = sub(r, 'link')
    assert (link['extent'], link['kind']) == ([], 'inapplicable')
    assert link['values']['format'] == sub(minimal('publication'), 'link')['values']['format'] == 'uri'
    assert legacy_fields(r) == []
    assert 'examples' not in link['values']


def test_dataset_location_says_where_the_dataset_is_stored():
    """A dataset may be stored in, or mirrored across, repositories; each location names its repository and
    gives the dataset's DOI there and a required link. The property is optional, since metadata may
    accompany the dataset itself (0029)."""
    d = minimal('dataset-location')
    names = [p['name'] for p in yaml.safe_load(open(ROOT / 'schema/minimal.yaml'))['properties']]
    assert names.index('dataset-location') == names.index('publication') + 1
    assert tree(d) == ('dataset-location', False, True, None, (), (
        ('repository', False, False, 'string', (), ()),
        ('doi', False, False, 'string', (), ()),
        ('link', True, False, 'string', (), ())))
    assert d['notes'] == ['Note: Omit when the metadata accompanies the dataset itself.']
    assert sub(d, 'link')['values']['format'] == 'uri'
    assert sub(d, 'doi')['values']['examples'] == ['https://doi.org/10.17863/CAM.65004']


@pytest.mark.parametrize('value, ok', [('https://doi.org/10.17863/CAM.65004', True),
                                       (['https://doi.org/10.17863/CAM.65004'], False),
                                       ('mc-ad83jsd3-1', False)])
def test_related_content_link_is_one_uri(value, ok):
    """A link is one URI, not a list, and a bare MatCore ID is not a URI.

    value (str | list): a candidate link; ok (bool): whether it conforms.
    """
    check = Draft202012Validator(value_schema(sub(minimal('related-content'), 'link')),
                                 format_checker=Draft202012Validator.FORMAT_CHECKER)
    assert check.is_valid(value) == ok


# SPDX 2.3.1 §8.4 (File checksum field), Table 39: the checksum algorithms SPDX names.
SPDX_CHECKSUM_ALGORITHMS = ['SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512', 'SHA3-256', 'SHA3-384', 'SHA3-512',
                            'BLAKE2b-256', 'BLAKE2b-384', 'BLAKE2b-512', 'BLAKE3', 'MD2', 'MD4', 'MD5', 'MD6',
                            'ADLER32']


def test_provenance_structure():
    """A provenance event says what changed, when and by whom, with an optional comment and the files it
    touched; each file holds its checksums, each naming its algorithm so it can be verified, and a file with
    several checksums gives its name once (0032)."""
    p = minimal('provenance')
    checksum = ('checksum', True, True, None, (), (
        ('algorithm', True, False, 'string', tuple(SPDX_CHECKSUM_ALGORITHMS), ()),
        ('value', True, False, 'string', (), ())))
    file = ('file', False, True, None, (), (('name', True, False, 'string', (), ()), checksum))
    assert tree(p) == ('provenance', False, True, None, (), (
        ('event-type', True, False, 'string', ('Initial creation', 'Admin update', 'Version update',
                                               'Metadata update'), ()),
        ('date', True, False, 'string', (), ()),
        tree(sub(p, 'agent')),
        ('comment', False, False, 'string', (), ()),
        file))
    assert legacy_fields(p) == []


def test_provenance_is_recommended_and_its_agent_is_described_like_a_creator():
    """Provenance is optional but recommended; the entity that made a change is described as a creator is, with
    a name, scheme-tagged identifiers and affiliations, and several may make one change (0030)."""
    p = minimal('provenance')
    assert p['notes'] == ['Note: It is recommended to record the provenance of the dataset and to keep it '
                          'current with each change.']
    agent, creator = sub(p, 'agent'), minimal('creator')
    assert tree(agent)[1:] == tree(creator)[1:]
    assert sub(agent, 'name')['description'] == 'The name of the entity that made the change.'
    assert sub(sub(agent, 'identifier'), 'scheme')['values'] == sub(sub(creator, 'identifier'), 'scheme')['values']


def test_provenance_date_takes_the_creation_date_forms():
    """An event's date is written as the dataset's creation date is, with the same pattern, examples and
    note, so one rule reads both."""
    assert sub(minimal('provenance'), 'date')['values'] == minimal('creation-date')['values']


@pytest.mark.parametrize('value, ok', [('9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', True),
                                       ('da39a3ee5e6b4b0d3255bfef95601890afd80709', True),
                                       ('9F86D081884C7D65', False), ('sha256:9f86d081', False), ('', False)])
def test_checksum_value_is_lowercase_hexadecimal(value, ok):
    """A checksum value is written as SPDX writes it, in lowercase hexadecimal digits.

    value (str): a candidate checksum; ok (bool): whether it conforms.
    """
    v = sub(sub(sub(minimal('provenance'), 'file'), 'checksum'), 'value')
    assert Draft202012Validator(value_schema(v)).is_valid(value) == ok


def test_matcore_gathers_the_record_information():
    """One required container says which standard the record follows, which dataset and version it describes,
    and who wrote it when; it replaces matcore-id, matcore-author and matcore-date at their place (0045)."""
    names = [p['name'] for p in yaml.safe_load(open(ROOT / 'schema/minimal.yaml'))['properties']]
    assert not {'matcore-id', 'matcore-author', 'matcore-date'} & set(names)
    assert names.index('matcore') == names.index('provenance') + 1
    m = minimal('matcore')
    assert [(s['name'], s['required'], s['repeatable']) for s in m['subproperties']] == [
        ('standard-version', True, False), ('standard-link', False, False), ('id', True, False),
        ('dataset-version', True, False), ('record-author', True, True), ('creation-date', True, False)]
    assert (m['required'], m['repeatable']) == (True, False)
    assert sub(m, 'standard-link')['values']['format'] == 'uri'
    assert sub(m, 'id')['description'] == 'An identifier of the dataset, the same for all its versions.'
    v = sub(m, 'dataset-version')
    assert (v['type'], v['kind'], v['values']['minimum']) == ('int', 'dimensionless', 1)
    assert v['notes'][0].endswith('When provenance is given, dataset-version is 1 more than the number of Version '
                                  'update events.')
    c, top = sub(m, 'creation-date'), minimal('creation-date')
    assert [c[k] for k in ('type', 'extent', 'kind', 'recommended-unit', 'values')] == \
           [top[k] for k in ('type', 'extent', 'kind', 'recommended-unit', 'values')]
    assert legacy_fields(m) == []


@pytest.mark.parametrize('value, ok', [('0.6.0', True), ('1.10.2', True), ('0.6', False), ('v0.6.0', False),
                                       ('01.6.0', False), ('0.6.0-dev', False)])
def test_standard_version_is_a_release_number(value, ok):
    """The standard version is written as releases.yaml writes a release, MAJOR.MINOR.PATCH (0010; 0045).

    value (str): a candidate version; ok (bool): whether it conforms.
    """
    v = sub(minimal('matcore'), 'standard-version')
    assert Draft202012Validator(value_schema(v)).is_valid(value) == ok


def test_license_entries_name_an_spdx_expression_or_a_custom_license():
    """A dataset may have several licenses, each applying to its part; each entry gives an SPDX expression of
    short identifiers, or a LicenseRef- with the custom license's name and a link to its text. The SPDX
    License List changes every few months, so the note names the forms instead of the schema copying the
    list (0031)."""
    p = minimal('license')
    assert tree(p) == ('license', True, True, None, (), (
        ('identifier', True, False, 'string', (), ()),
        ('name', False, False, 'string', (), ()),
        ('link', False, False, 'string', (), ()),
        ('applies-to', False, False, 'string', (), ())))
    ident = sub(p, 'identifier')['values']
    assert ident['examples'] == ['CC-BY-4.0', 'CC0-1.0', 'LicenseRef-NIST-data']
    assert 'terms' not in ident and 'enum' not in ident
    assert sub(p, 'link')['values']['format'] == 'uri'
    note = p['notes'][0]
    assert 'https://spdx.org/licenses/' in note and '`CC-BY-4.0 OR CC0-1.0`' in note
    assert 'Give the SPDX short identifier, not the license\'s full name' in note
    assert 'with its `name` and a `link` to its full text, both required in this case' in note
    assert 'GPL' not in note and 'MIT' not in note
    assert legacy_fields(p) == []


def test_minimal_is_complete():
    """Every typed field of the minimal section is filled, so it declares itself complete (0004 item 36)."""
    doc = yaml.safe_load(open(ROOT / 'schema/minimal.yaml'))
    assert doc.get('legacy_complete') is True
    assert [k for p in doc['properties'] for k in legacy_fields(p)] == []


def dft(name):
    """Return a property of schema/dft.yaml's settings block (0046 item 7).

    name (str): the property's name.
    """
    settings = yaml.safe_load(open(ROOT / 'schema/dft.yaml'))['properties'][0]
    return next(p for p in settings['subproperties'] if p['name'] == name)


def test_xc_functional_structure():
    """A calculation names each exchange-correlation functional by its form, with optional prose and
    parameters; the parameter is a generic parameter, since the schema cannot know which a functional
    uses (0016)."""
    from check_generic import generic_errors
    xc = dft('xc-functional')
    param = ('xc-parameter', False, True, None, (), (
        ('name', True, False, 'string', (), ()), ('value', True, False, 'any', (), ()),
        ('unit', True, False, 'string', (), ()), ('description', False, False, 'string', (), ())))
    normalization = ('normalization', False, False, None, (), (
        ('components', True, False, 'string', (), ()), ('source', True, False, 'string', ('LibXC',), ())))
    assert tree(xc) == ('xc-functional', True, True, None, (), (
        ('type', True, False, 'string', ('LDA', 'GGA', 'Meta GGA', 'Hybrid', 'ML'), ()),
        ('name', False, False, 'string', (), ()),
        ('description', False, False, 'string', (), ()), normalization, param))
    assert generic_errors(sub(xc, 'xc-parameter')) == []
    assert legacy_fields(xc) == []


def test_xc_functional_name_lists_the_named_functionals_and_description_is_prose():
    """The named functionals by family are examples of `name`, so its note lists them and points to the
    normalization; `description` is free text for what `type` and `name` do not say (0024)."""
    xc = dft('xc-functional')
    name_values = sub(xc, 'name')['values']
    assert 'examples' not in name_values  # the note's list names PBE and HSE06; a second "Examples:" repeats it
    name_note = ' '.join(name_values['note'].split())
    assert name_note.startswith('Examples of possible content by type: LDA: Common parameterizations: VWN')
    assert 'GGA: Typical choices are PW91, PBE' in name_note and 'is given in normalization.' in name_note
    assert sub(xc, 'description')['values']['note'] == (
        'Free text on what `type` and `name` do not say, e.g. a modification of the functional or the reason '
        'for choosing it.')
    import json
    example = json.loads((ROOT / 'examples/dft.json').read_text(encoding='utf-8'))['dft']['settings'][0]['xc-functional'][0]
    assert list(example)[:3] == ['type', 'name', 'description'] and example['name'] == 'PW91'


def test_xc_functional_keeps_the_name_beside_its_normalization():
    """The functional is kept as the author names it (e.g. PBE), and a normalized decomposition, if given,
    always names its source, so the two never stand without each other's context (0017)."""
    xc = dft('xc-functional')
    name, norm = sub(xc, 'name'), sub(xc, 'normalization')
    assert (name['extent'], name['kind']) == ([], 'inapplicable')
    components = sub(norm, 'components')
    assert (components['extent'], components['kind']) == ([':'], 'inapplicable')
    assert components['values']['examples'] == [['GGA_X_PBE', 'GGA_C_PBE']]
    assert sub(norm, 'source')['values']['terms'] == ['LibXC']


def test_core_electron_treatment_structure():
    """The core-electron treatment names its method and, for pseudopotential methods, each pseudopotential: its
    name and form, how many electrons it treats explicitly, where it came from, and what identifies it."""
    c = dft('core-electron-treatment')
    count = ('number-of-valence-electrons', True, False, 'int', (), ())
    file = ('file', False, False, None, (), tuple(tree(s) for s in sub(minimal('provenance'), 'file')['subproperties']))
    pseudopotential = ('pseudopotential-or-paw', False, True, None, (), (
        ('name', True, False, 'string', (), ()), ('species', True, False, 'string', (), ()),
        ('type', True, False, 'string', ('Norm conserving', 'PAW', 'Ultrasoft'), ()),
        ('description', False, False, 'string', (), ()), count,
        ('repository', False, False, 'string', (), ()), ('version', False, False, 'string', (), ()),
        ('doi', False, False, 'string', (), ()), file,
        ('unique-identifier', False, False, 'string', (), ())))
    assert tree(c) == ('core-electron-treatment', True, False, None, (), (
        ('type', True, False, 'string', ('All-electron', 'PAW', 'Pseudopotential'), ()), pseudopotential))
    assert legacy_fields(c) == []


def test_pseudopotential_or_paw_names_both_in_every_text():
    """A PAW dataset is described in the same container as a pseudopotential, so no description or note
    of the container names the pseudopotential alone (0021)."""
    def texts(p):
        """Yield the description and notes of p and of every subproperty below it.

        p (dict): property entry.
        """
        yield p['description']
        yield from p.get('notes') or []
        for s in p.get('subproperties') or []:
            yield from texts(s)
    pp = sub(dft('core-electron-treatment'), 'pseudopotential-or-paw')
    alone = [t for t in texts(pp) if 'pseudopotential' in t.replace('pseudopotential or PAW', '')
             .replace('Pseudopotential', '')]
    assert alone == []


def test_pseudopotential_file_is_provenance_file():
    """A pseudopotential's file is written exactly as a provenance file (name, then checksums of an algorithm
    with the SPDX names and a value in lowercase hex), so one rule reads both (0032)."""
    p = sub(sub(dft('core-electron-treatment'), 'pseudopotential-or-paw'), 'file')
    assert p['subproperties'] == sub(minimal('provenance'), 'file')['subproperties']


def test_checksum_and_unique_identifier_point_to_each_other():
    """A checksum and any other designation are kept apart: each note sends the reader to the other."""
    pp = sub(dft('core-electron-treatment'), 'pseudopotential-or-paw')
    assert sub(pp, 'file')['notes'][0].startswith('Note: Use file when')
    assert 'use unique-identifier' in sub(pp, 'file')['notes'][0]
    assert sub(pp, 'unique-identifier')['notes'][0].endswith('use file instead.')
    assert 'hash' not in sub(pp, 'unique-identifier')['description'].lower()


@pytest.mark.parametrize('value, ok', [(1, True), (4, True), (19, True), (0, False), (4.0, True), (4.5, False)])
def test_number_of_valence_electrons_is_a_positive_count(value, ok):
    """A pseudopotential treats at least one electron explicitly.

    value (int | float): a candidate count; ok (bool): whether it conforms.
    """
    v = sub(sub(dft('core-electron-treatment'), 'pseudopotential-or-paw'), 'number-of-valence-electrons')
    assert (v['kind'], v['recommended-unit']) == ('dimensionless', None)
    assert Draft202012Validator(value_schema(v)).is_valid(value) == ok


def test_wavefunction_representation_structure():
    """The wavefunction representation names its types, the localized-orbital basis sets used, and the
    plane-wave cutoffs; a basis set is identified as a pseudopotential is, by checksum or other token."""
    v = dft('wavefunction-representation')
    file = ('file', False, False, None, (), tuple(tree(s) for s in sub(minimal('provenance'), 'file')['subproperties']))
    basis = ('localized-orbital-basis-set', False, True, None, (), (
        ('type', True, False, 'string', (), ()), ('species', False, True, 'string', (), ()),
        ('repository', False, False, 'string', (), ()),
        ('version', False, False, 'string', (), ()), ('doi', False, False, 'string', (), ()), file,
        ('unique-identifier', False, False, 'string', (), ())))
    cutoff = lambda n: (n, False, False, None, (), (('value', True, False, 'float', (), ()),
                                                    ('unit', True, False, 'string', (), ())))
    assert tree(v) == ('wavefunction-representation', True, False, None, (), (
        ('type', True, True, 'string', (
            'Gaussian basis sets', 'LAPW', 'Local atomic orbitals', 'Numerical atomic orbitals', 'Plane waves',
            'Real space grids'), ()), basis,
        cutoff('kinetic-energy-cutoff'), ('lapw-basis-cutoff', False, False, 'float', (), ()),
        cutoff('charge-density-cutoff')))
    assert legacy_fields(v) == []


def test_representation_note_groups_every_term():
    """The note numbers the three groups of 0018 and explains every representation term, so no term is
    listed without a meaning."""
    t = sub(dft('wavefunction-representation'), 'type')['values']
    assert t['terms'] == sorted(t['terms'])
    for mark in ('(1) Basis-function expansions:', '(2) Grid methods:', '(3) Augmented methods:'):
        assert mark in t['note']
    assert all(f'"{term}" –' in t['note'] for term in t['terms'])


@pytest.mark.parametrize('name, terms', [
    ('localized-orbital-basis-set', ['Gaussian basis sets', 'Local atomic orbitals', 'Numerical atomic orbitals']),
    ('kinetic-energy-cutoff', ['LAPW', 'Plane waves']), ('lapw-basis-cutoff', ['LAPW']),
    ('charge-density-cutoff', ['LAPW', 'Plane waves'])])
def test_conditional_subproperties_name_the_types_they_serve(name, terms):
    """A subproperty that applies to some representations names them, and each named one is a listed term.

    name (str): the subproperty; terms (list[str]): the types it serves.
    """
    w = dft('wavefunction-representation')
    listed = sub(w, 'type')['values']['terms']
    d = sub(w, name)['description']
    assert all(t in listed and f'"{t}"' in d for t in terms) and 'Localized orbitals' not in d


def test_basis_set_identifiers_match_the_pseudopotential_split():
    """The basis set's file is provenance's, and its two identifiers point to each other (0032)."""
    b = sub(dft('wavefunction-representation'), 'localized-orbital-basis-set')
    assert sub(b, 'file')['subproperties'] == sub(minimal('provenance'), 'file')['subproperties']
    assert sub(b, 'file')['notes'][0].startswith('Note: Use file when')
    assert sub(b, 'unique-identifier')['notes'][0].endswith('use file instead.')


@pytest.mark.parametrize('name', ['kinetic-energy-cutoff', 'charge-density-cutoff'])
def test_cutoffs_are_energies(name):
    """Each plane-wave cutoff is an energy, recommended in eV (0001 A3.1), and not negative.

    name (str): the cutoff's name.
    """
    v = sub(sub(dft('wavefunction-representation'), name), 'value')
    assert (v['extent'], v['kind'], v['recommended-unit']) == ([], 'Energy', 'eV')
    assert v['values']['minimum'] == 0


def test_scf_convergence_structure():
    """The SCF loop records how the density is mixed, how the orbitals are obtained (several methods may
    be combined), and the tolerance with the quantity it applies to (0019, 0020)."""
    s = dft('self-consistent-field-convergence')
    tolerance = ('tolerance', True, False, None, (), (
        ('criterion', True, False, 'string', ('Energy', 'Charge density', 'Potential'), ()),
        ('value', True, False, 'float', (), ()), ('unit', True, False, 'string', (), ())))
    assert tree(s) == ('self-consistent-field-convergence', False, False, None, (), (
        ('method-density', False, False, 'string', ('Simple mixing', 'Pulay mixing', 'DIIS', 'Broyden mixing'),
         ()),
        ('method-diagonalization', False, True, 'string', (
            'Car-Parrinello', 'Chebyshev filtering', 'Conjugate gradient', 'Davidson method',
            'Direct diagonalization', 'Lanczos', 'LOBPCG', 'RMM-DIIS'), ()), tolerance))
    assert legacy_fields(s) == []


def test_scf_tolerance_value_has_an_open_kind():
    """The tolerance's unit depends on the criterion, so its Kind is open, it has no recommended unit,
    and its unit is written as a generic parameter's (0019 items 1, 5)."""
    t = sub(dft('self-consistent-field-convergence'), 'tolerance')
    v, u = sub(t, 'value'), sub(t, 'unit')
    assert (v['extent'], v['kind'], v['recommended-unit'], v['values']['minimum']) == ([], 'any', None, 0)
    assert (u['description'], u['values']) == (UNIT_DESCRIPTION, {'note': UNIT_NOTE})


def test_diagonalization_note_defines_the_acronyms_and_car_parrinello():
    """Every acronym, and the one term that is not a diagonalization, is explained in the note (0020)."""
    note = sub(dft('self-consistent-field-convergence'), 'method-diagonalization')['values']['note']
    for term in ('Car-Parrinello', 'LOBPCG', 'RMM-DIIS'):
        assert f'"{term}" –' in note


def test_relaxation_tolerance_energy_is_an_energy():
    """The relaxation stops on a change in energy: a non-negative energy, recommended in eV, with
    its unit stated (0001 A3.1)."""
    r = dft('relaxation-tolerance-energy')
    assert tree(r) == ('relaxation-tolerance-energy', False, False, None, (), (
        ('value', True, False, 'float', (), ()), ('unit', True, False, 'string', (), ())))
    v = sub(r, 'value')
    assert (v['extent'], v['kind'], v['recommended-unit'], v['values']) == ([], 'Energy', 'eV', {'minimum': 0})
    assert legacy_fields(r) == []


def test_convergence_energy_is_the_free_energy_when_smeared():
    """With smeared occupations the forces derive from F = E − TS, so the relaxation's energy is F; without
    smearing it is E. The SCF criterion "Energy" uses the same definition (0023)."""
    r = dft('relaxation-tolerance-energy')
    assert r['description'] == 'Energy convergence criterion for atomic relaxation.'
    assert r['notes'] == ['Note: The energy is the Helmholtz free energy F = E − TS, including the entropy S of '
                          'the smeared electrons at the smearing temperature T, when occupations are smeared '
                          '(e.g. a metal), and the total energy E otherwise (e.g. an insulator). It is not the '
                          'energy extrapolated to zero smearing.',
                          "Note: Give it when the computation's task is Optimization."]
    criterion = sub(sub(dft('self-consistent-field-convergence'), 'tolerance'), 'criterion')
    assert ('"Energy" – The change in the energy between successive iterations, defined as for '
            '`relaxation-tolerance-energy`.') in ' '.join(criterion['values']['note'].split())


def test_relaxation_tolerance_forces_is_a_force():
    """The relaxation stops when the largest force falls below a bound: a non-negative force, recommended
    in eV/angstrom, with its unit stated (0001 A3.1)."""
    r = dft('relaxation-tolerance-forces')
    assert tree(r) == ('relaxation-tolerance-forces', False, False, None, (), (
        ('value', True, False, 'float', (), ()), ('unit', True, False, 'string', (), ())))
    v = sub(r, 'value')
    assert (v['extent'], v['kind'], v['recommended-unit'], v['values']) == (
        [], 'Force', 'eV/angstrom', {'minimum': 0})
    assert legacy_fields(r) == []


def test_dft_comment_is_free_text():
    """A DFT comment is free text that may be given several times, one remark per entry."""
    c = dft('comment')
    assert (c['required'], c['repeatable'], c['type'], c['extent'], c['kind'], c['recommended-unit'],
            c['values']) == (False, True, 'string', [], 'inapplicable', None, None)
    assert legacy_fields(c) == []


def test_dft_is_complete():
    """Every typed field of the dft section is filled, so it declares itself complete (0004 item 36)."""
    doc = yaml.safe_load(open(ROOT / 'schema/dft.yaml'))
    assert doc.get('legacy_complete') is True
    assert [k for p in doc['properties'] for k in legacy_fields(p)] == []


def test_calculation_physics_lists_the_added_phenomena():
    """Each phenomenon beyond a standard DFT calculation is one entry from an open vocabulary, so a
    calculation that includes several repeats the property."""
    p = dft('calculation-physics')
    terms = ('Collinear spin polarization', 'Noncollinear spin polarization', 'On-site correlation',
             'Orbital polarization', 'Spin-orbit coupling', 'Van der Waals')
    assert tree(p) == ('calculation-physics', False, True, 'string', terms, ())
    assert (p['extent'], p['kind']) == ([], 'inapplicable')
    assert legacy_fields(p) == []


def test_calculation_physics_note_defines_every_term_and_the_spin_rule():
    """Each term is explained so users read it alike, and the note says a calculation gives at most one
    of the two spin-polarization terms, which the schema cannot check (0022)."""
    p = dft('calculation-physics')
    note = p['values']['note']
    for term in p['values']['terms']:
        assert f'"{term}" – ' in note, term
    assert 'DFT+U' in note and 'Brooks' in note
    assert 'Give at most one of the two spin-polarization terms.' in note
    assert 'List each phenomenon as a separate entry' in note


def test_k_point_mesh_structure():
    """A k-point mesh is given by its kind and its explicit number of points, never also by a spacing that
    could contradict them, with fractional shifts (0004 item 47); the smearing is given beside it, since it
    concerns occupations, not the mesh (0053)."""
    from check_generic import generic_errors
    k = dft('k-point-mesh')
    number = lambda n, t: (n, False, False, None, (), (('value', True, False, t, (), ()),
                                                      ('unit', True, False, 'string', (), ())))
    param = ('parameter', False, True, None, (), (
        ('name', True, False, 'string', (), ()), ('value', True, False, 'any', (), ()),
        ('unit', True, False, 'string', (), ()), ('description', False, False, 'string', (), ())))
    assert tree(k) == ('k-point-mesh', False, False, None, (), (
        ('type', True, False, 'string', ('Regular gamma-centered', 'Regular shifted', 'Irregular'), ()),
        ('number-of-points', False, False, 'int', (), ()), ('shift', False, False, 'float', (), ())))
    smearing = dft('smearing')
    assert tree(smearing) == ('smearing', False, False, None, (), (
        ('type', False, False, 'string', ('None', 'None - tetrahedron', 'None - Blöchl-corrected tetrahedron',
                                          'Gaussian', 'Fermi-Dirac', 'Methfessel-Paxton', 'Marzari-Vanderbilt'), ()),
        number('width', 'float'), param))
    assert generic_errors(sub(smearing, 'parameter')) == []
    assert legacy_fields(k) == []


def test_k_point_mesh_quantities():
    """Three points counted along each reciprocal lattice vector (at least one), three fractional shifts,
    and a smearing width in eV (0001 A3.1; 0004 item 47)."""
    k = dft('k-point-mesh')
    v = lambda n: datum(sub(k, n))
    assert (v('number-of-points')['extent'], v('number-of-points')['kind'], v('number-of-points')['values']['minimum']) \
        == ([3], 'dimensionless', 1)
    assert (v('shift')['extent'], v('shift')['kind'], v('shift')['recommended-unit']) == ([3], 'dimensionless', None)
    assert sub(k, 'number-of-points').get('subproperties') is None and sub(k, 'shift').get('subproperties') is None
    assert 'fractions of the mesh spacing' in v('shift')['values']['note']
    width = datum(sub(dft('smearing'), 'width'))
    assert (width['kind'], width['recommended-unit']) == ('Energy', 'eV')


@pytest.mark.parametrize('name', [n for n in SIMULATION_CONDITIONS if n != 'cell-periodicity'])
def test_varying_conditions_are_qualified_entries(name):
    """Each numerical condition repeats, one entry per qualifier, so a tool reads a ramp or a range instead
    of prose; a pure number keeps no unit (0035 items 2 and 6).

    name (str): the condition.
    """
    c = sub(sub(minimal('computation'), 'conditions'), name)
    names = [s['name'] for s in c['subproperties']]
    unit = [] if datum(c)['kind'] == 'dimensionless' else ['unit']
    convention = {'electrode-potential': ['reference'], 'chemical-potential': ['species', 'relative-to']}.get(
        name, [])  # 0041, 0042
    assert c['repeatable'] and names == ['value', *unit, *convention, 'qualifier']
    q = sub(c, 'qualifier')
    note = QUALIFIER_NOTE.replace('the only one for the condition', 'the only one for the species') \
        if name == 'chemical-potential' else QUALIFIER_NOTE  # 0042
    assert (q['required'], q['values']['terms'], q['values']['note']) == (False, list(QUALIFIERS), note)
    if not unit:
        assert datum(c)['description'] == 'The value of the property.'


def test_varying_conditions_note_and_description():
    """The note and description say how a varying condition is given, as qualified entries, and the
    description says how it varies (0035 items 3 and 4); type's axes replace the flags (0036)."""
    sc = sub(minimal('computation'), 'conditions')
    description = sub(sc, 'description')['description']
    assert description.startswith('Explanatory text clarifying the simulation type, and how any condition varies')
    assert description.endswith('For a condition that varies, it states how, e.g. the shape of a ramp or the '
                                'region a value applies to.')
    assert sc['notes'][0].endswith('A condition that varies is given as several entries, each with a qualifier; '
                                   'the description explains how it varies.')
    assert 'representative value' not in sc['notes'][0]
    assert 'constant throughout' not in sub(sc, 'strain-rate')['description']
    assert not {'spatially-varying', 'time-varying'} & {s['name'] for s in sc['subproperties']}
    assert not sc['repeatable']
    assert not sub(sc, 'cell-periodicity')['repeatable']


@pytest.mark.parametrize('name, vector, rows', [
    ('cell', 'cell vector', 'a, b and c'),
    ('cell-reference', 'reference cell vector', 'a<sub>0</sub>, b<sub>0</sub> and c<sub>0</sub>')])
def test_cell_rows_are_the_vectors_in_cartesian_components(name, vector, rows):
    """Each row of the 3×3 value is one cell vector, in Cartesian components of the simulation's frame, not
    of the stress basis built from the cell itself (0038 items 2-4).

    name (str): the condition; vector (str): what each row is; rows (str): the rows, in order.
    """
    v = datum(sub(sub(minimal('computation'), 'conditions'), name))
    assert v['extent'] == [3, 3]
    assert (f'`value[i][j]` is the j-th Cartesian component, in the frame of the simulation, of the i-th {vector}, '
            f'so the rows are {rows}.') in v['values']['note']


# 0039: each simulation condition says what is imposed, in its own terms.
IMPOSED_DEFINITIONS = {
    'conditions': 'The conditions imposed on the simulated system during the computation, e.g. by a '
                  'thermostat, a barostat, a loading device or a fixed simulation cell. Omitted when no condition '
                  'is imposed, e.g. for a single point or a training computation.',
    'number-of-particles': 'The number of particles (atoms or other discrete entities) in the simulated system, as '
                           'imposed by the simulation.',
    'net-charge': 'The net electric charge of the simulated system, as imposed by the simulation, e.g. by fixing the '
                  'number of electrons of a charged defect or an ion, or the charge of an electrode.',
    'volume': 'The volume of the simulated system, as imposed by the simulation.',
    'mass-density': 'The mass density of the simulated system, as imposed by the simulation.',
    'cell': 'The simulation cell, as imposed by the simulation.',
    'cell-reference': 'The simulation cell in the reference configuration, relative to which strain and strain rate '
                      'are defined.',
    'cell-periodicity': 'Whether periodic boundary conditions are applied along each cell vector, for both cell and '
                        'cell-reference.',
    'temperature': 'The temperature imposed on the simulated system, e.g. by a thermostat or a heat bath in thermal '
                   'contact with it.',
    'stress': 'The stress, normal and shear components, imposed on the simulated system, e.g. by a barostat or an '
              'external loading device.',
    'strain': 'The strain imposed on the simulation cell relative to cell-reference, as the Lagrangian strain tensor.',
    'strain-rate': 'The strain rate imposed on the simulation cell relative to cell-reference, as the time derivative '
                   'of the Lagrangian strain tensor.',
    'heat-flux': 'The heat flux imposed on the simulated system, the thermal energy per unit area per unit time driven '
                 'through it, e.g. by exchanging energy between a heat source and a heat sink.',
    'temperature-gradient': 'The temperature gradient imposed on the simulated system, e.g. by thermostatting two '
                            'regions at different temperatures.',
    'electric-field': 'The electric field imposed on the simulated system, e.g. a uniform applied field.',
    'magnetic-field': 'The magnetic field imposed on the simulated system, given as the magnetic flux density '
                      '<i>B</i>.',
    'body-force': 'The body force per unit mass imposed on the simulated system, e.g. gravity or a constant force '
                  'driving a flow.',
    'electrode-potential': 'The potential of the working electrode imposed on the simulated system, e.g. by a '
                           'potentiostat in a constant-potential simulation, relative to the reference given in '
                           '`reference`.',
    'chemical-potential': 'The chemical potential of a species imposed on the simulated system by a reservoir, e.g. '
                          'in a grand-canonical or semi-grand-canonical simulation.',
}
SC_NOTE = ('Note: The conditions below, other than type and description, are given as appropriate to the simulation. '
           'Each is imposed on the simulation as an external constraint. A quantity computed from the simulation, e.g. '
           'a heat flux measured under an imposed temperature gradient or the temperature of a microcanonical run, is '
           'a result, not a condition, and is not given here. A condition that varies is given as several entries, '
           'each with a qualifier; the description explains how it varies.')
HEAT_NOTE = 'Note: Give heat-flux or temperature-gradient, whichever the simulation imposes; the other is a result.'
BASIS_NOTES = {
    'stress': 'Note 1: Requires cell, which defines the basis of the tensor components.',
    'strain': 'Note: Requires cell-reference, which defines the basis of the tensor components.',
    'strain-rate': 'Note: Requires cell-reference, which defines the basis of the tensor components.',
}


def test_simulation_conditions_are_defined_as_imposed():
    """A condition is a constraint the simulation imposes, not a quantity it measures, and each definition
    says so in the property's own terms (0039 items 1-5)."""
    sc = sub(minimal('computation'), 'conditions')
    got = {'conditions': sc['description']} | {
        s['name']: s['description'] for s in sc['subproperties'] if s['name'] in IMPOSED_DEFINITIONS}
    assert got == IMPOSED_DEFINITIONS
    assert sc['notes'] == [SC_NOTE]
    for name in ('heat-flux', 'temperature-gradient'):
        assert sub(sc, name)['notes'] == [HEAT_NOTE], name
    for name, note in BASIS_NOTES.items():
        assert sub(sc, name)['notes'][0] == note, name
    assert 'supercell' not in datum(sub(sc, 'cell'))['values']['note']
    assert 'heat flux vector <i>q</i>' in datum(sub(sc, 'heat-flux'))['values']['note']


@pytest.mark.parametrize('name, vector', [
    ('electric-field', 'electric field vector <i>E</i>'),
    ('magnetic-field', 'magnetic flux density vector <i>B</i>'),
    ('body-force', 'body force per unit mass <i>g</i>')])
def test_applied_fields_are_vectors_in_the_cell_basis(name, vector):
    """An applied field is a vector given in the orthonormal basis built from the cell, as the heat flux is, so
    it requires cell (0040 item 3).

    name (str): the condition; vector (str): the vector its value note names.
    """
    c = sub(sub(minimal('computation'), 'conditions'), name)
    note = datum(c)['values']['note']
    assert note.startswith(f'The components of the {vector}. ')
    assert 'where e<sub>1</sub> is in the direction of a' in note
    assert c['notes'] == ['Note: Requires cell, which defines the basis of the vector components.']


def test_electrode_potential_names_its_reference():
    """A potential means nothing without its reference, which a unit cannot express, so it is a required
    enumerated subproperty beside the value, each term defined (0041 item 3)."""
    c = sub(sub(minimal('computation'), 'conditions'), 'electrode-potential')
    r = sub(c, 'reference')
    assert (r['required'], r['repeatable'], r['type'], r['extent'], r['kind'], r['recommended-unit']) == (
        True, False, 'string', [], 'inapplicable', None)
    assert r['values']['terms'] == ['SHE', 'RHE', 'Vacuum']
    assert r['description'] == 'The reference against which the potential is given.'
    assert r['values']['note'] == ('One of: "SHE" – The standard hydrogen electrode. "RHE" – The reversible hydrogen '
                                   'electrode, at the pH of the simulation. "Vacuum" – The vacuum level, giving an '
                                   'absolute potential.')


def test_chemical_potential_names_its_species():
    """A chemical potential belongs to a species of the formula, and a semi-grand-canonical simulation imposes a
    difference between two; an absolute value depends on the model's energy zero (0042 item 1)."""
    c = sub(sub(minimal('computation'), 'conditions'), 'chemical-potential')
    for name, required in (('species', True), ('relative-to', False)):
        p = sub(c, name)
        assert (p['required'], p['repeatable'], p['type'], p['extent'], p['kind']) == (
            required, False, 'string', [], 'inapplicable'), name
    assert sub(c, 'species')['values']['examples'] == ['Cu', 'H2O', 'Ja']
    assert sub(c, 'relative-to')['notes'] == ['Note: Give relative-to when the simulation imposes a difference of '
                                              'chemical potentials, as a semi-grand-canonical simulation does.']
    note = datum(c)['values']['note']
    assert note.startswith('The chemical potential <i>μ</i> per particle, or the difference')
    assert 'named in `input` with the role Interaction model' in note and 'kJ/mol' in note
    from check_formula import formula_errors
    assert all(formula_errors(e) == [] for e in sub(c, 'species')['values']['examples'])


SOFTWARE_ROLES = ('Calculation method', 'Interaction model', 'Script', 'Simulation code', 'Workflow framework')
DEPENDENCY_ROLES = ('Compiler', 'FFT library', 'Interpreter', 'Library', 'Linear algebra library', 'MPI library')


def test_software_is_one_entry_per_layer():
    """Every layer that took part (a calculation method or workflow, the simulation code it drives, a custom
    script) is a software entry with a role; each is identified exactly, lists the components that can
    change its results, and holds the files it reads (0043 items 1-3)."""
    sw = sub(minimal('computation'), 'software')
    string = lambda name, required=False, terms=(): (name, required, False, 'string', terms, ())
    identifier = ('identifier', False, True, None, (), (
        ('value', True, False, 'string', (), ()), ('scheme', True, False, 'string', ('DOI', 'SWHID'), ())))
    dependency = ('dependency', False, True, None, (), (
        string('name', True), string('version'), string('role', terms=DEPENDENCY_ROLES)))
    file = ('file', False, True, None, (), (
        string('name', True), string('description', True), string('contents'), string('encoding', terms=('Base64',)),
        string('link'), tree(sub(sub(minimal('provenance'), 'file'), 'checksum'))))
    assert tree(sw) == ('software', True, True, None, (), (
        string('name', True), string('role', terms=SOFTWARE_ROLES), string('description'), string('version'),
        string('link'), string('revision'), identifier, dependency, string('build-options'), file))
    assert sw['description'] == ('A program, package or script used to perform the calculations: the simulation '
                                 'code, a calculation method or workflow framework that drives it, or a custom script.')
    assert sw['notes'] == ['Note: Give one entry for each layer that took part, outermost first. A file is given '
                           'under the entry that reads it; for a script, its own code is its file.']
    for path, terms in ((('role',), SOFTWARE_ROLES), (('dependency', 'role'), DEPENDENCY_ROLES)):
        p = sw
        for n in path:
            p = sub(p, n)
        assert all(f'"{t}" –' in p['values']['note'] for t in terms), path
    assert sub(sw, 'link')['values']['format'] == 'uri'
    assert sub(sw, 'revision')['notes'] == ['Note: Give the full commit hash where possible; a tag or a branch can move.']
    assert sub(sw, 'version')['notes'] == ['Note: Give the version for an official release. For any other state of the '
                                           'code, e.g. a branch or a tag, give link and revision.']


def test_file_contents_are_text_unless_encoded():
    """A string holds Unicode text, so a binary file, or a text file whose exact bytes matter, is given in
    Base64 and says so (0043 item 3)."""
    f = sub(sub(minimal('computation'), 'software'), 'file')
    assert sub(f, 'encoding')['notes'] == ['Note: Without encoding, contents is the file\'s text. With Base64, '
                                           'contents is the file\'s bytes encoded as Base64 (RFC 4648); use it for a '
                                           'binary file, or for a text file whose exact bytes matter.']
    assert sub(f, 'contents')['description'] == ('The contents of the file: its text, or its bytes encoded as given '
                                                 'in encoding. Not required in case a link to the file is provided '
                                                 'instead.')


def test_software_file_checksum_is_written_as_everywhere():
    """A linked or Base64 file is checked against its checksum, written exactly as provenance's file checksum,
    so one rule reads every checksum in the standard (0032; 0043 item 4, amended)."""
    software = sub(sub(sub(minimal('computation'), 'software'), 'file'), 'checksum')
    assert software == sub(sub(minimal('provenance'), 'file'), 'checksum')


def test_example_software_has_a_role():
    """The example names its simulation code's role and invents nothing else about the build (0043 item 4)."""
    import json
    minimal = json.loads((ROOT / 'examples/minimal.json').read_text(encoding='utf-8'))['minimal']
    sw = minimal['computation'][0]['software']
    assert sw == [{'name': 'CASTEP', 'role': 'Simulation code'}]


def test_number_density_is_gone():
    """Number density is N/V, given by number-of-particles and volume, so a third value could only
    contradict them (0037)."""
    sc = sub(minimal('computation'), 'conditions')
    assert 'number-density' not in [s['name'] for s in sc['subproperties']]


def test_set_up_is_gone():
    """The qualifier Initial says what "as set up" said, so no note repeats it (0035 item 5)."""
    assert 'as set up' not in open(ROOT / 'schema/minimal.yaml').read()


def test_reviewed_sections_do_not_name_the_nesting_level():
    """The tree nests to any depth, so text names a property or calls it a condition, never a "SubProperty"
    or "SubSubProperty", the baseline's per-table terms (0026)."""
    import re
    for section in ('minimal', 'dft'):
        text = re.sub(r'^\s*-? ?subproperties:', '', open(ROOT / f'schema/{section}.yaml').read(), flags=re.M)
        assert not re.search(r'sub(sub)*propert', text, re.I), section


SIMULATION_TYPE = {
    'thermodynamic-state': (True, ('Equilibrium', 'Steady state', 'Transient')),
    'system-openness': (False, ('Isolated', 'Closed', 'Open')),
    'time-dependence': (False, ('Constant', 'Varying', 'Cyclic')),
    'spatial-uniformity': (False, ('Uniform', 'Nonuniform', 'Periodic')),
}


def test_simulation_type_has_four_axes():
    """A simulation is classified by its thermodynamic state, what it exchanges, and how the imposed
    conditions change in time and vary in space, so a steady state or a relaxation toward equilibrium can
    be said and searched for; every term is defined in its note (0036)."""
    sc = sub(minimal('computation'), 'conditions')
    t = sub(sc, 'type')
    assert tree(t) == ('type', True, False, None, (), tuple(
        (name, required, False, 'string', terms, ()) for name, (required, terms) in SIMULATION_TYPE.items()))
    assert t['notes'] == ['Note: Detailed explanations of the simulation conditions are given in `description`.']
    for name, (_, terms) in SIMULATION_TYPE.items():
        note = sub(t, name)['values']['note']
        assert all(f'"{term}" –' in note for term in terms), name
    assert 'cell-periodicity' in sub(t, 'spatial-uniformity')['values']['note']
    assert [s['name'] for s in sc['subproperties']][:2] == ['type', 'description']
    assert sc['notes'][0].startswith('Note: The conditions below, other than type and description, are given as '
                                     'appropriate to the simulation.')


def test_record_author_names_who_wrote_the_record():
    """The record's author may differ from the dataset's creators, so it is its own member of matcore, with
    creator's identifier schemes (0033; 0045)."""
    a = sub(minimal('matcore'), 'record-author')
    assert sub(a, 'name')['description'] == 'The name of the entity that created the metadata record.'
    assert sub(sub(a, 'identifier'), 'scheme')['values'] == sub(sub(minimal('creator'), 'identifier'), 'scheme')['values']


def test_example_record_names_its_standard_and_version():
    """The example follows 0.6.0, points to its tag, and describes the first version of its dataset (0045 item 3)."""
    import json
    m = json.loads((ROOT / 'examples/minimal.json').read_text(encoding='utf-8'))['minimal']['matcore']
    assert {k: m[k] for k in ('standard-version', 'standard-link', 'id', 'dataset-version', 'creation-date')} == {
        'standard-version': '0.6.0', 'standard-link': 'https://github.com/matcore-standard/matcore/tree/v0.6.0/schema',
        'id': 'mc-ad83jsd3', 'dataset-version': 1, 'creation-date': '2026-02-14'}


def test_net_charge_follows_the_number_of_particles():
    """A charged defect, an ion or a constant-charge electrode fixes the number of electrons, imposed as the
    number of particles is; a fractional charge may be imposed, so the value is a float in elementary charges
    (0049 item 2)."""
    names = [s['name'] for s in sub(minimal('computation'), 'conditions')['subproperties']]
    assert names.index('net-charge') == names.index('number-of-particles') + 1
    c = sub(sub(minimal('computation'), 'conditions'), 'net-charge')
    assert (c['required'], c['repeatable']) == (False, True)
    assert [s['name'] for s in c['subproperties']] == ['value', 'unit', 'qualifier']
