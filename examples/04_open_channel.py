"""Example 4 - Uniform and critical flow in a trapezoidal canal."""

from fluidmech.open_channel import MANNING_N, TrapezoidalChannel, hydraulic_jump_depth

canal = TrapezoidalChannel(bottom_width=4.0, side_slope=1.5)
n = MANNING_N["finished_concrete"]
slope = 0.0008  # bed slope S0 [m/m] (0.8 m fall per km)
Q = 25.0  # design discharge [m3/s]

yn = canal.normal_depth(Q, n, slope)
yc = canal.critical_depth(Q)

print(f"Trapezoidal canal: b = 4 m, z = 1.5, n = {n}, S0 = {slope}, Q = {Q} m3/s")
print(f"  normal depth   y_n = {yn:.3f} m (Fr = {canal.froude(yn, Q):.3f}, {canal.flow_type(yn, Q)})")
print(f"  critical depth y_c = {yc:.3f} m")
print(f"  specific energy at y_n = {canal.specific_energy(yn, Q):.3f} m")
print(f"  minimum specific energy = {canal.specific_energy(yc, Q):.3f} m")
print("  -> mild slope (y_n > y_c)" if yn > yc else "  -> steep slope (y_n < y_c)")

print("\nHydraulic jump below a spillway (rectangular apron):")
y1, fr1 = 0.4, 5.0  # depth [m] and Froude number entering the jump
print(f"  y1 = {y1} m, Fr1 = {fr1} -> sequent depth y2 = {hydraulic_jump_depth(y1, fr1):.2f} m")
