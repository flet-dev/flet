import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="Range slider with divisions and labels",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=30),
                ft.RangeSlider(
                    min=0,
                    max=50,
                    start_value=10,
                    divisions=10,
                    end_value=20,
                    inactive_color=ft.Colors.GREEN_300,
                    active_color=ft.Colors.GREEN_700,
                    overlay_color=ft.Colors.GREEN_100,
                    label="{value}",
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
