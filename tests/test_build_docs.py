"""The generated section pages follow the layout of decision record 0007.

Each test reads the real schema, so a property lost, duplicated or mis-marked in rendering fails here.
"""
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_docs  # noqa: E402

SECTIONS = ['minimal', 'dft', 'md', 'mbpt', 'ml', 'pf', 'derived']
OPEN = re.compile(r'<details class="note mc-property" id="([^"]+)" markdown="1">')


def load(key):
    """Parse one schema section file.

    key (str): section key, e.g. 'minimal'.
    """
    return yaml.safe_load(open(ROOT / f'schema/{key}.yaml'))


def walk(props, path):
    """Yield (address, property) for every property at every depth, in schema order.

    props (list[dict]): property entries; path (list[str]): section key and names above them.
    """
    for p in props:
        here = path + [p['name']]
        yield '.'.join(here), p
        yield from walk(p.get('subproperties') or [], here)


def blocks(md):
    """Map each block id to (parent id or None, block text without nested blocks' lines).

    md (str): rendered page.
    """
    out, stack = {}, []
    for line in md.splitlines():
        m = OPEN.match(line)
        if m:
            out[m.group(1)] = [stack[-1] if stack else None, []]
            stack.append(m.group(1))
        elif line == '</details>':
            stack.pop()
        elif stack:
            out[stack[-1]][1].append(line)
    assert not stack, 'unclosed <details>'
    return {k: (parent, '\n'.join(lines)) for k, (parent, lines) in out.items()}


@pytest.fixture(scope='module', params=SECTIONS)
def page(request):
    """A rendered section with legacy text shown, plus its parsed schema."""
    data = load(request.param)
    return data, build_docs.render_section(data, show_legacy=True)


def test_every_property_is_one_block_at_its_address(page):
    """No property is lost, duplicated or misplaced: block ids are exactly the schema's paths, in order."""
    data, md = page
    expected = [addr for addr, _ in walk(data['properties'], [data['section']])]
    assert OPEN.findall(md) == expected


def test_subproperties_nest_inside_their_parent(page):
    """The nesting of blocks mirrors the subproperty tree, so the page shows the hierarchy."""
    data, md = page
    parsed = blocks(md)
    for addr, _ in walk(data['properties'], [data['section']]):
        parent = addr.rsplit('.', 1)[0]
        assert parsed[addr][0] == (parent if parent.count('.') else None)


def test_title_marks_required_and_repeatable(page):
    """Red asterisk exactly when required; autorenew icon when repeatable, autorenew-off otherwise."""
    data, md = page
    parsed = blocks(md)
    for addr, p in walk(data['properties'], [data['section']]):
        summary = next(l for l in parsed[addr][1].splitlines() if l.startswith('<summary>'))
        assert ('class="mc-star"' in summary) == p['required'], addr
        assert ('mc-i-rep' in summary) == p['repeatable'], addr
        assert ('mc-i-once' in summary) == (not p['repeatable']), addr


def test_attribute_table_states_required_and_repeatable_in_words(page):
    """The table repeats the title symbols in words, for readers who do not know the symbols. A container
    (a property with subproperties) has no value of its own, so its table shows only those two columns
    (0007 item 12); a property with a value shows all six."""
    data, md = page
    parsed = blocks(md)
    for addr, p in walk(data['properties'], [data['section']]):
        text = parsed[addr][1]
        if p.get('subproperties'):
            assert '| Required | Repeatable |\n|---|---|' in text, addr
            assert '| Type |' not in text, addr
        else:
            assert '| Required | Repeatable | Type | Extent | Kind | Rec. unit |' in text, addr
        row = f"| {'yes' if p['required'] else 'no'} | {'yes' if p['repeatable'] else 'no'} |"
        assert row in text, addr


