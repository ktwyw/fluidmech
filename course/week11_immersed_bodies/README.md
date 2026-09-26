# Week 11 - Flow over immersed bodies

**Syllabus:** Creep flow, laminar and turbulent flow with boundary-layer separation. Drag coefficients for simple geometries. Terminal velocities of drops and bubbles.

**Course learning outcomes:** CLO 2, 3, 4, 5  |  **Assessment:** Lab Assignment #3

**Reading:** White, Sections 7.5-7.6.

## Learning objectives

- Use the sphere and cylinder drag curves across flow regimes.
- Compute terminal velocities of particles, drops and bubbles, choosing a valid model.
- Assess vortex-shedding resonance and wind loads.
- Apply hindered-settling relations to clarifier and thickener sizing.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w11_01_sphere_drag_regimes.py`](w11_01_sphere_drag_regimes.py) | The drag curve of a sphere | matplotlib |
| [`w11_02_terminal_velocity_particles.py`](w11_02_terminal_velocity_particles.py) | Terminal settling velocity of particles | fluidmech only |
| [`w11_03_drops_and_bubbles.py`](w11_03_drops_and_bubbles.py) | Terminal velocities of drops and bubbles | fluidmech only |
| [`w11_04_cylinder_vortex_shedding.py`](w11_04_cylinder_vortex_shedding.py) | Flow past cylinders - drag and vortex shedding | fluidmech only |
| [`w11_05_hindered_settling.py`](w11_05_hindered_settling.py) | Settling of concentrated suspensions (hindered settling) | fluidmech only |
| [`w11_06_friction_vs_pressure_drag.py`](w11_06_friction_vs_pressure_drag.py) | Friction drag versus pressure (form) drag - why streamlining works | fluidmech only |
| [`w11_07_centrifuge_and_cyclone.py`](w11_07_centrifuge_and_cyclone.py) | Separating particles faster than gravity - centrifuges and cyclones | fluidmech only |
| [`w11_08_approach_to_terminal_velocity.py`](w11_08_approach_to_terminal_velocity.py) | How quickly does a falling sphere reach terminal velocity? | fluidmech only |
| [`w11_09_gravity_settling_chamber.py`](w11_09_gravity_settling_chamber.py) | Sizing a gravity settling chamber | fluidmech only |
| [`w11_10_bubble_column_holdup.py`](w11_10_bubble_column_holdup.py) | Gas holdup and interfacial area in a bubble column | fluidmech only |
| [`w11_11_particle_size_from_settling.py`](w11_11_particle_size_from_settling.py) | Sedimentation analysis - particle size from settling speed | fluidmech only |
| [`w11_12_elutriation.py`](w11_12_elutriation.py) | Elutriation - which particles are blown out of a fluidised bed? | fluidmech only |
| [`w11_13_extraction_column_holdup.py`](w11_13_extraction_column_holdup.py) | Drops in a liquid-liquid extraction column - holdup and flooding | fluidmech only |
| [`w11_14_aerosols_slip_and_brownian.py`](w11_14_aerosols_slip_and_brownian.py) | Very small particles - slip correction and Brownian motion | fluidmech only |
| [`w11_15_pneumatic_conveying.py`](w11_15_pneumatic_conveying.py) | Lifting solids with air - vertical pneumatic conveying | fluidmech only |
| [`w11_lab3_settling_experiment.py`](w11_lab3_settling_experiment.py) | Drag coefficients from a settling experiment | matplotlib |

Run a script from this folder, e.g. `python w11_01_sphere_drag_regimes.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Enter your Lab 3 timings in `w11_lab3` and correct the results for the wall effect.
2. Find the particle size that is just carried out of the fluidised bed in `w12_03` (elutriation).
3. Check a thermowell in a water line with `w11_04` - which velocity is safe?
