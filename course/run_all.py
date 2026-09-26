"""Run every CHME 202 course script and report which ones pass.

Usage:  python course/run_all.py [--verbose]
Figures are written to course/output/.
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
    scripts = sorted(HERE.glob("week*/w*.py"))
    failures = []
    for script in scripts:
        result = subprocess.run([sys.executable, str(script)], cwd=OUTPUT, env=env, capture_output=True, text=True)
        ok = result.returncode == 0
        print(f"[{'PASS' if ok else 'FAIL'}] {script.parent.name}/{script.name}")
        if verbose or not ok:
            print(result.stdout)
            print(result.stderr)
        if not ok:
            failures.append(script.name)
    print(f"\n{len(scripts) - len(failures)}/{len(scripts)} course scripts ran successfully.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
