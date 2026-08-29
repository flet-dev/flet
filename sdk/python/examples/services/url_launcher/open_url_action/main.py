import flet as ft


def main(page: ft.Page):
    # `action` is performed by the client while it is still handling the click,
    # so opening a new tab is not treated as an unsolicited popup. Compare with
    # `UrlLauncher().launch_url()`, which has to reach Python first and is
    # therefore blocked by Safari on iOS.
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text("Both buttons open the same page:"),
                    ft.Button(
                        "Open in this tab",
                        action=ft.OpenUrl("https://flet.dev", target=ft.UrlTarget.SELF),
                    ),
                    ft.Button(
                        "Open in a new tab",
                        action=ft.OpenUrl(
                            "https://flet.dev",
                            target=ft.UrlTarget.BLANK,
                        ),
                    ),
                    ft.Text(
                        "An action can be combined with on_click - the action "
                        "runs on the client, then your handler runs in Python."
                    ),
                    ft.Button(
                        "Open and log",
                        action=ft.OpenUrl("https://flet.dev/docs"),
                        on_click=lambda e: page.show_dialog(
                            ft.SnackBar(ft.Text("Docs opened"))
                        ),
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
