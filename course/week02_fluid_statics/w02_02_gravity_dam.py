"""CHME 202 - Week 2 - Example 2: forces on a dam and its stability.

A concrete gravity dam with a trapezoidal cross-section holds back water.
We compute the hydrostatic thrust, its line of action, and the safety factors
against overturning and sliding, with and without uplift pressure under the base.
Reading: White, Sections 2.5-2.6.
"""

from fluidmech.constants import G
from fluidmech.hydrostatics import rectangular_gate

h_water = 20.0  # water depth [m]
crest, base, height = 4.0, 16.0, 22.0  # dam geometry (vertical upstream face)
rho_w, rho_c = 1000.0, 2400.0
mu_friction = 0.7  # concrete-rock friction coefficient

# Hydrostatic force per metre of dam length
face = rectangular_gate(width=1.0, height=h_water, top_depth=0.0)
F_h = face.force
arm_h = h_water - face.center_of_pressure_depth  # height above the base
print(f"Hydrostatic thrust {F_h / 1e3:.0f} kN per metre, acting {arm_h:.2f} m above the base (h/3)")

# Dam weight: rectangle (crest width) + triangle, moments about the downstream toe
w_rect = rho_c * G * crest * height
w_tri = rho_c * G * 0.5 * (base - crest) * height
x_rect = base - crest / 2  # distance from toe (downstream edge)
x_tri = (base - crest) * 2 / 3
W = w_rect + w_tri
M_restoring = w_rect * x_rect + w_tri * x_tri
M_overturning = F_h * arm_h
print(f"Dam weight {W / 1e3:.0f} kN per metre")

for label, uplift in [("no uplift", 0.0), ("full uplift", 1.0)]:
    U = uplift * 0.5 * rho_w * G * h_water * base  # triangular uplift pressure under the base
    M_uplift = U * base * 2 / 3
    fs_overturn = M_restoring / (M_overturning + M_uplift)
    fs_slide = mu_friction * (W - U) / F_h
    print(f"\n{label}:")
    print(f"  uplift force               {U / 1e3:8.0f} kN/m")
    print(f"  FS against overturning     {fs_overturn:8.2f}  (require > 1.5)")
    print(f"  FS against sliding         {fs_slide:8.2f}  (require > 1.5)")
print("\nUplift from seepage under the dam is often the controlling load - hence drainage galleries.")
