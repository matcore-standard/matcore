"""Tests of the JSON Schema generated from the standard (decision 0078)."""
import json
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_json_schema  # noqa: E402

UNITS = yaml.safe_load((ROOT / 'schema/units.yaml').read_text())
SCHEMA = build_json_schema.build()
SECTIONS = build_json_schema.SECTIONS


def valid(doc, schema):
    """Return whether doc satisfies schema, a JSON Schema whose $refs point into SCHEMA's $defs.

    doc: a parsed JSON value; schema (dict): the subschema to check against.
    """
    return Draft202012Validator(schema | {'$defs': SCHEMA['$defs']},
                                format_checker=Draft202012Validator.FORMAT_CHECKER).is_valid(doc)


def section(key):
    """Return the schema of one section, by reference into the generated $defs.

    key (str): the section key.
    """
    return {'$ref': f'#/$defs/{key}'}


PROPS = [
    {'name': 'person', 'required': True, 'repeatable': True, 'type': None, 'extent': None, 'kind': None,
     'values': None, 'subproperties': [
         {'name': 'name', 'required': True, 'repeatable': False, 'type': 'string', 'extent': [], 'kind': 'inapplicable',
          'values': None},
         {'name': 'age', 'required': False, 'repeatable': False, 'type': 'int', 'extent': [], 'kind': 'dimensionless',
          'values': {'minimum': 0}},
         {'name': 'position', 'required': False, 'repeatable': False, 'type': 'float', 'extent': [3],
          'kind': 'dimensionless', 'values': None},
         {'name': 'active', 'required': False, 'repeatable': False, 'type': 'bool', 'extent': [], 'kind': 'inapplicable',
          'values': None}]},
    {'name': 'title', 'required': True, 'repeatable': False, 'type': 'string', 'extent': [], 'kind': 'inapplicable',
     'values': None},
]
SYNTHETIC = build_json_schema.section_schema(PROPS, UNITS)


def test_a_conforming_document_is_valid():
    """Required properties present, a repeatable one as an array, typed leaves with values of their Type and shape,
    an optional one omitted: conformant (0044 item 2)."""
    assert valid({'person': [{'name': 'A'}, {'name': 'B', 'age': 40, 'position': [0, 1.5, 2], 'active': True}],
                  'title': 'T'}, SYNTHETIC)


@pytest.mark.parametrize('doc', [
    {'person': [{'name': 'A'}], 'title': 'T', 'color': 'red'},   # a name the standard does not define
    {'person': [{'name': 'A'}]},                                 # a required property missing
    {'person': [{'age': 3}], 'title': 'T'},                      # a required property missing at depth
    {'person': {'name': 'A'}, 'title': 'T'},                     # a repeatable property not an array
    {'person': [{'name': 'A'}], 'title': ['T']},                 # a value of the wrong Type
    {'person': [{'name': 'A'}], 'title': {'x': 1}},              # an object where a leaf is expected
    {'person': [{'name': 'A', 'age': 4.5}], 'title': 'T'},       # a fraction for an int
    {'person': [{'name': 'A', 'age': True}], 'title': 'T'},      # a bool for an int
    {'person': [{'name': 'A', 'age': -1}], 'title': 'T'},        # below the minimum
    {'person': [{'name': 'A', 'position': [0, 1]}], 'title': 'T'},  # the wrong number of components
    {'person': [{'name': 'A', 'position': 1.0}], 'title': 'T'},  # a scalar where the Extent lists dimensions
    {'person': [{'name': 'A', 'active': 'yes'}], 'title': 'T'},  # a string for a bool
    {'person': [{'name': 'A'}], 'title': None},                  # null, never written (0044 item 2)
    {'person': ['A'], 'title': 'T'},                             # a container not an object
])
def test_each_kind_of_violation_is_rejected(doc):
    """An unknown member, a missing required property at any depth, a repeatable property not given as an array, a
    value of the wrong Type, bounds or shape, a null, and a container not given as an object are each rejected (0012;
    0044 item 2).

    doc (dict): an instance that breaks one rule.
    """
    assert not valid(doc, SYNTHETIC)


GENERIC = build_json_schema.section_schema([
    {'name': 'parameter', 'required': False, 'repeatable': True, 'type': None, 'extent': None, 'kind': None,
     'values': None, 'subproperties': [
         {'name': 'name', 'required': True, 'repeatable': False, 'type': 'string', 'extent': [],
          'kind': 'inapplicable', 'values': None},
         {'name': 'value', 'required': True, 'repeatable': False, 'type': 'any', 'extent': 'any', 'kind': 'any',
          'values': None},
         {'name': 'unit', 'required': False, 'repeatable': False, 'type': 'string', 'extent': [],
          'kind': 'inapplicable', 'values': None}]}], UNITS)


