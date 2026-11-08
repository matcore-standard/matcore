#!/usr/bin/env python3
"""Parse and check a material component's chemical formula (decision 0034).

formula_errors() checks one formula against the grammar of the `formula` note; component_errors() also
checks it against the component's `variable` and `molecule` entries; example_errors() applies
component_errors() to every material component in examples/. Called by scripts/validate_schema.py;
component_errors() is also what an instance validator applies.

A count is held as a linear expression: a dict from variable name to coefficient, '' for the constant.
"""
import itertools
import re
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

from check_examples import SECTIONS

ROOT = Path(__file__).resolve().parents[1]
# The 118 symbols of the IUPAC Periodic Table, atomic numbers 1 to 118, as listed in the Standard Atomic
# Weights table of the IUPAC Commission on Isotopic Abundances and Atomic Weights (https://www.ciaaw.org/atomic-weights.htm).
ELEMENTS = (
    'H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y '
    'Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re '
    'Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds '
    'Rg Cn Nh Fl Mc Lv Ts Og').split()
NUMBER = re.compile(r'[0-9]+(\.[0-9]+)?')
USER = re.compile(r'J[a-z]+')
SYMBOL = re.compile(r'[A-Z][a-z]?')
TOLERANCE = 1e-9


class FormulaError(ValueError):
    """A formula that does not follow the grammar; the message says where."""


class Parser:
    """Recursive-descent parser for the grammar of decision 0034 item 3.

    text (str): the formula. After parse(), `groups` holds the text inside every pair of group parentheses.
    """

    def __init__(self, text):
        self.s, self.i, self.groups = text, 0, []

    def peek(self):
        """Return the next character, or '' at the end."""
        return self.s[self.i:self.i + 1]

    def fail(self, message):
        """Raise a FormulaError at the current position.

        message (str): what is wrong.
        """
        raise FormulaError(f'{self.s!r}, position {self.i}: {message}')

    def expect(self, char, what):
        """Consume char, or fail: 'unclosed' at the end, 'unexpected' before another character.

        char (str): the closing character; what (str): the bracket's name, for the message.
        """
        if self.peek() == char:
            self.i += 1
        elif self.peek():
            self.fail(f'unexpected character {self.peek()!r}')
        else:
            self.fail(f'unclosed {what}')

    def parse(self):
        """Return the formula's terms, a list of (item, count); an item is a symbol (str) or a list of terms."""
        if not self.s:
            raise FormulaError('empty formula')
        terms = self.formula()
        if self.peek():
            self.fail(f'unexpected character {self.peek()!r}')
        return terms

    def formula(self):
        """Return the terms up to the end or a closing parenthesis."""
        terms = []
        while self.peek() and self.peek() != ')':
            terms.append(self.term())
        if not terms:
            self.fail('empty group')
        return terms

    def term(self):
        """Return one (item, count): an element, a user-defined species or a group, then its count."""
        c, start = self.peek(), self.i
        if c == '(':
            self.i += 1
            item = self.formula()
            self.expect(')', 'parenthesis')
            self.groups.append(self.s[start + 1:self.i - 1])
        elif c == 'J':
            m = USER.match(self.s, self.i)
            if not m:
                self.fail('a user-defined species is J followed by lowercase letters')
            item, self.i = m.group(), m.end()
        elif c.isupper():
            m = SYMBOL.match(self.s, self.i)
            item = m.group() if m.group() in ELEMENTS else c
            if item not in ELEMENTS:
                self.fail(f'unknown element symbol {m.group()!r}')
            self.i += len(item)
        else:
            self.fail(f'unexpected character {c!r}')
        return item, self.count()

    def count(self):
        """Return the count after a term: a number, an expression in braces, or 1 when none is written."""
        if self.peek() == '{':
            self.i += 1
            e = self.expr()
            self.expect('}', 'brace')
            if set(e) <= {''}:
                self.fail('braces hold an expression with a variable; write a fixed count as a number')
            return e
        m = NUMBER.match(self.s, self.i)
        if not m:
            return {'': 1.0}
        value = float(m.group())
        if value == 0:
            self.fail('a count must be positive')
        if value == 1:
            self.fail('a count of 1 is omitted')
        self.i = m.end()
        return {'': value}

    def expr(self):
        """Return a sum of products, each optionally signed, as a linear expression."""
        out = {}
        while True:
            sign = 1
            if self.peek() in ('+', '-'):
                sign = -1 if self.peek() == '-' else 1
                self.i += 1
            for k, v in self.product().items():
                out[k] = out.get(k, 0) + sign * v
            if not (self.peek() and self.peek() in '+-'):
                return out

    def product(self):
        """Return a product of factors written side by side (implied multiplication), which must stay linear."""
        out = None
        while self.peek() and (self.peek().isdigit() or self.peek().islower() or self.peek() == '('):
            f = self.factor()
            if out is None:
                out = f
            elif set(out) - {''} and set(f) - {''}:
                self.fail('an expression must be linear in its variables')
            else:
                c, e = (out, f) if set(out) <= {''} else (f, out)
                out = {k: c[''] * v for k, v in e.items()}
        if out is None:
            self.fail(f'unexpected character {self.peek()!r}' if self.peek() else 'unclosed brace')
        return out

    def factor(self):
        """Return a number, a one-letter variable, or a parenthesized expression."""
        if self.peek() == '(':
            self.i += 1
            e = self.expr()
            self.expect(')', 'parenthesis')
            return e
        m = NUMBER.match(self.s, self.i)
        if m:
            self.i = m.end()
            return {'': float(m.group())}
        self.i += 1
        return {self.s[self.i - 1]: 1.0}


