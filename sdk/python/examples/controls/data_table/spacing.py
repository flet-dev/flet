import flet as ft


def _cell(label: str, color: str = ft.Colors.SURFACE_CONTAINER_HIGHEST) -> ft.DataCell:
    return ft.DataCell(
        ft.Container(
            content=ft.Text(label, size=12, weight=ft.FontWeight.W_600),
            width=90,
            height=32,
            alignment=ft.Alignment.CENTER,
            bgcolor=color,
            border=ft.Border.all(1, ft.Colors.BLACK_26),
        )
    )


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    def update_spacing(e: ft.Event[ft.Slider] = None):
        table.horizontal_margin = horizontal_margin_slider.value
        table.column_spacing = column_spacing_slider.value
        page.update()

    def set_preset(horizontal_margin: float, column_spacing: float):
        horizontal_margin_slider.value = horizontal_margin
        column_spacing_slider.value = column_spacing
        update_spacing()

    page.appbar = ft.AppBar(title="DataTable spacing")
    page.add(
        ft.Container(
            width=520,
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("horizontal_margin (outer edges)"),
                    horizontal_margin_slider := ft.Slider(
                        min=0,
                        max=40,
                        divisions=40,
                        value=16,
                        label="{value}",
                        on_change=update_spacing,
                    ),
                    ft.Text("column_spacing (between columns)"),
                    column_spacing_slider := ft.Slider(
                        min=0,
                        max=40,
                        divisions=40,
                        value=16,
                        label="{value}",
                        on_change=update_spacing,
                    ),
                    ft.Row(
                        wrap=True,
                        controls=[
                            ft.FilledButton(
                                "Reset",
                                on_click=lambda _: set_preset(16, 16),
                            ),
                            ft.OutlinedButton(
                                "Compact preset",
                                on_click=lambda _: set_preset(0, 0),
                            ),
                            ft.OutlinedButton(
                                "Spacious preset",
                                on_click=lambda _: set_preset(24, 32),
                            ),
                        ],
                    ),
                ],
            ),
        ),
        table := ft.DataTable(
            border=ft.Border.all(1, ft.Colors.ON_SURFACE_VARIANT),
            horizontal_margin=horizontal_margin_slider.value,
            column_spacing=column_spacing_slider.value,
            horizontal_lines=ft.BorderSide(1, ft.Colors.ON_SURFACE_VARIANT),
            vertical_lines=ft.BorderSide(1, ft.Colors.ON_SURFACE_VARIANT),
            heading_row_height=40,
            data_row_min_height=40,
            data_row_max_height=40,
            columns=[
                ft.DataColumn(label="Col A"),
                ft.DataColumn(label="Col B"),
                ft.DataColumn(label="Col C"),
            ],
            rows=[
                ft.DataRow(
                    cells=[_cell("A1"), _cell("B1"), _cell("C1")],
                ),
                ft.DataRow(
                    cells=[_cell("A2"), _cell("B2"), _cell("C2")],
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
