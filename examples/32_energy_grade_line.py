"""Example 32 - Energy and hydraulic grade lines for a pumped pipeline.

Water is pumped from reservoir A (surface 100 m) to reservoir B (surface 130 m)
through a pipeline with a pump near A. The EGL and HGL are tabulated along
the route, and the pipeline is checked for negative pressures over a ridge.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.bernoulli import velocity_head

water = Fluid.water(15)
Q, D = 0.08, 0.25  # flow [m3/s], diameter [m]
eps = pf.ROUGHNESS["cast_iron"]
z_A, z_B = 100.0, 130.0  # reservoir surface levels [m]

# (chainage [m], pipe centreline elevation [m], label)
route = [
    (0, 95.0, "reservoir A outlet"),
    (20, 95.0, "pump suction"),
    (20, 95.0, "pump discharge"),
    (600, 118.0, ""),
    (1400, 142.0, "ridge"),
    (2000, 121.0, ""),
    (2800, 125.0, "reservoir B inlet"),
]

v = pf.mean_velocity(Q, D)
hv = velocity_head(v)
per_metre = pf.head_loss(Q, D, 1000.0, water, eps).major_head_loss / 1000.0  # friction slope [m per m of pipe]
k_entrance, k_exit = 0.5, 1.0  # entrance and exit loss coefficients
total_friction = per_metre * route[-1][0]
h_pump = (z_B - z_A) + total_friction + (k_entrance + k_exit) * hv
print(f"Q = {Q * 1000:.0f} L/s, D = {D * 1000:.0f} mm, V = {v:.2f} m/s, velocity head = {hv:.3f} m")
print(f"Friction slope = {per_metre * 1000:.2f} m/km, pump head required = {h_pump:.1f} m\n")

print(f"{'chainage':>9} {'z pipe':>7} {'EGL':>8} {'HGL':>8} {'p/rho g':>8}  point")
egl = z_A - k_entrance * hv  # EGL just inside the pipe: reservoir level minus the entrance loss
prev_x = 0
min_head = (float("inf"), "")
for x, z, label in route:
    egl -= per_metre * (x - prev_x)
    if label == "pump discharge":
        egl += h_pump
    prev_x = x
    hgl = egl - hv
    p_head = hgl - z
    if p_head < min_head[0]:
        min_head = (p_head, label or f"ch {x}")
    flag = "  <-- NEGATIVE" if p_head < 0 else ""
    print(f"{x:>9} {z:>7.1f} {egl:>8.2f} {hgl:>8.2f} {p_head:>8.2f}  {label}{flag}")
print(f"\nEGL at B after exit loss: {egl - k_exit * hv:.2f} m (reservoir B surface = {z_B} m)")
print(f"Lowest pressure head: {min_head[0]:.2f} m at {min_head[1]}")
if min_head[0] < 0:
    print("Negative pressure: add a booster pump or re-route the pipeline below the HGL.")
else:
    print("The HGL stays above the pipe everywhere - no risk of sub-atmospheric pressure.")
