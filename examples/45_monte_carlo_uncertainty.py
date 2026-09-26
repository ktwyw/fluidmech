"""Example 45 - How uncertain is a head-loss calculation? Monte Carlo analysis.

Pipe roughness, water temperature, flow rate and the true inside diameter are
never known exactly. Sampling them randomly shows the spread of the result -
often much wider than engineers expect.
"""

import random
import statistics

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

random.seed(42)
N = 5000  # number of random samples
nominal = {"Q": 0.05, "D": 0.20, "L": 1500.0, "eps": 0.26e-3, "T": 15.0}
results = []
for _ in range(N):  # each pass draws one plausible set of inputs
    q = random.gauss(nominal["Q"], 0.03 * nominal["Q"])  # flow meter +/-3 % (1 sigma)
    d = random.gauss(nominal["D"], 0.005)  # manufacturing / lining tolerance
    # log-normal: roughness is positive and very uncertain
    eps = random.lognormvariate(0.0, 0.5) * nominal["eps"]  # roughness: highly uncertain
    t = random.uniform(5.0, 25.0)  # seasonal temperature
    r = pf.head_loss(q, d, nominal["L"], Fluid.water(t), eps)
    results.append(r.total_head_loss)

nominal_loss = pf.head_loss(
    nominal["Q"], nominal["D"], nominal["L"], Fluid.water(nominal["T"]), nominal["eps"]
).total_head_loss
results.sort()
pct = lambda p: results[int(p / 100 * (N - 1))]  # noqa: E731
print(f"Nominal head loss: {nominal_loss:.2f} m\n")
print(f"Monte Carlo ({N} samples):")
print(f"  mean     {statistics.mean(results):6.2f} m")
print(f"  std dev  {statistics.stdev(results):6.2f} m ({statistics.stdev(results) / statistics.mean(results):.0%})")
for p in (5, 50, 95, 99):
    print(f"  P{p:<2}      {pct(p):6.2f} m")

# Text histogram
lo, hi = results[0], results[-1]
bins = 15  # histogram bins
width = (hi - lo) / bins
counts = [0] * bins
for x in results:
    counts[min(int((x - lo) / width), bins - 1)] += 1
print("\nDistribution of head loss:")
for i, c in enumerate(counts):
    print(f"  {lo + i * width:6.2f}-{lo + (i + 1) * width:6.2f} m | {'#' * int(60 * c / max(counts))}")

# Which input matters most? One-at-a-time sensitivity
print("\nOne-at-a-time sensitivity (each input moved to a plausible adverse value):")
base = dict(nominal)
tests = {
    "flow +3 %": ("Q", nominal["Q"] * 1.03),
    "diameter -5 mm": ("D", nominal["D"] - 0.005),
    "roughness x1.65": ("eps", nominal["eps"] * 1.65),
    "temperature 5 C": ("T", 5.0),
}
for label, (key, value) in tests.items():
    p = dict(base, **{key: value})
    h = pf.head_loss(p["Q"], p["D"], p["L"], Fluid.water(p["T"]), p["eps"]).total_head_loss
    print(f"  {label:<18} {h - nominal_loss:+6.2f} m ({h / nominal_loss - 1:+.1%})")
print("\nDesign to the P95 value (or add a safety margin) rather than the nominal answer.")
