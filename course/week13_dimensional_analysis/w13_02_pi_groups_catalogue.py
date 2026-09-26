"""CHME 202 - Week 13 - Example 2: Pi groups for classic problems, found automatically.

For each problem list the dependent variable first, then the preferred
repeating variables. Compare with your hand derivation!
"""

from fluidmech import dimensional as dim

problems = {
    "Drag on a sphere": {"F": "force", "rho": "density", "V": "velocity", "D": "diameter", "mu": "dynamic_viscosity"},
    "Pump performance": {
        "H_g": "specific_energy",
        "N": "angular_velocity",
        "D": "diameter",
        "rho": "density",
        "Q": "flow_rate",
        "mu": "dynamic_viscosity",
    },
    "Stirred-tank power": {
        "P": "power",
        "N": "angular_velocity",
        "D": "diameter",
        "rho": "density",
        "mu": "dynamic_viscosity",
        "g": "gravity",
    },
    "Bubble rise velocity": {
        "U": "velocity",
        "d": "diameter",
        "g": "gravity",
        "rho": "density",
        "mu": "dynamic_viscosity",
        "sigma": "surface_tension",
    },
    "Flow over a weir": {"Q_per_width": "L^2 T^-1", "g": "gravity", "H": "length"},
    "Capillary rise": {"h": "length", "r": "length", "rho": "density", "g": "gravity", "sigma": "surface_tension"},
    "Kolmogorov scale": {"eta": "length", "nu": "kinematic_viscosity", "eps": "dissipation_rate"},
}
for title, variables in problems.items():
    groups = dim.pi_groups(variables)
    print(f"{title}: {len(variables)} variables, rank {dim.dimension_matrix_rank(variables)}")
    for g in groups:
        assert dim.is_dimensionless(g, variables)
        print(f"   {dim.format_group(g)}")
print("\nRecognise them: drag coefficient and Re; head coefficient gH/(N^2 D^2), flow coefficient Q/(N D^3);")
print("power number P/(rho N^3 D^5) and Froude N^2 D/g; weir: Q ~ sqrt(g) H^(3/2); Kolmogorov: eta ~ (nu^3/eps)^(1/4).")
print("When only ONE Pi group exists (weir, Kolmogorov), it must equal a constant: the scaling law follows")
print("directly, and only the constant needs an experiment.")
