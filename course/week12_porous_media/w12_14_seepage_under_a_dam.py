"""CHME 202 - Week 12 - Example 14: seepage under a dam - Darcy flow and the Laplace equation.

In a homogeneous soil the hydraulic head h satisfies Laplace's equation (Darcy + continuity,
as potential flow did in Week 4). We solve it with finite differences under an impervious
dam base, then compute the seepage flow and the uplift pressure on the base
(the uplift used in the dam-stability check of Week 2, Example 2).

# requires: numpy
"""

import numpy as np

from fluidmech.constants import G

K = 1e-5  # soil hydraulic conductivity [m/s]
Lx, Ly, dx = 60.0, 15.0, 0.5
H_up, H_down = 20.0, 0.0  # reservoir and tailwater heads above the ground surface [m]
x0, x1 = 22.0, 38.0  # dam base spans x0..x1 on the ground surface
nx, ny = int(Lx / dx) + 1, int(Ly / dx) + 1
h = np.full((ny, nx), (H_up + H_down) / 2)
xs = np.linspace(0, Lx, nx)
top = ny - 1  # row index of the ground surface
up = xs <= x0
down = xs >= x1
base = ~up & ~down
for _ in range(20000):  # Jacobi iterations until the head field stops changing
    old = h.copy()
    # Laplace: each node = mean of its neighbours
    h[1:-1, 1:-1] = 0.25 * (h[1:-1, 2:] + h[1:-1, :-2] + h[2:, 1:-1] + h[:-2, 1:-1])
    h[0, :] = h[1, :]  # impervious bedrock (no flow)
    h[:, 0], h[:, -1] = h[:, 1], h[:, -2]  # far boundaries: no flow
    h[top, up], h[top, down] = H_up, H_down  # reservoir and tailwater
    h[top, base] = h[top - 1, base]  # impervious dam base
    if np.max(np.abs(h - old)) < 1e-6:
        break
# seepage leaving through the downstream ground surface: q = sum K dh/dy dx
q = np.sum(K * (h[top - 1, down] - h[top, down]) / dx) * dx
print(f"Dam base {x1 - x0:.0f} m wide on {Ly:.0f} m of soil (K = {K} m/s), head difference {H_up - H_down:.0f} m")
print(f"Seepage under the dam: {q * 86400:.2f} m3/day per metre of dam length")
print("\nUplift pressure under the dam base (pressure head = total head - elevation, datum at the surface):")
for x in [x0, (x0 + x1) / 2 - 4, (x0 + x1) / 2, (x0 + x1) / 2 + 4, x1]:
    i = int(round(x / dx))
    print(f"  x = {x:5.1f} m: {h[top, i]:5.2f} m of water = {1000 * G * h[top, i] / 1e3:6.1f} kPa")
print("\nThe uplift falls from the full reservoir head to zero across the base - steeply near the two edges,")
print("gently in the middle - close to the linear (triangular) distribution assumed in Week 2.")
print("Cut-off walls and drains under the dam reduce both seepage and uplift.")
