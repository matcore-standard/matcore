#!/usr/bin/env python3
"""Render schema/*.yaml into Markdown pages under docs/standard/ for MkDocs.

Section pages follow the layout of decision record 0007: every property is a collapsible block
whose id is its citable address, nested as in the schema. Styles and behaviour are in
docs/assets/matcore/layout.css and layout.js.

Usage: build_docs.py [--show-legacy] [--out DIR]. Idempotent. legacy_* text is left out unless
--show-legacy is given; CI builds with it until every section's typed fields are filled.
"""
import argparse
from pathlib import Path

import material
import yaml

ROOT = Path(__file__).resolve().parents[1]
ORDER = ['minimal', 'dft', 'md', 'mbpt', 'ml', 'pf', 'derived']
ICON_DIR = Path(material.__file__).parent / 'templates/.icons/material'

# Material Design Icons as bundled with mkdocs-material. Each SVG gets an intrinsic size so it
# never renders page-wide before the stylesheet applies.
ICONS = {n: (ICON_DIR / f'{n}.svg').read_text().strip().replace('<svg ', '<svg width="18" height="18" ', 1)
         for n in ('autorenew', 'autorenew-off')}
REPEATABLE = ('autorenew', 'mc-i-rep', 'repeatable: may appear more than once')
ONCE = ('autorenew-off', 'mc-i-once', 'appears at most once')
KEY = ('<span class="mc-legend"><span class="mc-star">*</span> required &emsp; '
       f'<span class="mc-icon mc-i-once">{ICONS[ONCE[0]]}</span> appears at most once &emsp; '
       f'<span class="mc-icon mc-i-rep">{ICONS[REPEATABLE[0]]}</span> repeatable</span>')


def extent(e):
    """Format a KIM extent for display.

    e (list | str | None): extent from the YAML; None while the typed field is unfilled.
    """
    if e is None:
        return '—'
    if e == 'any':
        return 'any'
    return '[' + ','.join(str(x) for x in e) + ']'


def values_text(p, show_legacy):
    """Text below a property's attribute table: structured values, then legacy prose if shown.

    p (dict): property entry; show_legacy (bool): whether to include legacy_* text.
    """
    out = []
    v = p.get('values') or {}
    if 'enum' in v:
        out.append('One of ' + ', '.join(f'`{x}`' for x in v['enum']) + '.')
    if 'examples' in v:
        out.append('Examples: ' + ', '.join(f'`{x}`' for x in v['examples']) + '.')
    if 'note' in v:
        out.append(v['note'])
    if p.get('convention'):
        c = p['convention']
        out.append(f"Required `{c['name']}`: " + ' or '.join(f'`{x}`' for x in c['enum']) + '.')
    if show_legacy:
        legacy = ' '.join((p.get('legacy_values') or '').split())
        if legacy and not legacy.startswith('Contains Sub'):  # the nesting shows subproperties
            out.append(f"<span class='legacy'>Legacy: {legacy}</span>")
        if p.get('legacy_unit'):
            out.append(f"<span class='legacy'>Legacy unit: {p['legacy_unit']}</span>")
    return ' '.join(out)


def title_bar(p):
    """HTML of a property block's title: name, red asterisk if required, repeat icon at the right.

    p (dict): property entry.
    """
    star = '<span class="mc-star" title="required" aria-label="required">*</span>' if p['required'] else ''
    icon, cls, tip = REPEATABLE if p['repeatable'] else ONCE
    return (f'<summary><span class="mc-name">{p["name"]}{star}</span>'
            f'<span class="mc-icon {cls}" title="{tip}" aria-label="{tip}">{ICONS[icon]}</span></summary>')


def render_property(p, path, out, show_legacy):
    """Append one property block, and its subproperties nested inside it, as Markdown-in-HTML.

    The block id is the property's citable address: section key and property path joined by dots.

    p (dict): property entry; path (list[str]): section key, then names down to p;
    out (list[str]): output lines; show_legacy (bool): whether to include legacy_* text.
    """
    out += [f'<details class="note mc-property" id="{".".join(path)}" markdown="1">', title_bar(p), '',
            ' '.join(p['description'].split()), '',
            '| Required | Repeatable | Type | Extent | Kind | Rec. unit |',
            '|---|---|---|---|---|---|',
            f"| {'yes' if p['required'] else 'no'} | {'yes' if p['repeatable'] else 'no'} "
            f"| {p.get('type') or '—'} | {extent(p.get('extent'))} | {p.get('kind') or '—'} "
            f"| {p.get('recommended-unit') or '—'} |", '']
    text = values_text(p, show_legacy)
    if text:
        out += [text, '']
    for note in p.get('notes') or []:
        out += [' '.join(note.split()), '']
    for s in p.get('subproperties') or []:
        render_property(s, path + [s['name']], out, show_legacy)
    out += ['</details>', '']


def render_section(section, show_legacy):
    """Return the Markdown of a section page: title, symbol key, then every property block.

    section (dict): a parsed schema/<section>.yaml; show_legacy (bool): whether to include legacy_* text.
    """
    out = [f"# {section['title']}", '', KEY, '']
    for p in section['properties']:
        render_property(p, [section['section'], p['name']], out, show_legacy)
    return '\n'.join(out)


def render_unit_table(units):
    """Return the Markdown of Annex U's unit table.

    units (dict): parsed schema/units.yaml.
    """
    rows = ["# Annex U — Unit Table (generated from schema/units.yaml)\n",
            "| Symbol | Kind | QUDT | GNU Units | Factor to SI | Source |", "|---|---|---|---|---|---|"]
    for sym, r in units['units'].items():
        rows.append(f"| `{sym}` | {r['kind']} | {r['qudt'] or '—'} | {r['gnu'] or '—'} | "
                    f"{r['si_factor'] if r['si_factor'] is not None else '—'} | {r['source']} |")
    return '\n'.join(rows)


def main(argv=None):
    """Write every section page and the unit table.

    argv (list[str] | None): command-line arguments; None reads sys.argv.
    """
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--show-legacy', action='store_true', help='include legacy_* text from the baseline migration')
    ap.add_argument('--out', type=Path, default=ROOT / 'docs/standard', help='output directory')
    args = ap.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    for i, key in enumerate(ORDER, start=2):
        section = yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))
        path = args.out / f'{i:02d}-{key}.md'
        path.write_text(render_section(section, args.show_legacy) + '\n')
        print('wrote', path)
    path = args.out / 'annex-u-table.md'
    path.write_text(render_unit_table(yaml.safe_load(open(ROOT / 'schema/units.yaml'))))
    print('wrote', path)


if __name__ == '__main__':
    main()
