import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent ScaffoldPage"
    page.padding = 0

    photos = 4

    def add_photo(e: ft.Event[fluent.CommandBarButton]):
        nonlocal photos
        photos += 1
        status.value = f"{photos} photos"

    status = ft.Text("4 photos")

    page.add(
        fluent.ScaffoldPage(
            expand=True,
            header=fluent.PageHeader(
                title="Photos",
                command_bar=fluent.CommandBar(
                    alignment=ft.MainAxisAlignment.END,
                    primary_items=[
                        fluent.CommandBarButton(
                            icon=fluent.FluentIcons.ADD,
                            content="Import",
                            on_click=add_photo,
                        ),
                        fluent.CommandBarButton(
                            icon=fluent.FluentIcons.SHARE, content="Share"
                        ),
                    ],
                ),
            ),
            content=status,
        )
    )


if __name__ == "__main__":
    ft.run(main)
