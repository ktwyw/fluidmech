"""Example 40 - Gas leak rate and blowdown time of a pressure vessel.

A 2 m3 compressed-air receiver at 10 bar(g) develops a 5 mm leak (Cd = 0.8).
The vessel empties through a choked orifice until the pressure ratio rises
above the critical value. The gas in the vessel is assumed to expand
isentropically (fast blowdown, no heat transfer).
"""

import math

from fluidmech import compressible as c
from fluidmech.constants import P_ATM, R_AIR

volume = 2.0  # receiver volume [m3]
d_hole, cd = 0.005, 0.8  # leak diameter [m], discharge coefficient
area = cd * math.pi * d_hole**2 / 4
k = 1.4  # ratio of specific heats for air
p, t = 10e5 + P_ATM, 20.0 + 273.15  # 10 bar(g) -> absolute Pa; temperature in K
mass = p * volume / (R_AIR * t)
p_init, m_init = p, mass

print(f"Initial: p = {p / 1e5:.2f} bar(a), T = {t - 273.15:.1f} degC, mass = {mass:.2f} kg")
print(f"Leak area (effective) = {area * 1e6:.1f} mm2; critical pressure ratio = {c.critical_pressure_ratio():.3f}")
print(f"Initial leak rate = {c.nozzle_mass_flow(area, p, P_ATM, t - 273.15) * 1000:.1f} g/s\n")

print(f"{'t [s]':>7} {'p [bar a]':>10} {'T [degC]':>9} {'m_dot [g/s]':>12} {'regime':>9}")
dt, time, next_print = 0.5, 0.0, 0.0  # time step [s], clock, next reporting time
while p > 1.02 * P_ATM:  # blow down until the vessel is ~2 % above atmospheric
    m_dot = c.nozzle_mass_flow(area, p, P_ATM, t - 273.15)
    if time >= next_print:
        regime = "choked" if P_ATM / p <= c.critical_pressure_ratio() else "subsonic"
        print(f"{time:>7.0f} {p / 1e5:>10.3f} {t - 273.15:>9.1f} {m_dot * 1000:>12.2f} {regime:>9}")
        next_print += 60.0
    mass -= m_dot * dt
    # isentropic expansion of the gas remaining in the vessel
    p = p_init * (mass / m_init) ** k  # isentropic expansion of the gas left in the vessel: p ~ rho^k
    t = p * volume / (mass * R_AIR)  # temperature from the ideal-gas law
    time += dt
print(f"\nVessel down to ~atmospheric after {time / 60:.1f} min; the gas cooled to {t - 273.15:.0f} degC.")
print(f"Air lost: {m_init - mass:.1f} kg.")
print("(Real vessels exchange heat with their walls, so the gas cools less and empties a little faster.)\n")
flow_fad = c.nozzle_mass_flow(area, p_init, P_ATM, 20.0) / 1.2  # m3/s of free air
kw = flow_fad * 1000 * 0.11  # compressors need ~0.11 kW per L/s of free air at 7-10 bar
print(f"If the leak were steady, it would waste {flow_fad * 1000:.0f} L/s of free air = {kw:.1f} kW of")
print(f"compressor power, about {kw * 8760 * 0.12:,.0f} $/yr at 0.12 $/kWh.")
