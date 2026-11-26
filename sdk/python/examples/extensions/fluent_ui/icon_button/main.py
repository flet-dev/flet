import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent IconButton"

    def toggle_favorite(e: ft.Event[fluent.IconButton]):
        favorite = e.control.icon == fluent.FluentIcons.STAR
        e.control.icon = (
            fluent.FluentIcons.STAR_FILLED if favorite else fluent.FluentIcons.STAR
        )
        status.value = "Added to favorites" if favorite else "Removed from favorites"

    def share(e: ft.Event[fluent.IconButton]):
        status.value = "Link copied"

    status = ft.Text()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            fluent.IconButton(
                                fluent.FluentIcons.STAR,
                                key="favorite",
                                tooltip="Favorite",
                                on_click=toggle_favorite,
                            ),
                            fluent.IconButton(
                                fluent.FluentIcons.SHARE,
                                tooltip="Share",
                                on_click=share,
                            ),
                            fluent.IconButton(
                                fluent.FluentIcons.DELETE,
                                tooltip="Delete",
                                disabled=True,
                            ),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