def test_notes_are_always_shown(page):
    """Notes are part of the standard, not migration leftovers: they appear even without --show-legacy."""
    data, _ = page
    parsed = blocks(build_docs.render_section(data, show_legacy=False))
    for addr, p in walk(data['properties'], [data['section']]):
        for note in p.get('notes') or []:
            assert ' '.join(note.split()) in ' '.join(parsed[addr][1].split()), addr


def test_legacy_text_only_with_show_legacy():
    """Legacy prose is hidden by default and shown, labelled, with --show-legacy."""
    data = load('minimal')
    data['properties'] = [{'name': 'thing', 'required': False, 'description': 'A thing.', 'type': None,
                           'extent': None, 'kind': None, 'recommended-unit': None, 'values': None,
                           'repeatable': False, 'legacy_values': 'A string naming the thing.'}]
    hidden = build_docs.render_section(data, show_legacy=False)
    shown = build_docs.render_section(data, show_legacy=True)
    assert 'Legacy:' not in hidden and "class='legacy'" not in hidden
    assert 'Legacy: A string naming the thing.' in shown


def test_subproperty_boilerplate_is_never_shown():
    """'Contains SubProperties as listed below' and its variants are replaced by the nesting itself."""
    for key in SECTIONS:
        assert 'Contains Sub' not in build_docs.render_section(load(key), show_legacy=True), key


def test_values_text_states_every_values_key():
    """Each key of decision 0013 reaches the reader; an open vocabulary says that other values are allowed."""
    def text(values):
        """Return the values text of a string property with these values.

        values (dict): the property's values.
        """
        return build_docs.values_text({'type': 'string', 'values': values}, show_legacy=False)
    assert text({'terms': ['Electronic', 'Atomistic']}) == 'Recommended: `Electronic`, `Atomistic`. Other values are allowed.'
    assert text({'enum': ['a', 'b']}) == 'One of `a`, `b`.'
    assert text({'minimum': 0, 'maximum': 1}) == 'From 0 to 1.'
    assert text({'minimum': 0}) == 'Minimum: 0.'
    assert text({'maximum': 1}) == 'Maximum: 1.'
    assert text({'depends-on': 'method-class',
                 'cases': {'Electronic': {'terms': ['DFT']}, 'Atomistic': {'terms': ['MD']}}}) == (
        'Depends on `method-class`. For `Electronic`: Recommended: `DFT`. Other values are allowed. '
        'For `Atomistic`: Recommended: `MD`. Other values are allowed.')
    assert text({'format': 'date'}) == 'Format: `date` (JSON Schema 2020-12).'
    assert text({'pattern': 'MC-[0-9]{4}'}) == 'Pattern: `MC-[0-9]{4}`.'
    assert text({'format': 'uri', 'examples': ['https://ror.org/x'], 'note': 'An ROR ID.'}) == \
        'Format: `uri` (JSON Schema 2020-12). Examples: `https://ror.org/x`. An ROR ID.'



def test_bounds_on_an_array_apply_to_each_component():
    """A bound on a list of numbers holds for each number, so the page says so instead of reading as one
    bound on the whole list (0013, settled 2026-11-05); a scalar's bounds keep the plain wording."""
    def text(values, extent):
        """Return the values text of an int property with these values and extent.

        values (dict): the property's values; extent (list | str): its extent.
        """
        return build_docs.values_text({'type': 'int', 'extent': extent, 'values': values}, show_legacy=False)
    assert text({'minimum': 1}, [3]) == 'Minimum: 1, for each component.'
    assert text({'maximum': 9}, [3, 3]) == 'Maximum: 9, for each component.'
    assert text({'minimum': 0, 'maximum': 1}, [':']) == 'From 0 to 1, for each component.'
    assert text({'minimum': 1}, []) == 'Minimum: 1.'
    assert text({'minimum': 1}, 'any') == 'Minimum: 1.'
    md = build_docs.render_section(load('dft'), show_legacy=False)
    assert 'Minimum: 1, for each component.' in md


