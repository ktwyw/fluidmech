"""CHME 202 - Week 4 - Example 8: solving potential flow numerically (Laplace equation).

For 2D irrotational incompressible flow the stream function satisfies Laplace's
equation, psi_xx + psi_yy = 0. We solve it with finite differences for flow in a
channel partly blocked by a baffle - a first step towards CFD. Saves channel_baffle_flow.png.

# requires: numpy, matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np

L, H, h = 4.0, 1.0, 0.05  # channel length, height and grid spacing [m]
nx, ny = int(L / h) + 1, int(H / h) + 1
Q = 1.0  # flow per unit depth [m2/s]
psi = np.zeros((ny, nx))
y = np.linspace(0, H, ny)
psi[:, 0] = Q * y / H  # uniform inflow
psi[:, -1] = Q * y / H  # uniform outflow
psi[-1, :] = Q  # top wall
# baffle rising from the bottom wall at x = 2 m, height 0.5 m (psi = 0, like the bottom wall)
ib = int(2.0 / h)
jb = int(0.5 / h)
solid = np.zeros_like(psi, dtype=bool)
solid[: jb + 1, ib] = True

for it in range(20000):  # noqa: B007 - 'it' is reported after the loop
    old = psi.copy()
    # Jacobi update: each node = mean of its 4 neighbours
    psi[1:-1, 1:-1] = 0.25 * (psi[1:-1, 2:] + psi[1:-1, :-2] + psi[2:, 1:-1] + psi[:-2, 1:-1])
    psi[solid] = 0.0  # the baffle is part of the bottom streamline
    if np.max(np.abs(psi - old)) < 1e-7:
        break

u = np.gradient(psi, h, axis=0)  # u = d(psi)/dy
v_over = u[jb + 1 :, ib]
gap_flow = psi[-1, ib] - psi[jb, ib]  # flow between two streamlines = difference in psi
print(f"Converged after {it} Jacobi iterations on a {nx} x {ny} grid")
print(f"Mean velocity upstream: {Q / H:.2f} m/s")
print(f"Mean velocity in the gap above the baffle (continuity, gap 0.5 m): {Q / (H - 0.5):.2f} m/s")
print(
    f"Numerical flow through the gap = psi(top) - psi(tip) = {gap_flow:.3f} m2/s -> mean {gap_flow / (H - jb * h):.2f} m/s"
)
print(
    f"Peak velocity near the baffle tip: {v_over.max():.2f} m/s ({v_over.max() / (Q / (H - jb * h)):.1f}x the gap mean)"
)
print("The flow accelerates round the baffle tip; potential flow gives very high speeds at sharp edges")
print("(in a real, viscous flow the boundary layer separates there and a recirculation forms).")

fig, ax = plt.subplots(figsize=(9, 2.8))
ax.contour(np.linspace(0, L, nx), y, psi, levels=np.linspace(0, Q, 15), colors="tab:blue", linewidths=0.8)
ax.plot([2.0, 2.0], [0, 0.5], "k", lw=4)
ax.set_aspect("equal")
ax.set(xlabel="x [m]", ylabel="y [m]", title="Potential-flow streamlines past a baffle")
fig.tight_layout()
fig.savefig("channel_baffle_flow.png", dpi=130)
print("Saved channel_baffle_flow.png")
