from bokeh.models import ColumnDataSource
from xbokeh.common.assertions import assert_type

from bokeh.models.glyphs import Line as _Line
from bokeh.models.renderers import GlyphRenderer

from xbokeh.figure.renderers.renderer import Renderer


class Line(Renderer):
    def __init__(self, renderer: GlyphRenderer, source: ColumnDataSource) -> None:
        super().__init__(renderer, source)

        assert_type(self._renderer.glyph, "_renderer.glyph", _Line)
        self._line = self._renderer.glyph

    def set_color(self, color: str):
        self._line.line_color = color
