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
    """The table repeats the title symbols in words, for readers who do not know the symbols."""
    data, md = page
    parsed = blocks(md)
    for addr, p in walk(data['properties'], [data['section']]):
        text = parsed[addr][1]
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
    hidden = build_docs.render_section(data, show_legacy=False)
    shown = build_docs.render_section(data, show_legacy=True)
    assert 'Legacy:' not in hidden and "class='legacy'" not in hidden
    assert 'Legacy: A string containing the entity affiliation.' in shown


def test_subproperty_boilerplate_is_never_shown():
    """'Contains SubProperties as listed below' and its variants are replaced by the nesting itself."""
    for key in SECTIONS:
        assert 'Contains Sub' not in build_docs.render_section(load(key), show_legacy=True), key


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


def test_main_writes_every_page_and_honours_the_flag(tmp_path):
    """The command writes one page per section plus the unit table; --show-legacy controls legacy text."""
    build_docs.main(['--out', str(tmp_path)])
    names = sorted(p.name for p in tmp_path.iterdir())
    assert names == sorted([f'{i:02d}-{k}.md' for i, k in enumerate(SECTIONS, start=2)] + ['annex-u-table.md'])
    assert 'Legacy:' not in (tmp_path / '02-minimal.md').read_text()
    build_docs.main(['--out', str(tmp_path), '--show-legacy'])
    assert 'Legacy:' in (tmp_path / '02-minimal.md').read_text()

