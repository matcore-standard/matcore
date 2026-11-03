"""Properties whose structure a decision record fixes keep that structure."""
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_values import value_schema  # noqa: E402


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


@pytest.mark.parametrize('value, ok', [(0, True), (12.5, True), (100, True), (-1, False), (100.5, False)])
def test_concentration_is_an_atomic_percent(value, ok):
    """concentration is an atomic percentage, a dimensionless number from 0 to 100 that carries no unit.

    value (float): a candidate concentration; ok (bool): whether it conforms.
    """
    c = sub(sub(minimal('material-component'), 'constituent'), 'concentration')
    assert (c['kind'], c['extent']) == ('dimensionless', [])
    assert 'atomic' in c['description']
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
