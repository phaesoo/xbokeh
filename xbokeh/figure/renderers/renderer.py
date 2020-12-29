from abc import ABC
from typing import (
    Dict,
    List,
)

from bokeh.models.renderers import GlyphRenderer
from bokeh.models.sources import ColumnDataSource

from xbokeh.common.assertions import assert_type


class Renderer(ABC):
    def __init__(self, renderer: GlyphRenderer, source: ColumnDataSource) -> None:
        """
        :renderer: instance of GlyphRenderer
        :data: data for ColumnDataSource.
            ex) data = {'x': [1,2,3,4], 'y': np.ndarray([10.0, 20.0, 30.0, 40.0])}
        """
        super().__init__()
        assert_type(renderer, "renderer", GlyphRenderer)

        # init_data will be used to initialize source.data
        self._init_data: Dict[str, List] = {k: [] for k in source.data}

        self._renderer = renderer
        self._source = source

    def clear(self):
        self._source.data = self._init_data.copy()
