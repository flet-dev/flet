import asyncio

import flet as ft


async def main(page: ft.Page):
    determinate_bar = ft.ProgressBar(width=400)
    determinate_message = ft.Text("Doing something...")

    page.add(
        ft.Text(
            value="Linear progress indicator",
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
        ),
        ft.Column(controls=[determinate_message, determinate_bar]),
        ft.Text(
            value="Indeterminate progress bar",
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
        ),
        ft.ProgressBar(width=400, color=ft.Colors.AMBER),
    )

    for i in range(0, 101):
        determinate_bar.value = i * 0.01
        await asyncio.sleep(0.1)
        if i == 100:
            determinate_message.value = "Finished!"
        page.update()


ft.run(main)