@pytest.mark.parametrize('entry, ok', [
    ({'name': 'n', 'value': 4, 'type': 'int', 'unit': 'dimensionless'}, True),
    ({'name': 'n', 'value': [0.5, 1], 'type': 'float', 'unit': 'm'}, True),
    ({'name': 'n', 'value': 'tanh', 'type': 'string'}, True),
    ({'name': 'n', 'value': True, 'type': 'bool'}, True),
    ({'name': 'n', 'value': 'tanh', 'type': 'string', 'unit': 'dimensionless'}, False),
    ({'name': 'n', 'value': False, 'type': 'bool', 'unit': 'dimensionless'}, False),
    ({'name': 'n', 'value': 4.0, 'type': 'float'}, False),
    ({'name': 'n', 'value': 4, 'type': 'int'}, False),
    ({'name': 'n', 'value': 4.0, 'type': 'float', 'unit': 'x-gnu:1/cm'}, True),
    ({'name': 'n', 'value': 4, 'unit': 'dimensionless'}, False),
    ({'name': 'n', 'value': 4, 'type': 'number', 'unit': 'dimensionless'}, False),
    ({'name': 'n', 'value': 4.5, 'type': 'int', 'unit': 'dimensionless'}, False),
    ({'name': 'n', 'value': [1, 'a'], 'type': 'float', 'unit': 'm'}, False),
    ({'name': 'n', 'value': 1.0, 'type': 'float', 'unit': 'furlong'}, False),
])
def test_a_generic_parameter_states_its_type(entry, ok):
    """JSON writes 4 and 4.0 alike, so a generic parameter's object states its instance type in a member `type`, and
    its value, or each component, has that type (0044 item 3). A float or int carries a unit, any Annex U symbol,
    `dimensionless`, or an x-gnu: expression (Annex U Rule 4); a string or bool is not measured and carries none
    (0084 item 1).

    entry (dict): one parameter entry; ok (bool): whether it conforms.
    """
    assert valid({'parameter': [entry]}, GENERIC) is ok


@pytest.mark.parametrize('unit, ok', [('eV', True), ('Ry', True), ('kJ/mol', False), ('angstrom', False),
                                      ('dimensionless', False), ('x-gnu:eV', False)])
def test_a_unit_matches_the_kind_of_its_value(unit, ok):
    """A unit beside a typed value is an Annex U symbol of that value's Kind: an energy cutoff takes eV or Ry, not a
    molar energy, a length, a pure number or a GNU Units expression (0015; Annex U Rule 8).

    unit (str): the unit written; ok (bool): whether it conforms.
    """
    dft = json.loads((ROOT / 'examples/dft.json').read_text(encoding='utf-8'))['dft']
    dft['settings'][0]['wavefunction-representation']['kinetic-energy-cutoff']['unit'] = unit
    assert valid(dft, section('dft')) is ok


def test_a_reduced_length_takes_dimensionless():
    """A phase field length or time in reduced units is written with unit dimensionless, which no other length takes
    (0075)."""
    nm = SCHEMA['$defs']['pf']['properties']['settings']['items']['properties']['numerical-method']['items']
    unit = nm['properties']['grid-spacing']['items']['properties']['unit']
    assert 'dimensionless' in unit['enum'] and 'm' in unit['enum'] and 's' not in unit['enum']


def test_a_record_requires_minimal_and_admits_only_sections():
    """A record holds minimal and the method sections it uses, and nothing else (0044 item 2; 0078 item 2)."""
    assert SCHEMA['required'] == ['minimal'] and SCHEMA['additionalProperties'] is False
    assert list(SCHEMA['properties']) == SECTIONS
    assert not valid({'dft': {'settings': []}}, SCHEMA | {'$defs': {}})


@pytest.mark.parametrize('key', SECTIONS)
def test_every_example_conforms_to_the_generated_schema(key):
    """The published examples follow the standard as it is now, so readers can copy them (0012); each is one JSON
    object whose only member is its section (0044 item 2)."""
    spec = yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))
    for ex in spec['examples']:
        doc = json.loads((ROOT / 'examples' / ex['file']).read_text(encoding='utf-8'))
        assert list(doc) == [key]
        assert valid(doc[key], section(key)), ex['file']


def test_the_published_schema_is_the_generated_one():
    """The schema published with each version is generated from the YAML and never edited by hand (0078 item 1)."""
    committed = json.loads((ROOT / 'docs/standard/matcore.schema.json').read_text(encoding='utf-8'))
    assert committed == SCHEMA
    Draft202012Validator.check_schema(committed)


def test_a_record_may_add_properties_named_with_x():
    """A record may add Properties of its own, at any level, named with the prefix x-; any other name the standard
    does not define is still rejected, so a misspelled property is caught (0079)."""
    assert valid({'person': [{'name': 'A', 'x-note': {'any': [1, 2]}}], 'title': 'T', 'x-beamline': 'ID13'},
                 SYNTHETIC)
    assert not valid({'person': [{'name': 'A', 'nmae': 'B'}], 'title': 'T'}, SYNTHETIC)
    assert SCHEMA['patternProperties'] == {'^x-': {}}
