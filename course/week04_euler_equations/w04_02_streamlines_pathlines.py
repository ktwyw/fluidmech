"""CHME 202 - Week 4 - Example 2: streamlines, pathlines and streaklines.

In steady flow the three coincide; in unsteady flow they do not. We release
particles in the oscillating flow u = U0, v = V0 cos(omega t) and compare.
Saves flow_lines.png.

# requires: matplotlib
"""

import math

import matplotlib.pyplot as plt

U0, V0, omega = 1.0, 0.8, 2.0  # mean speed [m/s], oscillation amplitude [m/s], frequency [rad/s]
dt, t_end = 0.002, 3.0  # integration time step and end time [s]


def velocity(t: float) -> tuple[float, float]:
    return U0, V0 * math.cos(omega * t)


def integrate(x: float, y: float, t0: float, t1: float) -> list[tuple[float, float]]:
    """Track a particle with the midpoint (RK2) method."""
    path = [(x, y)]
    t = t0
    while t < t1 - 1e-12:  # midpoint (RK2) integration of dx/dt = u(t), dy/dt = v(t)
        h = min(dt, t1 - t)
        u2, v2 = velocity(t + h / 2)
        x, y = x + h * u2, y + h * v2
        t += h
        path.append((x, y))
    return path


# Pathline: one particle released at t = 0 from the origin
pathline = integrate(0.0, 0.0, 0.0, t_end)

# Streakline at t_end: all particles released from the origin at earlier times
# positions now of particles released every 0.02 s
streak = [integrate(0.0, 0.0, tr, t_end)[-1] for tr in [i * 0.02 for i in range(int(t_end / 0.02))]]

# Streamline through the origin at t_end: tangent to the instantaneous velocity (a straight line here)
u, v = velocity(t_end)
streamline = [(s * u, s * v) for s in (0.0, t_end)]

print(f"At t = {t_end} s the instantaneous velocity is ({u:.2f}, {v:.2f}) m/s everywhere.")
print(f"Pathline end point: ({pathline[-1][0]:.3f}, {pathline[-1][1]:.3f}) m")
print("The pathline is a wavy curve, the streakline another wavy curve, the streamline a straight line.")
print("A dye filament (streakline) in unsteady flow does NOT show the instantaneous streamlines!")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(*zip(*pathline), label="pathline (particle released at t = 0)")
ax.plot(*zip(*streak), label=f"streakline at t = {t_end} s (dye from origin)")
ax.plot(*zip(*streamline), "--", label=f"streamline at t = {t_end} s")
ax.set(xlabel="x [m]", ylabel="y [m]", title="u = U0, v = V0 cos(wt)")
ax.set_aspect("equal")
ax.legend(fontsize=8)
ax.grid(alpha=0.4)
fig.tight_layout()
fig.savefig("flow_lines.png", dpi=130)
print("Saved flow_lines.png")
