import flet as ft


def main(page: ft.Page):
    page.padding = 0

    async def show_previous_page(e: ft.Event[ft.FloatingActionButton]):
        await view.previous_page(
            animation_curve=ft.AnimationCurve.BOUNCE_IN_OUT,
            animation_duration=ft.Duration(seconds=3),
        )

    async def show_next_page(e: ft.Event[ft.FloatingActionButton]):
        await view.next_page(
            animation_curve=ft.AnimationCurve.BOUNCE_IN_OUT,
            animation_duration=ft.Duration(seconds=3),
        )

    page.floating_action_button = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
        controls=[
            ft.FloatingActionButton(
                icon=ft.Icons.SWIPE_LEFT,
                on_click=show_previous_page,
                tooltip="Previous Page",
            ),
            ft.FloatingActionButton(
                icon=ft.Icons.SWIPE_RIGHT,
                on_click=show_next_page,
                tooltip="Next Page",
            ),
        ],
    )

    page.add(
        view := ft.PageView(
            expand=True,
            viewport_fraction=0.9,
            selected_index=1,
            horizontal=True,
            controls=[
                ft.Container(
                    bgcolor=bgcolor,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(f"Page {idx}", size=55, weight=ft.FontWeight.BOLD),
                        ],
                    ),
                )
                for idx, bgcolor in enumerate(
                    [
                        ft.Colors.RED_800,
                        ft.Colors.BLUE_800,
                        ft.Colors.GREEN_800,
                        ft.Colors.ORANGE_800,
                        ft.Colors.PURPLE_800,
                        ft.Colors.PINK_800,
                    ]
                )
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
