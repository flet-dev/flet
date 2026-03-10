import flet as ft


def main(page: ft.Page):
    events = ft.Column()

    def handle_checkbox_change(e: ft.Event[ft.Checkbox]):
        events.controls.append(ft.Text(f"Checkbox value changed to {e.control.value}"))
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Checkbox(
                        label="Checkbox with 'change' event",
                        on_change=handle_checkbox_change,
                    ),
                    events,
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
