import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Tooltip"

    page.add(
        ft.SafeArea(
            content=ft.Row(
                controls=[
                    fluent.Tooltip(
                        message="Save the document",
                        content=fluent.IconButton(fluent.FluentIcons.SAVE),
                    ),
                    fluent.Tooltip(
                        message="Print the document",
                        content=fluent.IconButton(fluent.FluentIcons.PRINT),
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
