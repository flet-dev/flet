from dataclasses import dataclass

import flet as ft
import flet_datatable2 as ftd


@dataclass
class Dessert:
    name: str
    calories: float
    fat: float
    carbs: float
    protein: float
    sodium: float
    calcium: float
    iron: float


desserts = [
    Dessert("Frozen Yogurt", 159, 6.0, 24, 4.0, 87, 14, 1),
    Dessert("Ice Cream Sandwich", 237, 9.0, 37, 4.3, 129, 8, 1),
    Dessert("Eclair", 262, 16.0, 24, 6.0, 337, 6, 7),
    Dessert("Cupcake", 305, 3.7, 67, 4.3, 413, 3, 8),
    Dessert("Gingerbread", 356, 16.0, 49, 3.9, 327, 7, 16),
    Dessert("Jelly Bean", 375, 0.0, 94, 0.0, 50, 0, 0),
    Dessert("Lollipop", 392, 0.2, 98, 0.0, 38, 0, 2),
    Dessert("Honeycomb", 408, 3.2, 87, 6.5, 562, 0, 45),
    Dessert("Donut", 452, 25.0, 51, 4.9, 326, 2, 22),
    Dessert("Apple Pie", 518, 26.0, 65, 7.0, 54, 12, 6),
    Dessert("Frozen Yougurt with sugar", 168, 6.0, 26, 4.0, 87, 14, 1),
    Dessert("Ice Cream Sandwich with sugar", 246, 9.0, 39, 4.3, 129, 8, 1),
    Dessert("Eclair with sugar", 271, 16.0, 26, 6.0, 337, 6, 7),
    Dessert("Cupcake with sugar", 314, 3.7, 69, 4.3, 413, 3, 8),
    Dessert("Gingerbread with sugar", 345, 16.0, 51, 3.9, 327, 7, 16),
    Dessert("Jelly Bean with sugar", 364, 0.0, 96, 0.0, 50, 0, 0),
    Dessert("Lollipop with sugar", 401, 0.2, 100, 0.0, 38, 0, 2),
    Dessert("Honeycomb with sugar", 417, 3.2, 89, 6.5, 562, 0, 45),
    Dessert("Donut with sugar", 461, 25.0, 53, 4.9, 326, 2, 22),
    Dessert("Apple pie with sugar", 527, 26.0, 67, 7.0, 54, 12, 6),
    Dessert("Frozen yougurt with honey", 223, 6.0, 36, 4.0, 87, 14, 1),
    Dessert("Ice Cream Sandwich with honey", 301, 9.0, 49, 4.3, 129, 8, 1),
    Dessert("Eclair with honey", 326, 16.0, 36, 6.0, 337, 6, 7),
    Dessert("Cupcake with honey", 369, 3.7, 79, 4.3, 413, 3, 8),
    Dessert("Gingerbread with honey", 420, 16.0, 61, 3.9, 327, 7, 16),
    Dessert("Jelly Bean with honey", 439, 0.0, 106, 0.0, 50, 0, 0),
    Dessert("Lollipop with honey", 456, 0.2, 110, 0.0, 38, 0, 2),
    Dessert("Honeycomb with honey", 472, 3.2, 99, 6.5, 562, 0, 45),
    Dessert("Donut with honey", 516, 25.0, 63, 4.9, 326, 2, 22),
    Dessert("Apple pie with honey", 582, 26.0, 77, 7.0, 54, 12, 6),
]


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_row_selection_change(e: ft.Event[ftd.DataRow2]):
        e.control.selected = not e.control.selected
        e.control.update()

    def sort_column(e: ft.DataColumnSortEvent):
        sorters = [
            lambda d: d.name.lower(),
            lambda d: d.calories,
            lambda d: d.fat,
            lambda d: d.carbs,
            lambda d: d.protein,
            lambda d: d.sodium,
            lambda d: d.calcium,
            lambda d: d.iron,
        ]

        table.rows = get_data_rows(
            sorted(desserts, key=sorters[e.column_index], reverse=not e.ascending)
        )
        table.sort_column_index = e.column_index
        table.sort_ascending = e.ascending
        table.update()

    def get_data_rows(data: list[Dessert]) -> list[ftd.DataRow2]:
        rows = []
        for dessert in data:
            rows.append(
                ftd.DataRow2(
                    specific_row_height=50,
                    on_select_change=handle_row_selection_change,
                    cells=[
                        ft.DataCell(content=str(dessert.name)),
                        ft.DataCell(content=str(dessert.calories)),
                        ft.DataCell(content=str(dessert.fat)),
                        ft.DataCell(content=str(dessert.carbs)),
                        ft.DataCell(content=str(dessert.protein)),
                        ft.DataCell(content=str(dessert.sodium)),
                        ft.DataCell(content=str(dessert.calcium)),
                        ft.DataCell(content=str(dessert.iron)),
                    ],
                )
            )
        return rows

    page.add(
        table := ftd.DataTable2(
            show_checkbox_column=True,
            expand=True,
            column_spacing=0,
            heading_row_color=ft.Colors.SECONDARY_CONTAINER,
            horizontal_margin=12,
            sort_ascending=True,
            bottom_margin=10,
            min_width=600,
            on_select_all=lambda e: print("All selected"),
            rows=get_data_rows(desserts),
            columns=[
                ftd.DataColumn2(
                    label="Name",
                    size=ftd.DataColumnSize.L,
                    on_sort=sort_column,
                    heading_row_alignment=ft.MainAxisAlignment.START,
                ),
                ftd.DataColumn2(
                    label="Calories",
                    on_sort=sort_column,
                    numeric=True,
                    heading_row_alignment=ft.MainAxisAlignment.END,
                ),
                ftd.DataColumn2(label="Fat", numeric=True, on_sort=sort_column),
                ftd.DataColumn2(label="Carbs", numeric=True, on_sort=sort_column),
                ftd.DataColumn2(label="Protein", numeric=True, on_sort=sort_column),
                ftd.DataColumn2(label="Sodium", numeric=True, on_sort=sort_column),
                ftd.DataColumn2(label="Calcium", numeric=True, on_sort=sort_column),
                ftd.DataColumn2(label="Iron", numeric=True, on_sort=sort_column),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
