"""CHME 202 - Week 1 - Example 15: why fluid temperature matters for a piping system.

The same water line carries the same flow at 5, 20, 50 and 80 degC. Viscosity falls
by a factor of ~4, so the Reynolds number rises and the friction factor and head loss fall.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

Q, D, L = 20 / 3600, 0.0779, 100.0  # 20 m3/h in m3/s; 3-inch Sch 40 ID [m]; length [m]
eps = pf.ROUGHNESS["commercial_steel"]
print(f"Q = {Q * 3600:.0f} m3/h through {L:.0f} m of 3-inch Sch 40 steel pipe\n")
print(f"{'T [degC]':>9} {'mu [mPa s]':>11} {'Re':>9} {'f':>8} {'h_f [m]':>8}")
for T in [5, 20, 50, 80]:
    w = Fluid.water(T)
    r = pf.head_loss(Q, D, L, w, eps)
    print(
        f"{T:>9} {w.dynamic_viscosity * 1000:>11.3f} {r.reynolds:>9.3g} {r.friction_factor:>8.4f} {r.major_head_loss:>8.3f}"
    )
print("\nIn turbulent flow f depends only weakly on Re, so the head loss changes by ~15 %, not 4x.")
oil20 = Fluid(890.0, 0.29, "oil")  # SAE 30-like
oil60 = Fluid(865.0, 0.06, "oil")
for label, fl in [("oil at 20 degC", oil20), ("oil at 60 degC", oil60)]:
    r = pf.head_loss(Q, D, L, fl, eps)
    print(f"{label:<15} Re = {r.reynolds:6.0f} ({r.regime}), h_f = {r.major_head_loss:.3f} m")
print("For viscous oils the flow stays laminar and h_f ~ nu: heating from 20 to 60 degC cuts the loss ~4.7x -")
print("a powerful way to cut pumping power (tank heaters, heat-traced lines).")
