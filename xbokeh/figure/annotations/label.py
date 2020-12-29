
from xbokeh.figure.annotations.annotation import Annotation
from bokeh.models import Label as Label_


class Label(Annotation):
    def __init__(self, label: Label_) -> None:
        super().__init__(Label_, label)
