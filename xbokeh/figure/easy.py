from typing import (
    List,
    Optional,
    Union,
)

import numpy as np
from bokeh.plotting import figure

from xbokeh.common.constants import DEFAULT_COLORSET
from xbokeh.figure.base import BaseFigure


class EasyFigure(BaseFigure):
    """
    Easy figure for easy start
    """
    GROUP_NAME = "default"

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

        super().__init__(fig)

    def easy_line(
        self,
        y: Union[List, np.ndarray],
        x: Optional[Union[List, np.ndarray]] = None,
        *,
        color: Optional[str] = None,
    ):
        if x is None:
            x = list(range(len(y)))

        index = len(self._lines)

        if color is None:
            color = DEFAULT_COLORSET[index]

        super().add_line(
            self.GROUP_NAME,
            str(index),
            {"x": x, "y": y},
            color=color,
        )
