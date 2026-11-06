"""A generic parameter has one canonical form, wherever it appears (decision 0016).

The schema cannot fix what such a parameter means, so its four subproperties must at least be written
the same way everywhere: a reader, and an instance validator, then find the name, the value, its unit
and the explanation in the same places in all five properties that use the form."""
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_generic import UNIT_DESCRIPTION, UNIT_NOTE, generic_errors  # noqa: E402


def leaf(name, required, description, **fields):
    """Return a leaf entry with the given fields over a plain-string default.

    name (str): the leaf's name; required (bool): its required flag; description (str): its description;
    fields (dict): fields that replace the default ones.
    """
    return {'name': name, 'required': required, 'description': description, 'type': 'string', 'extent': [],
            'kind': 'inapplicable', 'recommended-unit': None, 'values': None, 'repeatable': False} | fields


def parameter(subs=None):
    """Return a generic parameter in the canonical form, or with these subproperties.

    subs (list[dict] | None): replacement subproperties; the canonical four when None.
    """
    canonical = [
        leaf('name', True, 'The designation of the parameter.'),
        leaf('value', True, 'The data associated with the parameter.', type='any', extent='any', kind='any'),
        leaf('unit', True, UNIT_DESCRIPTION, values={'note': UNIT_NOTE}),
        leaf('description', False, 'An explanation of the parameter.'),
    ]
    return {'name': 'xc-parameter', 'type': None, 'subproperties': canonical if subs is None else subs}


def test_the_canonical_form_passes_with_its_own_descriptions():
    """name, value and description keep descriptions specific to each parameter (0016 item 1)."""
    assert generic_errors(parameter()) == []
    p = parameter()
    p['subproperties'][0]['description'] = 'The designation of the exchange-correlation parameter.'
    assert generic_errors(p) == []


def test_unit_carries_the_fixed_text_of_0001():
    """The unit's description is 0001 B9's, its note 0001 A3.2's, with the x-gnu escape."""
    assert UNIT_DESCRIPTION == 'The unit in which the associated value is expressed.'
    assert 'Annex U' in UNIT_NOTE and '`dimensionless`' in UNIT_NOTE and '`x-gnu:`' in UNIT_NOTE


def test_departures_from_the_form_fail():
    """A missing, extra or reordered subproperty, or a changed field, breaks the single form (0016 item 3)."""
    subs = parameter()['subproperties']
    assert generic_errors(parameter(subs[:3]))                                  # description missing
    assert generic_errors(parameter(subs + [leaf('type', False, 'x')]))         # extra subproperty
    assert generic_errors(parameter([subs[1], subs[0], subs[2], subs[3]]))      # reordered
    for i, change in [(0, {'required': False}), (1, {'extent': []}), (1, {'repeatable': True}),
                      (2, {'description': 'The unit.'}), (2, {'values': None}), (3, {'kind': 'any'})]:
        changed = [dict(s) for s in subs]
        changed[i] |= change
        assert generic_errors(parameter(changed)), (i, change)


def test_only_a_value_of_kind_any_makes_a_generic_parameter():
    """Recognised by structure, with no tag (0016 item 2): a quantity's value + unit is not one."""
    quantity = {'name': 'temperature', 'subproperties': [leaf('value', True, 'v', type='float', kind='Temperature'),
                                                         leaf('unit', True, 'u')]}
    assert generic_errors(quantity) == []
    assert generic_errors(leaf('title', True, 'A title.')) == []


def test_a_value_of_fixed_type_and_kind_any_is_not_a_generic_parameter():
    """A float whose unit the instance chooses, as the SCF tolerance, is not a generic parameter: only a
    value whose Type and Kind are both open is one (0019 item 3)."""
    tolerance = {'name': 'tolerance', 'subproperties': [
        leaf('criterion', True, 'c'), leaf('value', True, 'v', type='float', kind='any'),
        leaf('unit', True, UNIT_DESCRIPTION, values={'note': UNIT_NOTE})]}
    assert generic_errors(tolerance) == []


def test_validate_schema_applies_the_check(tmp_path):
    """validate_schema.py, which CI runs, fails when a generic parameter loses its unit's fixed note."""
    for d in ('schema', 'scripts', 'examples'):
        shutil.copytree(ROOT / d, tmp_path / d)
    f = tmp_path / 'schema/dft.yaml'
    doc = yaml.safe_load(f.read_text())
    xc = next(p for p in doc['properties'] if p['name'] == 'xc-functional')
    param = next(s for s in xc['subproperties'] if s['name'] == 'xc-parameter')
    next(s for s in param['subproperties'] if s['name'] == 'unit')['values'] = None
    f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    run = subprocess.run([sys.executable, tmp_path / 'scripts/validate_schema.py'], capture_output=True, text=True)
    assert run.returncode == 1 and 'xc-parameter' in run.stdout and 'generic parameter' in run.stdout
