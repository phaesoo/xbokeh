import pytest
from xbokeh.figure import SimpleFigure


@pytest.fixture
def sf():  # pylint: disable=invalid-name
    return SimpleFigure()
