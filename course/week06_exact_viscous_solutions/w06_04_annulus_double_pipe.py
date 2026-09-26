"""CHME 202 - Week 6 - Example 4: laminar flow in a concentric annulus (double-pipe heat exchanger).

Exact solution versus the hydraulic-diameter approximation. The maximum
velocity is NOT at mid-gap: it shifts towards the inner (more curved) wall.
Saves annulus_profile.png.

# requires: matplotlib
"""

import math

import matplotlib.pyplot as plt

from fluidmech.laminar import annulus_flow_rate, annulus_fre, annulus_max_velocity_radius, annulus_velocity

mu, rho = 0.05, 900.0  # a viscous oil in the annulus
Ri, Ro = 0.0127, 0.0254  # 1-inch tube inside a 2-inch shell (radii)
G = 2000.0  # Pa/m
Q = annulus_flow_rate(Ri, Ro, G, mu)
area = math.pi * (Ro**2 - Ri**2)
V = Q / area
Dh = 2 * (Ro - Ri)  # hydraulic diameter of an annulus
re = rho * V * Dh / mu
r_star = annulus_max_velocity_radius(Ri, Ro)
print(f"Annulus Ri = {Ri * 1000:.1f} mm, Ro = {Ro * 1000:.1f} mm, G = {G} Pa/m, oil mu = {mu} Pa s")
print(f"  Q = {Q * 1000:.3f} L/s, mean V = {V:.3f} m/s, Re (on D_h) = {re:.0f} -> laminar")
print(f"  maximum velocity at r = {r_star * 1000:.2f} mm (mid-gap is {(Ri + Ro) / 2 * 1000:.2f} mm)")

k = Ri / Ro
print(f"\nFriction: exact f Re = {annulus_fre(k):.1f}; the circular-pipe value 64 with D_h would")
print(f"underpredict the pressure drop by {1 - 64 / annulus_fre(k):.0%}. The hydraulic diameter works")
print("reasonably for TURBULENT flow but not for laminar flow.\n")
print(f"{'Ri/Ro':>6} {'f Re':>7}")
for kk in [0.01, 0.1, 0.25, 0.5, 0.75, 0.99]:
    print(f"{kk:>6} {annulus_fre(kk):>7.1f}")
print("(tends to 64 as the inner tube vanishes... slowly! and to 96 = parallel plates as k -> 1)")

rs = [Ri + (Ro - Ri) * i / 100 for i in range(101)]  # radii across the gap
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([r * 1000 for r in rs], [annulus_velocity(r, Ri, Ro, G, mu) for r in rs])
ax.axvline(r_star * 1000, ls="--", color="grey", label="max velocity")
ax.axvline((Ri + Ro) / 2 * 1000, ls=":", color="k", label="mid-gap")
ax.set(xlabel="r [mm]", ylabel="u [m/s]", title="Laminar annular flow")
ax.legend()
fig.tight_layout()
fig.savefig("annulus_profile.png", dpi=130)
print("Saved annulus_profile.png")
