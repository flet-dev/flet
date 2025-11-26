import flet as ft
import flet_rive as ftr


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


if __name__ == "__main__":
    ft.run(main)
