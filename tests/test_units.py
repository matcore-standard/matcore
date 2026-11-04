"""A property is a leaf or a container, never both, and every numerical value is a container holding a
fixed `value` and a fixed `unit` (decision 0015, amended twice 2026-11-04).

Every value with a physical Kind must state its unit, since no default unit is ever implied; one fixed
form for `value` and `unit` lets a validator relate the symbol to the value's Kind through units.yaml,
and lets every serialization write a quantity as a node with two children."""
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_units import NUMERICAL, UNIT_FORM, VALUE_FORM, unit_errors  # noqa: E402


def value(kind='Temperature', **change):
    """Return a `value` leaf in the fixed form, with the given Kind and changes.

    kind (str): the value's Kind; change (dict): fields that replace those of the fixed form.
    """
    return VALUE_FORM | {'type': 'float', 'extent': [], 'kind': kind, 'recommended-unit': None,
                         'values': None} | change


def errors(subs):
    """Return the unit errors of every subproperty of a quantity, each checked against its siblings.

    subs (list[dict]): the quantity's subproperties.
    """
    return [e for s in subs for e in unit_errors(s, subs)]


def test_numerical_kinds_are_the_unit_table_kinds():
    """Every kind of units.yaml, dimensionless included, is the Kind of a number that needs a unit;
    `dimensionless` is the only symbol of its Kind (0015, second amendment)."""
    u = yaml.safe_load((ROOT / 'schema/units.yaml').read_text())
    assert NUMERICAL == set(u['kinds']) and {'Temperature', 'dimensionless'} <= NUMERICAL
    assert [s for s, x in u['units'].items() if x['kind'] == 'dimensionless'] == ['dimensionless']


def test_a_value_and_unit_in_the_fixed_form_pass():
    """The fixed forms of the amendment's item 2 are accepted, with other siblings beside them."""
    assert errors([value(), dict(UNIT_FORM)]) == []
    assert errors([{'name': 'scaling', 'type': 'string', 'kind': 'inapplicable'}, value('Length'), dict(UNIT_FORM)]) == []


def test_a_container_has_no_value_of_its_own():
    """A property with subproperties has null typed fields (amendment item 1)."""
    temperature = {'name': 'temperature', 'type': 'float', 'extent': [], 'kind': 'Temperature',
                   'subproperties': [dict(UNIT_FORM)]}
    assert unit_errors(temperature, [temperature])
    container = {'name': 'creator', 'type': None, 'extent': None, 'kind': None, 'recommended-unit': None,
                 'values': None, 'subproperties': [{'name': 'name'}]}
    assert unit_errors(container, [container]) == []


def test_a_physical_leaf_is_a_value_beside_a_unit():
    """A physical value not named `value`, or with no `unit` beside it, could not be read with its unit."""
    assert errors([value(name='volume')])
    assert errors([value(name='volume'), dict(UNIT_FORM)])
    assert errors([value()])


def test_value_and_unit_that_depart_from_the_fixed_form_fail():
    """An optional or repeatable value, a reworded description, or a changed unit breaks the single form."""
    for change in ({'required': False}, {'repeatable': True}, {'description': 'The volume.'}):
        assert errors([value(**change), dict(UNIT_FORM)]), change
    for change in ({'required': False}, {'kind': 'Temperature'}, {'values': {'enum': ['K']}}, {'notes': ['x']}):
        assert errors([value(), dict(UNIT_FORM) | change]), change
    assert errors([value(), dict(UNIT_FORM), dict(UNIT_FORM)])


def test_every_number_is_a_value_beside_a_unit():
    """A dimensionless value takes the same form as a physical one, so every number in an instance sits in
    a `value` beside its `unit`; only non-quantities are leaves (0015, second amendment)."""
    assert errors([value('dimensionless'), dict(UNIT_FORM)]) == []
    assert errors([{'name': 'number-of-particles', 'type': 'int', 'kind': 'dimensionless'}])
    assert errors([value('dimensionless')])
    assert errors([{'name': 'title', 'type': 'string', 'kind': 'inapplicable'}]) == []


def test_generic_parameters_and_free_form_units_are_outside_the_check():
    """A `value` of Kind any, or a `unit` with no `value`, is settled in its own PR (amendment item 3)."""
    free = {'name': 'unit', 'type': None, 'kind': None}
    assert errors([{'name': 'name', 'kind': 'inapplicable'}, value('any', required=False), free]) == []
    assert errors([{'name': 'name', 'kind': 'inapplicable'}, free]) == []


def test_validate_schema_applies_the_check(tmp_path):
    """validate_schema.py, which CI runs, fails when a number is written as a bare leaf with no unit."""
    for d in ('schema', 'scripts', 'examples'):
        shutil.copytree(ROOT / d, tmp_path / d)
    f = tmp_path / 'schema/minimal.yaml'
    doc = yaml.safe_load(f.read_text())
    mc = next(p for p in doc['properties'] if p['name'] == 'material-component')
    c = next(s for s in mc['subproperties'][0]['subproperties'] if s['name'] == 'concentration')
    value = c.pop('subproperties')[0]
    c.update({k: value[k] for k in ('type', 'extent', 'kind', 'recommended-unit', 'values')})
    f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    run = subprocess.run([sys.executable, tmp_path / 'scripts/validate_schema.py'], capture_output=True, text=True)
    assert run.returncode == 1 and 'concentration' in run.stdout and 'unit' in run.stdout
