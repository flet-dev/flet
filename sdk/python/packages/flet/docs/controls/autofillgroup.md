::: flet.AutofillGroup

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/autofillgroup)

### Basic example



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.AutofillGroup(
            ft.Column(
                controls=[
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
        )
    )

ft.run(main)
```



<img src="/img/docs/controls/autofillgroup/autofillgroup-example.gif" className="screenshot-40"/>
