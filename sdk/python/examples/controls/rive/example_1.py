import flet_rive as ftr

import flet as ft


def main(page: ft.Page):
    page.add(
        ftr.Rive(
            src="https://cdn.rive.app/animations/vehicles.riv",
            placeholder=ft.ProgressBar(),
            width=300,
            height=200,
        ),
        ftr.Rive(
            src="vehicles.riv",
            placeholder=ft.ProgressBar(),
            width=300,
            height=200,
        ),
    )


ft.run(main)
