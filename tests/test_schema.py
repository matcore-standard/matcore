import subprocess, sys, pathlib

import jsonschema
import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
def test_validate(): assert subprocess.run([sys.executable, ROOT/'scripts/validate_schema.py']).returncode == 0


def test_meta_schema_types_the_introduction():
    """A section's introduction is Markdown text; anything else is rejected (0004 item 23)."""
    meta = yaml.safe_load(open(ROOT / 'schema/meta-schema.yaml'))
    section = {'section': 'x', 'title': 'X', 'properties': []}
    jsonschema.validate(section | {'introduction': 'Some *Markdown* text.'}, meta)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(section | {'introduction': ['not', 'text']}, meta)


def test_unit_factors_are_exact_decimal_text():
    """Factors keep their published digits (e.g. CODATA's trailing zeros) as text that parses as a number (0009)."""
    units = yaml.safe_load(open(ROOT / 'schema/units.yaml'))
    for sym, u in units['units'].items():
        f = u['si_factor']
        if sym == 'dimensionless':
            assert f is None
            continue
        assert isinstance(f, str), sym
        float(f)
    assert units['units']['Ry']['si_factor'] == '2.1798723611030e-18'


def test_every_kind_states_its_si_unit_and_dimension():
    """Table U.3 and the factors in Table U.4 need each kind's SI dimension and coherent SI unit (0009)."""
    units = yaml.safe_load(open(ROOT / 'schema/units.yaml'))
    for name, k in units['kinds'].items():
        assert k.get('si_unit') and k.get('si_dimension'), name


def test_meta_schema_types_the_examples():
    """An example has a caption, an XML file in examples/, a dataset source, and optional notes; nothing else (0004 item 23)."""
    meta = yaml.safe_load(open(ROOT / 'schema/meta-schema.yaml'))
    section = {'section': 'x', 'title': 'X', 'properties': []}
    good = {'caption': 'C', 'file': 'minimal.xml', 'source': 'https://doi.org/x'}
    jsonschema.validate(section | {'examples': [good, good | {'notes': 'N'}]}, meta)
    for bad in ({'caption': 'C', 'file': 'minimal.xml'}, good | {'file': 'sub/dir.xml'}, good | {'extra': 1}):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(section | {'examples': [bad]}, meta)
