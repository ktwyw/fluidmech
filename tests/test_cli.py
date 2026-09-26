"""Command-line interface: each sub-command runs, prints the expected numbers and reports errors."""

import pytest

from fluidmech.cli import main


def test_pipe_type1(capsys):
    assert main(["pipe", "-Q", "0.02", "-D", "0.1", "-L", "200", "-e", "commercial_steel"]) == 0
    out = capsys.readouterr().out
    assert "turbulent" in out and "12.01" in out


def test_pipe_type2_and_type3(capsys):
    assert main(["pipe", "-D", "0.1", "--head-loss", "8", "-L", "200", "-e", "0.045"]) == 0
    assert main(["pipe", "-Q", "0.02", "--head-loss", "5", "-L", "200"]) == 0
    assert "Diameter" in capsys.readouterr().out


def test_pipe_requires_two_inputs():
    with pytest.raises(SystemExit):
        main(["pipe", "-Q", "0.02", "-L", "200"])


def test_channel_props_convert(capsys):
    assert main(["channel", "-Q", "25", "-b", "4", "-z", "1.5", "-n", "0.012", "-S", "0.0008"]) == 0
    assert main(["props", "--fluid", "air", "-T", "15"]) == 0
    assert main(["convert", "100", "gpm", "L/s"]) == 0
    out = capsys.readouterr().out
    assert "1.603" in out and "1.22" in out and "6.309" in out


def test_error_is_reported(capsys):
    assert main(["convert", "1", "m", "psi"]) == 2
    assert "error" in capsys.readouterr().err
