#!/usr/bin/env python3
"""Check generic parameters against their canonical form (decision 0016).

A container is a generic parameter when one of its subproperties is a `value` whose Type and Kind are
both `any` (0019 item 3). Its
subproperties are then exactly `name`, `value`, `unit` and `description`, in that order, each with the
fields of FORM; `unit` also has the fixed description and note of 0001 B9 and A3.2. The descriptions of
`name`, `value` and `description` are the parameter's own. Called by scripts/validate_schema.py for
every property.
"""
UNIT_DESCRIPTION = 'The unit in which the associated value is expressed.'
UNIT_NOTE = ('A symbol from the MatCore Unit Table (Annex U), or the reserved symbol `dimensionless`. If and only if '
             'no Annex U symbol applies, a string prefixed `x-gnu:` giving a GNU Units expression (accepted with a '
             'validation warning).')
STRING = {'type': 'string', 'extent': [], 'kind': 'inapplicable', 'recommended-unit': None, 'values': None,
          'repeatable': False}
FORM = {
    'name': STRING | {'required': True},
    'value': STRING | {'required': True, 'type': 'any', 'extent': 'any', 'kind': 'any'},
    'unit': STRING | {'required': True, 'description': UNIT_DESCRIPTION, 'values': {'note': UNIT_NOTE}},
    'description': STRING | {'required': False},
}


def generic_errors(p):
    """Return the errors in a generic parameter's form, as messages; none if p is not one.

    p (dict): property entry, with its subproperties.
    """
    subs = p.get('subproperties') or []
    if not any(s['name'] == 'value' and s.get('type') == s.get('kind') == 'any' for s in subs):
        return []
    names = [s['name'] for s in subs]
    if names != list(FORM):
        return [f"a generic parameter has subproperties {', '.join(FORM)}, not {', '.join(names)} (0016)"]
    return [f"generic parameter {s['name']}: {k} departs from the form of 0016"
            for s in subs for k, v in FORM[s['name']].items() if s.get(k) != v] + \
           [f"generic parameter {s['name']}: has subproperties (0016)" for s in subs if s.get('subproperties')]
