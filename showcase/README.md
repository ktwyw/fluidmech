# Showcase: advanced topics, animations, publication figures and apps

This folder goes beyond the course: small but real CFD codes, animations you can put in a
presentation, figures ready for a thesis or paper, and interactive apps. Everything is built on
the tested `fluidmech` library, and every advanced result is checked against the literature
(see [`docs/VALIDATION.md`](../docs/VALIDATION.md)).

```bash
pip install -e ".[showcase,apps]"      # numpy, scipy, matplotlib, pillow, streamlit
```

Run any script from a scratch directory; it prints its results and writes its figures there.
Set `FLUIDMECH_QUICK=1` for a fast, coarse run (this is what the automated tests use).

## Interactive apps

| App | How to start | What it does |
|---|---|---|
| **FluidMech Studio** | `streamlit run showcase/apps/fluidmech_studio.py` | Six calculators in your browser: pipe flow on the Moody chart, pump operating point with a speed slider, open-channel depths, potential flow and lift, particle settling, water hammer |
| Moody explorer | `python showcase/apps/explorer_moody.py` | Drag sliders for flow, diameter and temperature and watch your pipe move on the Moody chart |
| Potential-flow explorer | `python showcase/apps/explorer_potential_flow.py` | Build flows from a stream, a source, a doublet and a vortex |

FluidMech Studio can be published for free on [Streamlit Community Cloud](https://streamlit.io/cloud)
so that anyone can use it from a phone. The two explorers need only matplotlib and a desktop.

## Advanced topics (`advanced/`)

| Script | Topic | Validated against |
|---|---|---|
| `a01_lid_driven_cavity.py` | 2D Navier–Stokes CFD (stream function–vorticity) | Ghia, Ghia & Shin (1982): centreline velocity within 0.003 |
| `a02_vortex_shedding_lbm.py` | Lattice-Boltzmann flow past a cylinder, von Kármán street (~2–3 min) | Strouhal number vs. Williamson (1996), with a domain-size study |
| `a03_blasius_boundary_layer.py` | Similarity solution by the shooting method | f″(0) = 0.33206, δ₉₉ = 4.91 |
| `a04_water_hammer_moc.py` | Method of characteristics for pipeline transients | Joukowsky surge |
| `a05_cavitation_bubble.py` | Rayleigh–Plesset bubble collapse and rebound | Rayleigh's collapse time |
| `a06_taylor_dispersion.py` | Monte Carlo random walk in laminar pipe flow | Taylor–Aris D_eff = D(1 + Pe²/48) |

Each script also discusses the limits of its model; for example, where the bubble-wall speed exceeds
the speed of sound, or where water hammer would make the liquid column separate.

## Animations (`animations/`)

| Script | GIF |
|---|---|
| `g01_flow_startup.py` | Channel flow starting from rest and approaching the Poiseuille profile |
| `g02_water_hammer_wave.py` | A pressure wave travelling up and down a pipeline |
| `g03_vortex_street.py` | Vortex shedding behind a cylinder (~2–3 min to compute) |
| `g04_taylor_dispersion.py` | A tracer pulse sheared by the parabolic profile |
| `g05_variable_speed_pump.py` | The operating point sliding along the system curve as a pump slows down |

The technique is the same in every script: compute a list of frames, then
`FuncAnimation(fig, draw, frames=...)` and `anim.save("name.gif", writer=PillowWriter(fps=...))`.

## Publication-quality figures (`figures/`)

| Script | Figure | Technique shown |
|---|---|---|
| `f01_pipe_flow_figure.py` | Moody chart with data, velocity profiles, duct friction | Three-panel double-column layout, panel letters |
| `f02_non_newtonian_figure.py` | Flow curves and pipe profiles of non-Newtonian fluids | Colours shared across panels, normalised profiles |
| `f03_pump_hill_chart.py` | Pump efficiency 'hill chart' with speed curves | Filled and labelled contours |
| `f04_open_channel_figure.py` | Specific-energy diagram and water-surface profiles | Annotations, physical-coordinate plots |

All of them use `fluidmech.viz`:

```python
from fluidmech import viz

with viz.style("paper"):  # or "slides" / "poster"
    fig, ax = viz.figure(width="single")  # 3.5 in journal column
    viz.moody_chart(ax)
    viz.savefig(fig, "moody", ("pdf", "png", "svg"))  # vector + 300-dpi raster
```

`viz.style` sets journal conventions (inward ticks, thin lines, embedded TrueType fonts) and the
Okabe–Ito colour-blind-safe palette. It is also used for the course and example figures if you wish.

## Challenges for students

1. **CFD:** run the cavity at Re = 400 and 1000 (Ghia also tabulates these) - how fine must the grid be?
2. **Vortex shedding:** measure St at Re = 60, 100 and 150 and compare with Williamson's St-Re curve.
3. **Water hammer:** add a surge tank or an air vessel to `transients.moc_valve_closure` and show how it
   limits the surge.
4. **Cavitation:** drive the bubble with an oscillating pressure `p_inf(t)` (acoustic cavitation) and
   look for the violent 'inertial' collapses.
5. **Apps:** add a page to FluidMech Studio (e.g. packed-bed pressure drop with `porous.ergun_pressure_gradient`).
6. **Figures:** reproduce a figure from your favourite textbook with `viz.style("paper")`.
