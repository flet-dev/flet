import flet as ft
import flet_webview as fwv


def main(page: ft.Page):
    page.add(
        fwv.WebView(
            url="https://flet.dev",
            on_page_started=lambda _: print("Page started"),
            on_page_ended=lambda _: print("Page ended"),
            on_web_resource_error=lambda e: print("WebView error:", e.data),
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
