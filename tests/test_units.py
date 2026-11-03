"""A physical quantity carries its unit in one fixed form, and nothing else carries one (decision 0015).

Every value with a physical Kind must state its unit, since no default unit is ever implied; one fixed
form for that `unit` lets a validator relate the symbol to the parent's Kind through units.yaml."""
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_units import PHYSICAL, UNIT_FORM, unit_errors  # noqa: E402


def quantity(kind, subs):
    """Return a typed property of the given Kind with these subproperties.

    kind (str): the property's Kind; subs (list[dict]): its subproperties.
    """
    return {'name': 'temperature', 'kind': kind, 'type': 'float', 'subproperties': subs}


def test_physical_kinds_are_the_unit_table_kinds_except_dimensionless():
    """dimensionless is listed among units.yaml's kinds but has no unit to state (0015 item 1)."""
    kinds = set(yaml.safe_load((ROOT / 'schema/units.yaml').read_text())['kinds'])
    assert PHYSICAL == kinds - {'dimensionless'} and 'Temperature' in PHYSICAL


def test_a_quantity_with_the_fixed_unit_passes():
    """The fixed form of 0015 item 2 is accepted."""
    assert unit_errors(quantity('Temperature', [dict(UNIT_FORM)])) == []


def test_a_quantity_without_a_unit_fails():
    """A physical value with no unit could not be interpreted."""
    assert unit_errors(quantity('Temperature', []))
    assert unit_errors({'name': 'volume', 'kind': 'Volume', 'type': 'float'})


def test_a_unit_that_departs_from_the_fixed_form_fails():
    """An optional unit, a typed unit, or an extra field each breaks the single form."""
    for change in ({'required': False}, {'kind': 'Temperature'}, {'values': {'enum': ['K']}}, {'notes': ['x']}):
        assert unit_errors(quantity('Temperature', [dict(UNIT_FORM) | change])), change


def test_a_unit_on_a_non_quantity_fails():
    """A dimensionless or inapplicable property carries no unit (0015 item 3)."""
    assert unit_errors(quantity('dimensionless', [dict(UNIT_FORM)]))
    assert unit_errors(quantity('inapplicable', [dict(UNIT_FORM)]))
    assert unit_errors(quantity('dimensionless', [])) == []


def test_containers_and_open_kinds_are_outside_the_check():
    """Generic parameters and free-form units keep their own unit, settled in their own PRs (0015 item 3)."""
    container = {'name': 'xc-parameter', 'kind': None, 'type': None,
                 'subproperties': [{'name': 'value', 'kind': 'any'}, {'name': 'unit', 'kind': None}]}
    assert unit_errors(container) == []
    assert unit_errors(quantity('any', [])) == []


def test_validate_schema_applies_the_check(tmp_path):
    """validate_schema.py, which CI runs, fails when a physical property lacks its unit."""
    for d in ('schema', 'scripts', 'examples'):
        shutil.copytree(ROOT / d, tmp_path / d)
    f = tmp_path / 'schema/minimal.yaml'
    doc = yaml.safe_load(f.read_text())
    mc = next(p for p in doc['properties'] if p['name'] == 'material-component')
    c = next(s for s in mc['subproperties'][0]['subproperties'] if s['name'] == 'concentration')
    c['kind'] = 'Temperature'
    f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    run = subprocess.run([sys.executable, tmp_path / 'scripts/validate_schema.py'], capture_output=True, text=True)
    assert run.returncode == 1 and 'concentration' in run.stdout and 'unit' in run.stdout