def test_list_examples_render_as_bracketed_lists():
    """An example of a list-valued property reads as a list of its items, not as Python's notation."""
    def text(examples, extent):
        """Return the values text of a string property with these examples and extent.

        examples (list): the examples; extent (list): the property's extent.
        """
        return build_docs.values_text({'type': 'string', 'extent': extent, 'values': {'examples': examples}},
                                      show_legacy=False)
    assert text([['GGA_X_PBE', 'GGA_C_PBE']], [':']) == 'Examples: `[GGA_X_PBE, GGA_C_PBE]`.'
    assert text([[[1, 0], [0, 1]]], [2, 2]) == 'Examples: `[[1, 0], [0, 1]]`.'
    assert text(['PBE', 'HSE06'], []) == 'Examples: `PBE`, `HSE06`.'

def test_inline_svgs_have_an_intrinsic_size():
    """An SVG without width/height renders page-wide until the stylesheet loads (0007 constraint)."""
    md = build_docs.render_section(load('minimal'), show_legacy=False)
    svgs = re.findall(r'<svg[^>]*>', md)
    assert svgs and all('width="' in s and 'height="' in s for s in svgs)


def test_page_starts_with_title_and_symbol_key():
    """Readers meet the key to the asterisk and the two icons before the first property."""
    data = load('minimal')
    md = build_docs.render_section(data, show_legacy=False)
    head = md.split('<details', 1)[0]
    assert head.startswith(f"# {data['title']}")
    assert 'mc-legend' in head and 'required' in head and 'repeatable' in head and 'at most once' in head


def test_every_section_has_its_introduction():
    """Each section opens with introductory text from the baseline .docx (0004 item 23)."""
    for key in SECTIONS:
        intro = load(key).get('introduction')
        assert isinstance(intro, str) and len(intro.split()) >= 10, key


def test_introduction_sits_between_title_and_symbol_key(page):
    """Readers meet the section's introduction right under its title, before the key and the properties."""
    data, md = page
    head = md.split('<details', 1)[0]
    first_words = ' '.join(data['introduction'].split()[:8])
    assert first_words in ' '.join(head.split())
    assert head.index(data['introduction'].split()[0]) < head.index('mc-legend')


def test_symbol_key_keeps_each_symbol_with_its_label():
    """On a narrow phone the key wraps between symbol-label pairs, never between a symbol and its label."""
    import re as _re
    groups = _re.findall(r'<span class="mc-key">(.*?)</span>(?=<span class="mc-key">|</span>$)', build_docs.KEY)
    assert len(groups) == 3, build_docs.KEY
    for group, (symbol, label) in zip(groups, [('mc-star', 'required'), ('mc-i-once', 'appears at most once'),
                                               ('mc-i-rep', 'repeatable')]):
        assert symbol in group and group.rstrip().endswith(label), group


def test_main_writes_every_page_and_honours_the_flag(tmp_path):
    """The command writes one page per section plus Annex U with its tables; --show-legacy controls legacy text."""
    build_docs.main(['--out', str(tmp_path)])
    names = sorted(p.name for p in tmp_path.iterdir())
    assert names == sorted([f'{i:02d}-{k}.md' for i, k in enumerate(SECTIONS, start=2)] + ['annex-i-identifiers.md', 'annex-u-units.md', 'index.md', 'revision-history.md'])
    assert 'Legacy:' not in (tmp_path / '03-dft.md').read_text()  # dft still holds legacy text
    build_docs.main(['--out', str(tmp_path), '--show-legacy'])
    assert 'Legacy:' in (tmp_path / '03-dft.md').read_text()


def test_every_section_has_a_well_formed_example():
    """Each section documents one real dataset with an XML example from the baseline (0004 items 23, 33)."""
    from xml.etree import ElementTree as ET
    for key in SECTIONS:
        examples = load(key).get('examples')
        assert examples and len(examples) == 1, key
        ex = examples[0]
        assert ex['caption'] and ex['source'].startswith('https://'), key
        ET.parse(ROOT / 'examples' / ex['file'])  # raises if not well-formed


