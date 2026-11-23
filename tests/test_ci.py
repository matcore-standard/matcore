"""CI deploys the site from one run at a time (decision 0010's deploys share the gh-pages branch)."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_deploys_wait_for_one_another_and_none_is_dropped():
    """A push to main and a tag pushed with it both deploy to gh-pages; run together, the second push of gh-pages is
    rejected. Pushes share one concurrency group, so a deploy waits for the one before it, and the queue keeps every
    waiting run, so a release is never cancelled by a later push. Pull requests deploy nothing and are not held."""
    job = yaml.safe_load((ROOT / '.github/workflows/ci.yml').read_text())['jobs']['validate-and-build']
    c = job['concurrency']
    assert c['group'] == "${{ github.event_name == 'push' && 'deploy-gh-pages' || github.run_id }}"
    assert c['cancel-in-progress'] is False
    assert c['queue'] == 'max'
