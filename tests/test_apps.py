"""GUIs: the Streamlit app is driven headlessly with AppTest; the matplotlib explorers through build()."""

import sys
from pathlib import Path

import pytest

APPS = Path(__file__).resolve().parent.parent / "showcase" / "apps"


def test_streamlit_studio_all_pages():
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APPS / "fluidmech_studio.py"), default_timeout=120).run()
    assert not at.exception
    for page in ["Pipe flow", "Pump & system", "Open channel", "Potential flow", "Particle settling", "Water hammer"]:
        at.sidebar.radio(key="page").set_value(page).run()
        assert not at.exception, page
        assert len(at.metric) >= 1, page
    # edge cases produce messages, not crashes
    at.sidebar.radio(key="page").set_value("Pump & system").run()
    at.slider(key="pump_speed").set_value(40).run()
    assert at.error and not at.exception
    at.sidebar.radio(key="page").set_value("Open channel").run()
    at.slider(key="ch_b").set_value(0.0).run()
    at.slider(key="ch_z").set_value(0.0).run()
    assert at.error and not at.exception


def test_matplotlib_explorers():
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    sys.path.insert(0, str(APPS))
    import explorer_moody
    import explorer_potential_flow

    fig, widgets, _ = explorer_moody.build()
    widgets["D"].set_val(200.0)  # 0.2 L/s in a 200 mm pipe: Re ~ 1270, genuinely laminar
    widgets["Q"].set_val(0.2)
    assert "laminar" in fig.texts[-1].get_text()
    widgets["Q"].set_val(100.0)
    assert "turbulent" in fig.texts[-1].get_text()
    fig2, sliders, _ = explorer_potential_flow.build()
    sliders["m"].set_val(2.0)
    sliders["gamma"].set_val(-8.0)
    assert fig2.axes[0].collections  # streamlines were drawn
