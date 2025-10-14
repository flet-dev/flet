import flet as ft
import flet_charts as fch


def main(page: ft.Page):
    page.title = "Radar chart"
    page.padding = 20
    page.vertical_alignment = page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.LIGHT

    categories = ["macOS", "Linux", "Windows"]

    page.add(
        fch.RadarChart(
            expand=True,
            titles=[fch.RadarChartTitle(text=label) for label in categories],
            center_min_value=True,
            radar_shape=fch.RadarShape.CIRCLE,
            tick_count=4,
            ticks_text_style=ft.TextStyle(size=20, color=ft.Colors.ON_SURFACE),
            title_text_style=ft.TextStyle(
                size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE
            ),
            on_event=lambda e: print(e.type),
            data_sets=[
                fch.RadarDataSet(
                    fill_color=ft.Colors.with_opacity(0.2, ft.Colors.DEEP_PURPLE),
                    border_color=ft.Colors.DEEP_PURPLE,
                    entry_radius=4,
                    entries=[
                        fch.RadarEntry(300),
                        fch.RadarEntry(50),
                        fch.RadarEntry(250),
                    ],
                ),
                fch.RadarDataSet(
                    fill_color=ft.Colors.with_opacity(0.15, ft.Colors.PINK),
                    border_color=ft.Colors.PINK,
                    entry_radius=4,
                    entries=[
                        fch.RadarEntry(250),
                        fch.RadarEntry(100),
                        fch.RadarEntry(200),
                    ],
                ),
                fch.RadarDataSet(
                    fill_color=ft.Colors.with_opacity(0.12, ft.Colors.CYAN),
                    border_color=ft.Colors.CYAN,
                    entry_radius=4,
                    entries=[
                        fch.RadarEntry(200),
                        fch.RadarEntry(150),
                        fch.RadarEntry(50),
                    ],
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
