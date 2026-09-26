"""Example 6 - Plot viscosity of water and air against temperature.

# requires: matplotlib
Saves property_plots.png in the current directory.
"""

import matplotlib.pyplot as plt

from fluidmech.properties import (
    air_dynamic_viscosity,
    air_kinematic_viscosity,
    water_dynamic_viscosity,
    water_kinematic_viscosity,
)

t_water = [t * 0.5 for t in range(0, 201)]  # 0-100 degC in 0.5 K steps
t_air = list(range(-40, 201, 2))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

ax = axes[0]
# scaled so both fluids fit one axis
ax.plot(t_water, [water_dynamic_viscosity(t) * 1e3 for t in t_water], label="water (x 1e-3 Pa s)")
# scaled by 1e5 (air is ~50x less viscous)
ax.plot(t_air, [air_dynamic_viscosity(t) * 1e5 for t in t_air], label="air (x 1e-5 Pa s)")
ax.set_xlabel("Temperature [degC]")
ax.set_ylabel("Dynamic viscosity (scaled)")
ax.set_title("Dynamic viscosity")
ax.grid(alpha=0.4)
ax.legend()

ax = axes[1]
ax.semilogy(t_water, [water_kinematic_viscosity(t) for t in t_water], label="water")
ax.semilogy(t_air, [air_kinematic_viscosity(t) for t in t_air], label="air, 1 atm")
ax.set_xlabel("Temperature [degC]")
ax.set_ylabel("Kinematic viscosity [m2/s]")
ax.set_title("Kinematic viscosity")
ax.grid(alpha=0.4, which="both")
ax.legend()

fig.tight_layout()
fig.savefig("property_plots.png", dpi=150)
print("Saved property_plots.png")
