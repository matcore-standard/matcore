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
meta = yaml.safe_load((ROOT/'schema/meta-schema.yaml').read_text())
units = yaml.safe_load((ROOT/'schema/units.yaml').read_text())
kinds = set(units['kinds']) | set(units['reserved_kinds'])
symbols = set(units['units'])
errors = 0

def walk(props, path):
    global errors
    for p in props:
        here = f"{path}/{p['name']}"
        k, u = p.get('kind'), p.get('recommended-unit')
        if k is not None and k not in kinds:
            print(f"ERROR {here}: unknown kind {k!r}"); errors += 1
        if u is not None:
            if u not in symbols: print(f"ERROR {here}: recommended-unit {u!r} not in units.yaml"); errors += 1
            elif k not in (None,'any') and units['units'][u]['kind'] != k:
                print(f"ERROR {here}: unit {u} has kind {units['units'][u]['kind']}, property kind is {k}"); errors += 1
        if p.get('type') in ('float','int') and k is None and p.get('legacy_values') is None:
            print(f"WARN  {here}: numeric type with no kind")
        walk(p.get('subproperties', []), here)

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
    if f.endswith(('meta-schema.yaml','units.yaml','releases.yaml')): continue
    doc = yaml.safe_load(open(f))
    errs = sorted(v.iter_errors(doc), key=lambda e: e.path)
    for e in errs:
        print(f"ERROR {Path(f).name}: {'/'.join(map(str,e.path))}: {e.message}"); errors += 1
    walk(doc['properties'], Path(f).stem)
    print(f"ok    {Path(f).name}: {len(errs)} schema errors")
# Examples follow the structure of the current standard (decision 0012).
sys.path.insert(0, str(ROOT/'scripts'))
from check_examples import all_errors
example_errors = all_errors()
for e in example_errors: print(f"ERROR {e}")
errors += len(example_errors)
print(f"ok    examples: {len(example_errors)} structural errors" if not example_errors else f"FAIL  examples: {len(example_errors)} structural errors")
sys.exit(1 if errors else 0)
