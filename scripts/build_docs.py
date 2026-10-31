#!/usr/bin/env python3
"""Render schema/*.yaml into Markdown pages under docs/standard/ for MkDocs. Idempotent; run by CI on every push."""
import yaml
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/standard'; OUT.mkdir(parents=True, exist_ok=True)
ORDER = ['minimal','dft','md','mbpt','ml','pf','derived']

def fmt_extent(e):
    if e is None: return ''
    if e == 'any': return 'any'
    return '[' + ','.join(str(x) for x in e) + ']' if e else '[]'

def render(p, depth, lines):
    name = p['name'] + ('*' if p['required'] else '')
    lines.append(f"{'#'*min(depth+2,6)} `{name}`\n")
    lines.append(p['description'] + '\n')
    sig = []
    if p.get('type'): sig.append(f"**Type:** {p['type']}")
    if p.get('extent') is not None: sig.append(f"**Extent:** `{fmt_extent(p['extent'])}`")
    if p.get('kind'): sig.append(f"**Kind:** {p['kind']}")
    if p.get('recommended-unit'): sig.append(f"**Recommended unit:** `{p['recommended-unit']}`")
    sig.append(f"**Repeatable:** {p['repeatable']}")
    lines.append(' · '.join(sig) + '\n')
    if p.get('values'):
        v = p['values']
        if 'enum' in v: lines.append('**Allowed values:** ' + ', '.join(f'`{x}`' for x in v['enum']) + '\n')
        if 'examples' in v: lines.append('**Examples:** ' + ', '.join(f'`{x}`' for x in v['examples']) + '\n')
        if 'note' in v: lines.append(v['note'] + '\n')
    if p.get('legacy_values'): lines.append(f"*Values (legacy text):* {p['legacy_values']}\n")
    if p.get('legacy_unit'): lines.append(f"*Standard units (legacy text):* {p['legacy_unit']}\n")
    if p.get('convention'): lines.append(f"**Convention `{p['convention']['name']}`** (required): " + ', '.join(f'`{x}`' for x in p['convention']['enum']) + '\n')
    for n in p.get('notes', []): lines.append(f"> {n}\n")
    for s in p.get('subproperties', []): render(s, depth+1, lines)

for i, key in enumerate(ORDER, start=2):
    d = yaml.safe_load(open(ROOT/f'schema/{key}.yaml'))
    lines = [f"# {d['title']}\n", "\\* = required property\n"]
    for p in d['properties']: render(p, 1, lines)
    (OUT/f"{i:02d}-{key}.md").write_text('\n'.join(lines))
    print('wrote', OUT/f"{i:02d}-{key}.md")

u = yaml.safe_load(open(ROOT/'schema/units.yaml'))
rows = ["# Annex U — Unit Table (generated from schema/units.yaml)\n", "| Symbol | Kind | QUDT | GNU Units | Factor to SI | Source |", "|---|---|---|---|---|---|"]
for sym, r in u['units'].items():
    rows.append(f"| `{sym}` | {r['kind']} | {r['qudt'] or '—'} | {r['gnu'] or '—'} | {r['si_factor'] if r['si_factor'] is not None else '—'} | {r['source']} |")
(OUT/'annex-u-table.md').write_text('\n'.join(rows)); print('wrote annex-u-table.md')
