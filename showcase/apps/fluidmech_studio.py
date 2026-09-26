"""FluidMech Studio - an interactive fluid-mechanics calculator in your web browser.

Run it with:
    pip install -e ".[apps]"
    streamlit run showcase/apps/fluidmech_studio.py

Each page is a small calculator built on the tested fluidmech library, with a live chart.
Change a slider and everything is recomputed instantly. It can also be deployed for free on
Streamlit Community Cloud so students can use it from a phone.

# requires: streamlit, matplotlib, numpy
"""

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import streamlit as st  # noqa: E402

from fluidmech import Fluid, PumpCurve, pumps, transients, viz  # noqa: E402
from fluidmech import pipe_flow as pf  # noqa: E402
from fluidmech.drag import sphere_drag_coefficient, terminal_velocity  # noqa: E402
from fluidmech.open_channel import TrapezoidalChannel  # noqa: E402
from fluidmech.potential_flow import cylinder, kutta_joukowski_lift  # noqa: E402

st.set_page_config(page_title="FluidMech Studio", page_icon="🌊", layout="wide")

PAGES = ["Pipe flow", "Pump & system", "Open channel", "Potential flow", "Particle settling", "Water hammer"]
page = st.sidebar.radio("Calculator", PAGES, key="page")
st.sidebar.markdown("---")
st.sidebar.caption("Built with the **fluidmech** Python library. All inputs in SI units.")


def fluid_picker(prefix: str) -> Fluid:
    """Sidebar-independent fluid selector used by several pages."""
    kind = st.selectbox("Fluid", ["Water", "Air", "Custom"], key=f"{prefix}_fluid")
    if kind == "Water":
        return Fluid.water(st.slider("Temperature [degC]", 0, 100, 20, key=f"{prefix}_T"))
    if kind == "Air":
        return Fluid.air(st.slider("Temperature [degC]", -40, 200, 20, key=f"{prefix}_Ta"))
    rho = st.number_input("Density [kg/m3]", 1.0, 20000.0, 900.0, key=f"{prefix}_rho")
    mu = st.number_input("Viscosity [Pa s]", 1e-6, 100.0, 0.05, format="%.5f", key=f"{prefix}_mu")
    return Fluid(rho, mu, "custom")


def show(fig) -> None:
    st.pyplot(fig, clear_figure=True)
    plt.close(fig)


# ---------------------------------------------------------------------------- pipe flow
if page == "Pipe flow":
    st.title("Pipe flow and the Moody diagram")
    left, right = st.columns([1, 2])
    with left:
        fluid = fluid_picker("pipe")
        q = st.number_input("Flow rate [L/s]", 0.01, 5000.0, 20.0, key="pipe_q") / 1000
        d = st.number_input("Inside diameter [mm]", 1.0, 3000.0, 100.0, key="pipe_d") / 1000
        length = st.number_input("Length [m]", 0.1, 1e5, 200.0, key="pipe_L")
        material = st.selectbox("Material", list(pf.ROUGHNESS), index=2, key="pipe_mat")
        k_total = st.number_input("Sum of fitting K", 0.0, 500.0, 3.0, key="pipe_k")
    r = pf.head_loss(q, d, length, fluid, pf.ROUGHNESS[material], k_total)
    with right:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Velocity", f"{r.velocity:.2f} m/s")
        c2.metric("Reynolds", f"{r.reynolds:,.0f}", r.regime)
        c3.metric("Friction factor", f"{r.friction_factor:.4f}")
        c4.metric("Head loss", f"{r.total_head_loss:.2f} m", f"{r.pressure_drop / 1e3:.1f} kPa", delta_color="off")
        with viz.style("slides"):
            fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
            viz.moody_chart(ax)
            ax.plot(r.reynolds, r.friction_factor, "*", ms=18, color=viz.COLORS["vermillion"], zorder=10)
            show(fig)
        st.caption(
            f"Pumping power at 70 % efficiency: {r.pumping_power(0.7) / 1e3:.2f} kW. "
            "Tip: pipes are usually sized for 1-3 m/s."
        )

