from bokeh.models import ColumnDataSource

from bokeh.models.glyphs import Line as Line_
from bokeh.models.renderers import GlyphRenderer

from xbokeh.figure.renderers.renderer import Renderer


class Line(Renderer):
    def __init__(self, renderer: GlyphRenderer, source: ColumnDataSource) -> None:
        super().__init__(Line_, renderer, source)

    def set_color(self, color: str):
        self.update(line_color=color)
