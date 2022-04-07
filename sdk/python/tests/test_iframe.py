from typing import List

import flet
from flet import IFrame
from flet.protocol import Command


def test_iframe_add():
    c = IFrame(src="https://google.com", border_style="solid")
    assert isinstance(c, flet.Control)
    assert isinstance(c, flet.IFrame)

    assert c.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["iframe"],
            attrs={"borderstyle": "solid", "src": "https://google.com"},
            lines=[],
            commands=[],
        )
    ], "Test failed"


def test_iframe_multiple_border_styles():
    c = IFrame(src="https://google.com", border_style=["solid", "none", "groove"])
    assert isinstance(c, flet.Control)
    assert isinstance(c, flet.IFrame)

    # check property reading as a list
    style = c.border_style
    assert isinstance(style, List)
    assert len(style) == 3

    assert c.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["iframe"],
            attrs={"borderstyle": "solid none groove", "src": "https://google.com"},
            lines=[],
            commands=[],
        )
    ], "Test failed"


def test_iframe_border_style():
    # list of values
    c = IFrame(border_style=["solid", "dashed"])
    v = c.border_style
    assert isinstance(v, List)
    assert len(v) == 2

    # single value
    c.border_style = "groove"
    v = c.border_style
    assert isinstance(v, str)
    assert v == "groove"

    # none
    c.border_style = None
    v = c.border_style
    assert v == ""


def test_iframe_border_color():
    # list of values
    c = IFrame(border_color=["red", "yellow"])
    v = c.border_color
    assert isinstance(v, List)
    assert len(v) == 2

    # single value
    c.border_color = "blue"
    v = c.border_color
    assert isinstance(v, str)
    assert v == "blue"

    # none
    c.border_color = None
    v = c.border_color
    assert v == ""


def test_iframe_border_width():
    # list of values
    c = IFrame(border_width=["1px", "2px", "1", "2"])
    v = c.border_width
    assert isinstance(v, List)
    assert len(v) == 4

    # single value
    c.border_width = "10"
    v = c.border_width
    assert isinstance(v, str)
    assert v == "10"

    # none
    c.border_width = None
    v = c.border_width
    assert v == ""


def test_iframe_border_width_mixed():
    # list of values
    c = IFrame(border_width=["1px", "2px", 1, 2])
    v = c.border_width
    assert isinstance(v, List)
    assert len(v) == 4


def test_iframe_border_radius():
    # list of values
    c = IFrame(border_radius=["1px", "2px", "1", "2"])
    v = c.border_radius
    assert isinstance(v, List)
    assert len(v) == 4

    # single value
    c.border_radius = "10"
    v = c.border_radius
    assert isinstance(v, str)
    assert v == "10"

    # none
    c.border_radius = None
    v = c.border_radius
    assert v == ""
