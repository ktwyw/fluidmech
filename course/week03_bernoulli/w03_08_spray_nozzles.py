"""CHME 202 - Week 3 - Example 8: spray nozzles - flow rate versus pressure.

A nozzle behaves like an orifice: Q = Cd A sqrt(2 dp / rho), so Q ~ sqrt(dp).
Manufacturers quote a 'K factor' Q = K sqrt(p). Doubling the flow needs 4x the pressure,
which limits the turndown of spray systems (scrubbers, cooling towers, fire sprinklers).
"""

import math

rho = 998.0  # water [kg/m3]
d, cd = 3.0e-3, 0.80  # orifice diameter [m], discharge coefficient
A = math.pi * d**2 / 4
print(f"Nozzle orifice {d * 1000:.0f} mm, Cd = {cd}")
print(f"{'dp [bar]':>9} {'Q [L/min]':>10} {'jet V [m/s]':>12}")
for bar in [0.5, 1, 2, 3, 5, 10]:
    dp = bar * 1e5  # bar -> Pa
    v = math.sqrt(2 * dp / rho)
    print(f"{bar:>9} {cd * A * v * 60000:>10.2f} {v:>12.1f}")
k = cd * A * math.sqrt(2 / rho) * 60000 * math.sqrt(1e5)  # K in L/min per sqrt(bar): m3/s -> L/min, bar -> Pa
print(f"\nK factor: Q [L/min] = {k:.2f} * sqrt(p [bar])")

need = 120.0  # L/min total
for n in [10, 20, 40]:
    per = need / n
    p_req = (per / k) ** 2  # invert Q = K sqrt(p)
    print(f"  {n:>2} nozzles sharing {need:.0f} L/min: each {per:5.1f} L/min at {p_req:6.2f} bar")
print("\nTurndown: to halve the flow of a fixed set of nozzles the pressure must drop to 1/4 -")
print("spray quality (droplet size) deteriorates at low pressure, so wide-range systems switch nozzles on/off.")
