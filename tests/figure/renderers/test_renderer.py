from bokeh.models.glyphs import Line
import pytest
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure


from xbokeh.figure.renderers.renderer import Renderer

_DATA = {"x": [1, 2], "y": [3, 4]}


class _Renderer(Renderer):
    pass


@pytest.fixture
def renderer():
    source = ColumnDataSource(_DATA)
    f = figure()
    r = f.line(source=source)
    return _Renderer(Line, r, source)


def test_init_data(renderer):
    assert renderer._init_data == {"x": [], "y": []}


def test_source_data(renderer):
    assert renderer._source.data == _DATA


def test_clear(renderer):
    ret = renderer.clear()

    assert ret is None
