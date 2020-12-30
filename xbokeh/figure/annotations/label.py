
from xbokeh.figure.annotations.annotation import Annotation
from bokeh.models import Label as Label_


class Label(Annotation):
    def __init__(self, label: Label_) -> None:
        super().__init__(Label_, label)
        self._prev_text_alpha = label.text_alpha

    def show(self):
        self.update(text_alpha=self._prev_text_alpha)

    def hide(self):
        self._prev_text_alpha = self._annotation.text_alpha
        self.update(text_alpha=0.0)
