"""The identifiers written in the examples pass Annex I (0014, 0033). The examples' structure is checked against the
generated JSON Schema in tests/test_json_schema.py (0078)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def identifiers(obj):
    """Yield (scheme, value) for every `identifier` entry found anywhere in a JSON value.

    obj: a parsed JSON value.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'identifier':
                for i in v if isinstance(v, list) else [v]:
                    if isinstance(i, dict) and 'scheme' in i:
                        yield i['scheme'], i['value']
            yield from identifiers(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from identifiers(v)


def test_example_identifiers_pass_annex_i():
    """Every identifier written in an example, with its scheme, is in Annex I's form and passes its check
    digits, so the examples show values a validator accepts; the record's author carries an ORCID iD
    (0033, amended)."""
    from check_identifiers import identifier_errors
    minimal = json.loads((ROOT / 'examples/minimal.json').read_text(encoding='utf-8'))['minimal']
    author = minimal['matcore']['record-author'][0]['identifier']
    assert {'value': 'https://orcid.org/0000-0003-3311-6299', 'scheme': 'ORCID'} in author
    assert all(identifier_errors(scheme, value) == [] for scheme, value in identifiers(minimal))
