#!/usr/bin/env python3
"""Render schema/*.yaml into Markdown pages under docs/standard/ for MkDocs, and Annex U's tables from schema/units.yaml.

Section pages follow the layout of decision record 0007: every property is a collapsible block
whose id is its citable address, nested as in the schema. Styles and behaviour are in
docs/assets/matcore/layout.css and layout.js.

Usage: build_docs.py [--show-legacy] [--out DIR]. Idempotent. legacy_* text is left out unless
--show-legacy is given; CI builds with it until every section's typed fields are filled.
"""
import argparse
from pathlib import Path
from urllib.parse import urlsplit

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
# Each symbol and its label form one unbreakable group, so a narrow screen wraps between groups.
KEY = ('<span class="mc-legend">'
       '<span class="mc-key"><span class="mc-star">*</span> required</span>'
       f'<span class="mc-key"><span class="mc-icon mc-i-once">{ICONS[ONCE[0]]}</span> appears at most once</span>'
       f'<span class="mc-key"><span class="mc-icon mc-i-rep">{ICONS[REPEATABLE[0]]}</span> repeatable</span>'
       '</span>')


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
    if 'terms' in v:  # open vocabulary (0013)
        out.append('Recommended: ' + ', '.join(f'`{x}`' for x in v['terms']) + '. Other values are allowed.')
    if 'enum' in v:
        out.append('One of ' + ', '.join(f'`{x}`' for x in v['enum']) + '.')
    # On a value whose extent lists dimensions, a bound holds for each component (0013, settled 2026-11-05).
    each = ', for each component' if isinstance(p.get('extent'), list) and p['extent'] else ''
    if 'minimum' in v and 'maximum' in v:
        out.append(f"From {v['minimum']} to {v['maximum']}{each}.")
    elif 'minimum' in v or 'maximum' in v:
        out.append(f"Minimum: {v['minimum']}{each}." if 'minimum' in v else f"Maximum: {v['maximum']}{each}.")
    if 'format' in v:
        out.append(f"Format: `{v['format']}` (JSON Schema 2020-12).")
    if 'pattern' in v:
        out.append(f"Pattern: `{v['pattern']}`.")
    if 'depends-on' in v:  # values that depend on a sibling (0013, settled 2026-11-03)
        out.append(f"Depends on `{v['depends-on']}`.")
        out += [f'For `{k}`: ' + values_text({'extent': p.get('extent'), 'values': case}, False)
                for k, case in v['cases'].items()]
    if 'examples' in v:  # a list-valued example is written as a bracketed list of its items
        show = lambda x: '[' + ', '.join(show(i) for i in x) + ']' if isinstance(x, list) else str(x)
        out.append('Examples: ' + ', '.join(f'`{show(x)}`' for x in v['examples']) + '.')
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
            ' '.join(p['description'].split()), '']
    flags = f"| {'yes' if p['required'] else 'no'} | {'yes' if p['repeatable'] else 'no'} |"
    if p.get('subproperties'):  # a container has no value of its own: no type, extent, kind or unit (0007 item 12)
        out += ['| Required | Repeatable |', '|---|---|', flags, '']
    else:
        out += ['| Required | Repeatable | Type | Extent | Kind | Rec. unit |', '|---|---|---|---|---|---|',
                f"{flags} {p.get('type') or '—'} | {extent(p.get('extent'))} | {p.get('kind') or '—'} "
                f"| {p.get('recommended-unit') or '—'} |", '']
    text = values_text(p, show_legacy)
    if text:
        out += [text, '']
    for note in p.get('notes') or []:
        out += [' '.join(note.split()), '']
    for s in p.get('subproperties') or []:
        render_property(s, path + [s['name']], out, show_legacy)
    out += ['</details>', '']


def current_version():
    """Return the current version of the standard: the newest entry of schema/releases.yaml (decision 0010)."""
    return yaml.safe_load(open(ROOT / 'schema/releases.yaml'))['releases'][0]['version']


def version_line():
    """HTML line stating the page's version; layout.js relabels it on the unreleased `dev` site (decision 0010)."""
    v = current_version()
    return f'<p class="mc-version" data-version="{v}">Version {v}</p>'


def render_revision_history(releases):
    """Return the Revision History page, generated from schema/releases.yaml (decision 0010).

    releases (list[dict]): the `releases` list, newest first.
    """
    rows = ['# MatCore Standard Revisions', '', version_line(), '',
            '| Version | Date | Change Type | Section(s) | Description of Change | Approved By |',
            '|---|---|---|---|---|---|']
    for r in releases:
        rows.append(f"| {r['version']} | {r['date'].strftime('%d-%b-%Y')} | {r['change_type']} | {r['sections']} | "
                    f"{'<br> '.join(r['description'])} | {r['approved_by']} |")
    return '\n'.join(rows) + '\n'


def render_section(section, show_legacy):
    """Return the Markdown of a section page: title, introduction, symbol key, property blocks, examples.

    section (dict): a parsed schema/<section>.yaml; show_legacy (bool): whether to include legacy_* text.
    """
    out = [f"# {section['title']}", '', version_line(), '']
    if section.get('introduction'):
        out += [section['introduction'].strip(), '']
    out += [KEY, '']
    for p in section['properties']:
        render_property(p, [section['section'], p['name']], out, show_legacy)
    for ex in section.get('examples') or []:
        xml = (ROOT / 'examples' / ex['file']).read_text()
        out += [f"## Example: {ex['caption']}", '', f"Dataset source: [{ex['source']}]({ex['source']})", '',
                f'```xml\n{xml}```', '']
        if ex.get('notes'):
            out += [f"Note: {' '.join(ex['notes'].split())}", '']
    return '\n'.join(out)


