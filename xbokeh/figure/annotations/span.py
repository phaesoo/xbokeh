
from xbokeh.figure.annotations.annotation import Annotation
from bokeh.models import Span as Span_


class Span(Annotation):
    def __init__(self, span: Span_) -> None:
        super().__init__(Span_, span)
