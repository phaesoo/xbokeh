from abc import ABC
from xbokeh.common.assertions import assert_type
from bokeh.models import Annotation as Annotation_
from typing import Type


class Annotation(ABC):
    def __init__(self, type_: Type, annotation: Annotation_) -> None:
        super().__init__()
        assert_type(annotation, "annotation", type_)

        self._annotation = annotation
