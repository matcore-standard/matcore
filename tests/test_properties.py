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


@pytest.mark.parametrize('entity, required', [('creator', True), ('contributor', False)])
def test_creator_and_contributor_follow_0014(entity, required):
    """creator and contributor carry scheme-tagged identifiers and affiliations that hold their own
    identifier (0014 item 1); each keeps its own required flag (contributor is optional, 0011).

    An affiliation and its identifier sit in one container, so they cannot come apart; each identifier
    names its scheme, so a validator knows which rule its value follows.

    entity (str): the property's name; required (bool): whether a dataset must have one.
    """
    prop = minimal(entity)
    name = ('name', True, False, 'string', (), ())
    value = ('value', True, False, 'string', (), ())
    entity_scheme = ('scheme', True, False, 'string', ('ORCID', 'ROR', 'DOI', 'SWHID', 'ISNI'), ())
    affiliation_scheme = ('scheme', True, False, 'string', ('ROR', 'ISNI'), ())
    identifier = ('identifier', False, True, None, (), (value, entity_scheme))
    affiliation = ('affiliation', False, True, None, (), (
        name, ('identifier', False, False, None, (), (value, affiliation_scheme))))
    assert tree(prop) == (entity, required, True, None, (), (name, identifier, affiliation))
    assert legacy_fields(prop) == []


def sub(p, name):
    """Return the subproperty of p with the given name.

    p (dict): property entry; name (str): the subproperty's name.
    """
    return next(s for s in p['subproperties'] if s['name'] == name)


def test_material_component_structure():
    """A material component lists its constituents and its phases, with optional prose; phase is a list
    (one or more phases per component), so it is named in the plural (0004 naming rule)."""
    p = minimal('material-component')
    phases = ('phases', True, False, 'string', ('Amorphous', 'Crystal', 'Quasicrystal', 'Molecule', 'Liquid',
                                                 'Gas', 'Plasma'), ())
    constituent = ('constituent', True, True, None, (), (
        ('species', True, False, 'string', (), ()), ('concentration', True, False, 'float', (), ())))
    assert tree(p) == ('material-component', True, True, None, (), (
        constituent, phases, ('description', False, False, 'string', (), ()),
        ('microstructure', False, False, 'string', (), ())))
    assert sub(p, 'phases')['extent'] == [':']
    assert legacy_fields(p) == []


@pytest.mark.parametrize('value, ok', [(0, True), (0.125, True), (1, True), (-0.1, False), (1.5, False),
                                       (12.5, False)])
def test_concentration_is_an_atomic_fraction(value, ok):
    """concentration is an atomic fraction, a dimensionless number from 0 to 1 whose unit is
    nothing, since a pure number carries no unit; a percentage such as 12.5 does not conform (0004 items
    46, 48).

    value (float): a candidate concentration; ok (bool): whether it conforms.
    """
    c = sub(sub(minimal('material-component'), 'constituent'), 'concentration')
    assert (c['kind'], c['extent'], c['recommended-unit'], c.get('subproperties')) == ('dimensionless', [], None, None)
    assert 'atomic fraction' in c['description'] and 'percent' not in c['description']
    assert Draft202012Validator(value_schema(c)).is_valid(value) == ok


@pytest.mark.parametrize('value, ok', [('C', True), ('Si', True), ('Og', True), ('D', False), ('X', False),
                                       ('si', False), ('Uut', False)])
def test_species_is_an_element_symbol(value, ok):
    """species is one of the 118 element symbols of the IUPAC periodic table and nothing else; an unknown
    symbol would leave the material's composition undefined.

    value (str): a candidate symbol; ok (bool): whether it conforms.
    """
    s = sub(sub(minimal('material-component'), 'constituent'), 'species')
    assert len(s['values']['enum']) == len(set(s['values']['enum'])) == 118
    assert Draft202012Validator(value_schema(s)).is_valid(value) == ok


