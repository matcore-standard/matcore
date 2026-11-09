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
    """An example has a caption, a JSON file in examples/, a dataset source, and optional notes; nothing else (0004
    item 23; 0044)."""
    meta = yaml.safe_load(open(ROOT / 'schema/meta-schema.yaml'))
    section = {'section': 'x', 'title': 'X', 'properties': []}
    good = {'caption': 'C', 'file': 'minimal.json', 'source': 'https://doi.org/x'}
    jsonschema.validate(section | {'examples': [good, good | {'notes': 'N'}]}, meta)
    for bad in ({'caption': 'C', 'file': 'minimal.json'}, good | {'file': 'sub/dir.json'}, good | {'file': 'minimal.xml'},
                good | {'extra': 1}):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(section | {'examples': [bad]}, meta)


def test_meta_schema_rejects_malformed_names():
    """Names are lowercase words joined by single hyphens: no leading, trailing or doubled hyphen (0004 item 13)."""
    meta = yaml.safe_load(open(ROOT / 'schema/meta-schema.yaml'))

    def section(name):
        """Return a one-property section document.

        name (str): the property name to test.
        """
        return {'section': 'x', 'title': 'X', 'properties': [
            {'name': name, 'required': True, 'description': 'D', 'repeatable': False}]}
    for good in ('unit', 'k-point-spacing', 'b3lyp', 'x2-y'):
        jsonschema.validate(section(good), meta)
    for bad in ('k--point', 'cutoff-', 'Cutoff', '2d-grid', 'a_b'):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(section(bad), meta)


def test_validate_rejects_fields_out_of_order(tmp_path):
    """Property fields follow one fixed order, so every entry reads the same way (0004 item 6)."""
    import shutil
    for d in ('schema', 'scripts', 'examples'):
        shutil.copytree(ROOT / d, tmp_path / d)
    f = tmp_path / 'schema/ml.yaml'
    # move a one-line `description` above `required` in the first top-level property
    lines = f.read_text().split('\n')
    i = next(n for n, l in enumerate(lines) if l.startswith('  required:'))
    lines[i], lines[i + 1] = lines[i + 1], lines[i]
    f.write_text('\n'.join(lines))
    run = subprocess.run([sys.executable, tmp_path / 'scripts/validate_schema.py'], capture_output=True, text=True)
    assert run.returncode == 1
    assert 'fields out of order' in run.stdout


def test_legacy_complete_requires_no_legacy_fields(tmp_path):
    """A section marked complete has had all its baseline prose moved to typed fields (0004 item 36)."""
    import shutil
    for d in ('schema', 'scripts', 'examples'):
        shutil.copytree(ROOT / d, tmp_path / d)
    f = tmp_path / 'schema/ml.yaml'
    doc = yaml.safe_load(f.read_text())

    def run():
        """Run the validator on the copy and return the completed process."""
        return subprocess.run([sys.executable, tmp_path / 'scripts/validate_schema.py'], capture_output=True, text=True)

    def strip(props):
        """Delete the legacy_* fields of every property in place.

        props (list[dict]): properties, with nested subproperties.
        """
        for p in props:
            for k in [k for k in p if k.startswith('legacy_')]:
                del p[k]
            strip(p.get('subproperties') or [])
    f.write_text(yaml.safe_dump(doc | {'legacy_complete': True}, sort_keys=False, allow_unicode=True))
    r = run()
    assert r.returncode == 1 and 'legacy_complete is true but' in r.stdout
    strip(doc['properties'])
    f.write_text(yaml.safe_dump(doc | {'legacy_complete': True}, sort_keys=False, allow_unicode=True))
    r = run()
    assert r.returncode == 0, r.stdout


def test_notes_name_only_properties_that_exist():
    """A note that cites a property by its quoted name must use a name the standard defines, so a rename
    cannot leave a note pointing at nothing (e.g. "basis-cutoff-planewave" for planewave-basis-cutoff)."""
    import re
    names, cited = set(), []

    def walk(props, path):
        for p in props:
            names.add(p['name'])
            for note in p.get('notes') or []:
                cited.extend((f'{path}/{p["name"]}', n) for n in re.findall(r'"([a-z][a-z0-9]*(?:-[a-z0-9]+)+)"', note))
            walk(p.get('subproperties') or [], f'{path}/{p["name"]}')
    for key in ['minimal', 'dft', 'pim', 'md', 'mbpt', 'ml', 'pf', 'derived']:
        walk(yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))['properties'], key)
    assert [c for c in cited if c[1] not in names] == []


def test_meta_schema_pairs_depends_on_with_cases():
    """depends-on and cases come together, and a case cannot depend on anything itself (0013 settled 2)."""
    meta = yaml.safe_load((ROOT/'schema/meta-schema.yaml').read_text())
    v = jsonschema.Draft202012Validator(meta)
    def section(values):
        """Return a one-property section whose property has these values.

        values (dict): the property's values.
        """
        return {'section': 'x', 'title': 'x', 'properties': [
            {'name': 'm', 'required': True, 'description': 'd', 'type': 'string', 'extent': [], 'kind': 'inapplicable',
             'recommended-unit': None, 'values': values, 'repeatable': False}]}
    case = {'terms': ['DFT']}
    assert v.is_valid(section({'depends-on': 'c', 'cases': {'A': case}, 'note': 'n'}))
    assert not v.is_valid(section({'depends-on': 'c'}))
    assert not v.is_valid(section({'cases': {'A': case}}))
    assert not v.is_valid(section({'depends-on': 'c', 'cases': {'A': {'depends-on': 'd', 'cases': {}}}}))
    assert not v.is_valid(section({'depends-on': 'c', 'cases': {'A': {'colour': 'red'}}}))
