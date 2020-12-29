from bokeh.plotting import figure
from xbokeh.figure.renderers import Line
import pytest


@pytest.fixture
def line():
    f = figure()
    l = f.line(x=[1, 2, 3], y=[1, 2, 3])

    return Line(l)


def test_set_color(line):
    line.set_color("black")


def test_clear(line):
    line.clear()
