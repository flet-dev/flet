from data import desserts

import flet as ft
import flet_datatable2 as ftd


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    sorted_desserts = list(desserts)
    data_table: ftd.DataTable2 | None = None

    def handle_row_selection_change(e: ft.Event[ftd.DataRow2]):
        e.control.selected = not e.control.selected
        e.control.update()

    def sort_column(e: ft.DataColumnSortEvent):
        if data_table is None:
            return
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
        sorted_desserts.sort(key=sorters[e.column_index], reverse=not e.ascending)
        data_table.rows = get_data_rows(sorted_desserts)
        data_table.sort_column_index = e.column_index
        data_table.sort_ascending = e.ascending
        data_table.update()

    def get_data_columns():
        data_columns = [
            ftd.DataColumn2(
                label=ft.Text("Name"),
                size=ftd.DataColumnSize.L,
                on_sort=sort_column,
                heading_row_alignment=ft.MainAxisAlignment.START,
            ),
            ftd.DataColumn2(
                label=ft.Text("Calories"),
                on_sort=sort_column,
                numeric=True,
                heading_row_alignment=ft.MainAxisAlignment.END,
            ),
            ftd.DataColumn2(
                label=ft.Text("Fat"),
                on_sort=sort_column,
                numeric=True,
            ),
            ftd.DataColumn2(
                label=ft.Text("Carbs"),
                on_sort=sort_column,
                numeric=True,
            ),
            ftd.DataColumn2(
                label=ft.Text("Protein"),
                on_sort=sort_column,
                numeric=True,
            ),
            ftd.DataColumn2(
                label=ft.Text("Sodium"),
                on_sort=sort_column,
                numeric=True,
            ),
            ftd.DataColumn2(
                label=ft.Text("Calcium"),
                on_sort=sort_column,
                numeric=True,
            ),
            ftd.DataColumn2(
                label=ft.Text("Iron"),
                on_sort=sort_column,
                numeric=True,
            ),
        ]
        return data_columns

    def get_data_rows(desserts):
        data_rows = []
        for dessert in desserts:
            data_rows.append(
                ftd.DataRow2(
                    specific_row_height=50,
                    on_select_change=handle_row_selection_change,
                    cells=[
                        ft.DataCell(content=ft.Text(dessert.name)),
                        ft.DataCell(content=ft.Text(dessert.calories)),
                        ft.DataCell(content=ft.Text(dessert.fat)),
                        ft.DataCell(content=ft.Text(dessert.carbs)),
                        ft.DataCell(content=ft.Text(dessert.protein)),
                        ft.DataCell(content=ft.Text(dessert.sodium)),
                        ft.DataCell(content=ft.Text(dessert.calcium)),
                        ft.DataCell(content=ft.Text(dessert.iron)),
                    ],
                )
            )
        return data_rows

    data_table = ftd.DataTable2(
        show_checkbox_column=True,
        expand=True,
        column_spacing=0,
        heading_row_color=ft.Colors.SECONDARY_CONTAINER,
        horizontal_margin=12,
        sort_ascending=True,
        bottom_margin=10,
        min_width=600,
        on_select_all=lambda e: print("All selected"),
        columns=get_data_columns(),
        rows=get_data_rows(sorted_desserts),
    )
    page.add(data_table)


if __name__ == "__main__":
    ft.run(main)
