"""CHME 202 - Week 14 - Example 14: characterising a real vessel from a tracer test.

A pulse of tracer is injected at the inlet and its outlet concentration C(t) is recorded.
From the RTD E(t) = C / integral(C dt): mean residence time tm = integral(t E dt), variance
sigma^2 = integral((t - tm)^2 E dt), and the tanks-in-series model gives N = tm^2 / sigma^2.
The 'measured' curve here is generated from a 4-tank vessel with noise.
"""

import random

from fluidmech import mixing as mx

random.seed(9)
tau_true, n_true = 120.0, 4  # vessel used to generate the 'measured' data
dt = 2.0  # sampling interval [s]
times = [i * dt for i in range(0, 400)]  # 800 s record
conc = [
    max(0.0, mx.tanks_in_series_rtd(t, tau_true, n_true) * (1 + random.gauss(0, 0.03))) if t > 0 else 0.0 for t in times
]
area = sum(conc) * dt
E = [c / area for c in conc]  # normalise so that the RTD integrates to 1
tm = sum(t * e for t, e in zip(times, E)) * dt
var = sum((t - tm) ** 2 * e for t, e in zip(times, E)) * dt
N = tm**2 / var
print(f"Tracer test: {len(times)} samples every {dt:.0f} s")
print(f"  mean residence time tm = {tm:.1f} s (vessel V/Q = {tau_true:.0f} s)")
print(f"  variance sigma^2 = {var:.0f} s^2 -> tanks-in-series N = tm^2 / sigma^2 = {N:.2f} (true {n_true})")
k_tau = 2.0  # first-order Damkohler number for the conversion check
print(f"\nPredicted first-order conversion at k tau = {k_tau}: ")
print(f"  using N = {N:.1f}: {mx.tanks_in_series_conversion(k_tau, round(N)):.3f}")
print(f"  ideal CSTR (N = 1): {mx.cstr_conversion(k_tau):.3f},  ideal PFR: {mx.pfr_conversion(k_tau):.3f}")
print("If tm is much shorter than V/Q the vessel has dead zones; an early sharp peak indicates bypassing.")
