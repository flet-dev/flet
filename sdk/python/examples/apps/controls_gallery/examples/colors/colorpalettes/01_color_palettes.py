import flet as ft

name = "Color palettes"


def example():
    class ColorSwatch:
        def __init__(self, name, display_name, accent=True):
            self.name = name
            self.display_name = display_name
            self.accent = accent

    class Color:
        def __init__(self, swatch, shade="", accent=False):
            if shade == "":
                self.name = swatch.name
                self.display_name = swatch.display_name
            else:
                if not accent:
                    self.name = f"{swatch.name}{shade}"
                    self.display_name = f"{swatch.display_name}_{shade}"
                else:
                    self.name = f"{swatch.name}accent{shade}"
                    self.display_name = f"{swatch.display_name}_ACCENT_{shade}"

    SHADES = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900"]
    ACCENT_SHADES = ["100", "200", "400", "700"]
    WHITE_SHADES = ["10", "12", "24", "30", "38", "54", "70"]
    BLACK_SHADES = ["12", "26", "38", "45", "54", "87"]

    swatches = [
        ColorSwatch(name="red", display_name="RED"),
        ColorSwatch(name="pink", display_name="PINK"),
        ColorSwatch(name="purple", display_name="PURPLE"),
        ColorSwatch(name="deeppurple", display_name="DEEP_PURPLE"),
        ColorSwatch(name="indigo", display_name="INDIGO"),
        ColorSwatch(name="blue", display_name="BLUE"),
        ColorSwatch(name="lightblue", display_name="LIGHT_BLUE"),
        ColorSwatch(name="cyan", display_name="CYAN"),
        ColorSwatch(name="teal", display_name="TEAL"),
        ColorSwatch(name="green", display_name="GREEN"),
        ColorSwatch(name="lightgreen", display_name="LIGHT_GREEN"),
        ColorSwatch(name="lime", display_name="LIME"),
        ColorSwatch(name="yellow", display_name="YELLOW"),
        ColorSwatch(name="amber", display_name="AMBER"),
        ColorSwatch(name="orange", display_name="ORANGE"),
        ColorSwatch(name="deeporange", display_name="DEEP_ORANGE"),
        ColorSwatch(name="brown", display_name="BROWN", accent=False),
        ColorSwatch(name="grey", display_name="GREY", accent=False),
        ColorSwatch(name="bluegrey", display_name="BLUE_GREY", accent=False),
        ColorSwatch(name="white", display_name="WHITE"),
        ColorSwatch(name="black", display_name="BLACK"),
    ]

    def generate_color_names(swatch):
        colors = []
        base_color = Color(swatch=swatch)
        colors.append(base_color)
        if swatch.name == "white":
            for shade in WHITE_SHADES:
                color = Color(swatch=swatch, shade=shade)
                colors.append(color)
            return colors
        if swatch.name == "black":
            for shade in BLACK_SHADES:
                color = Color(swatch=swatch, shade=shade)
                colors.append(color)
            return colors
        for shade in SHADES:
            color = Color(swatch=swatch, shade=shade)
            colors.append(color)
        if swatch.accent:
            for shade in ACCENT_SHADES:
                color = Color(swatch=swatch, shade=shade, accent=True)
                colors.append(color)
        return colors

    responsive_row = ft.ResponsiveRow(
        run_spacing=10, vertical_alignment=ft.CrossAxisAlignment.START
    )

    responsive_row.controls = []

    def copy_to_clipboard(e):
        e.control.page.set_clipboard(f"ft.Colors.{e.control.content.value}")
        e.control.page.open(
            ft.SnackBar(
                ft.Text(f"Copied to clipboard: ft.Colors.{e.control.content.value}"),
                open=True,
            )
        )

    for swatch in swatches:
        swatch_colors = ft.Column(spacing=0, controls=[])
        responsive_row.controls.append(
            ft.Column(
                [ft.Container(border_radius=10, content=swatch_colors)],
                col={"sm": 6, "md": 4, "xl": 2},
            )
        )
        for color in generate_color_names(swatch):
            swatch_colors.controls.append(
                ft.Container(
                    height=50,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=color.name,
                    on_click=copy_to_clipboard,
                    content=ft.Text(color.display_name, weight=ft.FontWeight.W_500),
                )
            )

    return responsive_row
