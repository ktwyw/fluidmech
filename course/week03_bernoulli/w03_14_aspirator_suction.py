"""CHME 202 - Week 3 - Example 14: using Bernoulli suction - aspirators and sprayers.

Where a stream speeds up its pressure falls. A side tube at the throat can lift a
liquid (paint sprayer, carburettor) or pull a vacuum (laboratory water aspirator).
Lift condition: 0.5 rho_gas (V_throat^2 - V_inlet^2) >= rho_liquid g h.
"""

import math

from fluidmech.constants import G
from fluidmech.properties import water_vapor_pressure

rho_air, rho_liq = 1.2, 1000.0  # [kg/m3]
area_ratio = 4.0  # inlet area / throat area
print("Air sprayer: throat suction must lift water h above the reservoir surface")
print(f"{'lift h [mm]':>12} {'required throat V [m/s]':>24}")
for h_mm in [20, 50, 100, 200]:
    # suction 0.5 rho_air (Vt^2 - V1^2) = rho_liq g h; mm -> m
    v_t = math.sqrt(2 * rho_liq * G * h_mm / 1000 / (rho_air * (1 - 1 / area_ratio**2)))
    print(f"{h_mm:>12} {v_t:>24.1f}")
print("(Air must move ~30 m/s to lift water just 5 cm: the density ratio is ~830.)\n")

print("Water-jet aspirator on a lab tap (inlet 200 kPa abs, throat area 1/6 of inlet):")
p1, ar = 200e3, 6.0  # inlet pressure [Pa abs], inlet/throat area ratio
for v1 in [1.0, 2.0, 3.0, 3.4]:
    v2 = v1 * ar
    p2 = p1 - 0.5 * 1000 * (v2**2 - v1**2)  # Bernoulli, water density 1000
    limit = water_vapor_pressure(15)
    shown = max(p2, limit)
    note = " (limited by vapour pressure - cavitating jet)" if p2 < limit else ""
    print(f"  inlet {v1} m/s -> throat {v2:.0f} m/s, suction {shown / 1e3:6.1f} kPa abs{note}")
print("An aspirator cannot pull below the vapour pressure of the water (~1.7 kPa at 15 degC).")
