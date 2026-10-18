import flet_shadcn_ui as shad

import flet as ft

INVOICES = [
    ("INV001", "Paid", "Credit Card", 250.00),
    ("INV002", "Pending", "PayPal", 150.00),
    ("INV003", "Unpaid", "Bank Transfer", 350.00),
    ("INV004", "Paid", "Credit Card", 450.00),
    ("INV005", "Paid", "PayPal", 550.00),
    ("INV006", "Pending", "Bank Transfer", 200.00),
    ("INV007", "Unpaid", "Credit Card", 300.00),
]


def main(page: ft.Page):
    page.title = "Shadcn Table"

    def handle_row_click(e: ft.Event[shad.Table]):
        invoice, status, method, amount = INVOICES[e.data]
        selection.value = f"{invoice}: {status}, ${amount:.2f} by {method}"

    right = ft.Alignment.CENTER_RIGHT
    selection = ft.Text("Click a row")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=560,
                spacing=16,
                controls=[
                    shad.Table(
                        on_row_click=handle_row_click,
                        columns=[
                            shad.TableColumn("Invoice"),
                            shad.TableColumn("Status"),
                            shad.TableColumn("Method", fill=True),
                            shad.TableColumn("Amount", width=120, alignment=right),
                        ],
                        rows=[
                            shad.TableRow(
                                cells=[
                                    shad.TableCell(
                                        ft.Text(invoice, weight=ft.FontWeight.W_500)
                                    ),
                                    shad.TableCell(status),
                                    shad.TableCell(method),
                                    shad.TableCell(f"${amount:.2f}"),
                                ]
                            )
                            for invoice, status, method, amount in INVOICES
                        ],
                        footer=[
                            shad.TableCell("Total"),
                            shad.TableCell(""),
                            shad.TableCell(""),
                            shad.TableCell(f"${sum(i[3] for i in INVOICES):,.2f}"),
                        ],
                    ),
                    selection,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
