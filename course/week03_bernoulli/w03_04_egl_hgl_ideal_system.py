"""CHME 202 - Week 3 - Example 4: energy and hydraulic grade lines for frictionless flow.

Water drains from a large tank through a pipe that rises over a hump and ends
in a nozzle. With no friction the EGL is flat; the HGL dips wherever the
velocity is high. If the HGL drops below the pipe, the pressure is below
atmospheric; if the absolute pressure reaches the vapour pressure, the liquid cavitates.
Saves egl_hgl.png.

# requires: matplotlib
"""

import math

import matplotlib.pyplot as plt

from fluidmech.constants import P_ATM, G
from fluidmech.properties import water_density, water_vapor_pressure

rho = water_density(20)
z_surface = 10.0  # tank water level [m]
d_pipe, d_nozzle = 0.10, 0.05  # [m]
z_exit = 0.0  # nozzle elevation [m]
v_exit = math.sqrt(2 * G * (z_surface - z_exit))  # frictionless: Torricelli at the nozzle
Q = v_exit * math.pi * d_nozzle**2 / 4
v_pipe = Q / (math.pi * d_pipe**2 / 4)
print(f"Nozzle exit velocity {v_exit:.2f} m/s, Q = {Q * 1000:.1f} L/s, pipe velocity {v_pipe:.2f} m/s")

# Pipe route: (distance along pipe, elevation of pipe centreline)
route = [(0, 7.0), (5, 7.0), (10, 12.0), (15, 12.0), (22, 2.0), (30, 0.0)]
hv = v_pipe**2 / (2 * G)
print(f"\n{'x [m]':>6} {'z pipe':>7} {'EGL':>6} {'HGL':>6} {'p gauge [kPa]':>14} {'p abs [kPa]':>12}")
p_vap = water_vapor_pressure(20)
for x, z in route:
    hgl = z_surface - hv
    p = rho * G * (hgl - z)  # gauge pressure = rho g (HGL - pipe elevation)
    flag = "  <- below atmospheric" if p < 0 else ""
    if p + P_ATM < p_vap:
        flag = "  <- CAVITATION"
    print(f"{x:>6} {z:>7.1f} {z_surface:>6.2f} {hgl:>6.2f} {p / 1e3:>14.2f} {(p + P_ATM) / 1e3:>12.2f}{flag}")

z_max = z_surface - hv + (P_ATM - p_vap) / (rho * G)
print(f"\nThe hump could rise to at most {z_max:.1f} m before the water cavitates (ideal flow).")

fig, ax = plt.subplots(figsize=(8, 4))
xs, zs = zip(*route)
ax.plot(xs, zs, "k-", lw=3, label="pipe")
ax.axhline(z_surface, color="tab:red", label="EGL (frictionless: constant)")
ax.axhline(z_surface - hv, color="tab:blue", ls="--", label="HGL = EGL - V^2/2g")
ax.set(xlabel="distance along pipe [m]", ylabel="elevation / head [m]", title="Grade lines, ideal flow")
ax.legend()
ax.grid(alpha=0.4)
fig.tight_layout()
fig.savefig("egl_hgl.png", dpi=130)
print("Saved egl_hgl.png")
