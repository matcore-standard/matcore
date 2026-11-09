"""The Preamble and the schema's prose keep the structure of the baseline .docx."""
import re
from pathlib import Path
from xml.etree import ElementTree as ET

import markdown
import pytest
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
    sections = ['minimal', 'dft', 'pim', 'md', 'mbpt', 'ml', 'pf', 'derived']
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


def test_objectives_state_fair_data_and_ai_readiness():
    """§1.1's first paragraph names the project's goals of FAIR data and AI readiness (0004 item 50)."""
    text = (ROOT / 'docs/standard/index.md').read_text()
    first = text.split('## 1.1 Objectives', 1)[1].strip().split('\n\n', 1)[0]
    assert first.endswith('guidelines for documentation of materials data. Its goals are to make computational '
                          'materials data FAIR (findable, accessible, interoperable and reusable) and to '
                          'contribute to its AI readiness.')


@pytest.mark.parametrize('acronym, expansion', [
    ('KIM', 'Knowledgebase of Interatomic Models (KIM)'),
    ('CODATA', 'Committee on Data of the International Science Council (CODATA)'),
    ('IRI', 'Internationalized Resource Identifier (IRI)'),
    ('QUDT', 'QUDT, an ontology of quantities, quantity kinds, units, dimensions and data types'),
])
def test_less_familiar_acronyms_are_spelled_out_at_first_use(acronym, expansion):
    """A reader of the Preamble may not know these acronyms, so each is spelled out where it first
    appears; QUDT gives no expansion of its name, so it is described in its own terms (0004 item 51).

    acronym (str): the acronym; expansion (str): the text at its first use.
    """
    text = (ROOT / 'docs/standard/index.md').read_text()
    first = re.search(rf'\b{acronym}\b', text).start()
    assert text.find(expansion) != -1 and text.find(expansion) <= first <= text.find(expansion) + len(expansion)


def test_scope_describes_computations_and_their_links():
    """§1.2 separates methods that supply energies and forces from those that use them, describes a dataset as
    computations that name what they use, and says MatCore does not record how to reproduce a dataset (0028;
    0046 item 11)."""
    text = (ROOT / 'docs/standard/index.md').read_text()
    assert ('Some methods supply energies and forces (e.g. DFT, or an interatomic potential), others use them to '
            'sample or evolve a system (e.g. MD). A dataset is described as one or more computations, each a group '
            'of calculations that share a method and its settings. A computation that uses the results of another '
            'names it, with the role the other plays: an ab initio molecular dynamics (AIMD) computation names the '
            'DFT computation that supplies its energies and forces. Each method-specific section describes the '
            'computations of its method. MatCore describes a dataset; it does not record how to reproduce its '
            'execution. The order of the calculations, their control flow and complete inputs belong to the '
            'provenance record of a workflow manager, to which a MatCore record may point.') in text
    assert 'It is allowable to include multiple method-specific metadata' not in text


def test_extent_states_the_order_of_an_array():
    """A value with more than one dimension is nested with its first index outermost, so every
    serialization writes the same array the same way (0038 item 1)."""
    text = (ROOT / 'docs/standard/index.md').read_text()
    assert ('or any when the schema does not fix it. A value with more than one dimension is a list of lists, the '
            'first index outermost: a value of extent [n,m] is a list of n entries, each a list of m components. '
            'A serialization preserves this nesting.') in text


def test_examples_are_said_to_be_in_json():
    """The Preamble names JSON, the first serialization, as the examples' format, and keeps them illustrative
    (0044 item 6)."""
    text = (ROOT / 'docs/standard/index.md').read_text()
    assert ('Examples are provided after each Standard specification in JSON, the first serialization adopted for '
            'MatCore instances. However, this is for clarification purposes only.') in text
    assert 'in XML format' not in text
