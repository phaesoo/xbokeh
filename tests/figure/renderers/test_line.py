from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure
from xbokeh.figure.renderers import Line
import pytest


@pytest.fixture
def line():
    source = ColumnDataSource(dict(x=[], y=[]))
    f = figure()
    r = f.line(source=source)
    return Line(r)


def test_set_color(line):
    line.set_color("black")
