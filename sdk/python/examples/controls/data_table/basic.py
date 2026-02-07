import flet as ft


def main(page: ft.Page):
    page.add(
        ft.DataTable(
            expand=True,
            columns=[
                ft.DataColumn(label=ft.Text("First name")),
                ft.DataColumn(label=ft.Text("Last name")),
                ft.DataColumn(label=ft.Text("Age"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("43")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Jack")),
                        ft.DataCell(ft.Text("Brown")),
                        ft.DataCell(ft.Text("19")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("25")),
                    ],
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
