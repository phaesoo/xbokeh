from xbokeh.figure.base import BaseFigure
from bokeh.plotting import figure as bpf
import pytest
from bokeh.models import NumeralTickFormatter


class _Figure(BaseFigure):
    def __init__(self):
        super().__init__(bpf())

    def _init_data(self) -> dict:
        return dict(x=[], y=[])


@pytest.fixture
def figure():
    return _Figure()


def test_set_axis_label(figure):
    ret = figure.set_axis_label(xaxis_label="X", yaxis_label="Y")

    assert ret is None
    assert figure.figure.xaxis.axis_label == "X"
    assert figure.figure.yaxis.axis_label == "Y"


def test_set_axis_formatter(figure):
    xaxis_formatter = NumeralTickFormatter(format="0.000")
    yaxis_formatter = NumeralTickFormatter(format="0.0")
    ret = figure.set_axis_formatter(
        xaxis_formatter=xaxis_formatter,
        yaxis_formatter=yaxis_formatter,
    )

    assert ret is None

    assert figure.figure.xaxis[0].formatter is xaxis_formatter
    assert figure.figure.yaxis[0].formatter is yaxis_formatter
