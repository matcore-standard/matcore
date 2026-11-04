"""The standard's versions and release history follow decision record 0010."""
import datetime
import re
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_docs  # noqa: E402

SECTIONS = ['minimal', 'dft', 'md', 'mbpt', 'ml', 'pf', 'derived']
RELEASES = yaml.safe_load(open(ROOT / 'schema/releases.yaml'))['releases']
FIELDS = {'version', 'date', 'change_type', 'sections', 'description', 'approved_by'}


def semver(v):
    """Parse MAJOR.MINOR.PATCH into a tuple of ints.

    v (str): version string.
    """
    assert re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', v), v
    return tuple(int(x) for x in v.split('.'))


def test_releases_are_semantic_versions_newest_first():
    """Each release is a full semantic version, newer than the next entry and not dated before it (0010 item 1, 3)."""
    for r in RELEASES:
        assert set(r) == FIELDS, r['version']
        assert isinstance(r['date'], datetime.date), r['version']
    for newer, older in zip(RELEASES, RELEASES[1:]):
        assert semver(newer['version']) > semver(older['version'])
        assert newer['date'] >= older['date']


def test_first_repository_release_is_0_4_0_after_matcore_org_0_3_0():
    """0.4.0 directly follows the last matcore.org release, 0.3.0 (0010 item 7), and the current version
    is the newest entry (0010 item 3)."""
    versions = [r['version'] for r in RELEASES]
    assert versions[versions.index('0.4.0') + 1] == '0.3.0'
    assert build_docs.current_version() == versions[0]


def test_section_files_carry_no_version_of_their_own():
    """The version has one source, releases.yaml; the meta-schema rejects a per-section version (0010 item 3)."""
    meta = yaml.safe_load(open(ROOT / 'schema/meta-schema.yaml'))
    for key in SECTIONS:
        assert 'matcore_version' not in yaml.safe_load(open(ROOT / f'schema/{key}.yaml')), key
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({'section': 'x', 'title': 'X', 'matcore_version': '0.4.0', 'properties': []}, meta)


def test_revision_history_reproduces_the_published_rows():
    """The generated page keeps the matcore.org rows character for character, with the newest release on top."""
    page = build_docs.render_revision_history(RELEASES)
    rows = [l for l in page.splitlines() if l.startswith('| 0.')]
    assert rows[0].startswith(f"| {RELEASES[0]['version']} | ")
    expected = (ROOT / 'tests/fixtures/revision_history_0.3.0_and_earlier.md').read_text().splitlines()
    assert rows[-len(expected):] == expected


def test_every_standard_page_states_its_version(tmp_path):
    """Readers can tell which version a standard page belongs to (0010 item 5)."""
    build_docs.main(['--out', str(tmp_path)])
    line = f'data-version="{build_docs.current_version()}"'
    for page in [f'{i:02d}-{k}.md' for i, k in enumerate(SECTIONS, start=2)] + ['index.md', 'annex-u-units.md', 'revision-history.md']:
        assert line in (tmp_path / page).read_text(), page
