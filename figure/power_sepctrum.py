from __future__ import print_function

# bokeh
from bokeh.plotting import figure

from .base import BaseFigure


class PowerSpectrumFigure(BaseFigure):
    def __init__(self, title, width, height, tools="", tick_num=5):
        fig = figure(
            title=title,
            plot_width=width,
            plot_height=height,
            x_axis_label="Days/Cycle",
            y_axis_label="Power",
            tools=tools,
            toolbar_location="above",
        )
        fig.xaxis.minor_tick_line_alpha = 0.0
        fig.yaxis.minor_tick_line_alpha = 0.3
        fig.xgrid[0].ticker.desired_num_ticks = tick_num

        super(PowerSpectrumFigure, self).__init__(fig)

    def _init_data(self):
        return dict(x=[], y=[])

    def set_source(self, group, name, **kwargs):
        super(PowerSpectrumFigure, self).set_source(group, name, **kwargs)
