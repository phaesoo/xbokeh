from abc import ABC
from typing import (
    Dict,
    List,
    Optional,
)

from bokeh.models.renderers import GlyphRenderer
from bokeh.models.sources import ColumnDataSource

from xbokeh.common.assertions import assert_type
from xbokeh.figure.renderers.validate import validate_data


class Renderer(ABC):
    def __init__(self, renderer: GlyphRenderer, data: Optional[dict]) -> None:
        super().__init__()
        assert_type(renderer, "renderer", GlyphRenderer)

        if data:
            validate_data(data)
        else:
            data = {"x": [], "y": []}

        # init_data will be used to initialize source.data
        self._init_data: Dict[str, List] = {k: [] for k in data}

        self._renderer = renderer
        self._source = ColumnDataSource(data=data)

    def clear(self):
        self._source.data = self._init_data.copy()
