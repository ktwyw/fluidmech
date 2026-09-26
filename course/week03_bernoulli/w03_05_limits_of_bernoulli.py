"""CHME 202 - Week 3 - Example 5: when does Bernoulli's equation fail?

Bernoulli assumes steady, incompressible, frictionless flow along a streamline.
We quantify the error when each assumption is violated.
Reading: White, Section 3.5 ("restrictions on the Bernoulli equation").
"""

import math

from fluidmech import Fluid
from fluidmech import compressible as c
from fluidmech import pipe_flow as pf
from fluidmech.bernoulli import torricelli_velocity

# 1. Compressibility: Pitot tube in air
print("1) Compressibility - Pitot tube in air at sea level")
print(f"{'true V [m/s]':>13} {'Mach':>6} {'incompressible estimate':>24} {'error':>7}")
a = c.speed_of_sound(15.0)
rho0, p_static = 1.225, 101325.0  # sea-level air
for v in [30, 100, 170, 250, 300]:
    m = v / a
    p0 = p_static / c.pressure_ratio(m)
    v_est = math.sqrt(2 * (p0 - p_static) / rho0)  # what the incompressible Pitot formula would report
    print(f"{v:>13} {m:>6.2f} {v_est:>24.1f} {v_est / v - 1:>+7.1%}")
print("   Incompressible flow is a good assumption up to Mach ~0.3 (error about 1 %).\n")

# 2. Friction: draining a tank through a pipe
water = Fluid.water(20)
H, D = 5.0, 0.025  # tank head [m], pipe diameter [m]
print(f"2) Friction - tank with {H} m head draining through a {D * 1000:.0f} mm pipe")
print(f"{'pipe length [m]':>16} {'ideal V':>8} {'real V':>8} {'real/ideal':>11}")
for length in [0.1, 1, 5, 20, 100]:
    q = pf.flow_rate_for_head_loss(H, D, length, water, pf.ROUGHNESS["pvc"], k_total=0.5 + 1.0)
    v = pf.mean_velocity(q, D)
    print(f"{length:>16} {torricelli_velocity(H):>8.2f} {v:>8.2f} {v / torricelli_velocity(H):>11.0%}")
print("   (entrance loss K = 0.5 plus the exit velocity head included in both)")
print("   Bernoulli is fine for short, smooth passages (nozzles, orifices) but not for long pipes.\n")

# 3. Unsteadiness: tank area vs outlet area
print("3) Unsteadiness - quasi-steady tank draining is accurate when A_tank >> A_outlet")
for ratio in [2, 5, 10, 100]:
    correction = 1 / math.sqrt(1 - 1 / ratio**2)  # Bernoulli + continuity with the tank's own velocity head
    print(f"   A_tank/A_hole = {ratio:>4}: exit speed is {correction - 1:+.2%} above Torricelli's value")