# ---------------------------------------------------------------------------- pumps
elif page == "Pump & system":
    st.title("Pump operating point")
    left, right = st.columns([1, 2])
    with left:
        h0 = st.slider("Pump shut-off head [m]", 10.0, 100.0, 42.0, key="pump_h0")
        q_run = st.slider("Pump run-out flow [L/s]", 20.0, 400.0, 160.0, key="pump_qr") / 1000
        speed = st.slider("Speed [% of rated]", 40, 110, 100, key="pump_speed") / 100
        static = st.slider("Static head [m]", 0.0, 60.0, 12.0, key="pump_static")
        d = st.slider("Pipe diameter [mm]", 50, 600, 250, key="pump_d") / 1000
        length = st.slider("Pipe length [m]", 10, 5000, 800, key="pump_L")
    water = Fluid.water(20)
    pump = PumpCurve(h0, 0.0, -h0 / q_run**2)  # simple parabolic pump curve through (0, h0) and (q_run, 0)
    system = pumps.system_curve(static, d, length, water, 0.26e-3, 8.0)
    with right:
        try:
            op = pumps.operating_point(pump.scaled(speed_ratio=speed), system, water.density)
            c1, c2, c3 = st.columns(3)
            c1.metric("Flow", f"{op.flow_rate * 1000:.1f} L/s")
            c2.metric("Head", f"{op.head:.1f} m")
            c3.metric("Hydraulic power", f"{water.density * 9.80665 * op.flow_rate * op.head / 1e3:.1f} kW")
        except ValueError:
            st.error("At this speed the pump cannot overcome the static head: no flow.")
        with viz.style("slides"):
            fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
            viz.pump_system_chart(ax, pump, system, q_run * 1.1, speeds=sorted({1.0, speed}))
            show(fig)

# ---------------------------------------------------------------------------- open channel
elif page == "Open channel":
    st.title("Uniform and critical flow in a channel")
    left, right = st.columns([1, 2])
    with left:
        b = st.slider("Bottom width b [m]", 0.0, 20.0, 4.0, key="ch_b")
        z = st.slider("Side slope z (H:V)", 0.0, 4.0, 1.5, key="ch_z")
        n = st.slider("Manning n", 0.009, 0.06, 0.014, step=0.001, format="%.3f", key="ch_n")
        slope = st.slider("Bed slope S0 [m/km]", 0.05, 20.0, 0.8, key="ch_s") / 1000
        q = st.slider("Discharge Q [m3/s]", 0.5, 300.0, 25.0, key="ch_q")
    if b == 0 and z == 0:
        st.error("The channel needs a bottom width or sloping sides.")
    else:
        ch = TrapezoidalChannel(b, z)
        yn, yc = ch.normal_depth(q, n, slope), ch.critical_depth(q)
        with right:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Normal depth", f"{yn:.2f} m")
            c2.metric("Critical depth", f"{yc:.2f} m")
            c3.metric("Froude number", f"{ch.froude(yn, q):.2f}", ch.flow_type(yn, q))
            c4.metric("Velocity", f"{q / ch.area(yn):.2f} m/s")
            with viz.style("slides"):
                fig, ax = plt.subplots(figsize=(8, 4), constrained_layout=True)
                top = max(yn, yc) * 1.4
                ax.fill([-b / 2 - z * top, -b / 2, b / 2, b / 2 + z * top], [top, 0, 0, top], color="0.85")
                ax.fill(
                    [-b / 2 - z * yn, -b / 2, b / 2, b / 2 + z * yn],
                    [yn, 0, 0, yn],
                    color=viz.COLORS["sky"],
                    label="normal depth",
                )
                ax.plot(
                    [-b / 2 - z * yc, b / 2 + z * yc],
                    [yc, yc],
                    "--",
                    color=viz.COLORS["vermillion"],
                    label="critical depth",
                )
                ax.set(xlabel="[m]", ylabel="depth [m]", aspect="equal")
                ax.legend(loc="upper right")
                show(fig)
            st.caption(
                "Mild slope (y_n > y_c): subcritical, controls act from downstream. "
                "Steep slope: supercritical, controls act from upstream."
            )

