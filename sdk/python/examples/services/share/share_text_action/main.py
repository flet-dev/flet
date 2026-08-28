import flet as ft


def main(page: ft.Page):
    # `action` is performed by the client while it is still handling the click.
    # Browsers only open the share sheet during a gesture, so `Share()` called
    # from Python has no effect on the web.
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text("Share this page with someone:"),
                    ft.Button(
                        "Share",
                        icon=ft.Icons.SHARE,
                        action=ft.ShareText(
                            "Flet lets you build multi-platform apps in Python: "
                            "https://flet.dev",
                            subject="Flet",
                        ),
                    ),
                    ft.Text(
                        "The share sheet is a system dialog - what it offers "
                        "depends on the platform, and on desktop browsers it "
                        "may not be available at all."
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
