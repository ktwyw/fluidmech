"""CHME 202 - Week 9 - Example 14: pressure-loss budget of a ventilation duct and the fan duty point.

Air handling in labs and plants: straight duct, bends, a filter and a heating coil add up
to the system resistance dp = k Q^2 (+ fixed component drops). The fan runs where its
curve meets that system curve. Fan data are ILLUSTRATIVE.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.solvers import bisect

air = Fluid.air(20)
D, L, eps = 0.40, 45.0, pf.ROUGHNESS["galvanized_iron"]  # duct diameter and length [m], roughness
k_fittings = 4 * 0.3 + 0.5 + 1.0  # bends, inlet, outlet


def system_dp(Q):
    if Q <= 0:
        return 0.0
    r = pf.head_loss(Q, D, L, air, eps, k_fittings)
    components = (150.0 + 90.0) * (Q / 1.5) ** 2  # filter + heating coil, rated at 1.5 m3/s
    return r.pressure_drop + components


def fan_dp(Q):
    return 900.0 - 60.0 * Q - 90.0 * Q**2  # Pa, illustrative fan curve


Q = bisect(lambda q: fan_dp(q) - system_dp(q), 0.01, 3.0)  # fan curve meets system curve
r = pf.head_loss(Q, D, L, air, eps, k_fittings)
print(f"Duct {D * 1000:.0f} mm x {L:.0f} m with bends, a filter and a heating coil")
print(
    f"Operating point: Q = {Q:.2f} m3/s ({Q * 3600:.0f} m3/h), fan pressure {fan_dp(Q):.0f} Pa, V = {r.velocity:.1f} m/s\n"
)
print("Pressure-loss budget at the operating point:")
budget = {
    "straight duct": pf.head_loss(Q, D, L, air, eps).pressure_drop,
    "bends, inlet, outlet": r.pressure_drop - pf.head_loss(Q, D, L, air, eps).pressure_drop,
    "filter": 150.0 * (Q / 1.5) ** 2,
    "heating coil": 90.0 * (Q / 1.5) ** 2,
}
for item, dp in budget.items():
    print(f"  {item:<22} {dp:7.1f} Pa  ({dp / sum(budget.values()):.0%})")
print(f"Air power {Q * fan_dp(Q):.0f} W; at 60 % fan efficiency the motor supplies {Q * fan_dp(Q) / 0.6:.0f} W.")
print("A clogged filter (drop doubling) moves the duty point left - fans need a margin for dirty filters.")
