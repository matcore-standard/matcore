"""Reference renderer for the standard-page layout of decision record 0007.

Not part of the build. It renders a section's properties as the nested, citable property
blocks of 0007, for build_docs.py to adopt. Run it to write a sample page:

    uv run python docs/decisions/0007-reference/render.py minimal OUT_DIR

which writes OUT_DIR/<section>.md. To view it, put that page, layout.css and layout.js in a
MkDocs docs folder whose mkdocs.yml has the settings listed in decision record 0007.
"""
import sys
from pathlib import Path

import material
import yaml

ROOT = Path(__file__).resolve().parents[3]
ICON_DIR = Path(material.__file__).parent / 'templates/.icons/material'

# Material Design Icons as bundled with mkdocs-material. Each SVG gets an intrinsic size so it
# never renders page-wide before the stylesheet applies.
ICONS = {n: (ICON_DIR / f'{n}.svg').read_text().strip().replace('<svg ', '<svg width="18" height="18" ', 1)
         for n in ('autorenew', 'autorenew-off')}
REPEATABLE = ('autorenew', 'repeatable: may appear more than once')
ONCE = ('autorenew-off', 'appears at most once')


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
    if 'note' in v:
        out.append(v['note'])
    if p.get('convention'):
        c = p['convention']
        out.append(f"Required `{c['name']}`: " + ' or '.join(f'`{x}`' for x in c['enum']) + '.')
    if show_legacy:
        if p.get('legacy_values') and not p['legacy_values'].startswith('Contains Sub'):
            out.append(f"<span class='legacy'>Legacy: {p['legacy_values']}</span>")
        if p.get('legacy_unit'):
            out.append(f"<span class='legacy'>Legacy unit: {p['legacy_unit']}</span>")
    return ' '.join(out)


def title_bar(p):
    """HTML of a property block's title: name, red asterisk if required, repeat icon at the right.

    p (dict): property entry.
    """
    star = '<span class="mc-star" title="required" aria-label="required">*</span>' if p['required'] else ''
    icon, tip = REPEATABLE if p['repeatable'] else ONCE
    cls = 'mc-i-rep' if p['repeatable'] else 'mc-i-once'
    return (f'<summary><span class="mc-name">{p["name"]}{star}</span>'
            f'<span class="mc-icon {cls}" title="{tip}" aria-label="{tip}">{ICONS[icon]}</span></summary>')


def render_property(p, path, out, show_legacy):
    """Append one property block, and its subproperties nested inside it, as Markdown-in-HTML.

    The block id is the property's citable address: section key and property path joined by dots.

    p (dict): property entry; path (list[str]): section key, then names down to p;
    out (list[str]): output lines; show_legacy (bool): whether to include legacy_* text.
    """
    out += [f'<details class="note mc-property" id="{".".join(path)}" markdown="1">', title_bar(p), '',
            p['description'], '',
            '| Required | Repeatable | Type | Extent | Kind | Rec. unit |',
            '|---|---|---|---|---|---|',
            f"| {'yes' if p['required'] else 'no'} | {'yes' if p['repeatable'] else 'no'} "
            f"| {p.get('type') or '—'} | {extent(p.get('extent'))} | {p.get('kind') or '—'} "
            f"| {p.get('recommended-unit') or '—'} |", '']
    text = values_text(p, show_legacy)
    if text:
        out += [text, '']
    for s in p.get('subproperties') or []:
        render_property(s, path + [s['name']], out, show_legacy)
    out += ['</details>', '']


KEY = ('<span class="mc-legend"><span class="mc-star">*</span> required &emsp; '
       f'<span class="mc-icon mc-i-once">{ICONS[ONCE[0]]}</span> appears at most once &emsp; '
       f'<span class="mc-icon mc-i-rep">{ICONS[REPEATABLE[0]]}</span> repeatable</span>')


def render_section(section, show_legacy=True):
    """Return the Markdown of a section page: title, symbol key, then every property block.

    section (dict): a parsed schema/<section>.yaml; show_legacy (bool): whether to include legacy_* text.
    """
    out = [f"# {section['title']}", '', KEY, '']
    for p in section['properties']:
        render_property(p, [section['section'], p['name']], out, show_legacy)
    return '\n'.join(out)


if __name__ == '__main__':
    key, out_dir = sys.argv[1], Path(sys.argv[2])
    data = yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f'{key}.md').write_text(render_section(data))
    print('wrote', out_dir / f'{key}.md')
