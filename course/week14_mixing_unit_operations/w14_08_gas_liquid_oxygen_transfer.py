"""CHME 202 - Week 14 - Example 8: oxygen transfer in an aerated stirred fermenter.

Mass transfer coefficient (van 't Riet 1979, coalescing air-water):
kLa = 0.026 (P/V)^0.4 u_g^0.5  [1/s], with P/V in W/m3 and superficial gas velocity u_g in m/s.
Oxygen transfer rate OTR = kLa (C* - C). Mixing power buys mass transfer.
"""

import math

C_star = 8.3e-3  # saturation O2 concentration in water at ~25 degC, air [kg/m3]
C_op = 2.0e-3  # operating dissolved O2 (above the cells' critical level)
T = 2.0  # fermenter diameter [m]
V = math.pi * T**3 / 4
print(f"Fermenter T = {T} m (V = {V:.1f} m3), C* = {C_star * 1000:.1f} mg/L, operated at {C_op * 1000:.1f} mg/L\n")
print(f"{'P/V [W/m3]':>11} " + "".join(f"{f'ug={u} cm/s':>14}" for u in (1, 2, 4)) + "   OTR [kg O2/(m3 h)]")
for pv in [250, 500, 1000, 2000, 4000]:
    cells = []
    for ug_cm in (1, 2, 4):
        kla = 0.026 * pv**0.4 * (ug_cm / 100) ** 0.5  # van 't Riet (coalescing); cm/s -> m/s
        otr = kla * (C_star - C_op) * 3600  # oxygen transfer rate [kg/(m3 h)]
        cells.append(f"{kla * 3600:5.0f}/h {otr:5.2f}")
    print(f"{pv:>11} " + "".join(f"{c:>14}" for c in cells))
need = 1.2  # oxygen uptake of a dense culture [kg/(m3 h)]
kla_need = need / 3600 / (C_star - C_op)
pv_need = (kla_need / (0.026 * 0.02**0.5)) ** (1 / 0.4)
print(f"\nA culture consuming {need} kg O2/(m3 h) needs kLa = {kla_need * 3600:.0f} 1/h; at u_g = 2 cm/s that is")
print(f"P/V ~ {pv_need:.0f} W/m3 ({pv_need * V / 1000:.0f} kW for this vessel). Aerated power is lower than ungassed")
print("power (gas cavities behind the blades), so impellers must be sized on the gassed power number.")
