import flet as ft


def main(page: ft.Page):
    # Source data for the table (your domain objects). Each record has a stable `id`
    # so we can track selection even when the table is sorted or rebuilt.
    inventory_items = [
        {"id": 1, "name": "Alpha", "qty": 4},
        {"id": 2, "name": "Bravo", "qty": 9},
        {"id": 3, "name": "Charlie", "qty": 2},
        {"id": 4, "name": "Delta", "qty": 6},
        {"id": 5, "name": "Echo", "qty": 3},
        {"id": 6, "name": "Foxtrot", "qty": 8},
        {"id": 7, "name": "Golf", "qty": 1},
        {"id": 8, "name": "Hotel", "qty": 7},
        {"id": 9, "name": "India", "qty": 5},
        {"id": 10, "name": "Juliet", "qty": 10},
    ]

    # Working list used for sorting/reordering. We keep it separate so the original
    # input remains untouched (useful if you later reload or re-filter data).
    displayed_items = list(inventory_items)

    # Store selected item ids (not row indices) so selection survives sorting.
    selected_item_ids: set[int] = {1, 3, 5}

    # Map column index -> callable used for sorting that column.
    # Note: DataColumnSortEvent provides a `column_index` and an `ascending` flag.
    sort_key_for_column = {
        0: lambda item: str(item["name"]).lower(),  # "Item" column
        1: lambda item: int(item["qty"]),  # "Quantity" column
    }

    def build_rows(items: list[dict[str, int | str]]) -> list[ft.DataRow]:
        """Convert a list of item dicts into DataRow objects."""
        return [
            ft.DataRow(
                selected=item["id"] in selected_item_ids,
                on_select_change=handle_row_selection_change,
                data=item["id"],  # used by event handlers to identify this item
                cells=[
                    ft.DataCell(ft.Text(item["name"])),
                    ft.DataCell(ft.Text(str(item["qty"]))),
                ],
            )
            for item in items
        ]

    def refresh_table_rows():
        """
        Rebuild and redraw the table rows.

        Rebuilding rows is the simplest way to keep selection checkboxes and row
        visuals consistent after a bulk change (sort, select-all, clear selection).
        """
        table.rows = build_rows(displayed_items)
        table.update()

    def handle_row_selection_change(e: ft.Event[ft.DataRow]):
        """Called when a single row's checkbox is toggled."""
        row = e.control
        item_id = row.data
        is_selected = e.data  # new selected state

        if is_selected:
            selected_item_ids.add(item_id)
        else:
            selected_item_ids.discard(item_id)

        # Reflect the new state immediately on the toggled row.
        e.control.selected = is_selected
        e.control.update()

    def handle_select_all(e: ft.Event[ft.DataTable]):
        """
        Called when the header "select all" checkbox is toggled.

        `e.data` is True when selecting all, False when clearing.
        """
        select_all = e.data

        if select_all:
            selected_item_ids.update(int(item["id"]) for item in displayed_items)
        else:
            selected_item_ids.clear()

        refresh_table_rows()

    def handle_column_sort(e: ft.DataColumnSortEvent):
        """
        Called when a column header is clicked to sort.

        We sort `displayed_items` in-place and then refresh the rows. Selection is
        preserved because it is tracked by item id in `selected_item_ids`.
        """
        displayed_items.sort(
            key=sort_key_for_column[e.column_index],
            reverse=not e.ascending,
        )

        # Let the Table know which column is currently sorted and in what order.
        table.sort_column_index = e.column_index
        table.sort_ascending = e.ascending

        refresh_table_rows()

    page.add(
        table := ft.DataTable(
            width=700,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            heading_row_height=100,
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(
                    0.08, ft.Colors.PRIMARY
                ),
                ft.ControlState.SELECTED: ft.Colors.with_opacity(
                    0.14, ft.Colors.PRIMARY
                ),
            },
            show_checkbox_column=True,
            on_select_all=handle_select_all,
            divider_thickness=1,
            column_spacing=200,
            columns=[
                ft.DataColumn(
                    label=ft.Text("Item"),
                    on_sort=handle_column_sort,
                ),
                ft.DataColumn(
                    label=ft.Text("Quantity"),
                    tooltip="Numeric quantity",
                    numeric=True,
                    on_sort=handle_column_sort,
                ),
            ],
            rows=build_rows(displayed_items),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
