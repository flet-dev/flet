import flet as ft

name = """AutofillGroup example"""


def example():
    return ft.Column(
        [
            ft.TextField(
                label="Name",
                autofill_hints=ft.AutofillHint.NAME,
            ),
            ft.TextField(
                label="Email",
                autofill_hints=[ft.AutofillHint.EMAIL],
            ),
            ft.TextField(
                label="Phone Number",
                autofill_hints=[ft.AutofillHint.TELEPHONE_NUMBER],
            ),
            ft.TextField(
                label="Street Address",
                autofill_hints=ft.AutofillHint.FULL_STREET_ADDRESS,
            ),
            ft.TextField(
                label="Postal Code",
                autofill_hints=ft.AutofillHint.POSTAL_CODE,
            ),
        ]
    )
