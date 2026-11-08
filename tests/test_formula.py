"""A material component's formula follows the grammar of decision 0034, so a tool can read its composition."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_formula import ELEMENTS, component_errors, formula_errors  # noqa: E402


def test_the_element_list_is_the_iupac_periodic_table():
    """The 118 symbols of the IUPAC Periodic Table, no more, so an unknown symbol is caught (0034 item 3)."""
    assert len(ELEMENTS) == len(set(ELEMENTS)) == 118
    assert {'H', 'Si', 'Xe', 'Og'} <= set(ELEMENTS) and not any(s.startswith('J') for s in ELEMENTS)


@pytest.mark.parametrize('formula', [
    'Si', 'SiO2', 'H2O2', 'HO', 'C2H6O', 'Si0.7Ge0.3', 'Si{x}Ge{1-x}', 'Li{2-2x}Mg{x}Cl2', 'Co{1-x}O',
    'Fe{3x}Li{4-x}Ti{2(1-x)}O6', 'Fe1.05Li3.65Ti1.3O6', '(H2O)0.9(C2H6O)0.1', '(SiO2){y}(GeO2){1-y}',
    '(Si0.3Ge0.7){y}(SiO2){1-y}', 'Ja0.8Jb0.2', 'Jlj', 'Xe', 'O2Si'])
def test_the_grammar_accepts_the_forms_of_0034(formula):
    """Elements in any order, decimal counts, variables in braces, groups and user-defined species all parse
    (0034 item 3; the Red Book IR-11.3.2 forms among them).

    formula (str): a formula that conforms.
    """
    assert formula_errors(formula) == []


@pytest.mark.parametrize('formula, fragment', [
    ('', 'empty'),
    ('si', 'unexpected'),
    ('Qq', 'unknown element'),
    ('Uut', 'unexpected'),           # U, then a lowercase letter that starts nothing
    ('J', 'user-defined species'),
    ('JA', 'user-defined species'),
    ('X-A', 'unknown element'),
    ('Si1', 'count of 1'),
    ('Si1.0Ge', 'count of 1'),
    ('Si0', 'positive'),
    ('Si{0.3}Ge{0.7}', 'variable'),
    ('Si{x*y}', 'unexpected'),
    ('Si{xy}', 'linear'),
    ('Si{x', 'unclosed'),
    ('(SiO2', 'unclosed'),
    ('SiO2)', 'unexpected'),
    ('Si Ge', 'unexpected'),
])
def test_the_grammar_rejects_what_0034_excludes(formula, fragment):
    """Lowercase starts, unknown symbols, a J without a lowercase name, the hyphenated X-NAME, an explicit
    count of 1, a zero count, braces without a variable, nonlinear expressions and unbalanced brackets are
    all reported (0034 item 3).

    formula (str): a formula that does not conform; fragment (str): part of the expected message.
    """
    found = formula_errors(formula)
    assert any(fragment in e for e in found), found


@pytest.mark.parametrize('formula, variables, molecules', [
    ('Si', [], []),
    ('Si{x}Ge{1-x}', [('x', 0, 'Minimum'), ('x', 1, 'Maximum')], []),
    ('Cu{x}Ni{1-x}', [('x', 0.5, 'Initial'), ('x', 0.42, 'Average')], []),
    ('(Si0.3Ge0.7){y}(SiO2){1-y}', [('y', 0.2, 'Minimum'), ('y', 0.5, 'Maximum')], []),
    ('(H2O)0.9(C2H6O)0.1', [], ['C2H6O']),
    ('C2H6O', [], ['C2H6O']),
])
def test_a_conforming_component_has_no_errors(formula, variables, molecules):
    """Variables with a range or several types, a mixture whose group counts sum to 1, and a molecule that is
    a group of the formula or the whole formula all conform (0034 items 2-4).

    formula (str); variables (list[tuple]): (name, value, type) entries; molecules (list[str]): molecule formulas.
    """
    assert component_errors(formula, variables, molecules) == []


@pytest.mark.parametrize('formula, variables, molecules, fragment', [
    ('Si{x}Ge{1-x}', [], [], "'x' has no variable entry"),
    ('Si', [('x', 0, 'Minimum'), ('x', 1, 'Maximum')], [], "'x' is not in the formula"),
    ('Si{x}Ge{1-x}', [('x', 0, 'Minimum'), ('x', 0.5, 'Minimum')], [], 'more than one Minimum'),
    ('Si{x}Ge{1-x}', [('x', 0, 'Minimum'), ('x', 1.5, 'Maximum')], [], 'below 0'),
    ('(H2O)0.9(C2H6O)0.2', [], [], 'sum to 1'),
    ('(SiO2){y}(GeO2){y}', [('y', 0, 'Minimum'), ('y', 0.5, 'Maximum')], [], 'sum to 1'),
    ('(H2O)0.9(C2H6O)0.1', [], ['C2H5OH'], 'not a group'),
    ('Ab', [], [], 'unknown element'),
    ('Si{xx}', [], [], 'linear'),
    ('Si', [('X', 0, 'Minimum'), ('X', 1, 'Maximum')], [], 'one lowercase letter'),
])
def test_each_component_rule_is_reported(formula, variables, molecules, fragment):
    """An undefined or unused variable, a repeated type, a negative
    count, mixture counts that do not sum to 1, a molecule that is not part of the formula, and a bad
    variable name are each reported (0034 items 2-4).

    formula (str); variables (list[tuple]); molecules (list[str]); fragment (str): part of the expected message.
    """
    found = component_errors(formula, variables, molecules)
    assert any(fragment in e for e in found), found


def test_validate_schema_checks_the_example_formulas(tmp_path):
    """validate_schema.py, which CI runs, fails when an example's formula breaks the grammar (0034 item 4)."""
    import shutil
    import subprocess
    for d in ('schema', 'scripts', 'examples'):
        shutil.copytree(ROOT / d, tmp_path / d)
    f = tmp_path / 'examples/minimal.xml'
    f.write_text(f.read_text().replace('<formula>Si</formula>', '<formula>Si1</formula>', 1))
    run = subprocess.run([sys.executable, tmp_path / 'scripts/validate_schema.py'], capture_output=True, text=True)
    assert run.returncode == 1 and 'count of 1' in run.stdout