def test_concentration_note_states_the_sum():
    """The constituents of a material component account for all of it, so their concentrations sum to
    1 (0004 items 40, 46); the schema cannot check the rule, so the note states it for readers and reviewers."""
    c = datum(sub(sub(minimal('material-component'), 'constituent'), 'concentration'))
    assert 'sum to 1.' in (c['values'].get('note') or '')


# 0001 Part A, A2.2: the Kind and recommended unit of each simulation condition, with the shape its
# baseline values text gives (three cell vectors of three components, six tensor components, ...).
SIMULATION_CONDITIONS = {
    'number-of-particles': ('int', [], 'dimensionless', None),
    'volume': ('float', [], 'Volume', 'angstrom^3'),
    'mass-density': ('float', [], 'MassDensity', 'kg/m^3'),
    'number-density': ('float', [], 'NumberDensity', '1/angstrom^3'),
    'cell': ('float', [3, 3], 'Length', 'angstrom'),
    'cell-reference': ('float', [3, 3], 'Length', 'angstrom'),
    'cell-periodicity': ('bool', [3], 'inapplicable', None),
    'temperature': ('float', [], 'Temperature', 'K'),
    'stress': ('float', [6], 'Pressure', 'GPa'),
    'strain': ('float', [6], 'dimensionless', None),
    'strain-rate': ('float', [6], 'InverseTime', '1/s'),
    'heat-flux': ('float', [3], 'HeatFluxDensity', 'W/m^2'),
    'temperature-gradient': ('float', [3], 'TemperatureGradient', 'K/m'),
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
    sc = sub(minimal('computation'), 'simulation-conditions')
    got = {s['name']: (d['type'], d['extent'], d['kind'], d['recommended-unit'])
           for s in sc['subproperties'] for d in [datum(s)]}
    assert got == SIMULATION_CONDITIONS | {'type': ('string', [], 'inapplicable', None),
                                           'description': ('string', [], 'inapplicable', None)}
    assert sub(sc, 'type')['values']['terms'] == ['Equilibrium', 'Nonequilibrium', 'Other']


def test_method_terms_depend_on_method_class():
    """A method is listed under the class it belongs to, so a validator can flag DFT given as Atomistic
    as user-specified (0013, settled 2026-11-03)."""
    c = minimal('computation')
    assert sub(c, 'method-class')['values']['terms'] == ['Electronic', 'Atomistic', 'Mesoscopic', 'Continuum',
                                                         'Data-driven']
    v = sub(c, 'method')['values']
    assert v['depends-on'] == 'method-class'
    assert {k: c_['terms'] for k, c_ in v['cases'].items()} == {
        'Electronic': ['CC', 'QMC', 'DFT', 'MBPT'], 'Atomistic': ['MC', 'MD'], 'Mesoscopic': ['DDD', 'KMC', 'CGMD'],
        'Continuum': ['PF'], 'Data-driven': ['ML']}


def test_computation_restores_the_docx_notation():
    """The tensor and vector notation of the .docx survives: subscripts, the dot of the strain rate Ė,
    and ASCII bars for vector lengths (the migration had flattened them)."""
    sc = sub(minimal('computation'), 'simulation-conditions')
    note = lambda n: datum(sub(sc, n))['values']['note']
    assert '<i>σ</i><sub>11</sub>' in note('stress') and '<i>E</i><sub>11</sub>' in note('strain')
    assert '<i>Ė</i><sub>11</sub>' in note('strain-rate') and 'Ė' in note('strain-rate')
    assert '|a|' in note('cell') and '│' not in note('cell') + note('cell-reference')
    assert 'a<sub>0</sub>' in note('cell-reference')
    assert legacy_fields(minimal('computation')) == []


def test_citation_structure():
    """A citation is a repeatable container of a required reference and an optional doi and link, all
    plain strings; the link is a URI."""
    c = minimal('citation')
    assert tree(c) == ('citation', False, True, None, (), (
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
    assert len(dois) == 4 and 'minimal/citation/doi' in [h for h, _ in dois]
    for here, p in dois:
        if p['type'] is not None:
            assert (p['type'], p['extent'], p['kind']) == ('string', [], 'inapplicable'), here
            assert p['values']['pattern'] == pattern, here


@pytest.mark.parametrize('value, ok', [('https://doi.org/10.1000/182', True),
                                       ('https://doi.org/10.1103/PhysRevX.8.041048', True),
                                       ('10.1000/182', False), ('doi:10.1000/182', False),
                                       ('http://dx.doi.org/10.1000/182', False)])
def test_citation_doi_is_the_https_uri(value, ok):
    """Only the https URI form at doi.org conforms; the bare and legacy forms do not."""
    check = Draft202012Validator(value_schema(sub(minimal('citation'), 'doi')))
    assert check.is_valid(value) == ok


def test_funding_structure():
    """A funding entry names its award and its funder; the funder has the structure of an affiliation, a
    name with at most one ROR or ISNI identifier, since the Crossref Open Funder Registry moves into ROR
    (0014, settled 2026-11-04)."""
    f = minimal('funding')
    value = ('value', True, False, 'string', (), ())
    identifier = ('identifier', False, False, None, (), (value, ('scheme', True, False, 'string', ('ROR', 'ISNI'), ())))
    assert tree(f) == ('funding', False, True, None, (), (
        ('award-title', True, False, 'string', (), ()),
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
    required link in the form of citation's link (a URI), and an optional description."""
    r = minimal('related-content')
    assert tree(r) == ('related-content', False, True, None, (), (
        ('link', True, False, 'string', (), ()),
        ('description', False, False, 'string', (), ())))
    link = sub(r, 'link')
    assert (link['extent'], link['kind']) == ([], 'inapplicable')
    assert link['values']['format'] == sub(minimal('citation'), 'link')['values']['format'] == 'uri'
    assert legacy_fields(r) == []


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
    """A provenance event says what changed, when and by whom, with an optional comment and the checksums
    of the files it touched; a checksum names its file and algorithm, so it can be verified."""
    p = minimal('provenance')
    checksum = ('checksum', False, True, None, (), (
        ('file', True, False, 'string', (), ()),
        ('algorithm', True, False, 'string', tuple(SPDX_CHECKSUM_ALGORITHMS), ()),
        ('value', True, False, 'string', (), ())))
    assert tree(p) == ('provenance', False, True, None, (), (
        ('event-type', True, False, 'string', ('Initial creation', 'Admin update', 'Version update',
                                               'Metadata update'), ()),
        ('date', True, False, 'string', (), ()),
        ('agent', True, False, 'string', (), ()),
        ('comment', False, False, 'string', (), ()),
        checksum))
    assert legacy_fields(p) == []


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
    v = sub(sub(minimal('provenance'), 'checksum'), 'value')
    assert Draft202012Validator(value_schema(v)).is_valid(value) == ok


def test_matcore_id_is_a_string_whose_form_is_open():
    """Every dataset has exactly one MatCore ID, a plain string. The baseline calls the example's format
    tentative, so no pattern is fixed until the form of a MatCore ID is decided."""
    p = minimal('matcore-id')
    assert (p['required'], p['repeatable'], p['type'], p['extent'], p['kind'], p['recommended-unit']) == (
        True, False, 'string', [], 'inapplicable', None)
    assert 'pattern' not in (p['values'] or {}) and 'format' not in (p['values'] or {})
    assert legacy_fields(p) == []


def test_matcore_date_is_written_as_creation_date():
    """The date of the MatCore document is written as the dataset's creation date is: the same type,
    pattern, examples and note, so one rule reads both."""
    p, c = minimal('matcore-date'), minimal('creation-date')
    assert (p['required'], p['repeatable']) == (True, False)
    assert [p[k] for k in ('type', 'extent', 'kind', 'recommended-unit', 'values')] == \
           [c[k] for k in ('type', 'extent', 'kind', 'recommended-unit', 'values')]
    assert legacy_fields(p) == []


def test_license_is_an_spdx_expression_described_in_its_note():
    """A dataset has exactly one license, a string holding an SPDX license expression. The SPDX License
    List changes every few months, so the note names the forms instead of the schema copying the list."""
    p = minimal('license')
    assert (p['required'], p['repeatable'], p['type'], p['extent'], p['kind']) == (
        True, False, 'string', [], 'inapplicable')
    v = p['values']
    assert v['examples'] == ['GPL-3.0-only', 'CC-BY-4.0'] and 'terms' not in v and 'enum' not in v
    assert 'https://spdx.org/licenses/' in v['note'] and 'LicenseRef-' in v['note']
    assert legacy_fields(p) == []


def test_minimal_is_complete():
    """Every typed field of the minimal section is filled, so it declares itself complete (0004 item 36)."""
    doc = yaml.safe_load(open(ROOT / 'schema/minimal.yaml'))
    assert doc.get('legacy_complete') is True
    assert [k for p in doc['properties'] for k in legacy_fields(p)] == []


def dft(name):
    """Return a top-level property of schema/dft.yaml.

    name (str): the property's name.
    """
    return next(p for p in yaml.safe_load(open(ROOT / 'schema/dft.yaml'))['properties'] if p['name'] == name)


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
    assert 'normalization' in sub(xc, 'description')['values']['note']
    assert legacy_fields(xc) == []


def test_xc_functional_keeps_the_name_beside_its_normalization():
    """The functional is kept as the author names it (e.g. PBE), and a normalized decomposition, if given,
    always names its source, so the two never stand without each other's context (0017)."""
    xc = dft('xc-functional')
    name, norm = sub(xc, 'name'), sub(xc, 'normalization')
    assert (name['extent'], name['kind']) == ([], 'inapplicable') and 'PBE' in name['values']['examples']
    components = sub(norm, 'components')
    assert (components['extent'], components['kind']) == ([':'], 'inapplicable')
    assert components['values']['examples'] == [['GGA_X_PBE', 'GGA_C_PBE']]
    assert sub(norm, 'source')['values']['terms'] == ['LibXC']


def test_core_electron_treatment_structure():
    """The core-electron treatment names its method and, for pseudopotential methods, each pseudopotential: its
    name and form, how many electrons it treats explicitly, where it came from, and what identifies it."""
    c = dft('core-electron-treatment')
    count = ('number-of-valence-electrons', True, False, 'int', (), ())
    checksum = ('checksum', False, False, None, (), tuple(tree(s) for s in
                                                          sub(minimal('provenance'), 'checksum')['subproperties']))
    pseudopotential = ('pseudopotential-or-paw', False, True, None, (), (
        ('name', True, False, 'string', (), ()),
        ('type', True, False, 'string', ('Norm conserving', 'PAW', 'Ultrasoft'), ()),
        ('description', False, False, 'string', (), ()), count,
        ('repository', False, False, 'string', (), ()), ('version', False, False, 'string', (), ()),
        ('doi', False, False, 'string', (), ()), checksum,
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


def test_pseudopotential_checksum_is_provenance_checksum():
    """A pseudopotential's checksum is written exactly as a provenance checksum (file, algorithm with the
    SPDX names, value in lowercase hex), so one rule reads both."""
    p = sub(sub(dft('core-electron-treatment'), 'pseudopotential-or-paw'), 'checksum')
    assert p['subproperties'] == sub(minimal('provenance'), 'checksum')['subproperties']


def test_checksum_and_unique_identifier_point_to_each_other():
    """A checksum and any other designation are kept apart: each note sends the reader to the other."""
    pp = sub(dft('core-electron-treatment'), 'pseudopotential-or-paw')
    assert 'unique-identifier' in sub(pp, 'checksum')['notes'][0]
    assert 'checksum' in sub(pp, 'unique-identifier')['notes'][0]
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
    checksum = ('checksum', False, False, None, (), tuple(tree(s) for s in
                                                          sub(minimal('provenance'), 'checksum')['subproperties']))
    basis = ('localized-orbital-basis-set', False, True, None, (), (
        ('type', True, False, 'string', (), ()), ('repository', False, False, 'string', (), ()),
        ('version', False, False, 'string', (), ()), ('doi', False, False, 'string', (), ()), checksum,
        ('unique-identifier', False, False, 'string', (), ())))
    cutoff = lambda n: (n, False, False, None, (), (('value', True, False, 'float', (), ()),
                                                    ('unit', True, False, 'string', (), ())))
    assert tree(v) == ('wavefunction-representation', True, False, None, (), (
        ('type', True, True, 'string', (
            'Gaussian basis sets', 'LAPW', 'Local atomic orbitals', 'Numerical atomic orbitals', 'Plane waves',
            'Real space grids'), ()), basis,
        cutoff('kinetic-energy-cutoff'), cutoff('charge-density-cutoff')))
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
    ('kinetic-energy-cutoff', ['LAPW', 'Plane waves']), ('charge-density-cutoff', ['LAPW', 'Plane waves'])])
def test_conditional_subproperties_name_the_types_they_serve(name, terms):
    """A subproperty that applies to some representations names them, and each named one is a listed term.

    name (str): the subproperty; terms (list[str]): the types it serves.
    """
    w = dft('wavefunction-representation')
    listed = sub(w, 'type')['values']['terms']
    d = sub(w, name)['description']
    assert all(t in listed and f'"{t}"' in d for t in terms) and 'Localized orbitals' not in d


def test_basis_set_identifiers_match_the_pseudopotential_split():
    """The basis set's checksum is provenance's, and its two identifiers point to each other."""
    b = sub(dft('wavefunction-representation'), 'localized-orbital-basis-set')
    assert sub(b, 'checksum')['subproperties'] == sub(minimal('provenance'), 'checksum')['subproperties']
    assert 'unique-identifier' in sub(b, 'checksum')['notes'][0]
    assert 'checksum' in sub(b, 'unique-identifier')['notes'][0]


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
    """The relaxation stops on a change in total energy: a non-negative energy, recommended in eV, with
    its unit stated (0001 A3.1)."""
    r = dft('relaxation-tolerance-energy')
    assert tree(r) == ('relaxation-tolerance-energy', False, False, None, (), (
        ('value', True, False, 'float', (), ()), ('unit', True, False, 'string', (), ())))
    v = sub(r, 'value')
    assert (v['extent'], v['kind'], v['recommended-unit'], v['values']) == ([], 'Energy', 'eV', {'minimum': 0})
    assert legacy_fields(r) == []


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
    could contradict them, with fractional shifts and the smearing and its parameters (0004 item 47)."""
    from check_generic import generic_errors
    k = dft('k-point-mesh')
    number = lambda n, t: (n, False, False, None, (), (('value', True, False, t, (), ()),
                                                      ('unit', True, False, 'string', (), ())))
    param = ('smearing-parameter', False, True, None, (), (
        ('name', True, False, 'string', (), ()), ('value', True, False, 'any', (), ()),
        ('unit', True, False, 'string', (), ()), ('description', False, False, 'string', (), ())))
    assert tree(k) == ('k-point-mesh', False, False, None, (), (
        ('type', True, False, 'string', ('Regular gamma-centered', 'Regular shifted', 'Irregular'), ()),
        ('number-of-points', False, False, 'int', (), ()), ('shift', False, False, 'float', (), ()),
        ('smearing-type', False, False, 'string', ('None', 'None - tetrahedron',
                                                    'None - Blöchl-corrected tetrahedron', 'Gaussian', 'Fermi-Dirac',
                                                    'Methfessel-Paxton', 'Marzari-Vanderbilt'), ()),
        number('smearing-width', 'float'), param))
    assert generic_errors(sub(k, 'smearing-parameter')) == []
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
    assert (v('smearing-width')['kind'], v('smearing-width')['recommended-unit']) == ('Energy', 'eV')
