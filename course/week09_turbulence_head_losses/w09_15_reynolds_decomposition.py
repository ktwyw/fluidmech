"""CHME 202 - Week 9 - Example 15: what is 'turbulent velocity'? Reynolds decomposition of a signal.

A turbulent velocity signal is split into a time average and fluctuations: u = U + u'.
From a synthetic (random but correlated) signal we compute the mean, the rms fluctuation,
the turbulence intensity and the Reynolds shear stress -rho <u'v'> that makes turbulent
flows so much more dissipative than laminar ones.
"""

import math
import random

random.seed(2)
U_mean, V_mean = 2.0, 0.0  # mean velocity components [m/s]
n, dt, t_corr = 20000, 1e-3, 0.02  # samples, time step, correlation time
a = math.exp(-dt / t_corr)  # memory factor of the correlated random process
u_p = v_p = 0.0
us, vs = [], []
for _ in range(n):  # generate the synthetic 'measured' velocity signal
    # correlated random fluctuations (Ornstein-Uhlenbeck process); v' is anti-correlated with u'
    e1, e2 = random.gauss(0, 1), random.gauss(0, 1)
    u_p = a * u_p + math.sqrt(1 - a * a) * 0.20 * e1
    v_p = a * v_p + math.sqrt(1 - a * a) * 0.12 * (-0.6 * e1 + 0.8 * e2)
    us.append(U_mean + u_p)
    vs.append(V_mean + v_p)

rho = 1000.0  # water [kg/m3]
mean_u = sum(us) / n
mean_v = sum(vs) / n
rms_u = math.sqrt(sum((u - mean_u) ** 2 for u in us) / n)
rms_v = math.sqrt(sum((v - mean_v) ** 2 for v in vs) / n)
uv = sum((u - mean_u) * (v - mean_v) for u, v in zip(us, vs)) / n  # time average of u'v'
print(f"{n} samples over {n * dt:.0f} s")
print(f"  mean velocity U = {mean_u:.3f} m/s, rms u' = {rms_u:.3f} m/s, rms v' = {rms_v:.3f} m/s")
print(f"  turbulence intensity u'/U = {rms_u / mean_u:.1%}")
print(f"  Reynolds shear stress -rho <u'v'> = {-rho * uv:.1f} Pa")
print("\nConvergence of the time average (longer records are needed for the second moments):")
for m in [100, 1000, 5000, 20000]:
    mu = sum(us[:m]) / m
    print(f"  first {m:>5} samples: U = {mu:.3f} m/s")
print("\nA laminar flow of water with a velocity gradient of 100 1/s has a viscous stress of only 0.1 Pa;")
print("the turbulent (Reynolds) stress here is ~100x larger - this is why turbulent friction is high.")
