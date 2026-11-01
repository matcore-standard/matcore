"""Every example conforms to the structure of the current standard (decision record 0012)."""
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_examples  # noqa: E402

SECTIONS = ['minimal', 'dft', 'md', 'mbpt', 'ml', 'pf', 'derived']
SCHEMA = [
    {'name': 'person', 'required': True, 'repeatable': True, 'subproperties': [
        {'name': 'name', 'required': True, 'repeatable': False},
        {'name': 'email', 'required': False, 'repeatable': False}]},
    {'name': 'title', 'required': True, 'repeatable': False},
]


def errors(xml):
    """Structural errors of a small XML document against SCHEMA.

    xml (str): document with a <root> element.
    """
    return check_examples.structure_errors(ET.fromstring(xml), SCHEMA, 'test')


def test_a_conforming_document_has_no_errors():
    """Required properties present, repeatable one repeated, optional one omitted: conformant."""
    assert errors('<root><person><name>A</name></person><person><name>B</name><email>b@x</email></person>'
                  '<title>T</title></root>') == []


@pytest.mark.parametrize('xml, fragment', [
    ('<root><person><name>A</name></person><title>T</title><color>red</color></root>', '<color>'),
    ('<root><person><name>A</name></person></root>', 'required <title>'),
    ('<root><person><email>e</email></person><title>T</title></root>', 'required <name>'),
    ('<root><person><name>A</name><name>B</name></person><title>T</title></root>', 'not repeatable'),
    ('<root><person><name>A</name></person><title><x>1</x></title></root>', 'no subproperties'),
])
def test_each_kind_of_violation_is_reported(xml, fragment):
    """Unknown element, missing required property (at any depth), repeated non-repeatable, unexpected nesting."""
    found = errors(xml)
    assert any(fragment in e for e in found), found


@pytest.mark.parametrize('key', SECTIONS)
def test_every_example_conforms_to_the_current_standard(key):
    """The published examples follow the standard as it is now, so readers can copy them (0012)."""
    section = yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))
    for ex in section['examples']:
        root = ET.parse(ROOT / 'examples' / ex['file']).getroot()
        assert check_examples.structure_errors(root, section['properties'], key) == []
