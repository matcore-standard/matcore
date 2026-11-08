"""The identifier-scheme table follows decision 0014: each scheme states how its values are written,
and its own example passes its pattern and check digit, so a broken rule cannot reach the validator."""
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_identifiers import SCHEMES, identifier_errors, scheme_terms_errors, table_errors  # noqa: E402


def test_table_lists_the_0014_and_0034_schemes_and_is_well_formed():
    """The five schemes of 0014 and the three topology schemes of 0034 are present, and every entry passes
    its own checks."""
    assert set(SCHEMES) == {'ORCID', 'ROR', 'DOI', 'SWHID', 'ISNI', 'AFLOW', 'InChI', 'SMILES'}
    assert SCHEMES['InChI']['identifies'] == SCHEMES['SMILES']['identifies'] == ['molecule']
    assert SCHEMES['AFLOW']['identifies'] == ['crystal structure']
    assert table_errors(SCHEMES) == []


@pytest.mark.parametrize('scheme, value, ok', [
    ('InChI', 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3', True),   # ethanol
    ('InChI', 'InChI=1S/C2H6O/c1-3-2/h1-2H3', True),        # dimethyl ether
    ('InChI', 'InChI=1/C2H6O/c1-2-3/h3H,2H2,1H3', False),   # non-standard prefix
    ('InChI', 'InChI=1BB/C30H18O14Ti', False),              # beta, "not stable across releases"
    ('InChI', 'C2H6O', False),
    ('SMILES', 'CCO', True), ('SMILES', '[CH3][CH2][OH]', True), ('SMILES', 'Oc1ccccc1.NCCO', True),
    ('SMILES', 'C C O', False), ('SMILES', '', False),
    ('AFLOW', 'ABC3_hR10_167_a_b_e', True),                 # calcite
    ('AFLOW', 'ABC3_oP20_62_c_c_cd', True),                 # aragonite
    ('AFLOW', 'AB2CD6_mP20_11_e_2e_e_2e2f', True),
    ('AFLOW', 'ABC3_hR10_167_a_b_e-002', False),            # library enumeration suffix
    ('AFLOW', 'ABC3_xR10_167_a_b_e', False),                # x is no crystal system
    ('AFLOW', 'CaCO3', False)])
def test_topology_identifiers(scheme, value, ok):
    """A molecule's InChI is the Standard InChI (prefix InChI=1S/), stable across software versions; a SMILES
    uses only the characters of the OpenSMILES grammar; a crystal's AFLOW prototype label has its four parts
    and no enumeration suffix, as OpenKIM writes it (0034 item 5, second amendment).

    scheme (str); value (str): a candidate identifier; ok (bool): whether it conforms.
    """
    assert (identifier_errors(scheme, value) == []) == ok


def test_real_identifiers_pass_and_altered_ones_fail():
    """Published identifiers conform; a changed check digit or a wrong form does not (0014 item 4)."""
    good = [('ORCID', 'https://orcid.org/0000-0001-5727-2427'), ('ROR', 'https://ror.org/02mhbdp94'),
            ('DOI', 'https://doi.org/10.1000/182'), ('ISNI', 'https://isni.org/isni/0000000121491740'),
            ('SWHID', 'swh:1:rel:22ece559cc7cc2364edc5e5593d63ae8bd229f9f')]
    for scheme, value in good:
        assert identifier_errors(scheme, value) == [], (scheme, value)
    bad = [('ORCID', 'https://orcid.org/0000-0001-5727-2428'),   # check digit changed
           ('ORCID', '0000-0001-5727-2427'),                     # bare, not the canonical URI
           ('ROR', 'https://ror.org/02mhbdp95'),                 # checksum changed
           ('ROR', 'https://ror.org/02mhbdu94'),                 # U is not Crockford base 32
           ('DOI', 'https://doi.org/11.1000/182'),               # prefix must start 10.
           ('ISNI', 'https://isni.org/isni/0000000121491741'),   # check digit changed
           ('SWHID', 'swh:1:abc:22ece559cc7cc2364edc5e5593d63ae8bd229f9f')]  # unknown object type
    for scheme, value in bad:
        assert identifier_errors(scheme, value), (scheme, value)


def test_an_unlisted_scheme_cannot_be_checked():
    """A scheme outside the table is open (0014 item 2): nothing is reported here."""
    assert identifier_errors('Scopus', 'anything') == []


def test_a_broken_entry_is_reported():
    """An entry missing a field, with an unknown check digit, or whose example fails is an error."""
    entry = dict(SCHEMES['ORCID'])
    assert table_errors({'X': {k: v for k, v in entry.items() if k != 'source'}})
    assert table_errors({'X': entry | {'checksum': 'luhn'}})
    assert table_errors({'X': entry | {'example': 'https://orcid.org/0000-0001-5727-2428'}})


def test_scheme_terms_must_be_in_the_table():
    """A `scheme` property under an `identifier` lists only schemes the table defines (0014 item 4)."""
    def identifier(terms):
        """Return an identifier container whose scheme lists these terms.

        terms (list[str]): the scheme's terms.
        """
        return {'name': 'identifier', 'subproperties': [
            {'name': 'value', 'values': None},
            {'name': 'scheme', 'values': {'terms': terms}}]}
    assert scheme_terms_errors([{'name': 'creator', 'subproperties': [identifier(['ORCID', 'ROR'])]}], 'minimal') == []
    assert scheme_terms_errors([{'name': 'creator', 'subproperties': [identifier(['ORCID', 'Scopus'])]}], 'minimal')


def test_validate_schema_checks_the_table(tmp_path):
    """validate_schema.py, which CI runs, fails when the table is broken."""
    import shutil
    import subprocess
    for d in ('schema', 'scripts', 'examples'):
        shutil.copytree(ROOT / d, tmp_path / d)
    f = tmp_path / 'schema/identifier-schemes.yaml'
    table = yaml.safe_load(f.read_text())
    table['schemes']['ORCID']['example'] = 'https://orcid.org/0000-0001-5727-2428'
    f.write_text(yaml.safe_dump(table, sort_keys=False))
    run = subprocess.run([sys.executable, tmp_path / 'scripts/validate_schema.py'], capture_output=True, text=True)
    assert run.returncode == 1 and 'identifier-schemes.yaml ORCID' in run.stdout
