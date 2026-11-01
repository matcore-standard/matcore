"""A property's structured values follow decision 0013: keys tied to the type, no contradictory keys,
formats from JSON Schema 2020-12 and always checked, and examples that satisfy their own property."""
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_values import FORMATS, values_errors  # noqa: E402


def prop(type_, values, extent=None):
    """Return a minimal property entry.

    type_ (str | None): the property's type; values (dict | None): its values;
    extent (list | None): its extent, scalar when None.
    """
    return {'name': 'x', 'type': type_, 'extent': [] if extent is None else extent, 'values': values}


def test_conforming_values_pass():
    """Each key on the type it belongs to raises nothing."""
    assert values_errors(prop('string', {'terms': ['Electronic', 'Atomistic'], 'examples': ['Quantum']})) == []
    assert values_errors(prop('string', {'enum': ['2pi-included', '2pi-excluded']})) == []
    assert values_errors(prop('float', {'minimum': 0, 'maximum': 1, 'examples': [0.5]})) == []
    assert values_errors(prop('string', {'format': 'date', 'examples': ['2024-06-01']})) == []
    assert values_errors(prop('string', {'pattern': 'MC-[0-9]{4}', 'examples': ['MC-0042']})) == []
    assert values_errors(prop('string', {'note': 'Any text.'})) == []
    assert values_errors(prop(None, None)) == []


def test_keys_are_tied_to_the_type():
    """A key on the wrong type, or on a property with no type, is an error (0013 item 2)."""
    assert values_errors(prop('int', {'terms': ['a']}))
    assert values_errors(prop('string', {'minimum': 0}))
    assert values_errors(prop('bool', {'format': 'date'}))
    assert values_errors(prop(None, {'enum': ['a']}))


def test_contradictory_keys_are_rejected():
    """At most one of terms/enum and of format/pattern; minimum does not exceed maximum (0013 item 2)."""
    assert values_errors(prop('string', {'terms': ['a'], 'enum': ['a']}))
    assert values_errors(prop('string', {'format': 'date', 'pattern': '.*'}))
    assert values_errors(prop('int', {'minimum': 5, 'maximum': 1}))


def test_formats_are_the_json_schema_2020_12_names_and_all_are_checked():
    """The format names are those of JSON Schema 2020-12 Validation §7.3, and the installed checker
    implements every one, so no format is silently accepted (0013 item 3)."""
    assert FORMATS == {'date-time', 'date', 'time', 'duration', 'email', 'idn-email', 'hostname', 'idn-hostname',
                       'ipv4', 'ipv6', 'uri', 'uri-reference', 'iri', 'iri-reference', 'uuid', 'uri-template',
                       'json-pointer', 'relative-json-pointer', 'regex'}
    assert FORMATS <= set(Draft202012Validator.FORMAT_CHECKER.checkers)
    assert values_errors(prop('string', {'format': 'phone'}))


def test_validate_schema_reports_values_errors(tmp_path):
    """validate_schema.py, which CI runs, applies these checks to every property in the section files."""
    import shutil
    import subprocess
    for d in ('schema', 'scripts', 'examples'):
        shutil.copytree(ROOT / d, tmp_path / d)
    f = tmp_path / 'schema/ml.yaml'
    f.write_text(f.read_text().replace('  values: null\n', '  values: {minimum: 0}\n', 1))
    run = subprocess.run([sys.executable, tmp_path / 'scripts/validate_schema.py'], capture_output=True, text=True)
    assert run.returncode == 1 and 'values.minimum needs type' in run.stdout


def test_meta_schema_allows_exactly_the_0013_keys():
    """values takes the eight keys of decision 0013 and no other."""
    import jsonschema
    import pytest
    import yaml
    meta = yaml.safe_load(open(ROOT / 'schema/meta-schema.yaml'))

    def section(values):
        """Return a one-property section document whose property has these values.

        values (dict): the property's values.
        """
        return {'section': 'x', 'title': 'X', 'properties': [
            {'name': 'x', 'required': True, 'description': 'D', 'repeatable': False, 'values': values}]}
    jsonschema.validate(section({'terms': ['a'], 'enum': ['a'], 'minimum': 0, 'maximum': 1, 'format': 'date',
                                 'pattern': '.*', 'examples': ['a'], 'note': 'N'}), meta)
    for bad in ({'choices': ['a']}, {'terms': [1]}, {'enum': [True]}):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(section(bad), meta)


def test_examples_must_satisfy_their_property():
    """An example is data: a wrong type, a value outside the rules, or a malformed format is an error,
    while an unlisted term is not, since terms are open (0013 item 1)."""
    bad = [prop('string', {'format': 'uri', 'examples': ['not a uri']}),
           prop('string', {'format': 'date', 'examples': ['2026-02-30']}),
           prop('string', {'enum': ['a', 'b'], 'examples': ['c']}),
           prop('float', {'minimum': 0, 'examples': [-1.0]}),
           prop('int', {'examples': ['three']}),
           prop('string', {'pattern': 'MC-[0-9]{4}', 'examples': ['xMC-0042']}),
           prop('bool', {'examples': [[True, False]]}, extent=[3])]
    for p in bad:
        assert values_errors(p), p
    assert values_errors(prop('string', {'format': 'uri', 'examples': ['https://orcid.org/0000-0002-1825-0097']})) == []
    assert values_errors(prop('bool', {'examples': [[True, False, True]]}, extent=[3])) == []
    assert values_errors(prop('float', {'examples': [[[1.0, 0, 0], [0, 1.0, 0]]]}, extent=[':', 3])) == []
