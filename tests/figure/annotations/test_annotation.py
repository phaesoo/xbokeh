import pytest
from bokeh.models import Annotation as Annotation_


from xbokeh.figure.annotations.annotation import Annotation


class _Annotation(Annotation):
    pass


@pytest.fixture
def annotation():
    return _Annotation(Annotation_, Annotation_())


def test_attributes(annotation):
    assert isinstance(annotation._annotation, Annotation_)
