import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "shadcn Switch"

    def handle_change(e: ft.Event[shad.Switch]):
        status.value = f"Airplane mode is {'on' if e.control.value else 'off'}"

    status = ft.Text("Airplane mode is off")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    shad.Switch(label="Airplane mode", on_change=handle_change),
                    shad.Switch(
                        label="Marketing emails",
                        sublabel="Receive emails about new products and features.",
                        value=True,
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
