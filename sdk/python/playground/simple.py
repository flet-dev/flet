from datetime import datetime

import flet
from flet import Column, ElevatedButton, Icon, Page, Row, Stack, Text, Theme

# theme = Theme(color_scheme_seed="red300", brightness="light")
# j = json.dumps(theme, default=vars)
# logging.debug(f"theme_json: {j}")


def main(page: Page):
    page.title = "Simple Example"
    page.theme_mode = "light"
    page.padding = 50
    page.spacing = 30
    page.vertical_alignment = "start"
    page.horizontal_alignment = "center"
    # page.bgcolor = "cyanAccent2003"
    page.theme = Theme(color_scheme_seed="red300")
    page.dark_theme = Theme(color_scheme_seed="cyan")
    page.update()

    def on_click1(e):
        page.add(Text(f"Line {datetime.now()}"))

    def on_click2(e):
        # page.controls.pop()
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    page.add(
        Row(
            [
                Icon(name="favorite", size=24, color="pink"),
                Icon(name="audiotrack", size=30, color="green"),
                Icon(name="beach_access", size=36, color="blue"),
            ]
        ),
        Stack([Text("Text 1"), Text("sdfjsdf")]),
        Row([Text("This is a button:"), ElevatedButton("Button!")]),
        Column(
            [
                ElevatedButton("Click me!", on_click=on_click1),
                ElevatedButton("Remove last control", on_click=on_click2),
            ],
            alignment="center",
            horizontal_alignment="end",
            spacing=30,
        ),
    )


flet.app(target=main, view=flet.WEB_BROWSER)
