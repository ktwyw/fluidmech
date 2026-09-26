"""Example 39 - Designing a converging-diverging (de Laval) nozzle.

Air from a reservoir at 700 kPa and 300 degC is expanded to Mach 2.5.
We size the throat and exit, then trace Mach number and pressure along
the nozzle and check what happens at off-design back pressures.
"""

import math

from fluidmech import compressible as c

p0, t0 = 700e3, 300.0  # Pa, degC
m_dot = 1.5  # kg/s
m_exit = 2.5

a_throat = m_dot / (c.choked_mass_flow(1.0, p0, t0))  # choked flow per unit area -> required throat area
a_exit = a_throat * c.area_ratio(m_exit)
t_exit = (t0 + 273.15) * c.temperature_ratio(m_exit)
v_exit = m_exit * c.speed_of_sound(t_exit - 273.15)

print(f"Design: m_dot = {m_dot} kg/s, p0 = {p0 / 1e3:.0f} kPa, T0 = {t0} degC, exit Mach {m_exit}")
print(f"  throat area {a_throat * 1e4:.2f} cm2 (D = {math.sqrt(4 * a_throat / math.pi) * 1000:.1f} mm)")
print(
    f"  exit area   {a_exit * 1e4:.2f} cm2 (D = {math.sqrt(4 * a_exit / math.pi) * 1000:.1f} mm), "
    f"A/A* = {c.area_ratio(m_exit):.3f}"
)
print(
    f"  exit: p = {p0 * c.pressure_ratio(m_exit) / 1e3:.1f} kPa, T = {t_exit - 273.15:.0f} degC, V = {v_exit:.0f} m/s"
)
print(f"  thrust (perfectly expanded) = {m_dot * v_exit:.0f} N\n")

# Conical nozzle geometry: inlet area 3 A*, throat at x = 0.1 m, exit at x = 0.3 m
print(f"{'x [m]':>6} {'A/A*':>6} {'Mach':>6} {'p [kPa]':>8} {'T [degC]':>9}")
for i in range(13):  # 13 stations along a 0.3 m nozzle
    x = 0.3 * i / 12
    if x <= 0.1:
        ratio = 3.0 - 2.0 * x / 0.1  # converging part: A/A* falls linearly from 3 to 1 at the throat (x = 0.1 m)
        mach = c.mach_from_area_ratio(ratio, supersonic=False)
    else:
        # diverging part: rises linearly to the exit area ratio
        ratio = 1.0 + (c.area_ratio(m_exit) - 1.0) * (x - 0.1) / 0.2
        mach = c.mach_from_area_ratio(ratio, supersonic=True)
    print(
        f"{x:>6.3f} {ratio:>6.3f} {mach:>6.3f} {p0 * c.pressure_ratio(mach) / 1e3:>8.1f} "
        f"{(t0 + 273.15) * c.temperature_ratio(mach) - 273.15:>9.1f}"
    )

# Operating regimes vs back pressure
p_design = p0 * c.pressure_ratio(m_exit)
p_sub = p0 * c.pressure_ratio(c.mach_from_area_ratio(c.area_ratio(m_exit)))
p_shock_exit = p_design * c.normal_shock(m_exit).pressure_ratio
print("\nBack-pressure regimes:")
print(f"  p_b > {p_sub / 1e3:6.1f} kPa           subsonic throughout (venturi), not choked")
print(f"  {p_shock_exit / 1e3:6.1f} < p_b < {p_sub / 1e3:6.1f} kPa  normal shock inside the diverging section")
print(f"  {p_design / 1e3:6.1f} < p_b < {p_shock_exit / 1e3:6.1f} kPa  overexpanded: oblique shocks outside")
print(f"  p_b = {p_design / 1e3:6.1f} kPa           design condition (perfectly expanded)")
print(f"  p_b < {p_design / 1e3:6.1f} kPa           underexpanded: expansion fans outside")
print(f"At sea level (101 kPa) this nozzle is {'overexpanded' if 101.3e3 > p_design else 'underexpanded'}.")