def formula_errors(formula):
    """Return the grammar errors of a formula, as messages (at most one: parsing stops at the first).

    formula (str): the formula.
    """
    try:
        Parser(formula).parse()
    except FormulaError as e:
        return [str(e)]
    return []


def counts(terms):
    """Yield every count in the terms, at every depth.

    terms (list): parsed terms, as Parser.parse() returns them.
    """
    for item, count in terms:
        yield count
        if isinstance(item, list):
            yield from counts(item)


def component_errors(formula, variables, molecules):
    """Return the errors of a material component's composition, as messages.

    formula (str): its `formula`; variables (list[tuple]): its `variable` entries as (name, value, type), type
    None when absent; molecules (list[str]): the `formula` of each of its `molecule` entries.
    """
    parser = Parser(formula)
    try:
        terms = parser.parse()
    except FormulaError as e:
        return [str(e)]
    out = [f'variable name {n!r} is not one lowercase letter' for n in {n for n, _, _ in variables}
           if not re.fullmatch('[a-z]', n)]
    used = {k for c in counts(terms) for k in c if k}
    given = {}
    for name, value, type_ in variables:
        given.setdefault(name, []).append((value, type_))
    out += [f'{n!r} has no variable entry' for n in sorted(used - set(given))]
    out += [f'variable {n!r} is not in the formula' for n in sorted(set(given) - used)]
    for name, entries in given.items():
        types = Counter(t for _, t in entries)
        out += [f'variable {name!r} has more than one {t}' for t, k in types.items() if t and k > 1]
    if not out:
        ranges = [[(n, min(v for v, _ in given[n])), (n, max(v for v, _ in given[n]))] for n in sorted(used)]
        for corner in itertools.product(*ranges):
            at = dict(corner)
            for c in counts(terms):
                if sum(v * at.get(k, 1) if k else v for k, v in c.items()) < -TOLERANCE:
                    where = ', '.join(f'{k}={v}' for k, v in at.items())
                    out.append(f'a count in {formula!r} falls below 0 at {where}')
                    break
    if len(terms) > 1 and all(isinstance(item, list) for item, _ in terms):
        total = Counter()
        for _, c in terms:
            total.update(c)
        if abs(total[''] - 1) > TOLERANCE or any(abs(v) > TOLERANCE for k, v in total.items() if k):
            out.append(f'the counts of the groups of {formula!r}, a mixture, must sum to 1')
    out += [f'molecule {m!r} is not a group of {formula!r} or the whole formula' for m in molecules
            if m != formula and m not in parser.groups]
    return out


def example_errors():
    """Return the composition errors of every material component in the examples the section files list."""
    out = []
    for section in SECTIONS:
        for ex in yaml.safe_load(open(ROOT / f'schema/{section}.yaml')).get('examples') or []:
            for mc in ET.parse(ROOT / 'examples' / ex['file']).getroot().iter('material-component'):
                variables = [(v.findtext('name'), float(v.findtext('value')), v.findtext('type'))
                             for v in mc.findall('variable')]
                molecules = [m.findtext('formula') for m in mc.findall('molecule')]
                out += [f'examples/{ex["file"]}: {e}'
                        for e in component_errors(mc.findtext('formula') or '', variables, molecules)]
    return out
