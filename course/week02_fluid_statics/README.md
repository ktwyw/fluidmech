# Week 2 - Fluid statics

**Syllabus:** Pascal's law and its use in manometers and other static problems like deposits and dams. Rigid bodies under linear movement or rotation.

**Course learning outcomes:** CLO 1, 2, 4  |  **Assessment:** HW-1

**Reading:** White, Ch. 2 (Sections 2.1-2.9).

## Learning objectives

- Apply the hydrostatic equation to multi-fluid manometers.
- Compute forces and centres of pressure on plane and curved surfaces; check dam stability.
- Apply buoyancy and stability (metacentric height) to floating bodies.
- Analyse liquids in rigid-body acceleration and rotation.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w02_01_manometer_chain.py`](w02_01_manometer_chain.py) | Solving multi-fluid manometers step by step | fluidmech only |
| [`w02_02_gravity_dam.py`](w02_02_gravity_dam.py) | Forces on a dam and its stability | fluidmech only |
| [`w02_03_curved_gate.py`](w02_03_curved_gate.py) | Hydrostatic force on a curved (radial) gate | fluidmech only |
| [`w02_04_buoyancy_hydrometer.py`](w02_04_buoyancy_hydrometer.py) | Buoyancy - hydrometers and the stability of a floating drum | fluidmech only |
| [`w02_05_accelerating_tank.py`](w02_05_accelerating_tank.py) | Rigid-body motion - a road tanker accelerating and braking | fluidmech only |
| [`w02_06_rotating_tank.py`](w02_06_rotating_tank.py) | Rigid-body rotation - the forced vortex | matplotlib |
| [`w02_07_atmosphere_and_altitude.py`](w02_07_atmosphere_and_altitude.py) | Pressure variation in the atmosphere | fluidmech only |
| [`w02_08_absolute_gauge_vacuum.py`](w02_08_absolute_gauge_vacuum.py) | Absolute, gauge and vacuum pressure; barometers | fluidmech only |
| [`w02_09_hydraulic_press.py`](w02_09_hydraulic_press.py) | Pascal's law - the hydraulic press and jack | fluidmech only |
| [`w02_10_storage_tank_wall.py`](w02_10_storage_tank_wall.py) | Hydrostatic load on a storage tank shell | fluidmech only |
| [`w02_11_chimney_draft.py`](w02_11_chimney_draft.py) | The stack effect - how a chimney creates draft | fluidmech only |
| [`w02_12_level_measurement.py`](w02_12_level_measurement.py) | Measuring liquid level with pressure | fluidmech only |
| [`w02_13_decanter_jackleg.py`](w02_13_decanter_jackleg.py) | The continuous gravity decanter and its jackleg | fluidmech only |
| [`w02_14_hinged_gate_force.py`](w02_14_hinged_gate_force.py) | Force needed to hold a hinged inclined gate closed | fluidmech only |
| [`w02_15_rotating_u_tube.py`](w02_15_rotating_u_tube.py) | Rigid-body rotation in a U-tube (a liquid tachometer) | fluidmech only |

Run a script from this folder, e.g. `python w02_01_manometer_chain.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Extend `w02_01` to an inclined-tube manometer and plot sensitivity versus angle.
2. Find the dam base width that just gives a sliding factor of safety of 1.5 with full uplift.
3. At what rotation speed does a 0.5 m diameter centrifuge bowl expose its bottom when half full?
