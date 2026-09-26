"""CHME 202 - Week 11 - Lab Assignment 3 (Python version): drag coefficients from a settling experiment.

Spheres of known size and density are timed over a marked distance in a
glycerol-water mixture. From each terminal velocity we compute Cd and Re and
compare them with the standard drag curve. Replace the data with your own.
Saves lab3_drag.png.

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech import Fluid
from fluidmech.constants import G
from fluidmech.drag import sphere_drag_coefficient

liquid = Fluid(1210.0, 0.060, "80 % glycerol")  # measure density and viscosity on the day!
tube_d, distance = 0.10, 0.50
# (material, diameter [mm], density [kg/m3], fall time over 0.50 m [s])
runs = [
    ("glass", 2.0, 2500, 13.54),
    ("glass", 3.0, 2500, 7.07),
    ("glass", 5.0, 2500, 3.8),
    ("steel", 2.0, 7800, 3.3),
    ("steel", 3.0, 7800, 2.01),
    ("steel", 4.0, 7800, 1.42),
    ("steel", 6.0, 7800, 1.01),
    ("steel", 8.0, 7800, 0.76),
]
print(f"Liquid: {liquid.name}, rho = {liquid.density} kg/m3, mu = {liquid.dynamic_viscosity} Pa s\n")
print(f"{'sphere':<14} {'U [m/s]':>8} {'Re':>8} {'Cd (exp)':>9} {'Cd (corr.)':>11} {'dev.':>6} {'d/D':>5}")
res_exp, cds = [], []
for mat, d_mm, rho_p, t in runs:
    d = d_mm / 1000  # mm -> m
    u = distance / t
    re = liquid.density * u * d / liquid.dynamic_viscosity
    # force balance at terminal velocity solved for Cd
    cd = 4 * (rho_p - liquid.density) * G * d / (3 * liquid.density * u**2)
    cd_ref = sphere_drag_coefficient(re)
    res_exp.append(re)
    cds.append(cd)
    print(
        f"{mat + f' {d_mm:.0f} mm':<14} {u:>8.4f} {re:>8.2f} {cd:>9.2f} {cd_ref:>11.2f} {cd / cd_ref - 1:>+6.0%} "
        f"{d / tube_d:>5.2f}"
    )
print("\nDiscussion: which points deviate most, and why? Consider the wall effect (d/D), whether the")
print("sphere had reached terminal velocity before the first mark, timing error for fast spheres,")
print("and the temperature sensitivity of glycerol viscosity (Week 1).")

fig, ax = plt.subplots(figsize=(6.5, 4.5))
rs = [10 ** (i / 20) for i in range(-30, 70)]  # Re 0.03-3000 for the reference curve
ax.loglog(rs, [sphere_drag_coefficient(r) for r in rs], "k", label="standard drag curve")
ax.loglog(res_exp, cds, "ro", label="experiment")
ax.set(xlabel="Re", ylabel="Cd", title="Lab 3: sphere drag")
ax.grid(alpha=0.3, which="both")
ax.legend()
fig.tight_layout()
fig.savefig("lab3_drag.png", dpi=130)
print("Saved lab3_drag.png")