# ---------------------------------------------------------------------------- potential flow
elif page == "Potential flow":
    st.title("Flow past a cylinder: circulation and lift")
    left, right = st.columns([1, 2])
    with left:
        U = st.slider("Free-stream speed U [m/s]", 1.0, 30.0, 10.0, key="pot_U")
        R = st.slider("Cylinder radius [m]", 0.1, 1.0, 0.5, key="pot_R")
        spin = st.slider("Circulation / (4 pi U R)", -1.5, 1.5, 0.3, step=0.05, key="pot_g")
    gamma = -spin * 4 * math.pi * U * R  # clockwise circulation gives upward lift for flow to the right
    flow = cylinder(U, R, gamma)
    with right:
        st.metric("Lift per metre (Kutta-Joukowski, air)", f"{kutta_joukowski_lift(1.2, U, -gamma):.1f} N/m")
        xs = np.linspace(-3 * R, 3 * R, 220)
        ys = np.linspace(-2 * R, 2 * R, 160)
        X, Y = np.meshgrid(xs, ys)
        psi = np.vectorize(lambda a, c: flow.stream_function(a, c) if a * a + c * c > R * R else np.nan)(X, Y)
        with viz.style("slides"):
            fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
            ax.contour(X, Y, psi, levels=35, colors=viz.COLORS["blue"], linewidths=0.9)
            ax.add_patch(plt.Circle((0, 0), R, color="0.4"))
            ax.set(aspect="equal", xlabel="x [m]", ylabel="y [m]")
            show(fig)
        st.caption(
            "Drag is zero for every circulation (d'Alembert's paradox). |value| > 1 lifts the "
            "stagnation point off the surface."
        )

# ---------------------------------------------------------------------------- settling
elif page == "Particle settling":
    st.title("Terminal velocity of a sphere")
    left, right = st.columns([1, 2])
    with left:
        fluid = fluid_picker("settle")
        d = st.number_input("Particle diameter [um]", 0.5, 20000.0, 200.0, key="set_d") * 1e-6
        rho_p = st.number_input("Particle density [kg/m3]", 1.0, 20000.0, 2650.0, key="set_rho")
    ut = terminal_velocity(d, rho_p, fluid)
    re = fluid.density * abs(ut) * d / fluid.dynamic_viscosity
    with right:
        c1, c2, c3 = st.columns(3)
        c1.metric(
            "Terminal velocity", f"{abs(ut) * 1000:.3g} mm/s", "rises" if ut < 0 else "settles", delta_color="off"
        )
        c2.metric("Reynolds number", f"{re:.3g}")
        c3.metric("Drag coefficient", f"{sphere_drag_coefficient(re):.3g}")
        with viz.style("slides"):
            fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
            viz.drag_curve_chart(ax, [(re, sphere_drag_coefficient(re))])
            show(fig)

# ---------------------------------------------------------------------------- water hammer
elif page == "Water hammer":
    st.title("Water hammer after valve closure (method of characteristics)")
    left, right = st.columns([1, 2])
    with left:
        length = st.slider("Pipe length [m]", 100, 3000, 600, key="wh_L")
        c = st.slider("Wave speed [m/s]", 300, 1400, 1200, key="wh_c")
        v0 = st.slider("Initial velocity [m/s]", 0.2, 4.0, 1.5, key="wh_v")
        tc = st.slider("Valve closure time [s]", 0.1, 20.0, 1.0, key="wh_tc")
    res = transients.moc_valve_closure(
        length, 0.5, c, 0.018, v0, 100.0, closure_time=tc, sections=20, t_end=max(8 * length / c, 1.5 * tc)
    )
    rise = max(res["head_valve"]) - res["head_valve"][0]
    with right:
        c1, c2, c3 = st.columns(3)
        c1.metric("Pipe period 2L/c", f"{2 * length / c:.2f} s")
        c2.metric("Peak surge", f"{rise:.0f} m", f"{rise * 9.81:.0f} kPa", delta_color="off")
        c3.metric("Joukowsky limit", f"{c * v0 / 9.80665:.0f} m")
        with viz.style("slides"):
            fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
            ax.plot(res["time"], res["head_valve"], color=viz.COLORS["blue"])
            ax.axvline(tc, ls=":", color="0.5")
            ax.set(xlabel="time [s]", ylabel="head at the valve [m]")
            show(fig)
        if tc < 2 * length / c:
            st.warning("Closure is faster than 2L/c: the full Joukowsky surge develops. Close more slowly!")
        else:
            st.success("Closure is slower than 2L/c: reflected waves limit the surge.")
