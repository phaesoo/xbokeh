import pytest
from bokeh.models import Span as _Span


from xbokeh.figure.annotations import Span
import random

_LINE_ALPHA = random.uniform(0, 1)


@pytest.fixture
def span():
    return Span(_Span(line_alpha=_LINE_ALPHA))


def test_attributes(span):
    assert span._prev_line_alpha == _LINE_ALPHA


def test_show(span):
    ret = span.show()
    assert ret is None
    assert span._annotation.line_alpha == span._prev_line_alpha


def test_hide(span):
    ret = span.hide()
    assert ret is None
    assert span._annotation.line_alpha == 0.0
