import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
def test_validate(): assert subprocess.run([sys.executable, ROOT/'scripts/validate_schema.py']).returncode == 0
