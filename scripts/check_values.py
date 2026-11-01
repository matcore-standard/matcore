#!/usr/bin/env python3
"""Check a property's structured `values` against decision 0013.

Each key applies only to the types it belongs to; `terms` and `enum`, and `format` and `pattern`,
exclude each other; `minimum` does not exceed `maximum`; a format is a JSON Schema 2020-12 name;
a pattern compiles; and every example satisfies the property's own type, extent and values, with
formats checked in full. Called by scripts/validate_schema.py for every property.
"""
import re

from jsonschema import Draft202012Validator

# JSON Schema 2020-12 Validation §7.3 (decision 0013 item 1).
FORMATS = {'date-time', 'date', 'time', 'duration', 'email', 'idn-email', 'hostname', 'idn-hostname', 'ipv4', 'ipv6',
           'uri', 'uri-reference', 'iri', 'iri-reference', 'uuid', 'uri-template', 'json-pointer',
           'relative-json-pointer', 'regex'}
JSON_TYPE = {'string': 'string', 'int': 'integer', 'float': 'number', 'bool': 'boolean'}
FOR_TYPE = {'terms': {'string'}, 'enum': {'string'}, 'format': {'string'}, 'pattern': {'string'},
            'minimum': {'int', 'float'}, 'maximum': {'int', 'float'}}


def value_schema(p):
    """Return the JSON Schema that one value of a property must satisfy.

    p (dict): property entry. `terms` adds nothing, since unlisted terms conform; a pattern must match
    the whole value; each extent dimension wraps the value in an array, of fixed length when an integer.
    """
    v = p.get('values') or {}
    s = {'type': JSON_TYPE[p['type']]} if p.get('type') in JSON_TYPE else {}
    s |= {k: v[k] for k in ('enum', 'minimum', 'maximum', 'format') if k in v}
    if 'pattern' in v:
        s['pattern'] = f"^(?:{v['pattern']})$"
    extent = p.get('extent') if isinstance(p.get('extent'), list) else []
    for n in reversed(extent):
        s = {'type': 'array', 'items': s} | ({'minItems': n, 'maxItems': n} if isinstance(n, int) else {})
    return s


def values_errors(p):
    """Return the errors in a property's `values`, as messages.

    p (dict): property entry with `type`, `extent` and `values`.
    """
    v = p.get('values') or {}
    out = [f"values.{k} needs type {' or '.join(sorted(types))}, not {p.get('type')}"
           for k, types in FOR_TYPE.items() if k in v and p.get('type') not in types]
    if 'terms' in v and 'enum' in v:
        out.append('values has both terms and enum')
    if 'format' in v and 'pattern' in v:
        out.append('values has both format and pattern')
    if 'minimum' in v and 'maximum' in v and v['minimum'] > v['maximum']:
        out.append(f"values.minimum {v['minimum']} exceeds values.maximum {v['maximum']}")
    if 'format' in v and v['format'] not in FORMATS:
        out.append(f"values.format {v['format']!r} is not a JSON Schema 2020-12 format")
    if 'pattern' in v:
        try:
            re.compile(v['pattern'])
        except re.error as e:
            out.append(f"values.pattern does not compile: {e}")
    if not out:
        check = Draft202012Validator(value_schema(p), format_checker=Draft202012Validator.FORMAT_CHECKER)
        out += [f'example {ex!r}: {e.message}' for ex in v.get('examples') or [] for e in check.iter_errors(ex)]
    return out
