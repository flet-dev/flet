import flet as ft

name = """Checkbox with different properties"""


def example():
    checkbox = ft.Checkbox(
        label="Checkbox label",
        value=True,
        label_position=ft.LabelPosition.LEFT,
        label_style=ft.TextStyle(size=20),
        tristate=True,
        autofocus=True,
        fill_color={
            ft.ControlState.HOVERED: ft.Colors.GREEN,
            ft.ControlState.FOCUSED: ft.Colors.RED,
            ft.ControlState.DEFAULT: ft.Colors.BLACK,
        },
        overlay_color={
            ft.ControlState.HOVERED: ft.Colors.GREEN,
            ft.ControlState.FOCUSED: ft.Colors.RED,
            ft.ControlState.DEFAULT: ft.Colors.BLACK,
        },
        check_color=ft.Colors.GREEN_800,
        active_color=ft.Colors.GREEN_200,
        hover_color=ft.Colors.AMBER_300,
        focus_color=ft.Colors.RED_200,
        semantics_label="semantics label",
        shape=ft.RoundedRectangleBorder(10),
        splash_radius=5,
        border_side={
            # ft.ControlState.HOVERED: ft.BorderSide(
            #     5, color=ft.Colors.RED, stroke_align=ft.BorderSideStrokeAlign.OUTSIDE
            # ),
            ft.ControlState.FOCUSED: ft.BorderSide(
                5, color=ft.Colors.RED, stroke_align=10
            ),
            ft.ControlState.DEFAULT: ft.BorderSide(5),
        },
        is_error=True,
        visual_density=ft.VisualDensity.COMFORTABLE,
        mouse_cursor=ft.MouseCursor.CONTEXT_MENU,
        on_change=lambda e: print("Changed!"),
        on_blur=lambda e: print("Blurred!"),
        on_focus=lambda e: print("Focused!"),
        badge=ft.Badge(
            label="1", offset=ft.Offset(-15, -25), alignment=ft.Alignment(0, 0)
        ),
        expand=False,
        expand_loose=True,
        adaptive=False,
        width=50,
        height=50,
        opacity=0.5,
        tooltip=ft.Tooltip(message="ToolTip"),
    )

    return ft.Column(
        [
            checkbox,
        ]
    )
