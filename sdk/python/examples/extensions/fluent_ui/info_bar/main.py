import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent InfoBar"

    def handle_close(e: ft.Event[fluent.InfoBar]):
        e.control.visible = False

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=500,
                controls=[
                    fluent.InfoBar(
                        title="Update available",
                        content="Restart the app to install it.",
                        action=fluent.Button("Restart"),
                    ),
                    fluent.InfoBar(
                        title="Saved",
                        content="Your changes were saved.",
                        severity=fluent.InfoBarSeverity.SUCCESS,
                        on_close=handle_close,
                    ),
                    fluent.InfoBar(
                        title="Low disk space",
                        content="Free some space to keep syncing.",
                        severity=fluent.InfoBarSeverity.WARNING,
                    ),
                    fluent.InfoBar(
                        title="Sync failed",
                        content="Check your connection and try again.",
                        severity=fluent.InfoBarSeverity.ERROR,
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