SUPERSCRIPT = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


def format_factor(unit, kinds):
    """Format a unit's factor to coherent SI as Table U.4 prints it, e.g. '2.179 872 361 103 0 × 10⁻¹⁸ J'.

    The factor is exact decimal text (decision 0009), so its significant digits are printed as written.

    unit (dict): one entry of units.yaml `units`; kinds (dict): units.yaml `kinds`.
    """
    si_unit = kinds[unit['kind']]['si_unit']
    if unit.get('exact'):
        return f"{unit['exact']} {si_unit}"
    if unit['si_factor'] is None:
        return '—'
    if unit['si_factor'] == '1':
        return '1'
    mantissa, _, exponent = unit['si_factor'].partition('e')
    whole, _, frac = mantissa.partition('.')
    text = whole + ('.' + ' '.join(frac[i:i + 3] for i in range(0, len(frac), 3)) if frac else '')
    if exponent:
        text += ' × 10' + exponent.translate(SUPERSCRIPT)
    return f'{text} {si_unit}'


def render_kind_table(units):
    """Return Table U.3 (kinds) of Annex U, generated from units.yaml.

    units (dict): parsed schema/units.yaml.
    """
    rows = ['| Kind | QUDT QuantityKind | QUDT dimension vector | SI dimension |', '|---|---|---|---|']
    for name, k in units['kinds'].items():
        rows.append(f"| {name} | {k['qudt']} | {k['dimension']} | {k['si_dimension']} |")
    for name in units['reserved_kinds']:
        if name not in units['kinds']:
            rows.append(f'| {name} | — | — | — |')
    return '\n'.join(rows) + '\n'


def render_unit_table(units):
    """Return Table U.4 (unit symbols) of Annex U, generated from units.yaml.

    units (dict): parsed schema/units.yaml.
    """
    rows = ['| Symbol | Kind | QUDT Unit | GNU Units expression | Factor to coherent SI | Source |',
            '|---|---|---|---|---|---|']
    for sym, u in units['units'].items():
        rows.append(f"| `{sym}` | {u['kind']} | {u['qudt'] or '—'} | {u['gnu'] or '—'} | "
                    f"{format_factor(u, units['kinds'])} | {u['source']} |")
    return '\n'.join(rows) + '\n'


CHECK_DIGIT = {'iso7064-mod11-2': 'ISO/IEC 7064 MOD 11-2', 'iso7064-mod97-10-ror': 'ISO/IEC 7064 MOD 97-10 (ROR)', None: '—'}


def render_scheme_table(schemes):
    """Return Table I.1 (identifier schemes) of Annex I, generated from identifier-schemes.yaml.

    schemes (dict): scheme name -> entry, as in schema/identifier-schemes.yaml.
    """
    rows = ['| Scheme | Identifies | Form | Pattern | Check digit | Example | Source |', '|---|---|---|---|---|---|---|']
    for name, s in schemes.items():
        rows.append(f"| {name} | {', '.join(s['identifies'])} | {s['form']} | `{s['pattern']}` | "
                    f"{CHECK_DIGIT[s['checksum']]} | `{s['example']}` | [{urlsplit(s['source']).netloc}]({s['source']}) |")
    return '\n'.join(rows) + '\n'


def splice(text, name, table, source='schema/units.yaml'):
    """Replace the generated region `name` of a hand-written page with `table`.

    text (str): page with '<!-- BEGIN generated: name ... -->' and '<!-- END generated -->' markers;
    name (str): region name; table (str): generated Markdown; source (str): file the region comes from.
    """
    begin = f'<!-- BEGIN generated: {name} from {source} by scripts/build_docs.py; do not edit -->'
    end = '<!-- END generated -->'
    head, found, rest = text.partition(begin)
    if not found:
        raise SystemExit(f'marker for {name!r} missing')
    _, found, tail = rest.partition(end)
    if not found:
        raise SystemExit(f'end marker for {name!r} missing')
    return f'{head}{begin}\n{table}{end}{tail}'


def main(argv=None):
    """Write every section page, the Revision History, and the generated parts of the Preamble and Annexes U and I.

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
    version = version_line() + '\n'
    preamble = splice((ROOT / 'docs/standard/index.md').read_text(), 'version', version, 'schema/releases.yaml')
    path = args.out / 'index.md'
    path.write_text(preamble)
    print('wrote', path)
    path = args.out / 'revision-history.md'
    path.write_text(render_revision_history(yaml.safe_load(open(ROOT / 'schema/releases.yaml'))['releases']))
    print('wrote', path)
    units = yaml.safe_load(open(ROOT / 'schema/units.yaml'))
    annex = (ROOT / 'docs/standard/annex-u-units.md').read_text()
    annex = splice(annex, 'version', version, 'schema/releases.yaml')
    annex = splice(annex, 'Table U.3', render_kind_table(units))
    annex = splice(annex, 'Table U.4', render_unit_table(units))
    path = args.out / 'annex-u-units.md'
    path.write_text(annex)
    print('wrote', path)
    schemes = yaml.safe_load(open(ROOT / 'schema/identifier-schemes.yaml'))['schemes']
    annex = (ROOT / 'docs/standard/annex-i-identifiers.md').read_text()
    annex = splice(annex, 'version', version, 'schema/releases.yaml')
    annex = splice(annex, 'Table I.1', render_scheme_table(schemes), 'schema/identifier-schemes.yaml')
    path = args.out / 'annex-i-identifiers.md'
    path.write_text(annex)
    print('wrote', path)


if __name__ == '__main__':
    main()
