import flet as ft

name = "Theme colors"


def example():
    class Color:
        def __init__(self, display_name, name, is_dark=False):
            self.name = name
            self.display_name = display_name
            self.is_dark = is_dark

    theme_colors = [
        Color("PRIMARY", "primary"),
        Color("ON_PRIMARY", "onprimary"),
        Color("PRIMARY_CONTAINER", "primarycontainer"),
        Color("ON_PRIMARY_CONTAINER", "onprimarycontainer", True),
        Color("SECONDARY", "secondary"),
        Color("ON_SECONDARY", "onsecondary"),
        Color("SECONDARY_CONTAINER", "secondarycontainer"),
        Color("ON_SECONDARY_CONTAINER", "onsecondarycontainer", True),
        Color("TERTIARY", "tertiary"),
        Color("ON_TERTIARY", "ontertiary"),
        Color("TERTIARY_CONTAINER", "tertiarycontainer"),
        Color("ON_TERTIARY_CONTAINER", "ontertiarycontainer", True),
        Color("ERROR", "error"),
        Color("ON_ERROR", "onerror"),
        Color("ERROR_CONTAINER", "errorcontainer"),
        Color("ON_ERROR_CONTAINER", "onerrorcontainer", True),
        Color("OUTLINE", "outline"),
        Color("OUTLINE_VARIANT", "outlinevariant", True),
        Color("BACKGROUND", "background"),
        Color("ON_BACKGROUND", "onbackground", True),
        Color("SURFACE_TINT", "surfacetint"),
        Color("ON_SURFACE_VARIANT", "onsurfacevariant", True),
        Color("INVERSE_SURFACE", "inversesurface", True),
        Color("ON_INVERSE_SURFACE", "oninversesurface"),
        Color("INVERSE_PRIMARY", "inverseprimary"),
        Color("SHADOW", "shadow", True),
        Color("SCRIM", "scrim", True),
    ]

    def copy_to_clipboard(e):
        e.control.page.set_clipboard(f"ft.Colors.{e.control.content.value}")
        e.control.page.open(
            ft.SnackBar(
                ft.Text(f"Copied to clipboard: ft.Colors.{e.control.content.value}"),
                open=True,
            )
        )

    theme_colors_column = ft.Column(spacing=0)

    theme_colors_column.controls = []

    for color in theme_colors:
        if color.is_dark:
            text_color = ft.Colors.SURFACE_TINT
        else:
            text_color = ft.Colors.ON_SURFACE_VARIANT

        theme_colors_column.controls.append(
            ft.Container(
                height=50,
                bgcolor=color.name,
                content=ft.Text(color.display_name, color=text_color),
                alignment=ft.Alignment.CENTER,
                on_click=copy_to_clipboard,
            )
        )

    return ft.Container(border_radius=10, content=theme_colors_column)
