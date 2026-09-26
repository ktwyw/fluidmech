"""Example 2 - Plot a Moody diagram.

# requires: matplotlib

Run:  python examples/02_moody_diagram.py
The figure is saved as moody_diagram.png in the current directory.
"""

import matplotlib.pyplot as plt
import numpy as np

from fluidmech.pipe_flow import colebrook

fig, ax = plt.subplots(figsize=(10, 6.5))

re_lam = np.logspace(np.log10(600), np.log10(2300), 50)
ax.loglog(re_lam, 64 / re_lam, "k", lw=2, label="Laminar, f = 64/Re")

re_turb = np.logspace(np.log10(4000), 8, 300)
for rr in [0, 1e-6, 1e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2]:
    f = [colebrook(re, rr) for re in re_turb]
    ax.loglog(re_turb, f, lw=1.2)
    label = "smooth" if rr == 0 else f"{rr:g}"
    ax.text(1.05e8, f[-1], label, va="center", fontsize=8)

ax.axvspan(2300, 4000, color="grey", alpha=0.15, label="Transition")
ax.set_xlim(600, 1e8)
ax.set_ylim(0.006, 0.1)
ax.set_xlabel("Reynolds number, Re")
ax.set_ylabel("Darcy friction factor, f")
ax.set_title("Moody diagram (Colebrook-White)")
ax.text(1.05e8, 0.095, "eps/D", fontsize=9, weight="bold")
ax.grid(True, which="both", lw=0.4, alpha=0.6)
ax.legend(loc="lower left")
fig.tight_layout()
fig.savefig("moody_diagram.png", dpi=150)
print("Saved moody_diagram.png")
