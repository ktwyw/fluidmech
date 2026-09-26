"""Run every example script in this folder and report which ones pass.

Usage:  python examples/run_all.py [--verbose]
Figures produced by the plotting examples are written to examples/output/.
"""

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"


def main() -> int:
    verbose = "--verbose" in sys.argv
    OUTPUT.mkdir(exist_ok=True)
    env = {**os.environ, "MPLBACKEND": "Agg"}
    scripts = sorted(p for p in HERE.glob("[0-9][0-9]_*.py"))
    failures = []
    for script in scripts:
        result = subprocess.run([sys.executable, str(script)], cwd=OUTPUT, env=env, capture_output=True, text=True)
        ok = result.returncode == 0
        print(f"[{'PASS' if ok else 'FAIL'}] {script.name}")
        if verbose or not ok:
            print(result.stdout)
            print(result.stderr)
        if not ok:
            failures.append(script.name)
    print(f"\n{len(scripts) - len(failures)}/{len(scripts)} examples ran successfully.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
