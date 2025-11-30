import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Container(
            alignment=ft.Alignment.CENTER,
            width=150,
            height=150,
            border_radius=ft.BorderRadius.all(5),
            gradient=ft.RadialGradient(
                center=ft.Alignment(0.7, -0.6),
                radius=0.2,
                colors=["0xFFFFFF00", "0xFF0099FF"],
                stops=[0.4, 1.0],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
