"""CHME 202 - Week 13 - Example 3: pump similarity and the affinity laws.

Dimensional analysis gives C_H = gH/(N^2 D^2) = f(C_Q = Q/(N D^3)) for
geometrically similar pumps (Re effects neglected). A model test therefore
predicts the full-size pump, and speed changes follow the affinity laws.
Reading: White, Sections 5.5 and 11.3.
"""

from fluidmech import PumpCurve
from fluidmech.constants import G

# Model test: D = 0.2 m at 1450 rpm
D_m, N_m = 0.20, 1450 / 60  # model diameter [m], speed [rev/s]
Q_m = [0.0, 0.01, 0.02, 0.03, 0.04]  # model test flows [m3/s]
H_m = [22.0, 21.4, 19.5, 16.2, 11.5]  # model heads [m]
eta_m = [0.0, 0.52, 0.74, 0.78, 0.66]  # model efficiencies
print(f"Model pump D = {D_m} m at {N_m * 60:.0f} rpm - dimensionless performance:")
print(f"{'C_Q':>8} {'C_H':>7} {'eta':>6}")
for q, h, e in zip(Q_m, H_m, eta_m):
    print(f"{q / (N_m * D_m**3):>8.4f} {G * h / (N_m**2 * D_m**2):>7.3f} {e:>6.2f}")

# Prototype: D = 0.5 m at 980 rpm
D_p, N_p = 0.50, 980 / 60  # prototype diameter [m], speed [rev/s]
print(f"\nPrototype D = {D_p} m at {N_p * 60:.0f} rpm (same C_Q, C_H):")
print(f"{'Q [m3/s]':>9} {'H [m]':>7}")
for q, h in zip(Q_m, H_m):
    cq, ch = q / (N_m * D_m**3), G * h / (N_m**2 * D_m**2)
    print(f"{cq * N_p * D_p**3:>9.3f} {ch * N_p**2 * D_p**2 / G:>7.1f}")
print(
    "Scale factors: Q x (N_p/N_m)(D_p/D_m)^3 =",
    f"{(N_p / N_m) * (D_p / D_m) ** 3:.2f},  H x (N_p/N_m)^2 (D_p/D_m)^2 = {(N_p / N_m) ** 2 * (D_p / D_m) ** 2:.2f}",
)

model = PumpCurve.from_points(Q_m, H_m, eta_m)
slow = model.scaled(speed_ratio=0.8)
print(
    f"\nAffinity check with PumpCurve.scaled(0.8): H(0.8 x 0.03) = {slow.head(0.024):.2f} m "
    f"= 0.64 x {model.head(0.03):.2f} = {0.64 * model.head(0.03):.2f} m"
)
print("Efficiency of the larger prototype is usually slightly HIGHER (Moody's step-up formula),")
print("because its Reynolds number is larger and relative roughness smaller - a scale effect.")
