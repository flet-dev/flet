import importlib
import sys
from pathlib import Path

import flet as ft


def _resolve_examples_root() -> tuple[Path, Path, str]:
    """
    Find examples/controls tree under sdk/python/examples.

    Falls back to the local controls folder if the repo path isn't available
    (e.g., packaged artifacts or custom layouts).
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "examples" / "controls"
        if candidate.is_dir():
            return parent, candidate, "examples.controls"

    fallback_root = here.parent
    return fallback_root, fallback_root / "controls", "controls"


PROJECT_PY_ROOT, EXAMPLES_ROOT, MODULE_PREFIX = _resolve_examples_root()
if str(PROJECT_PY_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PY_ROOT))


def discover_examples():
    controls: dict[str, list[dict[str, object]]] = {}
    for path in sorted(EXAMPLES_ROOT.rglob("*.py")):
        if path.name.startswith("_"):
            continue
        if any(
            part.startswith("__")
            or part == "media"
            or part in {"ads", "video", "webview"}
            for part in path.parts
        ):
            continue

        rel = path.relative_to(EXAMPLES_ROOT).with_suffix("")
        parts = rel.parts
        if len(parts) < 2:
            continue  # expect control_name/file.py

        control_name = "".join(word.title() for word in parts[0].split("_"))
        slug = "/".join(parts)
        module_name = f"{MODULE_PREFIX}." + ".".join(parts)

        try:
            mod = importlib.import_module(module_name)
        except Exception:
            continue

        runner = getattr(mod, "main", None)
        if runner is None:
            continue

        controls.setdefault(control_name, []).append({"slug": slug, "runner": runner})

    return controls


CONTROL_EXAMPLES = discover_examples()
EXAMPLES_BY_SLUG = {
    ex["slug"]: ex for group in CONTROL_EXAMPLES.values() for ex in group
}


def pretty_example_title(slug: str) -> str:
    parts = slug.split("/")
    if not parts:
        return slug

    def prettify(token: str) -> str:
        return " ".join(word.title() for word in token.replace("_", " ").split())

    rest = parts[1:]
    if not rest:
        return prettify(parts[0])

    # Direct file under control: just show the file name.
    if len(rest) == 1:
        return prettify(rest[0])

    # Subfolders: use the deepest group as the leading label.
    groups, leaf = rest[:-1], rest[-1]
    return f"{prettify(groups[-1])} / {prettify(leaf)}"


def main(page: ft.Page):
    page.title = "Flet Examples"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO
    search_ref: ft.Ref[ft.TextField] = ft.Ref()

    def open_example(slug: str):
        page.go(f"/{slug}")

    def filter_controls(query: str) -> dict[str, list[dict[str, object]]]:
        q = query.strip().lower()
        if not q:
            return CONTROL_EXAMPLES
        filtered: dict[str, list[dict[str, object]]] = {}
        for control_name, examples in CONTROL_EXAMPLES.items():
            matches = []
            for ex in examples:
                slug_match = q in ex["slug"].lower()
                title_match = q in pretty_example_title(ex["slug"]).lower()
                if slug_match or title_match or q in control_name.lower():
                    matches.append(ex)
            if matches:
                filtered[control_name] = matches
        return filtered

    def render_home():
        page.appbar = ft.AppBar(
            title=ft.Text("Flet examples", weight=ft.FontWeight.W_600),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            automatically_imply_leading=False,
        )
        page.clean()

        grid_view = ft.GridView(
            expand=1,
            runs_count=0,
            max_extent=420,
            spacing=12,
            run_spacing=12,
        )

        def update_controls():
            query = search_ref.current.value if search_ref.current else ""
            visible_controls = filter_controls(query or "")

            control_cards = []
            for control_name, examples in visible_controls.items():
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
                                        expand=True,
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            ft.ListTile(
                                                title=ft.Text(
                                                    value=pretty_example_title(
                                                        ex["slug"]
                                                    ),
                                                    weight=ft.FontWeight.W_600,
                                                ),
                                                subtitle=ft.Text(f"/{ex['slug']}"),
                                                on_click=lambda e,
                                                s=ex["slug"]: open_example(s),
                                                trailing=ft.Icon(
                                                    ft.Icons.CHEVRON_RIGHT
                                                ),
                                            )
                                            for ex in examples
                                        ],
                                    ),
                                ],
                            ),
                        ),
                    )
                )

            grid_view.controls = control_cards
            grid_view.update()

        page.add(
            ft.TextField(
                ref=search_ref,
                prefix_icon=ft.Icons.SEARCH,
                hint_text="Search controls or examples",
                on_change=lambda e: update_controls(),
                dense=True,
            ),
            ft.Divider(),
            ft.Text(
                "Open examples via tile click or route (e.g. /checkbox/basic).",
                theme_style=ft.TextThemeStyle.BODY_MEDIUM,
            ),
            ft.Divider(),
            grid_view,
        )
        update_controls()

    def reset_page():
        page.appbar = None
        page.clean()
        page.overlay.clear()
        page.pop_dialog()
        page.theme = page.dark_theme = page.floating_action_button = None
        page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    def render_example(slug: str):
        info = EXAMPLES_BY_SLUG.get(slug)
        if not info:
            page.go("/")
            return

        # Show only the example content.
        reset_page()
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
    ft.run(
        main,
        # route_url_strategy=ft.RouteUrlStrategy.HASH,
    )
