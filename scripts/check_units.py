#!/usr/bin/env python3
"""Check the `unit` subproperty of typed quantities against decision 0015.

A property whose Kind is physical (a units.yaml kind other than `dimensionless`) has exactly one
`unit` subproperty, in the fixed form UNIT_FORM; a property whose Kind is `dimensionless` or
`inapplicable` has none. Containers and Kind `any` are outside the check. Called by
scripts/validate_schema.py for every property.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PHYSICAL = set(yaml.safe_load((ROOT / 'schema/units.yaml').read_text())['kinds']) - {'dimensionless'}
UNIT_FORM = {
    'name': 'unit',
    'required': True,
    'description': 'The unit of the value, an Annex U symbol whose Kind is the Kind of the property.',
    'type': 'string',
    'extent': [],
    'kind': 'inapplicable',
    'recommended-unit': None,
    'values': None,
    'repeatable': False,
}


def unit_errors(p):
    """Return the errors in a property's `unit` subproperty, as messages.

    p (dict): property entry, with its subproperties.
    """
    units = [s for s in p.get('subproperties') or [] if s['name'] == 'unit']
    if p.get('kind') in PHYSICAL:
        if len(units) != 1:
            return [f"kind {p['kind']} needs exactly one unit subproperty (0015)"]
        if units[0] != UNIT_FORM:
            return ['unit subproperty departs from the fixed form of 0015']
    elif p.get('kind') in ('dimensionless', 'inapplicable') and units:
        return [f"kind {p['kind']} carries no unit subproperty (0015)"]
    return []
