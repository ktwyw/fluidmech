"""Smoke test: every example, CHME 202 course script and showcase script must run without errors.

Showcase scripts run with FLUIDMECH_QUICK=1 (coarse grids, short runs) to keep the suite fast.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = (
    sorted(ROOT.glob("examples/[0-9][0-9]_*.py"))
    + sorted(ROOT.glob("course/week*/w*.py"))
    + sorted(ROOT.glob("showcase/advanced/a*.py"))
    + sorted(ROOT.glob("showcase/animations/g*.py"))
    + sorted(ROOT.glob("showcase/figures/f*.py"))
)


def _missing_requirements(script: Path) -> list[str]:
    for line in script.read_text().splitlines():
        if line.strip().startswith("# requires:"):
            names = [n.strip() for n in line.split(":", 1)[1].split(",")]
            return [n for n in names if importlib.util.find_spec(n) is None]
    return []


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: f"{p.parent.name}/{p.name}")
def test_script_runs(script, tmp_path):
    missing = _missing_requirements(script)
    if missing:
        pytest.skip(f"needs {', '.join(missing)}")
    env = {
        **os.environ,
        "MPLBACKEND": "Agg",
        "FLUIDMECH_QUICK": "1",
        "PYTHONPATH": os.pathsep.join(filter(None, [str(ROOT / "src"), os.environ.get("PYTHONPATH")])),
    }
    result = subprocess.run(
        [sys.executable, str(script)], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=300
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip(), "script printed nothing"
