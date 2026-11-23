#!/usr/bin/env python3
"""Generate the JSON Schema of MatCore records in JSON, the first serialization, from schema/*.yaml (decision 0078).

The schema (draft 2020-12) describes one record: an object with one member per section, minimal required. It follows
0044's mapping: a container is an object of its subproperties and nothing else, a repeatable property an array of
entries, a leaf a JSON value of its Type nested as its Extent gives, never null. A unit beside a typed value takes the
Annex U symbols of that value's Kind (0015), plus dimensionless for reduced phase field lengths and times (0075); a
unit the schema does not fix takes any symbol, dimensionless or an x-gnu: expression. A generic parameter carries the
JSON member `type` and its value has that type (0044 item 3); it has a unit when that type is float or int and none
when it is string or bool (0084 item 1). A record may add members named with the prefix x- at any
level (0079). Open terms, references by label and formula grammar are left to other checks.

Usage: build_json_schema.py writes docs/standard/matcore.schema.json; scripts/build_docs.py calls write().
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ['minimal', 'dft', 'pim', 'ps', 'mbpt', 'ml', 'pf', 'derived']
OUT = ROOT / 'docs/standard/matcore.schema.json'
JSON_TYPES = {'string': 'string', 'float': 'number', 'int': 'integer', 'bool': 'boolean'}
REDUCED = {'domain-size', 'grid-spacing', 'time-step-size'}  # lengths and times that may be reduced (0075)
EXTENSION = {'^x-': {}}  # a Property a record adds, of any value (0079)


def nested(t):
    """Return a reference to a value of Type t, or arrays of such values to any depth.

    t (str): a MatCore Type, one of JSON_TYPES.
    """
    return {'$ref': f'#/$defs/any-depth-{t}'}


def leaf_schema(p):
    """Return the schema of a leaf's value: its Type, nested as its Extent gives, with its values' keys.

    p (dict): a property with a value of its own.
    """
    t, extent, v = p.get('type'), p.get('extent'), p.get('values') or {}
    if t not in JSON_TYPES:
        return {'not': {'type': ['object', 'null']}}  # Type any: fixed by the instance
    if extent == 'any':
        return nested(t)
    s = {'type': JSON_TYPES[t]}
    s |= {k: v[k] for k in ('minimum', 'maximum', 'pattern', 'format') if k in v}
    if 'enum' in v:
        s['enum'] = v['enum']
    for dim in reversed(extent or []):
        s = {'type': 'array', 'items': s} | ({'minItems': dim, 'maxItems': dim} if isinstance(dim, int) else {})
    return s


def unit_schema(value, container, units):
    """Return the schema of a `unit`: the symbols of its value's Kind, or any unit where the Kind is not fixed.

    value (dict | None): the sibling `value`, if any; container (str): the name of the property holding the unit;
    units (dict): the parsed schema/units.yaml.
    """
    kind = value.get('kind') if value else None
    if kind in units['kinds'] and kind != 'dimensionless':
        symbols = sorted(s for s, u in units['units'].items() if u['kind'] == kind)
        return {'enum': symbols + ['dimensionless'] * (container in REDUCED)}
    return {'anyOf': [{'enum': sorted(units['units'])}, {'type': 'string', 'pattern': '^x-gnu:'}]}


def property_schema(p, container, siblings, units):
    """Return the schema of one property, as an array of entries when it repeats.

    p (dict): the property; container (str): the name of the property holding it; siblings (list[dict]): the
    properties beside it; units (dict): the parsed schema/units.yaml.
    """
    if p.get('subproperties'):
        s = section_schema(p['subproperties'], units, p['name'])
    elif p['name'] == 'unit' and p.get('kind') == 'inapplicable':
        s = unit_schema(next((q for q in siblings if q['name'] == 'value'), None), container, units)
    else:
        s = leaf_schema(p)
    s = {'description': p['description']} | s if p.get('description') else s
    return {'type': 'array', 'items': s, 'minItems': 1} if p['repeatable'] else s


def section_schema(props, units, name=''):
    """Return the schema of an object holding these properties and nothing else.

    props (list[dict]): the properties; units (dict): the parsed schema/units.yaml; name (str): the name of the
    property holding them, if any.
    """
    s = {'type': 'object',
         'properties': {p['name']: property_schema(p, name, props, units) for p in props},
         'required': [p['name'] for p in props if p['required']],
         'patternProperties': EXTENSION,
         'additionalProperties': False}
    value = next((q for q in props if q['name'] == 'value'), None)
    if value and value.get('type') == value.get('kind') == 'any':  # a generic parameter (0016, 0044 item 3)
        s['properties']['type'] = {'enum': list(JSON_TYPES)}
        s['required'].append('type')
        s['allOf'] = [{'if': {'properties': {'type': {'const': t}}},
                       'then': {'properties': {'value': nested(t)}} | (
                           {'required': ['unit']} if t in ('float', 'int') else {'not': {'required': ['unit']}})}
                      for t in JSON_TYPES]  # a string or bool is not measured, so it has no unit (0084 item 1)
    return s


def build():
    """Return the JSON Schema of a MatCore record, generated from schema/*.yaml and schema/units.yaml."""
    units = yaml.safe_load((ROOT / 'schema/units.yaml').read_text())
    version = yaml.safe_load((ROOT / 'schema/releases.yaml').read_text())['releases'][0]['version']
    defs = {}
    for key in SECTIONS:
        doc = yaml.safe_load((ROOT / f'schema/{key}.yaml').read_text())
        defs[key] = {'title': doc['title']} | section_schema(doc['properties'], units)
    for t, j in JSON_TYPES.items():
        defs[f'any-depth-{t}'] = {'anyOf': [{'type': j}, {'type': 'array', 'items': nested(t)}]}
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': f'MatCore record, standard version {version}',
            'description': 'A MatCore metadata record in JSON, generated from the standard (decision record 0078).',
            'type': 'object',
            'properties': {key: {'$ref': f'#/$defs/{key}'} for key in SECTIONS},
            'required': ['minimal'],
            'patternProperties': EXTENSION,
            'additionalProperties': False,
            '$defs': defs}


def write(path=OUT):
    """Write the generated schema as JSON.

    path (Path): the output file.
    """
    path.write_text(json.dumps(build(), indent=1, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    write()
    print(f'wrote {OUT}')
