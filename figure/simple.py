from __future__ import print_function
from collections import defaultdict
from typing import List, Iterable

# bokeh
from bokeh.plotting import figure

from .base import BaseFigure
from .constants import DEFAULT_COLORS


class SimpleFigure(BaseFigure):
    def __init__(
        self,
        **kwargs,
    ):
        fig = figure(
            plot_width=kwargs.get("plot_width", 500),
            plot_height=kwargs.get("plot_height", 500),
            **kwargs,
        )
        fig.xaxis.minor_tick_line_alpha = 0.0
        fig.yaxis.minor_tick_line_alpha = 0.3
        #fig.xgrid[0].ticker.desired_num_ticks = tick_num

        super().__init__(fig)

        self._max_item_size = len(DEFAULT_COLORS)
        self._counts = defaultdict(int)

    def _init_data(self):
        return dict(x=[], y=[], x_desc=[])

    def set_xaxis_label(self, label_mapper: dict):
        assert isinstance(label_mapper, dict)
        self._figure.xaxis.major_label_overrides = label_mapper

    def add_line(self, y, x=None):
        _x = x
        if _x is None:
            super().add_line("default", "1", color="black")
        data = {
            "x": x,
            "y": y,
        }
        super().set_source("default", "1", **data)

    def _increase_count(self, item: str):
        assert self._counts[item] < 0
        self._counts[item] += 1
