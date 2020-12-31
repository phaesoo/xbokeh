import pytest
from xbokeh.figure import EasyFigure
from xbokeh.common.constants import DEFAULT_COLORSET


@pytest.fixture
def ef():  # pylint: disable=invalid-name
    return EasyFigure()


def test_easy_line_with_param_y(ef):
    y_1 = [3, 4, 5]
    ef.easy_line(y_1)
    line = ef._lines[ef.GROUP_NAME]["0"]

    assert len(ef._lines[ef.GROUP_NAME]) == 1
    assert line._glyph.line_color == DEFAULT_COLORSET[0]
    assert line.data == {"x": [0, 1, 2], "y": y_1}

    y_2 = [6, 7, 8]
    ef.easy_line(y_2)
    line = ef._lines[ef.GROUP_NAME]["1"]

    assert len(ef._lines[ef.GROUP_NAME]) == 2
    assert line._glyph.line_color == DEFAULT_COLORSET[1]
    assert line.data == {"x": [0, 1, 2], "y": y_2}


def test_easy_line_with_param_y_x(ef):
    y = [6, 7, 8]
    x = [3, 4, 5]
    ef.easy_line(y, x=x)
    line = ef._lines[ef.GROUP_NAME]["0"]

    assert len(ef._lines[ef.GROUP_NAME]) == 1
    assert line._glyph.line_color == DEFAULT_COLORSET[0]
    assert line.data == {"x": x, "y": y}


def test_easy_line_with_param_y_x_color(ef):
    y = [6, 7, 8]
    x = [3, 4, 5]
    color = "black"
    ef.easy_line(y, x=x, color=color)
    line = ef._lines[ef.GROUP_NAME]["0"]

    assert line._glyph.line_color == color


def test_easy_vbar_with_param_y_x_color(ef):
    y = [6, 7, 8]
    x = [3, 4, 5]
    color = "black"
    ef.easy_vbar(y, x=x, color=color)
    line = ef._vbars[ef.GROUP_NAME]["0"]

    assert len(ef._vbars[ef.GROUP_NAME]) == 1
    assert line.data == {"x": x, "y": y}
    assert line._glyph.fill_color == color
