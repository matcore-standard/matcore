#!/usr/bin/env python3
"""Check that each example in examples/ follows the structure of the current standard (decision 0012).

For every element under <root>: it names a property defined at that place in the section's
hierarchy, every required property is present wherever its parent is, no non-repeatable
property appears twice, and only properties with subproperties contain elements. Values,
types and units are not checked; that waits for the typed fields (status step 5) and the
generated schema of status step 7.

Run alone, or through scripts/validate_schema.py, which CI runs. Exit non-zero on any error.
"""
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ['minimal', 'dft', 'md', 'mbpt', 'ml', 'pf', 'derived']


def structure_errors(parent, props, path):
    """Return the structural errors of an element's children against the properties allowed there.

    parent (Element): the element whose children are checked (an example's <root>, or a property);
    props (list[dict]): the schema properties allowed as its children; path (str): location for messages.
    """
    out = []
    by_name = {p['name']: p for p in props}
    counts = Counter(child.tag for child in parent)
    for tag, n in counts.items():
        if tag not in by_name:
            out.append(f'{path}: <{tag}> is not a property defined here')
        elif n > 1 and not by_name[tag]['repeatable']:
            out.append(f'{path}: <{tag}> appears {n} times but is not repeatable')
    for p in props:
        if p['required'] and p['name'] not in counts:
            out.append(f'{path}: required <{p["name"]}> is missing')
    for child in parent:
        p = by_name.get(child.tag)
        if p is None:
            continue
        subs = p.get('subproperties') or []
        if subs:
            out += structure_errors(child, subs, f'{path}/{child.tag}')
        elif len(child):
            out.append(f'{path}/{child.tag}: contains elements, but the property has no subproperties')
    return out


def all_errors():
    """Return the structural errors of every example listed in the section files."""
    out = []
    for key in SECTIONS:
        section = yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))
        for ex in section.get('examples') or []:
            root = ET.parse(ROOT / 'examples' / ex['file']).getroot()
            out += [f'examples/{ex["file"]}: {e}' for e in structure_errors(root, section['properties'], key)]
    return out


if __name__ == '__main__':
    errs = all_errors()
    for e in errs:
        print('ERROR', e)
    print(f'{"ok   " if not errs else "FAIL "} examples: {len(errs)} structural errors')
    sys.exit(1 if errs else 0)
