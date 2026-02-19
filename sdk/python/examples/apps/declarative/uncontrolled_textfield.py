import random
from typing import cast

import flet as ft


@ft.component
def App():
    state, set_state = ft.use_state("")

    async def submit(e: ft.Event[ft.Button]):
        e.page.show_dialog(
            ft.AlertDialog(
                title="Hello",
                content=ft.Text(f"{first_name.value} {last_name.value}!"),
            )
        )

    def reset():
        set_state("reset" + str(random.randint(1, 1000)))

    return [
        first_name := ft.TextField(
            label="First name",
        ),
        last_name := ft.TextField(
            label="Last name",
        ),
        ft.Row(
            cast(
                list[ft.Control],
                [
                    ft.FilledButton("Submit", on_click=submit),
                    ft.FilledTonalButton("Reset", on_click=reset),
                ],
            )
        ),
    ]


ft.run(lambda page: page.render(App))
