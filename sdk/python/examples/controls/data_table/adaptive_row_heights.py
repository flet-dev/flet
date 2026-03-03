import flet as ft


def main(page: ft.Page):
    page.add(
        ft.DataTable(
            width=560,
            data_row_min_height=48,
            data_row_max_height=float("inf"),  # infinity to allow adaptive row heights
            columns=[
                ft.DataColumn(label="Description"),
                ft.DataColumn(label="Notes"),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell("TWO lines visible without overflow"),
                        ft.DataCell("Line 1\nLine 2"),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell("FOUR lines visible without overflow"),
                        ft.DataCell("Line 1\nLine 2\nLine 3\nLine 4"),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell("FIVE lines visible without overflow"),
                        ft.DataCell("Line 1\nLine 2\nLine 3\nLine 4\nLine 5"),
                    ],
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
