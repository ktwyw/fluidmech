"""CHME 202 - Week 12 - Example 15: washing the filter cake.

After filtration the cake is washed to displace the mother liquor. In a leaf filter the wash
liquid follows the same path as the filtrate, so the wash rate equals the FINAL filtration rate
at the same pressure: dV/dt = A^2 dp / (mu (alpha c V + R_m A)). Wash time = wash volume / rate.
"""

mu, dp, A, c = 1e-3, 3e5, 20.0, 40.0  # water, 3 bar [Pa], area [m2], kg solids per m3 filtrate
alpha, r_m = 4e11, 1e11  # specific cake resistance [m/kg], medium resistance [1/m]
V_filtrate = 6.0  # m3 collected at the end of filtration
cake_mass = c * V_filtrate
rho_s, eps_cake = 2600.0, 0.45  # solid density [kg/m3], cake porosity
cake_volume = cake_mass / (rho_s * (1 - eps_cake))
void_volume = eps_cake * cake_volume
rate = A**2 * dp / (mu * (alpha * c * V_filtrate + r_m * A))  # dV/dt from the Ruth equation at the end of filtration
t_filter = mu * alpha * c / (2 * A**2 * dp) * V_filtrate**2 + mu * r_m / (A * dp) * V_filtrate
print(f"Leaf filter {A} m2 at {dp / 1e5:.0f} bar: {V_filtrate} m3 filtered in {t_filter / 60:.0f} min")
print(f"Cake {cake_mass:.0f} kg ({cake_volume:.2f} m3, {void_volume:.2f} m3 of liquor in the pores)")
print(f"Final filtration rate = wash rate = {rate * 3600:.2f} m3/h\n")
for n_voids in [1, 2, 3]:
    v_wash = n_voids * void_volume
    print(f"  wash with {n_voids} void volume(s) = {v_wash:.2f} m3: {v_wash / rate / 60:5.1f} min")
print("\nThe wash runs at the LOWEST rate of the cycle (thickest cake). Here the cake is thin, so washing")
print(f"takes minutes against {t_filter / 60:.0f} min of filtering; thick, fine, compressible cakes needing many wash")
print("volumes can make washing the slowest step. In a plate-and-")
print("frame press with thorough washing the wash liquid crosses the WHOLE cake and half the cloth area,")
print("so its rate is about 1/4 of the final filtration rate.")
