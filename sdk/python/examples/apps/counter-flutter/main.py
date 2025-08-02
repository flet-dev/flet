import flet as ft


class State:
    counter = 0


def main(page: ft.Page):
    state = State()

    def add_click(e):
        state.counter += 1
        counter.value = str(state.counter)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=add_click
    )
    page.add(
        ft.SafeArea(
            ft.Container(
                counter := ft.Text("0", size=50),
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.run(main)
