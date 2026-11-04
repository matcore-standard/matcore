#!/usr/bin/env python3
"""Check leaves, containers and quantities with a unit against decision 0015 (amended 2026-11-04).

A property with subproperties is a container and has no typed fields. A leaf whose Kind is physical
(a units.yaml kind other than `dimensionless`) is named `value`, has the fixed fields of VALUE_FORM,
and has exactly one sibling `unit` in the fixed form UNIT_FORM; a `value` whose Kind is
`dimensionless` or `inapplicable` has no sibling `unit`. A `value` of Kind `any` (generic parameters)
and a `unit` with no `value` (free-form units) are outside the check. Called by
scripts/validate_schema.py for every property.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PHYSICAL = set(yaml.safe_load((ROOT / 'schema/units.yaml').read_text())['kinds']) - {'dimensionless'}
TYPED = ('type', 'extent', 'kind', 'recommended-unit', 'values')
VALUE_FORM = {
    'name': 'value',
    'required': True,
    'description': 'The value of the property, in the unit given by `unit`.',
    'repeatable': False,
}
UNIT_FORM = {
    'name': 'unit',
    'required': True,
    'description': 'The unit of the value, an Annex U symbol whose Kind is the Kind of `value`.',
    'type': 'string',
    'extent': [],
    'kind': 'inapplicable',
    'recommended-unit': None,
    'values': None,
    'repeatable': False,
}


def unit_errors(p, siblings):
    """Return the errors in a property's shape as a leaf, a container or a quantity's value, as messages.

    p (dict): property entry; siblings (list[dict]): the properties under the same parent, p included.
    """
    if p.get('subproperties'):
        typed = [k for k in TYPED if p.get(k) is not None]
        return [f"a container has no value of its own, but {', '.join(typed)} set (0015)"] if typed else []
    units = [s for s in siblings if s['name'] == 'unit']
    if p.get('kind') in PHYSICAL:
        if p['name'] != 'value':
            return [f"kind {p['kind']} makes this a container of value and unit (0015)"]
        out = [] if {k: p.get(k) for k in VALUE_FORM} == VALUE_FORM else ['value departs from the fixed form of 0015']
        if len(units) != 1:
            return out + [f"value of kind {p['kind']} needs exactly one sibling unit (0015)"]
        return out + ([] if units[0] == UNIT_FORM else ['unit departs from the fixed form of 0015'])
    if p['name'] == 'value' and p.get('kind') in ('dimensionless', 'inapplicable') and units:
        return [f"value of kind {p['kind']} carries no unit (0015)"]
    return []
