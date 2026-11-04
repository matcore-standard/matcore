"""The Preamble and the schema's prose keep the structure of the baseline .docx."""
import re
from pathlib import Path
from xml.etree import ElementTree as ET

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]


def format_tree():
    """Return §1.3's bullet list as nested (first words, children) pairs, rendered as MkDocs renders it."""
    text = (ROOT / 'docs/standard/index.md').read_text()
    section = text.split('## 1.3 Format', 1)[1]
    html = markdown.markdown(section, extensions=['attr_list', 'md_in_html'])
    root = ET.fromstring(f'<div>{html}</div>')

    def items(ul):
        """Return the items of a list element.

        ul (Element): a <ul> element.
        """
        out = []
        for li in ul.findall('li'):
            words = ' '.join(''.join(li.find('p').itertext() if li.find('p') is not None else li.text or '').split()[:2])
            sub = li.find('ul')
            out.append((words, items(sub) if sub is not None else []))
        return out
    return items(root.find('ul'))


def test_format_bullets_nest_as_in_the_docx():
    """§1.3 has three levels: rules about names, the features of a property, and the rules under Values."""
    tree = dict(format_tree())
    assert list(tree) == ['Each Property', 'Required Properties', 'Properties have']
    features = dict(tree['Properties have'])
    assert list(features) == ['Definition: A', 'Type: The', 'Extent: The', 'Values: The', 'Kind: The',
                              'Recommended unit:', 'Repeatable: A', 'Note(s): Additional']
    assert [w for w, _ in features['Values: The']] == ['When appropriate', 'When a', 'A Property', 'A generic', 'A Property']


def test_notes_keep_the_space_after_note():
    """A note that opens with "Note:" keeps the space the .docx has after the colon."""
    def notes(props):
        """Yield every note of these properties and their subproperties.

        props (list[dict]): properties.
        """
        for p in props:
            yield from p.get('notes') or []
            yield from notes(p.get('subproperties') or [])
    sections = ['minimal', 'dft', 'md', 'mbpt', 'ml', 'pf', 'derived']
    found = [n for s in sections for n in notes(yaml.safe_load(open(ROOT / f'schema/{s}.yaml'))['properties'])]
    assert found and not [n for n in found if re.match(r'Note\s*\d*:\S', n)]


def test_bullet_symbols_change_with_depth():
    """Each nesting level keeps the .docx's own bullet (● ○ ■), so a reader can tell the levels apart."""
    css = re.sub(r'\s+', ' ', (ROOT / 'docs/assets/matcore/layout.css').read_text())
    assert '.md-typeset ul ul { list-style-type: circle; }' in css
    assert '.md-typeset ul ul ul { list-style-type: square; }' in css


def test_preamble_defines_the_generic_parameter():
    """§1.3 defines the term once, naming the four subproperties in their order, so the five properties
    that use the form can refer to it (0016 item 4)."""
    text = (ROOT / 'docs/standard/index.md').read_text()
    line = next(l for l in text.splitlines() if 'A *generic parameter*' in l)
    assert [line.index(f'`{n}` (') for n in ('name', 'value', 'unit', 'description')] == sorted(
        line.index(f'`{n}` (') for n in ('name', 'value', 'unit', 'description'))
    assert '`x-gnu:`' in line and '`any`' in line
