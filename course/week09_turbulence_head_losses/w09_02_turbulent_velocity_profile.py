"""CHME 202 - Week 9 - Example 2: turbulent velocity profiles and the law of the wall.

Near a wall, u+ = f(y+) universally: viscous sublayer (u+ = y+), buffer layer
and log layer (u+ = ln(y+)/0.41 + 5.0). Also: is a pipe hydraulically smooth?
Saves law_of_the_wall.png.
Reading: White, Section 6.5.

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech import turbulence as tb

water = Fluid.water(20)
D, V = 0.1, 2.0  # pipe diameter [m], mean velocity [m/s]
r = pf.head_loss(V * pf.area(D), D, 1.0, water, pf.ROUGHNESS["commercial_steel"])
tau_w = tb.pipe_wall_shear_stress(r.friction_factor, water.density, V)
u_tau = tb.friction_velocity(tau_w, water.density)
nu = water.kinematic_viscosity
print(f"Water, D = {D * 1000:.0f} mm, V = {V} m/s: Re = {r.reynolds:.3g}, f = {r.friction_factor:.4f}")
print(f"  wall shear {tau_w:.2f} Pa, friction velocity u_tau = {u_tau:.4f} m/s")
print(f"  viscous sublayer thickness 5 nu/u_tau = {tb.viscous_sublayer_thickness(nu, u_tau) * 1e6:.0f} um")

for name, eps in [
    ("drawn tubing", pf.ROUGHNESS["drawn_tubing"]),
    ("commercial steel", pf.ROUGHNESS["commercial_steel"]),
    ("cast iron", pf.ROUGHNESS["cast_iron"]),
    ("concrete", pf.ROUGHNESS["concrete"]),
]:
    eps_plus = eps * u_tau / nu  # roughness in wall units: < 5 smooth, > 70 fully rough
    kind = "hydraulically smooth" if eps_plus < 5 else ("transitionally rough" if eps_plus < 70 else "fully rough")
    print(f"  {name:<17} eps+ = {eps_plus:7.1f} -> {kind}")

# Velocity profile across the pipe from the law of the wall vs the 1/7 power law
R = D / 2
n = tb.power_law_exponent(r.reynolds)
u_max = V / tb.mean_to_max_velocity_ratio(n)
print(f"\n{'y [mm]':>7} {'y+':>8} {'region':>17} {'u (wall law)':>13} {'u (power law)':>14}")
for y in [0.005e-3, 0.02e-3, 0.1e-3, 0.5e-3, 2e-3, 10e-3, 30e-3, 50e-3]:
    yp = y * u_tau / nu
    u_wall = tb.law_of_the_wall(yp) * u_tau
    u_pow = tb.power_law_profile(R - y, R, u_max, n)
    print(f"{y * 1000:>7.3f} {yp:>8.1f} {tb.wall_region(yp):>17} {u_wall:>11.3f} m/s {u_pow:>12.3f} m/s")
print("The power law is fine in the core but wrong near the wall (infinite slope at y = 0).")

fig, ax = plt.subplots(figsize=(7, 4.5))
yps = [10 ** (i / 50) for i in range(-50, 201)]  # y+ from 0.1 to 10 000, evenly spaced on a log axis
ax.semilogx(yps, [tb.law_of_the_wall(y) for y in yps], "k", lw=2, label="Spalding (full inner layer)")
ax.semilogx([y for y in yps if y < 12], [y for y in yps if y < 12], "--", label="u+ = y+")
ax.semilogx([y for y in yps if y > 10], [tb.log_law(y) for y in yps if y > 10], "--", label="log law")
for x in (5, 30):
    ax.axvline(x, color="grey", lw=0.6)
ax.set(xlabel="y+", ylabel="u+", title="Law of the wall", ylim=(0, 30))
ax.legend()
fig.tight_layout()
fig.savefig("law_of_the_wall.png", dpi=130)
print("Saved law_of_the_wall.png")
