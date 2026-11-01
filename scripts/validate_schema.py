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

v = Draft202012Validator(meta)
for f in sorted(glob.glob(str(ROOT/'schema/[a-z]*.yaml'))):
    if f.endswith(('meta-schema.yaml','units.yaml')): continue
    doc = yaml.safe_load(open(f))
    errs = sorted(v.iter_errors(doc), key=lambda e: e.path)
    for e in errs:
        print(f"ERROR {Path(f).name}: {'/'.join(map(str,e.path))}: {e.message}"); errors += 1
    walk(doc['properties'], Path(f).stem)
    print(f"ok    {Path(f).name}: {len(errs)} schema errors")
sys.exit(1 if errors else 0)
