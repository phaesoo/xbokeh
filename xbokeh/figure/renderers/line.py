

from typing import Optional
from xbokeh.common.assertions import assert_type

from bokeh.models.glyphs import Line as _Line
from bokeh.models.renderers import GlyphRenderer

from xbokeh.figure.renderers.renderer import Renderer


class Line(Renderer):
    def __init__(self, renderer: GlyphRenderer, data: Optional[dict] = None) -> None:
        """
        :renderer: GlyphRenderer return by figure.line
        :data: data for ColumnDataSource.
            ex) data = {'x': [1,2,3,4], 'y': np.ndarray([10.0, 20.0, 30.0, 40.0])}
        """
        super().__init__(renderer, data)

        assert_type(self._renderer.glyph, "_renderer.glyph", _Line)
        self._line = self._renderer.glyph

    def set_color(self, color: str):
        self._line.line_color = color
