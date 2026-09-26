"""CHME 202 - Week 15 - Integrated design problem: feed system for a packed-bed reactor.

One problem that uses most of the course:
  Week 1  fluid properties at the process temperature
  Week 2  static head and vessel pressure
  Week 9  friction and fitting losses, Reynolds number, velocity guidelines
  Week 12 Ergun pressure drop through the catalyst bed
  Week 10 system curve, pump operating point, NPSH
  Week 13 dimensionless checks

A liquid feed at 60 degC is pumped from an atmospheric day tank through 40 m of pipe
and up through a packed catalyst bed into a reactor held at 2 bar(g).
"""

import math

from fluidmech import Fluid, PumpCurve, pumps
from fluidmech import pipe_flow as pf
from fluidmech import porous as por
from fluidmech.constants import G

# Week 1: properties (water-like feed at 60 degC)
feed = Fluid.water(60)
print(f"Feed: {feed.name}, rho = {feed.density:.1f} kg/m3, mu = {feed.dynamic_viscosity * 1000:.3f} mPa s\n")

Q_design = 12 / 3600  # 12 m3/h -> m3/s
D_pipe, L_pipe, K_pipe = 0.0525, 40.0, 0.5 + 8 * 0.3 + 2 * 0.15 + 3.0 + 1.0  # 2" Sch 40
bed = {"diameter": 0.6, "height": 1.5, "particle": 3e-3, "voidage": 0.38, "sphericity": 0.9}
dz, p_reactor = 7.0, 2e5  # lift [m], reactor pressure [Pa gauge]


def system_head(q: float) -> dict[str, float]:
    parts = {"static": dz, "pressure": p_reactor / (feed.density * G)}
    if q <= 0:
        parts.update(pipe=0.0, bed=0.0)
    else:
        parts["pipe"] = pf.head_loss(q, D_pipe, L_pipe, feed, pf.ROUGHNESS["commercial_steel"], K_pipe).total_head_loss
        u = q / (math.pi * bed["diameter"] ** 2 / 4)  # superficial velocity through the bed
        dp_bed = (
            por.ergun_pressure_gradient(
                u, bed["particle"], bed["voidage"], feed.dynamic_viscosity, feed.density, bed["sphericity"]
            )
            * bed["height"]
        )
        parts["bed"] = dp_bed / (feed.density * G)
    parts["total"] = sum(parts.values())
    return parts


# Weeks 9, 12, 13: the design point
parts = system_head(Q_design)
v = pf.mean_velocity(Q_design, D_pipe)
u_bed = Q_design / (math.pi * bed["diameter"] ** 2 / 4)
re_pipe = v * D_pipe / feed.kinematic_viscosity
re_bed = por.bed_reynolds(
    u_bed, bed["particle"], bed["voidage"], feed.dynamic_viscosity, feed.density, bed["sphericity"]
)
print(f"Design flow {Q_design * 3600:.0f} m3/h")
print(f"  pipe velocity {v:.2f} m/s (guideline 1-3 m/s), Re = {re_pipe:.3g} -> turbulent")
print(f"  bed superficial velocity {u_bed * 1000:.1f} mm/s, bed Re_p = {re_bed:.1f} -> both Ergun terms matter")
print("  head breakdown [m]: " + ", ".join(f"{k} {val:.2f}" for k, val in parts.items()))

# Week 10: pump, operating point, NPSH (illustrative pump curve)
pump = PumpCurve.from_points([0, 0.002, 0.004, 0.006], [42, 40.5, 36, 28], [0, 0.50, 0.66, 0.60])
op = pumps.operating_point(pump, lambda q: system_head(q)["total"], feed.density)
print(
    f"\nPump operating point: {op.flow_rate * 3600:.1f} m3/h at {op.head:.1f} m, efficiency {op.efficiency:.0%}, "
    f"shaft power {op.shaft_power / 1e3:.2f} kW"
)
print(
    f"  a control valve must throttle {pump.head(Q_design) - parts['total']:.1f} m to hold {Q_design * 3600:.0f} m3/h"
)

suction_loss = pf.head_loss(Q_design, 0.0779, 3.0, feed, pf.ROUGHNESS["commercial_steel"], 0.8).total_head_loss
for z_s in (-1.0, 1.5):
    npsha = pumps.npsh_available(z_s, suction_loss, fluid_temperature=60)
    print(
        f"  NPSHa with the tank level {abs(z_s)} m {'below' if z_s < 0 else 'above'} the pump: {npsha:.2f} m "
        f"(NPSHr ~2.5 m -> {'OK' if npsha > 3.5 else 'insufficient margin'})"
    )

print("\nReflection questions:")
for q in [
    "Which head component dominates? What would you change first to reduce pumping energy?",
    "How does the bed pressure drop change if fines reduce the voidage to 0.34?",
    "Why does the 60 degC feed make the NPSH check critical?",
    "The catalyst supplier offers 1.5 mm particles. Estimate the new bed head loss and discuss the trade-off.",
]:
    print(f"  - {q}")
