"""Example 34 - When to put pumps in series and when in parallel.

The answer depends on the shape of the system curve: flat (friction-light,
high static head) or steep (friction-dominated).
"""

from fluidmech import Fluid, PumpCurve, pumps

water = Fluid.water(20)
pump = PumpCurve.from_points([0.0, 0.02, 0.04, 0.06], [30.0, 28.5, 24.0, 16.5], [0.0, 0.65, 0.78, 0.39])

systems = {
    "high static head, short pipe": pumps.system_curve(22.0, 0.20, 150.0, water, 0.045e-3, 5.0),
    "low static head, long pipe": pumps.system_curve(5.0, 0.15, 2500.0, water, 0.045e-3, 5.0),
}
configs = {  # name: (combined curve, flow through each pump as a fraction of total)
    "one pump": (pump, 1.0),
    "two in parallel": (pump.in_parallel(2), 0.5),
    "two in series": (pump.in_series(2), 1.0),
}
CATALOGUE_MAX = 0.06  # the data sheet only covers 0-60 L/s

for label, system in systems.items():
    print(f"System: {label}  (static head {system(0.0):.0f} m)")
    print(f"  {'configuration':<17} {'Q [L/s]':>8} {'per pump':>9} {'H [m]':>7} {'eta':>6} {'P [kW]':>7}")
    base = None
    for name, (curve, share) in configs.items():
        op = pumps.operating_point(curve, system, water.density)
        base = base or op.flow_rate
        per_pump = op.flow_rate * share
        if per_pump > CATALOGUE_MAX:
            tail = "  <- each pump beyond its catalogue curve: not acceptable"
            eta_txt, p_txt = "  n/a", "    n/a"
        else:
            tail = f"  ({op.flow_rate / base - 1:+.0%} flow)"
            eta_txt, p_txt = f"{op.efficiency:>6.1%}", f"{op.shaft_power / 1e3:>7.1f}"  # power in kW
        print(
            f"  {name:<17} {op.flow_rate * 1000:>8.1f} {per_pump * 1000:>9.1f} {op.head:>7.1f} {eta_txt} {p_txt}{tail}"
        )
    print()

print("High static head (flat system curve): parallel pumps share the flow and stay near their best")
print("efficiency point; series pumps would each be forced to run out. Steep, friction-dominated")
print("system: parallel pumps barely add flow, series pumps add the head that is needed.")
