"""CHME 202 - Week 5 - Example 3: start-up of pressure-driven flow between plates.

A pressure gradient is suddenly applied to fluid at rest: u_t = G/rho + nu u_yy.
The velocity grows from zero to the parabolic Poiseuille profile on the
viscous time scale h^2 / nu. Saves startup_flow.png.

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech.laminar import plates_velocity

rho, mu = 1000.0, 1e-3  # water
nu = mu / rho
h, G = 0.01, 0.1  # 10 mm gap, G = -dp/dx [Pa/m]
n = 51
dy = h / (n - 1)
dt = 0.4 * dy**2 / nu  # explicit stability needs nu dt / dy^2 <= 0.5
u = [0.0] * n
u_steady = [plates_velocity(i * dy, h, G, mu) for i in range(n)]
snapshots = {}
t, t95 = 0.0, None
targets = [5.0, 10.0, 20.0, 40.0, 80.0]  # times at which to store profiles [s]
while t < 100.0:  # u_t = G/rho + nu u_yy, explicit time stepping
    u = [0.0] + [u[i] + dt * (G / rho + nu * (u[i + 1] - 2 * u[i] + u[i - 1]) / dy**2) for i in range(1, n - 1)] + [0.0]
    t += dt
    centre = u[n // 2] / u_steady[n // 2]
    if t95 is None and centre >= 0.95:
        t95 = t
    for tt in targets:
        if tt not in snapshots and t >= tt:
            snapshots[tt] = list(u)

print(f"Gap h = {h * 1000:.0f} mm of water, G = {G} Pa/m -> steady centreline speed {u_steady[n // 2] * 1000:.2f} mm/s")
print(f"Viscous time scale h^2/nu = {h**2 / nu:.0f} s")
print(f"Centreline reaches 95 % of steady speed after {t95:.0f} s = {t95 / (h**2 / nu):.3f} h^2/nu\n")
for tt, prof in snapshots.items():
    print(f"  t = {tt:5.0f} s: centreline at {prof[n // 2] / u_steady[n // 2]:5.1%} of steady")
print("\nWhy it matters: for a 1 m pipe of oil the same time scale is hours - 'fully developed' takes time.")

fig, ax = plt.subplots(figsize=(6, 4.5))
ys = [i * dy * 1000 for i in range(n)]  # m -> mm for the plot
for tt, prof in snapshots.items():
    ax.plot([v * 1000 for v in prof], ys, label=f"t = {tt:.0f} s")
ax.plot([v * 1000 for v in u_steady], ys, "k--", label="steady Poiseuille")
ax.set(xlabel="u [mm/s]", ylabel="y [mm]", title="Start-up of channel flow")
ax.legend()
fig.tight_layout()
fig.savefig("startup_flow.png", dpi=130)
print("Saved startup_flow.png")
