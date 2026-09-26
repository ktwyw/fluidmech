"""CHME 202 - Week 10 - Example 4: when the 'water assumption' fails - pumping viscous liquids.

The same line and flow rate with glycerol-water mixtures of rising viscosity:
the flow turns laminar and friction head rises dramatically. Centrifugal pump
performance also degrades with viscosity (the Hydraulic Institute correction
method is used in practice); positive-displacement pumps are often chosen instead.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

# Approximate properties of glycerol-water mixtures at 20 degC
mixtures = [
    ("water", 998, 0.001),
    ("40 % glycerol", 1100, 0.0037),
    ("60 % glycerol", 1154, 0.0108),
    ("80 % glycerol", 1209, 0.060),
    ("90 % glycerol", 1235, 0.219),
    ("pure glycerol", 1261, 1.41),
]
Q, D, L = 5 / 3600, 0.0525, 50.0  # 5 m3/h through 50 m of 2" Sch 40
print(f"Q = {Q * 3600:.0f} m3/h through {L:.0f} m of {D * 1000:.1f} mm pipe (+ fittings, K = 5)\n")
print(f"{'liquid':<16} {'mu [mPa s]':>11} {'Re':>9} {'regime':>12} {'f':>8} {'head loss [m]':>14} {'power [kW]':>11}")
losses = []
for name, rho, mu in mixtures:
    fl = Fluid(rho, mu, name)
    r = pf.head_loss(Q, D, L, fl, pf.ROUGHNESS["commercial_steel"], 5.0)
    losses.append(r.total_head_loss)
    print(
        f"{name:<16} {mu * 1000:>11.1f} {r.reynolds:>9.0f} {r.regime:>12} {r.friction_factor:>8.4f} "
        f"{r.total_head_loss:>14.2f} {r.pumping_power(0.6) / 1e3:>11.3f}"
    )
print(f"\nFrom water to pure glycerol the friction head rises {losses[-1] / losses[0]:.0f}-fold at the same flow.")
print("Remedies: larger pipes, heating the liquid (Week 1: viscosity falls steeply with T),")
print("or a positive-displacement pump whose flow is nearly independent of head.")
print("Note: in laminar flow the fitting K values are themselves higher than the turbulent values used here.")
