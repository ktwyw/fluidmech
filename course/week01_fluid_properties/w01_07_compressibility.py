"""CHME 202 - Week 1 - Example 7: compressibility - when can a fluid be treated as incompressible?

Bulk modulus K = -V dp/dV. Liquids have K ~ 1e9 Pa (nearly incompressible);
gases have K = p (isothermal) or k p (isentropic). Speed of sound c = sqrt(K / rho).
Reading: White, Sections 1.8-1.9.
"""

import math

from fluidmech import Fluid
from fluidmech.compressible import pressure_ratio, speed_of_sound

K_water = 2.2e9  # bulk modulus of water [Pa]
water = Fluid.water(20)
print(f"Water: bulk modulus {K_water / 1e9:.1f} GPa, speed of sound {math.sqrt(K_water / water.density):.0f} m/s")
for dp_bar in [10, 100, 1000]:
    print(f"  compressing by {dp_bar:>5} bar changes its density by {dp_bar * 1e5 / K_water:.3%}")
print(f"  a 1 % volume reduction needs {0.01 * K_water / 1e6:.0f} MPa (~{0.01 * K_water / 1e5:.0f} bar)\n")

print(f"Air: speed of sound {speed_of_sound(20):.0f} m/s; isothermal bulk modulus = p = 101 kPa")
print("  (about 20 000 times more compressible than water)\n")

print("Density change of air brought to rest from speed V (isentropic):")
print(f"{'V [m/s]':>8} {'Mach':>6} {'density rise':>13}")
for v in [10, 50, 100, 150, 200]:
    m = v / speed_of_sound(20)
    rise = (1 / pressure_ratio(m)) ** (1 / 1.4) - 1  # isentropic: rho0/rho = (p0/p)^(1/k)
    print(f"{v:>8} {m:>6.2f} {rise:>13.2%}")
print("Rule of thumb: gas flows with Mach < 0.3 (density change < ~5 %) can be treated as incompressible.")
print("Most process-pipe gas flows (10-30 m/s) qualify; compressor and relief-valve flows do not.")
