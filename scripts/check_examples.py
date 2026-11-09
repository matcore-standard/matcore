#!/usr/bin/env python3
"""Check that each example in examples/ follows the structure of the current standard (decisions 0012, 0044).

An example is a JSON object whose only member is its section, holding that section's top-level properties.
For every member: it names a property defined at that place in the section's hierarchy; every required
property is present wherever its parent is; a repeatable property is an array of entries; a container is
an object; a leaf with a Type has a value of that Type and of the shape its Extent gives; nothing is null.
A leaf whose Type is not yet filled (status step 5) takes any value but an object or null.

Run alone, or through scripts/validate_schema.py, which CI runs. Exit non-zero on any error.
"""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ['minimal', 'dft', 'pim', 'md', 'mbpt', 'ml', 'pf', 'derived']
SCALARS = {
    'string': (lambda v: isinstance(v, str), 'a string'),
    'bool': (lambda v: isinstance(v, bool), 'true or false'),
    'int': (lambda v: isinstance(v, int) and not isinstance(v, bool), 'an integer'),
    'float': (lambda v: isinstance(v, (int, float)) and not isinstance(v, bool), 'a number'),
}


def value_errors(value, p, path):
    """Return the errors of a leaf's value against its property's Type and Extent, as messages.

    value: the parsed JSON value; p (dict): the property; path (str): location for messages.
    """
    if value is None:
        return [f'{path}: null is not written; omit an optional property instead']
    if isinstance(value, dict):
        return [f'{path}: is an object, but the property has no subproperties']
    t, extent = p.get('type'), p.get('extent')
    if t not in SCALARS or not isinstance(extent, list):
        return []  # Type or Extent not fixed (any, file, or not yet filled)
    check, word = SCALARS[t]

    def shape(v, dims, where):
        """Return the errors of v against the remaining dimensions dims, as messages."""
        if not dims:
            return [] if check(v) else [f'{where}: must be {word}']
        if not isinstance(v, list):
            return [f'{where}: must be an array (extent {extent})']
        if dims[0] != ':' and len(v) != dims[0]:
            return [f'{where}: must have {dims[0]} components']
        return [e for i, item in enumerate(v) for e in shape(item, dims[1:], f'{where}[{i}]')]
    return shape(value, extent, path)


def structure_errors(obj, props, path):
    """Return the errors of an object's members against the properties allowed there, as messages.

    obj: the parsed JSON object (a section's members, or a container's); props (list[dict]): the schema
    properties allowed as its members; path (str): location for messages.
    """
    if not isinstance(obj, dict):
        return [f'{path}: must be an object']
    by_name = {p['name']: p for p in props}
    out = [f'{path}: "{k}" is not a property defined here' for k in obj if k not in by_name]
    out += [f'{path}: required "{p["name"]}" is missing' for p in props if p['required'] and p['name'] not in obj]
    for key, value in obj.items():
        p = by_name.get(key)
        if p is None:
            continue
        here = f'{path}/{key}'
        if p['repeatable'] and not isinstance(value, list):
            out.append(f'{here}: is repeatable, so it is an array of entries')
            continue
        for i, entry in enumerate(value if p['repeatable'] else [value]):
            where = f'{here}[{i}]' if p['repeatable'] else here
            subs = p.get('subproperties') or []
            out += structure_errors(entry, subs, where) if subs else value_errors(entry, p, where)
    return out


def all_errors():
    """Return the structural errors of every example listed in the section files."""
    out = []
    for key in SECTIONS:
        section = yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))
        for ex in section.get('examples') or []:
            doc = json.loads((ROOT / 'examples' / ex['file']).read_text(encoding='utf-8'))
            if not isinstance(doc, dict) or list(doc) != [key]:
                out.append(f'examples/{ex["file"]}: must be an object whose only member is "{key}"')
                continue
            out += [f'examples/{ex["file"]}: {e}' for e in structure_errors(doc[key], section['properties'], key)]
    return out


if __name__ == '__main__':
    errs = all_errors()
    for e in errs:
        print('ERROR', e)
    print(f'{"ok   " if not errs else "FAIL "} examples: {len(errs)} structural errors')
    sys.exit(1 if errs else 0)
