"""CHME 202 - Week 2 - Example 8: absolute, gauge and vacuum pressure; barometers.

p_abs = p_atm + p_gauge; vacuum = p_atm - p_abs. A barometer column balances the
atmosphere: h = p_atm / (rho g).
Reading: White, Section 2.3.
"""

from fluidmech.constants import P_ATM, G
from fluidmech.properties import water_vapor_pressure
from fluidmech.units import convert

print("Barometer column heights for 1 atm:")
for name, rho, pv in [
    ("mercury", 13546.0, 0.17),
    ("water", 998.0, water_vapor_pressure(20)),
    ("ethanol", 789.0, 5.9e3),
]:
    h = (P_ATM - pv) / (rho * G)
    print(f"  {name:<8} {h:6.3f} m  (vapour pressure {pv / 1e3:.2f} kPa fills the space above)")

print("\nReading process gauges (local atmosphere 95 kPa):")
p_atm = 95e3  # local atmospheric pressure [Pa] (an inland plant site)
readings = [
    ("reactor, Bourdon gauge", 3.5, "bar(g)"),
    ("vacuum still, compound gauge", -0.8, "bar(g)"),
    ("steam header", 150.0, "psi"),
    ("absolute transmitter", 20.0, "kPa"),
]
for name, value, unit in readings:
    if unit == "bar(g)":
        p_abs = p_atm + value * 1e5  # bar(g) -> Pa(abs)
    elif unit == "psi":
        p_abs = p_atm + convert(value, "psi", "Pa")  # assume psig
    else:
        p_abs = value * 1e3  # kPa(abs) -> Pa
    kind = "vacuum" if p_abs < p_atm else "overpressure"
    print(
        f"  {name:<30} {value:>7} {unit:<6} -> {p_abs / 1e3:8.1f} kPa(abs), {kind} {abs(p_abs - p_atm) / 1e3:.1f} kPa"
    )
print("\nAlways state 'g' or 'a': a vessel rated for 3 bar(g) can hold 4 bar(a). Vacuum equipment must")
print("withstand full external atmospheric pressure (buckling), which thin tanks often cannot.")
