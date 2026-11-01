#!/usr/bin/env python3
"""Check identifiers against schema/identifier-schemes.yaml (decision 0014).

identifier_errors() checks one value against its scheme's pattern and check digit; table_errors() checks
that each table entry is complete and that its own example passes; scheme_terms_errors() checks that a
`scheme` property under an `identifier` lists only schemes the table defines. Called by
scripts/validate_schema.py; identifier_errors() is also what an instance validator applies.
"""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMES = yaml.safe_load((ROOT / 'schema/identifier-schemes.yaml').read_text())['schemes']
FIELDS = {'identifies', 'form', 'pattern', 'checksum', 'example', 'source'}
CROCKFORD = '0123456789abcdefghjkmnpqrstvwxyz'


def mod11_2(chars):
    """Return True if the last of chars (str) is the ISO/IEC 7064 MOD 11-2 check character of the rest."""
    total = 0
    for c in chars[:-1]:
        total = (total + int(c)) * 2
    r = (12 - total % 11) % 11
    return chars[-1] == ('X' if r == 10 else str(r))


def mod97_10_ror(chars):
    """Return True if the last two of chars (str, e.g. '02mhbdp94') are ROR's checksum of the six before them."""
    n = 0
    for c in chars[1:7]:
        n = n * 32 + CROCKFORD.index(c)
    return chars[7:] == str(98 - (n * 100) % 97).zfill(2)


CHECKSUMS = {'iso7064-mod11-2': mod11_2, 'iso7064-mod97-10-ror': mod97_10_ror, None: None}


def identifier_errors(scheme, value, schemes=SCHEMES):
    """Return the errors of an identifier value, as messages; none for a scheme outside the table.

    scheme (str): the identifier's scheme; value (str): its value; schemes (dict): the scheme table.
    """
    s = schemes.get(scheme)
    if s is None:
        return []
    if not re.fullmatch(s['pattern'], value):
        return [f'{value!r} is not in the form of {scheme}: {s["form"]}']
    check = CHECKSUMS[s['checksum']]
    if check and not check(value.rsplit('/', 1)[-1].replace('-', '')):
        return [f'{value!r} fails the {scheme} check digit']
    return []


def table_errors(schemes):
    """Return the errors in a scheme table, as messages.

    schemes (dict): scheme name -> entry, as in schema/identifier-schemes.yaml.
    """
    out = []
    for name, s in schemes.items():
        if set(s) != FIELDS:
            out.append(f'{name}: fields must be {sorted(FIELDS)}')
        elif s['checksum'] not in CHECKSUMS:
            out.append(f'{name}: unknown checksum {s["checksum"]!r}')
        else:
            out += [f'{name}: example {e}' for e in identifier_errors(name, s['example'], schemes)]
    return out


def scheme_terms_errors(props, path):
    """Return errors for schemes that a `scheme` property under an `identifier` lists but the table lacks.

    props (list[dict]): properties, with nested subproperties; path (str): location for messages.
    """
    out = []
    for p in props:
        here = f"{path}/{p['name']}"
        for sub in p.get('subproperties') or []:
            if p['name'] == 'identifier' and sub['name'] == 'scheme':
                out += [f'{here}/scheme: term {t!r} is not in identifier-schemes.yaml'
                        for t in (sub.get('values') or {}).get('terms', []) if t not in SCHEMES]
        out += scheme_terms_errors(p.get('subproperties') or [], here)
    return out
