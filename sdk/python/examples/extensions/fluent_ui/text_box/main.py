import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent TextBox"

    def handle_change(e: ft.Event[fluent.TextBox]):
        greeting.value = f"Hello, {e.control.value}!" if e.control.value else ""

    greeting = ft.Text()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=300,
                controls=[
                    fluent.TextBox(
                        key="name",
                        placeholder="Your name",
                        prefix=fluent.FluentIcons.CONTACT,
                        on_change=handle_change,
                    ),
                    fluent.TextBox(placeholder="Password", password=True),
                    fluent.TextBox(placeholder="Notes", multiline=True, min_lines=3),
                    greeting,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
