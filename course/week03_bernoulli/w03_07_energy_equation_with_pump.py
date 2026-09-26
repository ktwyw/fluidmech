"""CHME 202 - Week 3 - Example 7: the steady-flow energy equation - Bernoulli plus pumps and losses.

p1/(rho g) + V1^2/2g + z1 + h_pump = p2/(rho g) + V2^2/2g + z2 + h_loss
This is the bridge from ideal Bernoulli to the pipe-system design of Weeks 9-10.
Reading: White, Section 3.7.
"""

from fluidmech.constants import G

rho = 1000.0  # water [kg/m3]
Q = 0.02  # m3/s
# Point 1: open sump surface; point 2: free jet from a nozzle 18 m higher
z1, z2 = 0.0, 18.0
d_nozzle = 0.05  # [m]
V2 = Q / (3.14159265 * d_nozzle**2 / 4)
for h_loss in [0.0, 3.0, 6.0]:
    h_pump = (z2 - z1) + V2**2 / (2 * G) + h_loss
    power = rho * G * Q * h_pump
    print(
        f"losses {h_loss:3.1f} m: pump head {h_pump:5.2f} m "
        f"(lift {z2 - z1:.0f} m + jet velocity head {V2**2 / (2 * G):.2f} m + losses), "
        f"power to fluid {power / 1e3:.2f} kW"
    )

print("\nWith a pump efficiency of 70 % the shaft power is 1/0.7 = 1.43 times larger.")
print("A turbine is the same equation with h_turbine on the other side: it extracts head from the flow.\n")

# Where does the energy go? Kinetic-energy correction factor alpha
print("Kinetic-energy correction factor alpha (V^2/2g -> alpha V^2/2g):")
for regime, alpha in [("laminar pipe flow", 2.0), ("turbulent pipe flow", 1.05), ("uniform (ideal)", 1.0)]:
    print(f"  {regime:<21} alpha = {alpha}:  velocity head at V = 3 m/s = {alpha * 9 / (2 * G):.3f} m")
print("For turbulent flow alpha ~ 1 is fine; for laminar flow ignoring alpha = 2 halves the kinetic-energy term.")
