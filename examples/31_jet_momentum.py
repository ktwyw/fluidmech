"""Example 31 - Momentum equation: forces from water jets.

Control-volume momentum: sum F = m_dot (V_out - V_in)
"""

import math

from fluidmech import Fluid
from fluidmech.bernoulli import torricelli_velocity

water = Fluid.water(20)
rho = water.density

d_jet = 0.05  # jet diameter [m]
A = math.pi * d_jet**2 / 4
V = 20.0  # jet velocity [m/s]
m_dot = rho * A * V
print(f"Jet: d = {d_jet * 1000:.0f} mm, V = {V} m/s, mass flow = {m_dot:.1f} kg/s\n")

# 1. Jet striking a flat plate normally (all momentum turned 90 deg)
print(f"1) Normal flat plate:        F = m_dot V                 = {m_dot * V:8.1f} N")

# 2. Curved vane deflecting the jet by angle theta (stationary)
print("2) Stationary curved vane, deflection angle theta:")
for theta in [45, 90, 135, 180]:
    t = math.radians(theta)
    fx = m_dot * V * (1 - math.cos(t))
    fy = m_dot * V * math.sin(t)
    print(f"     theta = {theta:>3} deg: Fx = {fx:7.1f} N, Fy = {fy:7.1f} N, |F| = {math.hypot(fx, fy):7.1f} N")

# 3. Moving vane / Pelton bucket
print("\n3) Pelton bucket (theta = 165 deg) moving at speed u:")
theta = math.radians(165)
print(f"{'u/V':>6} {'force [N]':>10} {'power [kW]':>11} {'efficiency':>11}")
for ratio in [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]:
    u = ratio * V
    # a wheel of many buckets intercepts the full jet mass flow
    force = m_dot * (V - u) * (1 - math.cos(theta))  # relative velocity V - u is turned through theta
    power = force * u
    eff = power / (0.5 * m_dot * V**2)
    print(f"{ratio:>6.1f} {force:>10.1f} {power / 1e3:>11.2f} {eff:>11.1%}")
print("Maximum power at u = V/2 -> Pelton wheels run with bucket speed ~0.46-0.5 V.")

# 4. Nozzle on a fire hose: force on the nozzle bolts / firefighter
d1, d2, p1 = 0.065, 0.025, 600e3  # hose, nozzle exit, hose gauge pressure
A1, A2 = math.pi * d1**2 / 4, math.pi * d2**2 / 4
V2 = math.sqrt(2 * p1 / (rho * (1 - (A2 / A1) ** 2)))
Q = A2 * V2
V1 = Q / A1
F = p1 * A1 - rho * Q * (V2 - V1)  # momentum balance on the water inside the nozzle
print(f"\n4) Fire-hose nozzle {d1 * 1000:.0f} -> {d2 * 1000:.0f} mm at {p1 / 1e3:.0f} kPa:")
print(f"   jet speed {V2:.1f} m/s, Q = {Q * 1000:.1f} L/s")
print(f"   tension in the hose-nozzle coupling = {F:.0f} N")
print(f"   reaction the firefighter must resist = {rho * Q * V2:.0f} N")

# 5. Rocket-style thrust from a tank draining horizontally
h = 3.0
v_out = torricelli_velocity(h)
print(
    f"\n5) Water jet from a tank with 3 m head through a 50 mm opening:"
    f" V = {v_out:.2f} m/s, thrust = {rho * A * v_out**2:.0f} N"
)
print("   (= 2 x the static pressure force rho g h A, a classic result)")
