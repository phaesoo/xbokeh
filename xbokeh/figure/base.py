from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from datetime import (
    date,
    datetime,
)
from typing import (
    Optional,
    Union,
)

from bokeh.model import Model
from bokeh.models import ColumnDataSource
from bokeh.models import Label as Label_
from bokeh.models import Span as Span_
from bokeh.models import TickFormatter
from bokeh.plotting import Figure

from xbokeh.common.assertions import assert_type
from xbokeh.figure.annotations import (
    Label,
    Span,
)
from xbokeh.figure.renderers import Line
from xbokeh.figure.renderers.vbar import VBar


class BaseFigure(ABC):
    """
    Highly utilized wrapper class for Bokeh Figure
    """

    def __init__(self, figure: Figure):
        assert_type(figure, "figure", Figure)
        self._figure = figure
        self._attr_dict: dict = {
            "source": defaultdict(dict),
            "label": defaultdict(dict),
            "span": defaultdict(dict),
            "line": defaultdict(dict),
        }

        self._lines: dict = defaultdict(dict)
        self._vbars: dict = defaultdict(dict)
        self._spans: dict = defaultdict(dict)
        self._labels: dict = defaultdict(dict)

    @property
    def figure(self):
        return self._figure

    @abstractmethod
    def _init_data(self) -> dict:
        return dict(x=[], y=[], x_desc=[], y_desc=[])

    def set_property(self, **kwargs):
        """
        Update bokeh Figure object's properties
        """
        self._figure.update(**kwargs)

    def set_axis_label(
        self,
        xaxis_label: Optional[str] = None,
        yaxis_label: Optional[str] = None,
    ):
        assert xaxis_label or yaxis_label, "xaxis_label and yaxis_label are both None"
        if xaxis_label:
            assert_type(xaxis_label, "xais_label", str)
            self._figure.xaxis.axis_label = xaxis_label
        if yaxis_label:
            assert_type(yaxis_label, "yaxis_label", str)
            self._figure.yaxis.axis_label = yaxis_label

    def set_axis_formatter(
        self,
        xaxis_formatter: Optional[TickFormatter] = None,
        yaxis_formatter: Optional[TickFormatter] = None,
    ):
        assert xaxis_formatter or yaxis_formatter, "xaxis_formatter and yaxis_formatter are both None"

        if xaxis_formatter is not None:
            assert_type(xaxis_formatter, "xaxis_formatter", TickFormatter)
            self._figure.xaxis[0].formatter = xaxis_formatter
        if yaxis_formatter is not None:
            assert_type(yaxis_formatter, "xaxis_formatter", TickFormatter)
            self._figure.yaxis[0].formatter = yaxis_formatter

    def set_axis_tick_label(
        self,
        xaxis_tick_label: Optional[dict] = None,
        yaxis_tick_label: Optional[dict] = None,
    ):
        assert xaxis_tick_label or yaxis_tick_label, "xaxis_tick_label and yaxis_tick_label are both None"

        if xaxis_tick_label is not None:
            assert_type(xaxis_tick_label, "xaxis_tick_label", dict)
            self._figure.xaxis.ticker = list(xaxis_tick_label.keys())
            self._figure.xaxis.major_label_overrides = xaxis_tick_label
        if yaxis_tick_label is not None:
            assert_type(yaxis_tick_label, "yaxis_tick_label", dict)
            self._figure.yaxis.ticker = list(yaxis_tick_label.keys())
            self._figure.yaxis.major_label_overrides = yaxis_tick_label

    def y_range(
        self,
        start: Union[int, float, datetime, date],
        end: Union[int, float, datetime, date],
        y_range_name=None,
    ):
        if y_range_name is None:
            self._figure.y_range.start = start
            self._figure.y_range.end = end
        else:
            self._figure.extra_y_ranges[y_range_name].start = start
            self._figure.extra_y_ranges[y_range_name].end = end

    def extra_y_ranges(self, y_range_dict):
        self._figure.extra_y_ranges = y_range_dict

    def add_layout(self, obj, place: str):
        self._figure.add_layout(obj, place)

    def add_line(
        self,
        group: str,
        name: str,
        *,
        color: str,
        line_width: float = 1.2,
        line_alpha: float = 1.0,
    ):
        source = ColumnDataSource(data=self._init_data())
        line = self._figure.line(
            "x",
            "y",
            source=source,
            color=color,
            line_width=line_width,
            line_alpha=line_alpha,
        )

        if name in self._lines[group]:
            raise ValueError(f"line already exists for group/name: {group}{name}")
        self._lines[group][name] = Line(line, source)

    def add_label(
        self,
        group: str,
        name: str,
        y_range_name: str = None,
    ):
        if y_range_name:
            label = Label_(x=0, y=0, x_offset=5, y_offset=-7, render_mode="css", text_font_size="10px",
                           text_alpha=1.0, background_fill_color="white", y_range_name=y_range_name)
        else:
            label = Label_(x=0, y=0, x_offset=5, y_offset=-7, render_mode="css",
                           text_font_size="10px", text_alpha=1.0, background_fill_color="white")
        self._figure.add_layout(label)

        if name in self._labels[group]:
            raise ValueError(f"span already exists for group/name: {group}{name}")
        self._labels[group][name] = Label(label)

    def add_span(
        self,
        group: str,
        name: str,
        location: float,
        dimension: str,
        color: str,
        width: float = 1.0,
        alpha: float = 1.0,
        line_dash: str = "solid",
    ):
        span = Span_(
            location=location,
            dimension=dimension,
            line_color=color,
            line_width=width,
            line_alpha=alpha,
            line_dash=line_dash,
        )
        self._figure.renderers.extend([span])

        if name in self._spans[group]:
            raise ValueError(f"span already exists for group/name: {group}{name}")
        self._spans[group][name] = Span(span)

    def add_vbar(
        self,
        group: str,
        name: str,
        color: str,
    ):
        source = ColumnDataSource(data=self._init_data())
        vbar = self._figure.vbar(
            x="x",
            top="y",
            width=0.98,
            source=source,
            fill_color=color,
            line_alpha=0.0,
        )

        if name in self._vbars[group]:
            raise ValueError(f"vbar already exists for group/name: {group}{name}")
        self._vbars[group][name] = VBar(vbar, source)

    def get_line(
        self,
        group: str,
        name: str,
    ) -> Line:
        try:
            return self._lines[group][name]
        except KeyError:
            raise ValueError(f"group/name line does not exist: {group}/{name}")

    def get_vbar(
        self,
        group: str,
        name: str,
    ) -> Line:
        try:
            return self._vbars[group][name]
        except KeyError:
            raise ValueError(f"group/name _vbars does not exist: {group}/{name}")

    def get_span(
        self,
        group: str,
        name: str,
    ) -> Span:
        try:
            return self._spans[group][name]
        except KeyError:
            raise ValueError(f"group/name _spans does not exist: {group}/{name}")

    def get_label(
        self,
        group: str,
        name: str,
    ) -> Span:
        try:
            return self._labels[group][name]
        except KeyError:
            raise ValueError(f"group/name _labels does not exist: {group}/{name}")

    def show_span(
        self,
        group: str,
        name: str,
        location: str,
    ):
        span = self._get_attr("span", group, name)
        span.location = location
        span.line_alpha = 1.0

    def hide_span(
        self,
        group: str,
        name: str,
    ):
        span = self._get_attr("span", group, name)
        span.line_alpha = 0.0

    def hide_span_group(
        self,
        group: str,
    ):
        names = self._get_group_member_names("span", group)
        for name in names:
            self.hide_span(group, name)

    def show_label(
        self,
        group: str,
        name: str,
        **kwargs,
    ):
        _kwargs = {
            "text_alpha": 1.0
        }
        _kwargs.update(**kwargs)

        label = self._get_attr("label", group, name)
        self._set_label(label, **_kwargs)

    def hide_label(
        self,
        group: str,
        name: Optional[str] = None,
    ):
        if name:
            attr = self._get_attr("label", group, name)
            self._set_label(attr, text_alpha=0.0)
        else:
            attrs = self._get_group_attrs("source", group)
            for k in attrs:
                self._set_label(attrs[k], text_alpha=0.0)

    def update_line(
        self,
        group: str,
        name: str,
        **kwargs,
    ):
        line = self._get_attr("line", group, name).glyph

        line_color = kwargs.get("line_color")
        if line_color:
            line.line_color = line_color

    @staticmethod
    def _set_label(
        label: Label_,
        **kwargs,
    ):
        if "text" in kwargs:
            label.text = kwargs["text"]
        if "x" in kwargs:
            label.x = kwargs["x"]
        if "y" in kwargs:
            label.y = kwargs["y"]
        if "text_alpha" in kwargs:
            label.text_alpha = kwargs["text_alpha"]

    def clear_source(
        self,
        group: str,
        name: Optional[str] = None,
    ):
        if name:
            attr = self._get_attr("source", group, name)
            attr.data = self._init_data()
        else:
            attrs = self._get_group_attrs("source", group)
            for k in attrs:
                attrs[k].data = self._init_data()

    def _get_attr_groups(
        self,
        attr_type: str,
    ) -> dict:
        attr_groups = self._attr_dict.get(attr_type)
        if attr_groups is None:
            raise ValueError("attr_type does not exist: {}".format(attr_type))
        return attr_groups

    def _get_group_attrs(
        self,
        attr_type: str,
        group: str,
    ) -> dict:
        group_attrs = self._get_attr_groups(attr_type).get(group)
        if group_attrs is None:
            raise ValueError("group does not exist: {}".format(group))
        return group_attrs

    def _get_attr(
        self,
        attr_type: str,
        group: str,
        name: str,
    ) -> Model:
        attr = self._get_group_attrs(attr_type, group).get(name)
        if attr is None:
            raise ValueError("attr does not exist: group({}), name({})".format(group, name))
        return attr

    def _get_group_member_names(
        self,
        attr_type: str,
        group: str,
    ):
        attr_dict = self._get_attr_groups(attr_type)
        return attr_dict[group].keys()

    # def _set_renderer(
    #     self,
    #     group: str,
    #     name: str,
    #     renderer: GlyphRenderer,
    # ):
    #     assert_type(renderer, "renderer", GlyphRenderer)

    #     attr_dict = self._get_attr_groups(attr_type)
    #     attr = attr_dict[group].get(name)
    #     if attr is not None:
    #         raise ValueError("Attr already existed: %s/%s/%s" %
    #                          (attr_type, group, name))
    #     attr_dict[group][name] = obj
