"""CHME 202 - Week 11 - Example 15: lifting solids with air - vertical pneumatic conveying.

In dilute-phase conveying each particle 'slips' behind the gas by about its terminal
velocity: u_solids ~ u_gas - U_t. The gas must also supply the pressure to hold up the
solids, dp_solids ~ (solids mass in the pipe) g / A. Plastic pellets are the example.
"""

import math

from fluidmech import Fluid
from fluidmech.constants import G
from fluidmech.drag import terminal_velocity

air = Fluid.air(20)
d, rho_p = 3e-3, 950.0  # polyethylene pellets
D, H = 0.1, 20.0  # pipe diameter and lift height
m_s = 1.0  # solids flow [kg/s]
ut = terminal_velocity(d, rho_p, air)
A = math.pi * D**2 / 4
print(f"Pellets d = {d * 1000:.0f} mm: terminal velocity {ut:.1f} m/s -> gas must exceed this to lift them\n")
print(f"{'gas velocity [m/s]':>19} {'solids velocity':>16} {'solids in pipe [kg]':>20} {'dp to lift solids [kPa]':>24}")
for ug in [12, 16, 20, 25, 30]:
    us = ug - ut  # particles lag the gas by about their terminal velocity
    hold = m_s * H / us  # kg of solids in the vertical pipe
    dp = hold * G / A  # pressure needed to support that weight
    print(f"{ug:>19} {us:>16.1f} {hold:>20.2f} {dp / 1e3:>24.2f}")
print("\nToo slow and the pipe chokes (solids fall back); too fast wastes energy and erodes bends. Typical")
print("dilute-phase gas velocities are 15-25 m/s for pellets. Gas friction and acceleration losses add")
print("to the solids hold-up term calculated here.")
