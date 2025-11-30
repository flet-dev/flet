import flet as ft
import flet_datatable2 as fdt


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


if __name__ == "__main__":
    ft.run(main)
