"""CHME 202 - Week 3 - Lab Assignment 1 (Python version): calibrating a Venturi meter.

Measured flow rates (weighing tank) are compared with the ideal Bernoulli
prediction to find the discharge coefficient Cd and its dependence on Reynolds
number. Saves lab1_venturi.png. Replace the data with your own measurements.

# requires: matplotlib
"""

import math

import matplotlib.pyplot as plt

from fluidmech import Fluid
from fluidmech.bernoulli import venturi_flow_rate
from fluidmech.constants import G

water = Fluid.water(18)
d1, d2 = 0.026, 0.016  # inlet and throat diameters [m]
# Manometer reading (water columns, mm) and measured flow (litres collected in time t)
dh_mm = [12, 35, 70, 115, 170, 240, 310, 390]
litres = [5.0, 8.0, 10.0, 10.0, 15.0, 15.0, 20.0, 20.0]  # volume collected in the weighing tank
seconds = [49.9, 46.8, 40.8, 31.9, 39.1, 33.0, 38.6, 34.4]  # stopwatch time for that volume

rows = []
for h, vol, t in zip(dh_mm, litres, seconds):
    q_meas = vol / 1000 / t  # L -> m3, divided by time
    dp = water.density * G * h / 1000  # water column mm -> Pa
    q_ideal = venturi_flow_rate(d1, d2, dp, water.density, discharge_coefficient=1.0)
    v_throat = q_meas / (math.pi * d2**2 / 4)
    re = v_throat * d2 / water.kinematic_viscosity
    rows.append((h, q_meas, q_ideal, q_meas / q_ideal, re))

print(f"Venturi: inlet {d1 * 1000:.0f} mm, throat {d2 * 1000:.0f} mm, beta = {d2 / d1:.3f}\n")
print(f"{'dh [mm]':>8} {'Q meas [L/s]':>13} {'Q ideal [L/s]':>14} {'Cd':>7} {'Re throat':>10}")
for h, qm, qi, cd, re in rows:
    print(f"{h:>8} {qm * 1000:>13.4f} {qi * 1000:>14.4f} {cd:>7.3f} {re:>10.0f}")

# Calibration curve Q = k (dh)^m by log-log regression; ideal m = 0.5
x = [math.log(r[0] / 1000) for r in rows]
y = [math.log(r[1]) for r in rows]
n = len(x)
xm, ym = sum(x) / n, sum(y) / n
# least-squares slope of ln Q vs ln dh
m = sum((a - xm) * (b - ym) for a, b in zip(x, y)) / sum((a - xm) ** 2 for a in x)
k = math.exp(ym - m * xm)
cds = [r[3] for r in rows]
print(f"\nCalibration: Q = {k:.5f} * (dh [m])^{m:.3f}  (theory exponent 0.5)")
print(f"Mean Cd = {sum(cds) / n:.3f}, range {min(cds):.3f}-{max(cds):.3f}; Cd rises towards ~0.98 as Re increases")
print("Discussion points: why is Cd < 1? why does it depend on Re? what is the uncertainty of dh at low flow?")

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].plot([r[0] for r in rows], [r[1] * 1000 for r in rows], "ko", label="measured")
hs = list(range(5, 400, 5))
axes[0].plot(hs, [k * (h / 1000) ** m * 1000 for h in hs], "k-", label="fitted calibration")
axes[0].plot(
    hs,
    [venturi_flow_rate(d1, d2, water.density * G * h / 1000, water.density, 1.0) * 1000 for h in hs],
    "--",
    label="ideal (Cd = 1)",
)
axes[0].set(xlabel="manometer reading dh [mm]", ylabel="Q [L/s]", title="Venturi calibration")
axes[0].legend()
axes[0].grid(alpha=0.4)
axes[1].semilogx([r[4] for r in rows], cds, "ko-")
axes[1].set(xlabel="throat Reynolds number", ylabel="Cd", title="Discharge coefficient")
axes[1].grid(alpha=0.4, which="both")
fig.tight_layout()
fig.savefig("lab1_venturi.png", dpi=130)
print("Saved lab1_venturi.png")
