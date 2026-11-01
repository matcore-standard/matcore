import subprocess, sys, pathlib

import jsonschema
import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
def test_validate(): assert subprocess.run([sys.executable, ROOT/'scripts/validate_schema.py']).returncode == 0


def test_meta_schema_types_the_introduction():
    """A section's introduction is Markdown text; anything else is rejected (0004 item 23)."""
    meta = yaml.safe_load(open(ROOT / 'schema/meta-schema.yaml'))
    section = {'section': 'x', 'title': 'X', 'matcore_version': '0', 'properties': []}
    jsonschema.validate(section | {'introduction': 'Some *Markdown* text.'}, meta)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(section | {'introduction': ['not', 'text']}, meta)

