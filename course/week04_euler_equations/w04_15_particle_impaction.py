"""CHME 202 - Week 4 - Example 15: do particles follow the streamlines? Impaction in stagnation flow.

Near a stagnation point the (inviscid) flow is v = -a y towards the wall. A small particle
with relaxation time tau = rho_p d^2 / (18 mu) obeys tau y'' + y' = -a y. It reaches the wall
only if the Stokes number St = a tau exceeds 1/4 - the principle of impactors, filters and
the erosion of pipe bends.
"""

import math

from fluidmech import Fluid

air = Fluid.air(20)
U, D = 10.0, 0.01  # approach speed and obstacle size -> a ~ U / D
a = U / D
print(f"Stagnation flow in front of a {D * 1000:.0f} mm obstacle, air at {U} m/s (a ~ U/D = {a:.0f} 1/s)\n")
print(f"{'d [um]':>7} {'tau [s]':>10} {'St = a tau':>11}  result")
for d_um in [0.5, 1, 2, 5, 10, 20]:
    tau = 1000.0 * (d_um * 1e-6) ** 2 / (18 * air.dynamic_viscosity)  # particle relaxation time [s], rho_p = 1000
    st = a * tau
    # integrate from y = D with the flow velocity; stop at the wall or when the particle 'stalls'
    y, vy, t, dt = D, -a * D, 0.0, tau / 50
    hit = False
    while t < 20 / a:  # integrate tau y'' + y' = -a y (explicit Euler) for many flow time scales
        acc = (-a * y - vy) / tau  # Stokes drag towards the local flow velocity -a y
        vy += acc * dt
        y += vy * dt
        t += dt
        if y <= 0:
            hit = True
            break
    result = "IMPACTS the wall" if hit else "follows the flow round the body"
    print(f"{d_um:>7} {tau:>10.2e} {st:>11.3f}  {result}")
print(f"\nTheory: impaction for St > 0.25 (overdamped otherwise). With a = {a:.0f} 1/s the critical size is")
print(f"d = {math.sqrt(0.25 / a * 18 * air.dynamic_viscosity / 1000.0) * 1e6:.1f} um for 1000 kg/m3 particles.")
print("Fine particles follow the Euler-equation streamlines; heavy ones cross them.")
