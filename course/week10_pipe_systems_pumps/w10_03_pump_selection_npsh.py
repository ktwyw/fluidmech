"""CHME 202 - Week 10 - Example 3: selecting a pump for a duty and checking NPSH.

Compare candidate pumps with the system curve at minimum, normal and maximum
flow; prefer operation near the best efficiency point (BEP), then check that
NPSH available exceeds NPSH required with a margin - especially for hot liquids.
Pump data are ILLUSTRATIVE catalogue-style curves, not real products.
"""

from fluidmech import Fluid, PumpCurve, pumps
from fluidmech import pipe_flow as pf

water = Fluid.water(25)
system = pumps.system_curve(
    # elevation + reactor pressure head [m] (from Example 1)
    static_head=42.6,
    diameter=0.0779,
    length=91.0,
    fluid=water,
    roughness=pf.ROUGHNESS["commercial_steel"],
    # sum of fitting loss coefficients
    k_total=14.0,
)
duty = {"minimum": 18 / 3600, "normal": 30 / 3600, "maximum": 38 / 3600}  # m3/h -> m3/s

candidates = {  # name: (flows m3/s, heads m, efficiencies, NPSHr at the 4 points)
    "Pump A (small, high speed)": (
        [0, 0.004, 0.008, 0.012],
        [70, 67, 58, 43],
        [0, 0.55, 0.70, 0.62],
        [1.5, 2.0, 3.2, 5.5],
    ),
    "Pump B (mid size)": ([0, 0.005, 0.010, 0.015], [62, 60, 54, 44], [0, 0.60, 0.76, 0.70], [1.2, 1.6, 2.5, 4.0]),
    "Pump C (oversized)": ([0, 0.010, 0.020, 0.030], [66, 64, 57, 45], [0, 0.62, 0.80, 0.72], [1.5, 2.2, 3.8, 6.5]),
}
print(f"System head at normal flow: {system(duty['normal']):.1f} m\n")
for name, (q, h, e, _npshr) in candidates.items():
    curve = PumpCurve.from_points(q, h, e)
    op = pumps.operating_point(curve, system, water.density)
    bep = curve.best_efficiency_point()
    print(
        f"{name}: natural operating point {op.flow_rate * 3600:.1f} m3/h at {op.head:.1f} m, BEP {bep * 3600:.1f} m3/h"
    )
    for label, qd in duty.items():
        if curve.head(qd) < system(qd):
            print(
                f"   {label:<8} {qd * 3600:5.1f} m3/h: CANNOT deliver (pump head {curve.head(qd):.1f} < system {system(qd):.1f} m)"
            )
            continue
        print(
            f"   {label:<8} {qd * 3600:5.1f} m3/h: {qd / bep:5.0%} of BEP, efficiency {curve.efficiency(qd):.0%}, "
            f"excess head {curve.head(qd) - system(qd):4.1f} m (throttled away)"
        )
print("\nGood practice: operate between ~70 % and 120 % of BEP. Pump B fits the normal and maximum duty best,")
print("but at minimum flow it runs at <50 % of BEP: use a variable-speed drive or a minimum-flow bypass.")

# NPSH check for pump B at maximum flow, water from an open tank 2 m below the pump
npshr_curve = PumpCurve.from_points([0, 0.005, 0.010, 0.015], [1.2, 1.6, 2.5, 4.0])
q = duty["maximum"]
suction = pf.head_loss(q, 0.1023, 6.0, water, pf.ROUGHNESS["commercial_steel"], 0.95)
print(f"\nNPSH check, Pump B at {q * 3600:.0f} m3/h (NPSHr = {npshr_curve.head(q):.2f} m), suction lift 2 m:")
for t in [25, 50, 70, 85]:
    a = pumps.npsh_available(-2.0, suction.total_head_loss, fluid_temperature=t)
    margin = a - npshr_curve.head(q)
    verdict = "OK" if margin > 1.0 else ("marginal" if margin > 0 else "CAVITATION")
    print(f"   water at {t:>2} degC: NPSHa = {a:5.2f} m, margin {margin:+5.2f} m -> {verdict}")
print("For hot liquids, place the pump below the tank (flooded suction) or cool the liquid.")
