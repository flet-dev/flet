import flet as ft


@ft.component
def App():
    count, set_count = ft.use_state(0)

    return ft.Row(
        controls=[
            ft.Text(value=f"{count}"),
            ft.Button("Add", on_click=lambda: set_count(count + 1)),
        ],
    )


ft.run(lambda page: page.render(App))
