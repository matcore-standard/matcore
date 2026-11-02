"""Properties whose structure a decision record fixes keep that structure."""
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def tree(p):
    """Return a property's structure as nested tuples: name, required, repeatable, type, scheme terms, children.

    p (dict): property entry, with nested subproperties.
    """
    terms = tuple((p.get('values') or {}).get('terms', ()))
    return (p['name'], p['required'], p['repeatable'], p['type'], terms,
            tuple(tree(s) for s in p.get('subproperties') or []))


def legacy_fields(p):
    """Return the legacy_* fields left in a property and its subproperties.

    p (dict): property entry.
    """
    return [k for k in p if k.startswith('legacy_')] + [k for s in p.get('subproperties') or [] for k in legacy_fields(s)]


def minimal(name):
    """Return a top-level property of schema/minimal.yaml.

    name (str): the property's name.
    """
    return next(p for p in yaml.safe_load(open(ROOT / 'schema/minimal.yaml'))['properties'] if p['name'] == name)


def test_title_is_one_required_string():
    """A dataset has exactly one title, a plain string that is not a physical quantity."""
    p = minimal('title')
    assert (p['required'], p['repeatable'], p['type'], p['extent'], p['kind'], p['recommended-unit']) == (
        True, False, 'string', [], 'inapplicable', None)
    assert legacy_fields(p) == []


@pytest.mark.parametrize('entity, required', [('creator', True), ('contributor', False)])
def test_creator_and_contributor_follow_0014(entity, required):
    """creator and contributor carry scheme-tagged identifiers and affiliations that hold their own
    identifier (0014 item 1); each keeps its own required flag (contributor is optional, 0011).

    An affiliation and its identifier sit in one container, so they cannot come apart; each identifier
    names its scheme, so a validator knows which rule its value follows.

    entity (str): the property's name; required (bool): whether a dataset must have one.
    """
    prop = minimal(entity)
    name = ('name', True, False, 'string', (), ())
    value = ('value', True, False, 'string', (), ())
    entity_scheme = ('scheme', True, False, 'string', ('ORCID', 'ROR', 'DOI', 'SWHID', 'ISNI'), ())
    affiliation_scheme = ('scheme', True, False, 'string', ('ROR', 'ISNI'), ())
    identifier = ('identifier', False, True, None, (), (value, entity_scheme))
    affiliation = ('affiliation', False, True, None, (), (
        name, ('identifier', False, False, None, (), (value, affiliation_scheme))))
    assert tree(prop) == (entity, required, True, None, (), (name, identifier, affiliation))
    assert legacy_fields(prop) == []
