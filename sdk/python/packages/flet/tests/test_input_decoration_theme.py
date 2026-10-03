import flet as ft
from flet.controls.base_control import BaseControl
from flet.messaging.protocol import configure_encode_object_for_msgpack

encode = configure_encode_object_for_msgpack(BaseControl)


def _deep(value):
    """Encode nested values the way msgpack would, one level at a time."""
    if isinstance(value, dict):
        return {k: _deep(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_deep(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return _deep(encode(value))


def _encoded_theme(theme: ft.Theme) -> dict:
    return _deep(theme)


def test_input_decoration_theme_single_border_is_encoded():
    theme = _encoded_theme(
        ft.Theme(
            input_decoration_theme=ft.InputDecorationTheme(
                border=ft.OutlineInputBorder(
                    border_radius=8, side=ft.BorderSide(color=ft.Colors.RED)
                ),
                label_style=ft.TextStyle(size=14),
                dense=True,
            )
        )
    )
    idt = theme["input_decoration_theme"]
    assert idt["border"]["_type"] == "outline"
    assert idt["border"]["border_radius"] == 8
    assert idt["border"]["side"]["color"] == ft.Colors.RED
    assert idt["label_style"]["size"] == 14
    assert idt["dense"] is True


def test_input_decoration_theme_state_borders_are_encoded_by_state():
    theme = _encoded_theme(
        ft.Theme(
            input_decoration_theme=ft.InputDecorationTheme(
                border={
                    ft.ControlState.DEFAULT: ft.OutlineInputBorder(),
                    ft.ControlState.HOVERED: ft.OutlineInputBorder(
                        side=ft.BorderSide(color=ft.Colors.BLUE)
                    ),
                }
            )
        )
    )
    # Keys go over the wire as the states' values ("default", "hovered").
    border = {k.value: v for k, v in theme["input_decoration_theme"]["border"].items()}
    assert set(border) == {"default", "hovered"}
    assert border["hovered"]["side"]["color"] == ft.Colors.BLUE


def test_text_field_theme_is_encoded():
    theme = _encoded_theme(
        ft.Theme(text_field_theme=ft.TextFieldTheme(text_style=ft.TextStyle(size=14)))
    )
    assert theme["text_field_theme"]["text_style"]["size"] == 14


def test_unset_themes_are_not_sent():
    theme = _encoded_theme(ft.Theme())
    assert "input_decoration_theme" not in theme
    assert "text_field_theme" not in theme
