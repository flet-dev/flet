import flet as ft


def example(page):
    gender = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="female", label="Female"),
                ft.Radio(value="male", label="Male"),
                ft.Radio(value="not_specified", label="Not specified"),
            ]
        )
    )

    choice_of_instrument = ft.Dropdown(
        label="Choice of instrument",
        options=[
            ft.dropdown.Option("Piano"),
            ft.dropdown.Option("Violin"),
            ft.dropdown.Option("Guitar"),
        ],
    )

    monday = ft.Checkbox(label="Monday", value=False)
    tuesday = ft.Checkbox(label="Tuesday", value=False)
    wednesday = ft.Checkbox(label="Wednesday", value=False)
    thursday = ft.Checkbox(label="Thursday", value=False)
    friday = ft.Checkbox(label="Friday", value=False)
    saturday = ft.Checkbox(label="Saturday", value=False)
    sunday = ft.Checkbox(label="Sunday", value=False)

    def submit_form(e):
        e.control.page.dialog = dlg
        dlg.open = True
        e.control.page.update()
        print("Submit form")

    def close_dlg(e):
        dlg.open = False
        e.control.page.update()

    def validate_required_text_field(e):
        if e.control.value == "":
            e.control.error_text = "The field is required"
            e.control.update()

    dlg = ft.AlertDialog(
        # modal=True,
        # title=ft.Text("Form submitted"),
        content=ft.Text("Thank you for submitting the form!"),
        actions=[
            ft.TextButton("OK", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    submit = ft.FilledButton("Submit", on_click=submit_form)

    return ft.SafeArea(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            # alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.TextField(
                    label="First name",
                    keyboard_type=ft.KeyboardType.NAME,
                    on_blur=validate_required_text_field,
                ),
                ft.TextField(
                    label="Last name",
                    keyboard_type=ft.KeyboardType.NAME,
                    on_blur=validate_required_text_field,
                ),
                ft.TextField(
                    label="Email",
                    keyboard_type=ft.KeyboardType.EMAIL,
                    on_blur=validate_required_text_field,
                ),
                ft.TextField(
                    label="Age",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    on_blur=validate_required_text_field,
                ),
                ft.Text("Gender:"),
                gender,
                ft.Divider(thickness=1),
                choice_of_instrument,
                ft.Text("Pick days for classes:"),
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                ft.Row(controls=[submit], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
        expand=True,
    )


def main(page: ft.Page):
    page.title = "Flet entry form example"
    page.window_width = 390
    page.window_height = 844
    page.add(example(main))


if __name__ == "__main__":
    ft.app(target=main)
