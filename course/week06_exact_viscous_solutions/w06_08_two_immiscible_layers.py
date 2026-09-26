"""CHME 202 - Week 6 - Example 8: two immiscible liquids between parallel plates.

Oil (top) and water (bottom) flow under a common pressure gradient between fixed
plates. In each layer u'' = -G/mu; at the interface velocity and shear stress are
continuous. Four conditions -> four constants, solved as a linear system.
A classic exam problem (and the basis of liquid-liquid microfluidic contactors).
"""

from fluidmech.solvers import solve_linear

G = 100.0  # -dp/dx [Pa/m]
h1, h2 = 0.004, 0.004  # water layer (bottom) and oil layer (top) thicknesses [m]
mu1, mu2 = 1e-3, 0.02  # water, oil
H = h1 + h2
# u1 = -G y^2/(2 mu1) + a1 y + b1 ;  u2 = -G y^2/(2 mu2) + a2 y + b2
# unknowns x = [a1, b1, a2, b2]
A = [
    [0, 1, 0, 0],  # u1(0) = 0
    [0, 0, H, 1],  # u2(H) = 0
    [h1, 1, -h1, -1],  # u1(h1) = u2(h1)
    [mu1, 0, -mu2, 0],  # mu1 u1'(h1) = mu2 u2'(h1)
]
rhs = [0.0, G * H**2 / (2 * mu2), G * h1**2 / (2 * mu1) - G * h1**2 / (2 * mu2), 0.0]
a1, b1, a2, b2 = solve_linear(A, rhs)  # four constants from four conditions


def u(y):
    if y <= h1:
        return -G * y**2 / (2 * mu1) + a1 * y + b1
    return -G * y**2 / (2 * mu2) + a2 * y + b2


print(f"Water layer {h1 * 1000:.0f} mm (mu = {mu1}), oil layer {h2 * 1000:.0f} mm (mu = {mu2}), G = {G} Pa/m\n")
print(f"{'y [mm]':>7} {'u [mm/s]':>9}  layer")
for i in range(9):
    y = H * i / 8
    print(f"{y * 1000:>7.1f} {(0.0 if abs(u(y)) < 1e-9 else u(y)) * 1000:>9.2f}  {'water' if y <= h1 else 'oil'}")
n = 2000
q1 = sum(u((i + 0.5) * h1 / n) for i in range(n)) * h1 / n  # flow in each layer by the midpoint rule
q2 = sum(u(h1 + (i + 0.5) * h2 / n) for i in range(n)) * h2 / n
print(f"\nFlow per metre width: water {q1 * 1e4:.2f} cm2/s, oil {q2 * 1e4:.2f} cm2/s")
print("The low-viscosity water layer carries most of the flow and 'lubricates' the oil - the idea")
print("behind core-annular pipelining of heavy crude oil with a water film.")
