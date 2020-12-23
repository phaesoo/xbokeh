from __future__ import print_function

import abc
from collections import defaultdict

# bokeh
from bokeh.models import ColumnDataSource, Label
from bokeh.models import Span


class AfterInit(type):
    """
    Meta for after_init() after __init__()
    """
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.check_figure()
        return obj


class BaseFigure(object):
    """
    Highly utilized figure class for control visual attributes
    """
    __metaclass__ = AfterInit

    def __init__(self, figure):
        # figure
        self._figure = figure

        self._attributes = dict(
            # group, name
            source=defaultdict(dict),
            label=defaultdict(dict),
            span=defaultdict(dict),
            line=defaultdict(dict),
        )

    def check_figure(self):
        if self._figure is None:
            raise NotImplementedError(
                "Please initialize figure in __init__() method")

    @property
    def figure(self):
        return self._figure

    @abc.abstractmethod
    def _init_data(self):
        return dict(x=[], y=[])

    def set_axis_label(self, x_axis=None, y_axis=None):
        if x_axis is not None:
            self._figure.xaxis.axis_label = x_axis
        if y_axis is not None:
            self._figure.yaxis.axis_label = y_axis

    def set_axis_formatter(self, x_axis=None, y_axis=None):
        if x_axis is not None:
            self._figure.xaxis[0].formatter = x_axis
        if y_axis is not None:
            self._figure.yaxis[0].formatter = y_axis

    def y_range(self, start, end, y_range_name=None):
        if y_range_name is None:
            self._figure.y_range.start = start
            self._figure.y_range.end = end
        else:
            self._figure.extra_y_ranges[y_range_name].start = start
            self._figure.extra_y_ranges[y_range_name].end = end

    def extra_y_ranges(self, y_range_dict):
        self._figure.extra_y_ranges = y_range_dict

    def add_layout(self, obj, place):
        self._figure.add_layout(obj, place)

    def add_line(self, group, name, color, line_width=1.2, line_alpha=1.0):
        source = ColumnDataSource(data=self._init_data())
        line = self._figure.line(
            "x", "y", source=source, color=color, line_width=line_width, line_alpha=line_alpha)

        self._set_attr("source", group, name, source)
        self._set_attr("line", group, name, line)
        return line

    def add_label(self, group, name, y_range_name=None):
        if y_range_name:
            label = Label(x=0, y=0, x_offset=5, y_offset=-7, render_mode="css", text_font_size="10px",
                          text_alpha=1.0, background_fill_color="white", y_range_name=y_range_name)
        else:
            label = Label(x=0, y=0, x_offset=5, y_offset=-7, render_mode="css",
                          text_font_size="10px", text_alpha=1.0, background_fill_color="white")

        self._figure.add_layout(label)
        self._set_attr("label", group, name, label)

    def add_span(self, group, name, location, dimension, color, width=1.0, alpha=1.0, line_dash="solid"):
        span = Span(location=location, dimension=dimension, line_color=color,
                    line_width=width, line_alpha=alpha, line_dash=line_dash)
        self._set_attr("span", group, name, span)
        self._figure.renderers.extend([span])

    def add_vbar(self, group, name, color):
        source = ColumnDataSource(data=self._init_data())
        self._figure.vbar(x="x", top="y", width=0.98,
                          source=source, fill_color=color, line_alpha=0.0)
        self._set_attr("source", group, name, source)

    def set_source(self, group, name, **kwargs):
        """
        :param group:
        :param name:
        :param kwargs: input for source.data
        :return:
        """
        source = self._get_attr("source", group, name)
        source_data = dict()

        for key, val in kwargs.items():
            if key not in source.data.keys():
                raise ValueError(self._init_data().keys(), key)
            source_data[key] = val
        source.data = source_data

    def show_span(self, group, name, location):
        span = self._get_attr("span", group, name)
        span.location = location
        span.line_alpha = 1.0

    def hide_span(self, group, name):
        span = self._get_attr("span", group, name)
        span.line_alpha = 0.0

    def hide_span_group(self, group):
        names = self._get_group_member_names("span", group)
        for name in names:
            self.hide_span(group, name)

    def show_label(self, group, name, **kwargs):
        if "text_alpha" not in kwargs:
            kwargs["text_alpha"] = 1.0

        label = self._get_attr("label", group, name)
        self._set_label(label, **kwargs)

    def hide_label_group(self, group):
        names = self._get_group_member_names("label", group)
        for name in names:
            self.hide_label(group, name)

    def hide_label(self, group, name):
        label = self._get_attr("label", group, name)
        self._set_label(label, text_alpha=0.0)

    def update_line(self, group, name, **kwargs):
        line = self._get_attr("line", group, name).glyph

        line_color = kwargs.get("line_color")
        if line_color:
            line.line_color = line_color

    @staticmethod
    def _set_label(label, **kwargs):
        if "text" in kwargs:
            label.text = kwargs["text"]
        if "x" in kwargs:
            label.x = kwargs["x"]
        if "y" in kwargs:
            label.y = kwargs["y"]
        if "text_alpha" in kwargs:
            label.text_alpha = kwargs["text_alpha"]

    def clear_source_group(self, group):
        names = self._get_group_member_names("source", group)
        for name in names:
            self.clear_source(group, name)

    def clear_source(self, group, name):
        source = self._get_attr("source", group, name)
        source.data = self._init_data()

    def _get_attr_dict(self, attr_type):
        attr_dict = self._attributes.get(attr_type)
        if attr_dict is None:
            raise ValueError("Invalid attribute: %s" % attr_type)
        return attr_dict

    def _get_attr_group(self, attr_type, group):
        attr_dict = self._get_attr_dict(attr_type)
        attr_group = attr_dict.get(group)
        if attr_group is None:
            raise ValueError("Not existed line name: %s" % group)
        return attr_group

    def _get_attr(self, attr_type, group, name):
        attr_dict = self._get_attr_dict(attr_type)
        attr = attr_dict[group].get(name)
        if attr is None:
            raise ValueError(
                "Not existed attr group/name: %s/%s" % (group, name))
        return attr

    def _get_group_member_names(self, attr_type, group):
        attr_dict = self._get_attr_dict(attr_type)
        return attr_dict[group].keys()

    def _set_attr(self, attr_type, group, name, obj):
        attr_dict = self._get_attr_dict(attr_type)
        attr = attr_dict[group].get(name)
        if attr is not None:
            raise ValueError("Attr already existed: %s/%s/%s" %
                             (attr_type, group, name))

        attr_dict[group][name] = obj
