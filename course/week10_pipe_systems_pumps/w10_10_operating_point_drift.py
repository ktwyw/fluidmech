"""CHME 202 - Week 10 - Example 10: why the operating point moves - tank level, fouling and ageing.

A pump runs where its curve meets the system curve, and the system curve is not
fixed: the static head changes as tanks fill and empty, and friction grows as
pipes foul. Designers check the whole envelope, not one duty point.
Pump data are ILLUSTRATIVE.
"""

from fluidmech import Fluid, PumpCurve, pumps

water = Fluid.water(20)
pump = PumpCurve.from_points([0, 0.01, 0.02, 0.03], [38, 36.5, 32, 24.5], [0, 0.62, 0.78, 0.70])
D, L, K = 0.1023, 300.0, 8.0  # 4-inch Sch 40 ID [m], length [m], fittings K
print(f"{'case':<42} {'Q [L/s]':>8} {'H [m]':>6} {'eta':>5} {'% of BEP':>9}")
bep = pump.best_efficiency_point()
cases = [
    ("design: static 15 m, new pipe", 15.0, 0.045e-3, 1.0),
    ("receiving tank full (+4 m static)", 19.0, 0.045e-3, 1.0),
    ("supply tank low (+3 m static)", 18.0, 0.045e-3, 1.0),
    ("10 years of scaling (eps 0.5 mm)", 15.0, 0.5e-3, 1.0),
    ("scaling + 8 % smaller bore (deposits)", 15.0, 0.5e-3, 0.92),
    ("worst case: tank full + fouled", 19.0, 0.5e-3, 0.92),
]
flows = []
for label, static, eps, bore in cases:
    system = pumps.system_curve(static, D * bore, L, water, eps, K)
    op = pumps.operating_point(pump, system, water.density)
    flows.append(op.flow_rate)
    print(f"{label:<42} {op.flow_rate * 1000:>8.2f} {op.head:>6.1f} {op.efficiency:>5.0%} {op.flow_rate / bep:>9.0%}")
print(
    f"\nPump BEP {bep * 1000:.1f} L/s. Flow falls by {1 - flows[-1] / flows[0]:.0%} from the design case to the worst case."
)
print("If the process needs a minimum flow in the worst case, size for it - and use a variable-speed")
print("drive or control valve to avoid running far to the right of BEP when the system is clean.")
