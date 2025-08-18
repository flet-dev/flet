from dataclasses import dataclass
from typing import cast

import flet as ft


@dataclass
class Form:
    first_name: str = ""
    last_name: str = ""

    def set_first_name(self, value):
        self.first_name = value

    def set_last_name(self, value):
        self.last_name = value

    async def submit(self, e: ft.ControlEvent):
        e.page.show_dialog(
            ft.AlertDialog(
                title="Hello",
                content=ft.Text(f"{self.first_name} {self.last_name}!"),
            )
        )

    async def reset(self):
        self.first_name = ""
        self.last_name = ""


def main(page: ft.Page):
    form = Form()

    page.add(
        ft.StateView(
            form,
            lambda state: ft.Column(
                cast(
                    list[ft.Control],
                    [
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
                            [
                                ft.FilledButton("Submit", on_click=form.submit),
                                ft.FilledTonalButton("Reset", on_click=form.reset),
                            ]
                        ),
                    ],
                )
            ),
        )
    )


ft.run(main)
