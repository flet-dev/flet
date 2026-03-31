import flet as ft


@ft.component
def App():
    count, set_count = ft.use_state(0)

    return ft.View(
        floating_action_button=ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=lambda: set_count(count + 1)
        ),
        controls=[
            ft.SafeArea(
                expand=True,
                content=ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(value=f"{count}", size=50),
                ),
            )
        ],
    )


def main(page: ft.Page):
    page.render_views(App)


if __name__ == "__main__":
    ft.run(main)
