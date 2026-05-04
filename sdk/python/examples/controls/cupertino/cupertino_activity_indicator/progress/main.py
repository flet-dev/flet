import flet as ft


async def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 20

    indicator = ft.CupertinoActivityIndicator(progress=1.0, radius=40)

    def handle_progress_change(e: ft.Event[ft.Slider]):
        indicator.progress = e.control.value

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    indicator,
                    ft.Slider(
                        min=0.0,
                        value=indicator.progress,
                        max=1.0,
                        divisions=10,
                        round=1,
                        label="Progress = {value}",
                        width=400,
                        on_change=handle_progress_change,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
