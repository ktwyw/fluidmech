"""Example 9 - Pressure distribution and wall force in a tank with two liquid layers.

An open tank holds 2 m of oil (SG = 0.85) floating on 3 m of water.
We compute the gauge pressure profile and the force on a 1 m wide side wall.
"""

from fluidmech.constants import G
from fluidmech.hydrostatics import pressure_at_depth

rho_oil, h_oil = 850.0, 2.0  # oil: density [kg/m3], layer depth [m]
rho_water, h_water = 1000.0, 3.0  # water: density [kg/m3], layer depth [m]

p_interface = pressure_at_depth(h_oil, rho_oil)


def pressure(z: float) -> float:
    """Gauge pressure at depth z below the free surface [Pa]."""
    if z <= h_oil:
        return pressure_at_depth(z, rho_oil)
    return pressure_at_depth(z - h_oil, rho_water, surface_pressure=p_interface)


print(f"{'depth [m]':>10} {'p [kPa]':>10}  layer")
steps = 10  # rows in the printed table
for i in range(steps + 1):
    z = (h_oil + h_water) * i / steps
    layer = "oil" if z < h_oil else "water"
    print(f"{z:>10.2f} {pressure(z) / 1e3:>10.2f}  {layer}")

# Force per metre of wall = area under the pressure diagram
f_oil = 0.5 * p_interface * h_oil  # triangle
p_bottom = pressure(h_oil + h_water)
f_water = 0.5 * (p_interface + p_bottom) * h_water  # trapezoid
f_total = f_oil + f_water

# Line of action: moments of each area about the free surface
m_oil = f_oil * (2.0 / 3.0) * h_oil
rect = p_interface * h_water  # rectangular part: the oil pressure transmitted down through the water
tri = 0.5 * (p_bottom - p_interface) * h_water  # triangular part of the water-layer pressure diagram
m_water = rect * (h_oil + h_water / 2.0) + tri * (h_oil + 2.0 * h_water / 3.0)
z_cp = (m_oil + m_water) / f_total

print(f"\nForce on 1 m width of wall: {f_total / 1e3:.1f} kN")
print(f"  from oil layer   : {f_oil / 1e3:.1f} kN")
print(f"  from water layer : {f_water / 1e3:.1f} kN")
print(f"Line of action {z_cp:.3f} m below the free surface")

# Numerical check by integrating the pressure profile (midpoint rule)
n = 20_000
dz = (h_oil + h_water) / n
f_num = sum(pressure((i + 0.5) * dz) * dz for i in range(n))  # midpoint-rule integral of p(z) dz
print(f"Numerical integration check: {f_num / 1e3:.1f} kN")
print(f"(If the tank held only water: {0.5 * rho_water * G * 25 / 1e3:.1f} kN)")
