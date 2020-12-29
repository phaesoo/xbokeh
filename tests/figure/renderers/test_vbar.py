from xbokeh.figure.renderers.vbar import VBar
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure
import pytest


@pytest.fixture
def vbar():
    source = ColumnDataSource(dict(x=[], y=[]))
    f = figure()
    r = f.vbar(source=source)
    return VBar(r, source)
