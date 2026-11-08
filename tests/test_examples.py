"""Every example conforms to the structure of the current standard (decision record 0012), written in JSON as
0044 maps the data model onto it."""
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_examples  # noqa: E402

SECTIONS = ['minimal', 'dft', 'md', 'mbpt', 'ml', 'pf', 'derived']
SCHEMA = [
    {'name': 'person', 'required': True, 'repeatable': True, 'type': None, 'extent': None, 'subproperties': [
        {'name': 'name', 'required': True, 'repeatable': False, 'type': 'string', 'extent': []},
        {'name': 'age', 'required': False, 'repeatable': False, 'type': 'int', 'extent': []},
        {'name': 'position', 'required': False, 'repeatable': False, 'type': 'float', 'extent': [3]},
        {'name': 'active', 'required': False, 'repeatable': False, 'type': 'bool', 'extent': []}]},
    {'name': 'title', 'required': True, 'repeatable': False, 'type': 'string', 'extent': []},
    {'name': 'note', 'required': False, 'repeatable': False, 'type': None, 'extent': None},
]


def errors(doc):
    """Structural errors of a small instance against SCHEMA.

    doc (dict): the members of one section.
    """
    return check_examples.structure_errors(doc, SCHEMA, 'test')


def test_a_conforming_document_has_no_errors():
    """Required properties present, a repeatable one as an array, typed leaves with values of their Type and
    shape, an optional one omitted, an untyped leaf as a string: conformant (0044 item 2)."""
    assert errors({'person': [{'name': 'A'}, {'name': 'B', 'age': 40, 'position': [0, 1.5, 2], 'active': True}],
                   'title': 'T', 'note': 'free text'}) == []


@pytest.mark.parametrize('doc, fragment', [
    ({'person': [{'name': 'A'}], 'title': 'T', 'color': 'red'}, '"color" is not a property defined here'),
    ({'person': [{'name': 'A'}]}, 'required "title" is missing'),
    ({'person': [{'age': 3}], 'title': 'T'}, 'required "name" is missing'),
    ({'person': {'name': 'A'}, 'title': 'T'}, 'repeatable, so it is an array'),
    ({'person': [{'name': 'A'}], 'title': ['T']}, 'a string'),
    ({'person': [{'name': 'A'}], 'title': {'x': 1}}, 'no subproperties'),
    ({'person': [{'name': 'A', 'age': 4.5}], 'title': 'T'}, 'an integer'),
    ({'person': [{'name': 'A', 'age': True}], 'title': 'T'}, 'an integer'),
    ({'person': [{'name': 'A', 'position': [0, 1]}], 'title': 'T'}, '3 components'),
    ({'person': [{'name': 'A', 'position': 1.0}], 'title': 'T'}, 'an array'),
    ({'person': [{'name': 'A', 'active': 'yes'}], 'title': 'T'}, 'true or false'),
    ({'person': [{'name': 'A'}], 'title': 'T', 'note': None}, 'null'),
    ({'person': ['A'], 'title': 'T'}, 'an object'),
])
def test_each_kind_of_violation_is_reported(doc, fragment):
    """An unknown member, a missing required property at any depth, a repeatable property not given as an
    array, a value of the wrong Type or shape, a null, and a container not given as an object are each
    reported (0012; 0044 item 2).

    doc (dict): an instance that breaks one rule; fragment (str): part of the expected message.
    """
    found = errors(doc)
    assert any(fragment in e for e in found), found


@pytest.mark.parametrize('key', SECTIONS)
def test_every_example_conforms_to_the_current_standard(key):
    """The published examples follow the standard as it is now, so readers can copy them (0012); each is one
    JSON object whose only member is its section (0044 item 2)."""
    section = yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))
    for ex in section['examples']:
        assert ex['file'].endswith('.json')
        doc = json.loads((ROOT / 'examples' / ex['file']).read_text(encoding='utf-8'))
        assert list(doc) == [key]
        assert check_examples.structure_errors(doc[key], section['properties'], key) == []


def identifiers(obj):
    """Yield (scheme, value) for every `identifier` entry found anywhere in a JSON value.

    obj: a parsed JSON value.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'identifier':
                for i in v if isinstance(v, list) else [v]:
                    if isinstance(i, dict) and 'scheme' in i:
                        yield i['scheme'], i['value']
            yield from identifiers(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from identifiers(v)


def test_example_identifiers_pass_annex_i():
    """Every identifier written in an example, with its scheme, is in Annex I's form and passes its check
    digits, so the examples show values a validator accepts; the record's author carries an ORCID iD
    (0033, amended)."""
    from check_identifiers import identifier_errors
    minimal = json.loads((ROOT / 'examples/minimal.json').read_text(encoding='utf-8'))['minimal']
    author = minimal['matcore-author'][0]['identifier']
    assert {'value': 'https://orcid.org/0000-0003-3311-6299', 'scheme': 'ORCID'} in author
    assert all(identifier_errors(scheme, value) == [] for scheme, value in identifiers(minimal))
