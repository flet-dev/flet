from dataclasses import dataclass
from typing import cast

import flet as ft


@dataclass
@ft.observable
class Form:
    first_name: str = ""
    last_name: str = ""

    def set_first_name(self, value):
        self.first_name = value

    def set_last_name(self, value):
        self.last_name = value

    async def submit(self, e: ft.Event[ft.Button]):
        e.page.show_dialog(
            ft.AlertDialog(
                title="Hello",
                content=ft.Text(f"{self.first_name} {self.last_name}!"),
            )
        )

    async def reset(self):
        self.first_name = ""
        self.last_name = ""


@ft.component
def App():
    form, _ = ft.use_state(Form())

    return [
        ft.TextField(
            label="First name",
            value=form.first_name,
            on_change=lambda e: form.set_first_name(e.control.value),
        ),
        ft.TextField(
            label="Last name",
            value=form.last_name,
            on_change=lambda e: form.set_last_name(e.control.value),
        ),
        ft.Row(
            cast(
                list[ft.Control],
                [
                    ft.FilledButton("Submit", on_click=form.submit),
                    ft.FilledTonalButton("Reset", on_click=form.reset),
                ],
            )
        ),
    ]


ft.run(lambda page: page.render(App))