def test_examples_appear_verbatim_after_the_properties(page):
    """The example closes the section page, its XML shown exactly as in examples/, with its dataset source linked."""
    data, md = page
    tail = md[md.rindex('</details>'):]
    for ex in data['examples']:
        xml = (ROOT / 'examples' / ex['file']).read_text()
        assert f"```xml\n{xml}```" in tail, ex['file']
        assert f"({ex['source']})" in tail and ex['caption'] in tail
        if ex.get('notes'):
            assert ' '.join(ex['notes'].split()) in ' '.join(tail.split())


UNITS = yaml.safe_load(open(ROOT / 'schema/units.yaml'))
FIXTURES = ROOT / 'tests/fixtures'


def test_kind_table_reproduces_the_annex():
    """Table U.3 generated from units.yaml equals the verified hand-typed table, character for character (0009)."""
    assert build_docs.render_kind_table(UNITS) == (FIXTURES / 'annex_u3_table.md').read_text()


def test_unit_table_reproduces_the_annex():
    """Table U.4 generated from units.yaml equals the verified hand-typed table, character for character (0009)."""
    assert build_docs.render_unit_table(UNITS) == (FIXTURES / 'annex_u4_table.md').read_text()


def test_annex_keeps_its_prose_and_gets_generated_tables(tmp_path):
    """Only the text between the markers is generated; the hand-written annex prose passes through unchanged."""
    build_docs.main(['--out', str(tmp_path)])
    out = (tmp_path / 'annex-u-units.md').read_text()
    src = (ROOT / 'docs/standard/annex-u-units.md').read_text()
    assert build_docs.render_kind_table(UNITS) in out and build_docs.render_unit_table(UNITS) in out
    strip = lambda s: re.sub(r'<!-- BEGIN generated:.*?<!-- END generated -->', '', s, flags=re.S)
    assert strip(out) == strip(src)
    assert '## U.2 Rules' in out and '## U.5 References' in out


def test_scheme_table_states_every_scheme_rule():
    """Table I.1 gives, for every scheme, what it identifies, its form, its pattern, its check digit, a valid
    example and its source, so readers see the exact rule a validator applies (0014)."""
    schemes = yaml.safe_load(open(ROOT / 'schema/identifier-schemes.yaml'))['schemes']
    table = build_docs.render_scheme_table(schemes)
    rows = table.strip().split('\n')
    assert rows[0] == '| Scheme | Identifies | Form | Pattern | Check digit | Example | Source |'
    assert len(rows) == 2 + len(schemes)
    import html
    import markdown
    rendered = markdown.markdown(table, extensions=['tables'])
    for name, s in schemes.items():
        row = next(r for r in rendered.split('<tr>') if f'<td>{name}</td>' in r)
        assert row.count('<td>') == 7, name  # a pipe in a pattern must not split its cell
        assert f'<code>{html.escape(s["pattern"], quote=False)}</code>' in row, name  # shown exactly
        assert s['example'] in row and s['source'] in row


def test_annex_i_keeps_its_prose_and_gets_its_table(tmp_path):
    """Annex I is built like Annex U: hand-written prose, a version line and Table I.1 generated (0014)."""
    build_docs.main(['--out', str(tmp_path)])
    out = (tmp_path / 'annex-i-identifiers.md').read_text()
    src = (ROOT / 'docs/standard/annex-i-identifiers.md').read_text()
    schemes = yaml.safe_load(open(ROOT / 'schema/identifier-schemes.yaml'))['schemes']
    assert build_docs.render_scheme_table(schemes) in out
    strip = lambda s: re.sub(r'<!-- BEGIN generated:.*?<!-- END generated -->', '', s, flags=re.S)
    assert strip(out) == strip(src)
    assert out.startswith('# Annex I — Identifier Schemes')
