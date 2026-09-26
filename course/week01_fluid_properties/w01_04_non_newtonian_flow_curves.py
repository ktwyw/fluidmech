"""CHME 202 - Week 1 - Example 4: non-Newtonian fluids and rheometer data.

Fits Newtonian, power-law, Bingham and Herschel-Bulkley models to flow curves
of three illustrative materials and plots the results (non_newtonian.png).
Reading: Wilkes, Fluid Mechanics for Chemical Engineers, Ch. on non-Newtonian fluids.

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech import rheology as rh

rates = [1, 2, 5, 10, 20, 50, 100, 200, 500]  # shear rates [1/s]
# Illustrative rheometer data (shear stress, Pa)
materials = {
    "polymer solution": [0.93, 1.40, 2.29, 3.33, 4.93, 8.05, 11.8, 17.2, 28.0],
    "toothpaste-like paste": [62.0, 64.5, 70.1, 76.4, 84.9, 102.0, 119.8, 144.2, 190.0],
    "cornstarch suspension": [0.05, 0.14, 0.55, 1.60, 4.5, 17.5, 50.0, 141.0, 560.0],
}

fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
for ax, (name, stress) in zip(axes, materials.items()):
    print(f"\n{name}")
    fits = {
        "Newtonian": rh.fit_newtonian(rates, stress),
        "power law": rh.fit_power_law(rates, stress),
        "Bingham": rh.fit_bingham(rates, stress),
        "Herschel-Bulkley": rh.fit_herschel_bulkley(rates, stress),
    }
    best = max(fits, key=lambda k: rh.r_squared(fits[k], rates, stress))
    for label, model in fits.items():
        params = ", ".join(f"{k}={v:.3g}" for k, v in model.__dict__.items())
        mark = "  <- best" if label == best else ""
        print(f"  {label:<17} R^2 = {rh.r_squared(model, rates, stress):7.4f}   {params}{mark}")
    pl = fits["power law"]
    print(f"  Power-law index n = {pl.n:.2f}: {pl.behaviour}")
    print(
        f"  Apparent viscosity falls from {stress[0] / rates[0]:.3g} to {stress[-1] / rates[-1]:.3g} Pa s"
        if stress[-1] / rates[-1] < stress[0] / rates[0]
        else f"  Apparent viscosity rises from {stress[0] / rates[0]:.3g} to {stress[-1] / rates[-1]:.3g} Pa s"
    )

    ax.loglog(rates, stress, "ko", label="data")
    gs = [1 * 1.05**i for i in range(128)]  # 1 to ~500 1/s, evenly spaced on a log axis
    for label, model in fits.items():
        ax.loglog(gs, [model.stress(g) for g in gs], label=label)
    ax.set(title=name, xlabel="shear rate [1/s]", ylabel="shear stress [Pa]")
    ax.grid(alpha=0.3, which="both")
axes[0].legend(fontsize=8)
fig.tight_layout()
fig.savefig("non_newtonian.png", dpi=130)
print("\nSaved non_newtonian.png")
print("A negative R^2 means the model is worse than simply using the mean stress.")
print("A yield-stress fluid shows a plateau at low shear rates; a straight line on log-log axes")
print("indicates power-law behaviour, with slope n < 1 (thinning) or n > 1 (thickening).")
