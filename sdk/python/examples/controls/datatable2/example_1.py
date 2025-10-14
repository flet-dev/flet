import flet_datatable2 as fdt

import flet as ft


def main(page: ft.Page):
    page.add(
        fdt.DataTable2(
            empty=ft.Text("This table is empty."),
            columns=[
                fdt.DataColumn2(label=ft.Text("First name")),
                fdt.DataColumn2(label=ft.Text("Last name")),
                fdt.DataColumn2(label=ft.Text("Age"), numeric=True),
            ],
        ),
    )


ft.run(main)
