import flet_core as ft
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Text()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["text"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_text_align_enum():
    r = ft.Text()
    assert r.text_align is None
    assert r._get_attr("textAlign") is None

    r = ft.Text(text_align=ft.TextAlign.RIGHT)
    assert isinstance(r.text_align, ft.TextAlign)
    assert r.text_align == ft.TextAlign.RIGHT
    assert r._get_attr("textAlign") == "right"

    r = ft.Text(text_align="left")
    assert isinstance(r.text_align, str)
    assert r._get_attr("textAlign") == "left"


def test_text_style_enum():
    r = ft.Text()
    assert r.style is None
    assert r._get_attr("style") is None

    r = ft.Text(style=ft.TextThemeStyle.DISPLAY_LARGE)
    assert isinstance(r.style, ft.TextThemeStyle)
    assert r.style == ft.TextThemeStyle.DISPLAY_LARGE
    assert r._get_attr("style") == "displayLarge"

    r = ft.Text(style="bodyMedium")
    assert isinstance(r.style, str)
    assert r._get_attr("style") == "bodyMedium"


def test_text_overflow_enum():
    r = ft.Text()
    assert r.overflow == ft.TextOverflow.NONE
    assert r._get_attr("overflow") is None

    r = ft.Text(overflow=ft.TextOverflow.ELLIPSIS)
    assert isinstance(r.overflow, ft.TextOverflow)
    assert r.overflow == ft.TextOverflow.ELLIPSIS
    assert r._get_attr("overflow") == "ellipsis"

    r = ft.Text(overflow="fade")
    assert isinstance(r.overflow, str)
    assert r._get_attr("overflow") == "fade"


def test_weight_enum():
    r = ft.Text()
    assert r.weight is None
    assert r._get_attr("weight") is None

    r = ft.Text(weight=ft.FontWeight.BOLD)
    assert isinstance(r.weight, ft.FontWeight)
    assert r.weight == ft.FontWeight.BOLD
    assert r._get_attr("weight") == "bold"

    r = ft.Text(weight="w100")
    assert isinstance(r.weight, str)
    assert r._get_attr("weight") == "w100"
