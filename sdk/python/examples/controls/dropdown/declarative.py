from dataclasses import dataclass
from typing import cast

import flet as ft


@dataclass
@ft.observable
class Form:
    color: str = "red"

    def change_color(self, new_color: str):
        print("New color:", new_color)
        self.color = new_color


@ft.component
def App():
    form, _ = ft.use_state(lambda: Form())

    return ft.SafeArea(
        ft.Column(
            cast(
                list[ft.Control],
                [
                    ft.Text(f"Selected color: {form.color}"),
                    ft.Column(
                        [
                            ft.Dropdown(
                                editable=True,
                                label="Color",
                                value=form.color,
                                on_select=lambda e: form.change_color(
                                    cast(str, e.control.value)
                                ),
                                options=[
                                    ft.DropdownOption(key="red", text="Red"),
                                    ft.DropdownOption(key="green", text="Green"),
                                    ft.DropdownOption(key="blue", text="Blue"),
                                ],
                            ),
                        ]
                    ),
                ],
            )
        ),
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
