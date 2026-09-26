"""CHME 202 - Week 6 - Example 6: pipe flow of non-Newtonian fluids.

Power-law fluids: shear-thinning (n < 1) gives a blunter profile; a Bingham
plastic moves as a solid plug in the core. We compare profiles and the
pressure gradient needed to pump a polymer solution and a slurry.
Saves non_newtonian_profiles.png.

# requires: matplotlib
"""

import math

import matplotlib.pyplot as plt

from fluidmech import Fluid
from fluidmech.laminar import (
    bingham_pipe_flow_rate,
    bingham_pipe_velocity,
    bingham_plug_radius,
    metzner_reed_reynolds,
    power_law_pipe_flow_rate,
    power_law_pipe_velocity,
)
from fluidmech.pipe_flow import head_loss
from fluidmech.solvers import positive_root

R = 0.025  # pipe radius [m]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
rs = [R * i / 100 for i in range(101)]  # radii for the profiles
print("Normalised velocity profiles u / u_mean at the same flow rate:")
for n in [0.3, 0.6, 1.0, 1.5]:
    G = 1000.0
    Q = power_law_pipe_flow_rate(G, R, 1.0, n)
    u_mean = Q / (math.pi * R**2)
    u = [power_law_pipe_velocity(r, R, G, 1.0, n) / u_mean for r in rs]
    print(f"  n = {n:<4} u_max / u_mean = {u[0]:.3f}  (theory (3n+1)/(n+1) = {(3 * n + 1) / (n + 1):.3f})")
    axes[0].plot([r / R for r in rs], u, label=f"power law n = {n}")
for phi in [0.3, 0.6]:
    tau_y, mu_p = 1.0, 1.0  # yield stress [Pa] and plastic viscosity [Pa s] (dimensionless demo)
    G = 2 * tau_y / (phi * R)  # choose G so that tau_y / tau_w = phi
    Q = bingham_pipe_flow_rate(G, R, tau_y, mu_p)
    u_mean = Q / (math.pi * R**2)
    axes[0].plot(
        [r / R for r in rs],
        [bingham_pipe_velocity(r, R, G, tau_y, mu_p) / u_mean for r in rs],
        "--",
        label=f"Bingham, tau_y/tau_w = {phi}",
    )
axes[0].set(xlabel="r / R", ylabel="u / u_mean", title="Profiles at equal flow rate")
axes[0].legend(fontsize=8)

# Pumping a polymer solution: pressure gradient for Q = 2 L/s in a 50 mm pipe
Q_target, rho = 2e-3, 1000.0
K, n = 0.5, 0.45  # power-law consistency [Pa s^n] and index
# gradient that delivers Q_target
G = positive_root(lambda g: power_law_pipe_flow_rate(g, R, K, n) - Q_target, guess=1000.0)
V = Q_target / (math.pi * R**2)
re = metzner_reed_reynolds(rho, V, 2 * R, K, n)
print(f"\nPolymer solution K = {K} Pa s^n, n = {n}: Q = 2 L/s needs dp/L = {G:.0f} Pa/m (Re_MR = {re:.0f}, laminar)")
water_r = head_loss(Q_target, 2 * R, 1.0, Fluid.water(20), roughness=0.0)
print(
    f"Water at the same flow is turbulent (Re = {water_r.reynolds:.0f}) and needs only {water_r.pressure_drop:.0f} Pa/m:"
)
print("the polymer solution needs about twice the pressure even though its flow is laminar.")

# Slurry (Bingham plastic): minimum pressure gradient to start flow
tau_y, mu_p = 15.0, 0.05
g_start = 2 * tau_y / R  # wall stress must exceed the yield stress before flow starts
print(f"\nSlurry tau_y = {tau_y} Pa: flow starts only when dp/L > 2 tau_y / R = {g_start:.0f} Pa/m")
gs = [g_start * (1 + 0.05 * i) for i in range(1, 60)]
axes[1].plot([bingham_pipe_flow_rate(g, R, tau_y, mu_p) * 1000 for g in gs], gs, label="Bingham slurry")
axes[1].plot([power_law_pipe_flow_rate(g, R, K, n) * 1000 for g in gs], gs, label="polymer (power law)")
axes[1].set(xlabel="Q [L/s]", ylabel="dp/L [Pa/m]", title="Pressure gradient vs flow")
axes[1].legend()
fig.tight_layout()
fig.savefig("non_newtonian_profiles.png", dpi=130)
print(f"Plug radius at 2x the start-up gradient: {bingham_plug_radius(2 * g_start, tau_y) * 1000:.1f} mm of R = 25 mm")
print("Saved non_newtonian_profiles.png")
