import flet as ft


@ft.component
def App():
    count, set_count = ft.use_state(0)

    return ft.SafeArea(
        content=ft.Row(
            controls=[
                ft.Text(value=f"{count}"),
                ft.Button("Add", on_click=lambda: set_count(count + 1)),
            ],
        )
    )


def main(page: ft.Page):
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
