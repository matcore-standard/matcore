#!/usr/bin/env python3
"""Validate schema/*.yaml against schema/meta-schema.yaml and check cross-references to units.yaml.
Exit non-zero on any error. Run in CI and before every commit that touches schema/."""
import sys, glob, yaml
from pathlib import Path
try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("pip install jsonschema pyyaml")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from check_values import dependency_errors, values_errors
from check_units import unit_errors
from check_generic import generic_errors
from check_identifiers import SCHEMES, scheme_terms_errors, table_errors
meta = yaml.safe_load((ROOT/'schema/meta-schema.yaml').read_text())
units = yaml.safe_load((ROOT/'schema/units.yaml').read_text())
kinds = set(units['kinds']) | set(units['reserved_kinds'])
symbols = set(units['units'])
errors = 0
# Field order of every property entry (decision 0004 item 6); the meta-schema rejects unknown fields.
ORDER = ['name', 'required', 'description', 'type', 'extent', 'kind', 'recommended-unit', 'values', 'repeatable',
         'convention', 'notes', 'legacy_values', 'legacy_unit', 'subproperties']

def walk(props, path):
    global errors
    for p in props:
        here = f"{path}/{p['name']}"
        expected = sorted(p, key=lambda k: ORDER.index(k) if k in ORDER else len(ORDER))
        if list(p) != expected:
            print(f"ERROR {here}: fields out of order; expected {', '.join(expected)}"); errors += 1
        k, u = p.get('kind'), p.get('recommended-unit')
        if k is not None and k not in kinds:
            print(f"ERROR {here}: unknown kind {k!r}"); errors += 1
        if u is not None:
            if u not in symbols: print(f"ERROR {here}: recommended-unit {u!r} not in units.yaml"); errors += 1
            elif k not in (None,'any') and units['units'][u]['kind'] != k:
                print(f"ERROR {here}: unit {u} has kind {units['units'][u]['kind']}, property kind is {k}"); errors += 1
        for e in values_errors(p) + dependency_errors(p, props) + unit_errors(p, props) + generic_errors(p):  # 0013, 0015, 0016
            print(f"ERROR {here}: {e}"); errors += 1
        if p.get('type') in ('float','int') and k is None and p.get('legacy_values') is None:
            print(f"WARN  {here}: numeric type with no kind")
        walk(p.get('subproperties', []), here)

def legacy_count(props):
    """Return the number of legacy_* fields in props (list[dict]), subproperties included."""
    return sum(sum(k.startswith('legacy_') for k in p) + legacy_count(p.get('subproperties') or []) for p in props)

for sym, u in units['units'].items():
    if u['kind'] not in kinds: print(f"ERROR units.yaml {sym}: kind {u['kind']} undefined"); errors += 1
    # si_factor is exact decimal text (decision 0009); null only for the reserved `dimensionless`.
    f = u.get('si_factor')
    if f is None:
        if sym != 'dimensionless': print(f"ERROR units.yaml {sym}: si_factor missing"); errors += 1
    elif not isinstance(f, str):
        print(f"ERROR units.yaml {sym}: si_factor {f!r} must be quoted decimal text"); errors += 1
    else:
        try: float(f)
        except ValueError: print(f"ERROR units.yaml {sym}: si_factor {f!r} is not a number"); errors += 1
for name, k in units['kinds'].items():
    for field in ('si_unit', 'si_dimension'):
        if not k.get(field): print(f"ERROR units.yaml kind {name}: {field} missing"); errors += 1

# identifier-schemes.yaml (decision 0014): complete entries whose examples pass their own rules.
for e in table_errors(SCHEMES): print(f"ERROR identifier-schemes.yaml {e}"); errors += 1

# releases.yaml (decision 0010): full semantic versions, newest first, dates not decreasing.
import datetime, re
releases = yaml.safe_load((ROOT/'schema/releases.yaml').read_text())['releases']
FIELDS = {'version', 'date', 'change_type', 'sections', 'description', 'approved_by'}
SEMVER = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)')
for r in releases:
    if set(r) != FIELDS: print(f"ERROR releases.yaml {r.get('version')}: fields must be {sorted(FIELDS)}"); errors += 1
    if not SEMVER.fullmatch(str(r.get('version'))): print(f"ERROR releases.yaml {r.get('version')!r}: not MAJOR.MINOR.PATCH"); errors += 1
    if not isinstance(r.get('date'), datetime.date): print(f"ERROR releases.yaml {r.get('version')}: date must be YYYY-MM-DD"); errors += 1
for newer, older in zip(releases, releases[1:]):
    key = lambda r: tuple(int(x) for x in str(r['version']).split('.')) if SEMVER.fullmatch(str(r['version'])) else ()
    if not key(newer) > key(older) or not newer['date'] >= older['date']:
        print(f"ERROR releases.yaml: {newer['version']} must be newer than {older['version']}, listed first"); errors += 1

v = Draft202012Validator(meta)
for f in sorted(glob.glob(str(ROOT/'schema/[a-z]*.yaml'))):
    if f.endswith(('meta-schema.yaml','units.yaml','releases.yaml','identifier-schemes.yaml')): continue
    doc = yaml.safe_load(open(f))
    errs = sorted(v.iter_errors(doc), key=lambda e: e.path)
    for e in errs:
        print(f"ERROR {Path(f).name}: {'/'.join(map(str,e.path))}: {e.message}"); errors += 1
    walk(doc['properties'], Path(f).stem)
    for e in scheme_terms_errors(doc['properties'], Path(f).stem):  # decision 0014
        print(f"ERROR {e}"); errors += 1
    # A section marked complete keeps no baseline prose (decision 0004 item 36).
    if doc.get('legacy_complete') and (n := legacy_count(doc['properties'])):
        print(f"ERROR {Path(f).name}: legacy_complete is true but {n} legacy_* fields remain"); errors += 1
    print(f"ok    {Path(f).name}: {len(errs)} schema errors")
# Examples follow the structure of the current standard (decision 0012).
from check_examples import all_errors
example_errors = all_errors()
for e in example_errors: print(f"ERROR {e}")
errors += len(example_errors)
print(f"ok    examples: {len(example_errors)} structural errors" if not example_errors else f"FAIL  examples: {len(example_errors)} structural errors")
sys.exit(1 if errors else 0)
