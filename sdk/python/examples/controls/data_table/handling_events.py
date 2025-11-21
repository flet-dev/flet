import flet as ft


def main(page: ft.Page):
    def handle_row_selection_change(e: ft.Event[ft.DataRow]):
        if e.control.data:
            if e.control.data == 1:
                row1.selected = not row1.selected
            elif e.control.data == 2:
                row2.selected = not row2.selected
            elif e.control.data == 3:
                row3.selected = not row3.selected
        page.update()

    def handle_column_sort(e: ft.DataColumnSortEvent):
        if e.control.data:
            if e.control.data == 1:
                print(f"{e.column_index}, {e.ascending}")
                # table.sort_column_index = 1
                table.sort_ascending = e.ascending
            elif e.control.data == 2:
                print(f"{e.column_index}, {e.ascending}")
                # table.sort_column_index = 2
                table.sort_ascending = e.ascending
        page.update()

    page.add(
        table := ft.DataTable(
            width=700,
            bgcolor=ft.Colors.TEAL_ACCENT_200,
            border=ft.Border.all(2, ft.Colors.RED_ACCENT_200),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE_600),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREEN_600),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.Colors.BLACK_12,
            heading_row_height=100,
            data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[
                ft.DataColumn(
                    label=ft.Text("Column 1"),
                    tooltip="This is the first column",
                    data=1,
                    on_sort=handle_column_sort,
                ),
                ft.DataColumn(
                    label=ft.Text("Column 2"),
                    tooltip="This is a second column",
                    numeric=True,
                    data=2,
                    on_sort=handle_column_sort,
                ),
            ],
            rows=[
                row1 := ft.DataRow(
                    cells=[ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                    selected=True,
                    on_select_change=handle_row_selection_change,
                    data=1,
                ),
                row2 := ft.DataRow(
                    cells=[ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
                    selected=False,
                    on_select_change=handle_row_selection_change,
                    data=2,
                ),
                row3 := ft.DataRow(
                    cells=[ft.DataCell(ft.Text("C")), ft.DataCell(ft.Text("3"))],
                    selected=False,
                    on_select_change=handle_row_selection_change,
                    data=3,
                ),
            ],
        )
    )


ft.run(main)
