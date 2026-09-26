"""Example 14 - Accuracy of explicit friction-factor formulas vs. Colebrook.

Swamee-Jain and Haaland avoid iteration; how much accuracy do they give up?
"""

from fluidmech.pipe_flow import colebrook, haaland, swamee_jain

reynolds_values = [4e3, 1e4, 1e5, 1e6, 1e7, 1e8]  # turbulent range of the Moody chart
roughness_values = [0.0, 1e-5, 1e-4, 1e-3, 1e-2, 5e-2]  # relative roughness eps/D

for name, func in [("Swamee-Jain", swamee_jain), ("Haaland", haaland)]:
    print(f"\n{name}: percentage error relative to Colebrook")
    print("eps/D \\ Re " + "".join(f"{re:>9.0e}" for re in reynolds_values))
    worst = 0.0  # largest |error| found
    for rr in roughness_values:
        row = []
        for re in reynolds_values:
            err = (func(re, rr) - colebrook(re, rr)) / colebrook(re, rr) * 100
            err = 0.0 if abs(err) < 0.005 else err  # avoid printing -0.00
            worst = max(worst, abs(err))
            row.append(f"{err:>+9.2f}")
        print(f"{rr:<11g}" + "".join(row))
    print(f"Worst case: {worst:.2f} %")

print("\nBoth are within ~3 % everywhere -- smaller than the uncertainty in the")
print("roughness value itself, which is easily +/-50 % for real pipes.")

# Sensitivity of f to roughness uncertainty
re = 2e5
print(f"\nSensitivity at Re = {re:.0e}: f for eps/D +/- 50 %")
for rr in [1e-4, 1e-3]:
    lo, mid, hi = (colebrook(re, rr * k) for k in (0.5, 1.0, 1.5))
    print(f"  eps/D = {rr:g}: f = {mid:.4f}  (range {lo:.4f} - {hi:.4f}, {(hi - lo) / mid:.0%} spread)")
