import sys
from pathlib import Path

import flet as ft

# Ensure the repo's Python root (sdk/python) is on sys.path so `examples.*` imports work
PROJECT_PY_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_PY_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PY_ROOT))

from examples.controls.button import basic as button_basic
from examples.controls.button import custom_content, handling_clicks, icons
from examples.controls.checkbox import basic as checkbox_basic
from examples.controls.checkbox import handling_events, styled

CONTROL_EXAMPLES = {
    "Checkbox": [
        {
            "slug": "checkbox/basic",
            "runner": checkbox_basic.main,
        },
        {
            "slug": "checkbox/handling_events",
            "runner": handling_events.main,
        },
        {
            "slug": "checkbox/styled",
            "runner": styled.main,
        },
    ],
    "Button": [
        {
            "slug": "button/basic",
            "runner": button_basic.main,
        },
        {
            "slug": "button/icons",
            "runner": icons.main,
        },
        {
            "slug": "button/custom_content",
            "runner": custom_content.main,
        },
        {
            "slug": "button/handling_clicks",
            "runner": handling_clicks.main,
        },
    ],
}

EXAMPLES_BY_SLUG = {
    ex["slug"]: ex for group in CONTROL_EXAMPLES.values() for ex in group
}


def main(page: ft.Page):
    page.title = "Examples POC"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO

    def open_example(slug: str):
        page.go(f"/{slug}")

    def render_home():
        page.appbar = ft.AppBar(
            title=ft.Text("Flet examples", weight=ft.FontWeight.W_600),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            automatically_imply_leading=False,
        )
        page.clean()

        control_cards = []
        for control_name, examples in CONTROL_EXAMPLES.items():
            control_cards.append(
                ft.Card(
                    elevation=2,
                    content=ft.Container(
                        padding=12,
                        content=ft.Column(
                            spacing=8,
                            controls=[
                                ft.Text(
                                    value=control_name,
                                    theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                    weight=ft.FontWeight.W_600,
                                ),
                                ft.ListView(
                                    spacing=4,
                                    height=None,
                                    controls=[
                                        ft.ListTile(
                                            title=ft.Text(
                                                ex["slug"]
                                                .split("/")[-1]
                                                .replace("_", " ")
                                                .title(),
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            subtitle=ft.Text(f"/{ex['slug']}"),
                                            on_click=lambda e,
                                            s=ex["slug"]: open_example(s),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                                        )
                                        for ex in examples
                                    ],
                                ),
                            ],
                        ),
                    ),
                )
            )

        page.add(
            ft.Text(
                "Open examples via tile click or route (e.g. /checkbox/basic).",
                theme_style=ft.TextThemeStyle.BODY_MEDIUM,
            ),
            ft.Divider(),
            ft.GridView(
                expand=1,
                runs_count=0,
                max_extent=420,
                spacing=12,
                run_spacing=12,
                controls=control_cards,
            ),
        )

    def prepare_page():
        page.appbar = None
        page.clean()
        page.overlay.clear()
        page.floating_action_button = None

    def render_example(slug: str):
        info = EXAMPLES_BY_SLUG.get(slug)
        if not info:
            page.go("/")
            return

        # Show only the example content.
        prepare_page()
        info["runner"](page)
        page.update()

    def handle_route_change(e=None):
        route = page.route.lstrip("/")
        if route == "":
            render_home()
        elif route in EXAMPLES_BY_SLUG:
            render_example(route)
        else:
            page.go("/")

    page.on_route_change = handle_route_change
    handle_route_change()


if __name__ == "__main__":
    ft.run(main)
