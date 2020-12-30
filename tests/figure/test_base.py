from bokeh.models.tickers import FixedTicker
from xbokeh.figure.base import BaseFigure
from bokeh.plotting import figure as bpf
import pytest
from bokeh.models import NumeralTickFormatter
from xbokeh.figure.renderers import Line


class _Figure(BaseFigure):
    def __init__(self):
        super().__init__(bpf())


@pytest.fixture
def fg():  # pylint: disable=invalid-name
    return _Figure()


@pytest.fixture
def fg2():  # pylint: disable=invalid-name
    f = _Figure()
    group = "group-0"
    name = "line-0"
    f.add_line(group, name, {"x": [0, 1, 2], "y": [3, 4, 5]}, color="black")
    return f


def test_set_axis_label(fg):
    xaxis_label = "X"
    yaxis_label = "Y"
    ret = fg.set_axis_label(xaxis_label=xaxis_label, yaxis_label=yaxis_label)

    assert ret is None
    assert fg.figure.xaxis.axis_label == "X"
    assert fg.figure.yaxis.axis_label == "Y"


def test_set_axis_formatter(fg):
    xaxis_formatter = NumeralTickFormatter(format="0.000")
    yaxis_formatter = NumeralTickFormatter(format="0.0")
    ret = fg.set_axis_formatter(
        xaxis_formatter,
        yaxis_formatter,
    )

    assert ret is None
    assert fg.figure.xaxis[0].formatter is xaxis_formatter
    assert fg.figure.yaxis[0].formatter is yaxis_formatter


def test_set_axis_tick_label(fg):
    xaxis_tick_label = {0: "A", 1: "B"}
    yaxis_tick_label = {0: "C", 1: "D"}
    ret = fg.set_axis_tick_label(
        xaxis_tick_label,
        yaxis_tick_label,
    )

    assert ret is None
    assert isinstance(fg.figure.xaxis.ticker, FixedTicker)
    assert fg.figure.xaxis.major_label_overrides == xaxis_tick_label
    assert isinstance(fg.figure.yaxis.ticker, FixedTicker)
    assert fg.figure.yaxis.major_label_overrides == yaxis_tick_label


def test_add_line(fg):
    group = "group-0"
    name = "line-0"
    ret = fg.add_line(group, name, {"x": [0, 1, 2], "y": [3, 4, 5]}, color="black")

    assert ret is None
    assert len(fg._lines[group]) == 1
    assert isinstance(fg._lines[group][name], Line)


def test_add_line_raises_if_name_duplicated(fg):
    group = "group-0"
    name = "line-0"
    fg.add_line(group, name, {"x": [0, 1, 2], "y": [3, 4, 5]}, color="black")

    with pytest.raises(ValueError):
        fg.add_line(group, name, {"x": [0, 1, 2], "y": [3, 4, 5]}, color="black")


def test_get_line(fg2):
    line = fg2.get_line("group-0", "line-0")

    assert isinstance(line, Line)


def test_get_line_raises(fg2):
    with pytest.raises(ValueError):
        fg2.get_line("group-0", "invalid")
