from abc import ABC
from typing import (
    Dict,
    List,
    Type,
)

from bokeh.models.glyph import Glyph
from xbokeh.figure.renderers.validate import validate_data

from bokeh.models.renderers import GlyphRenderer
from bokeh.models.sources import ColumnDataSource

from xbokeh.common.assertions import assert_type


class Renderer(ABC):
    def __init__(self, type_: Type, renderer: GlyphRenderer, source: ColumnDataSource) -> None:
        """
        :renderer: instance of GlyphRenderer
        :data: data for ColumnDataSource.
            ex) data = {'x': [1,2,3,4], 'y': np.ndarray([10.0, 20.0, 30.0, 40.0])}
        """
        super().__init__()
        assert_type(renderer, "renderer", GlyphRenderer)
        assert_type(renderer.glyph, "_renderer.glyph", type_)

        # init_data will be used to initialize source.data
        self._init_data: Dict[str, List] = {k: [] for k in source.data}

        self._renderer = renderer
        self._glyph: Glyph = renderer.glyph
        self._source = source

    def set_data(self, data: dict):
        assert_type(data, "data", dict)
        validate_data(data)
        self._source.data = data

    def set_property(self, **kwargs):
        """
        Updates the model's property
        """
        self._glyph.update(**kwargs)

    def clear(self):
        self._source.data = self._init_data.copy()
