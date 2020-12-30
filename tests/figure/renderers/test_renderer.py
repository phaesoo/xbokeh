import pytest
from bokeh.models.glyphs import Line
from bokeh.models.renderers import GlyphRenderer
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
    return _Renderer(Line, r)


def test_member_variables(renderer):
    assert isinstance(renderer._renderer, GlyphRenderer)
    assert isinstance(renderer._glyph, Line)
    assert renderer._renderer.data_source.data == _DATA


def test_clear(renderer):
    ret = renderer.clear()

    assert ret is None
