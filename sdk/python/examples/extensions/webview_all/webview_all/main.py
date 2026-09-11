import flet as ft
import flet_webview_all as fwa


def main(page: ft.Page):
    page.add(
        fwa.FletWebviewAll(
            url="https://flet.dev",
            expand=True,
            on_page_started=lambda e: print(f"Loading: {e.url}"),
            on_page_finished=lambda e: print(f"Loaded: {e.url}"),
        )
    )


if __name__ == "__main__":
    ft.run(main)
