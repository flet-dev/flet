import flet as ft


@ft.component
def App():
    items, set_items = ft.use_state(list(range(5)))

    return ft.SafeArea(
        content=ft.ListView(
            controls=[
                ft.Dismissible(
                    key=i,
                    dismiss_direction=ft.DismissDirection.HORIZONTAL,
                    background=ft.Container(bgcolor=ft.Colors.GREEN),
                    secondary_background=ft.Container(bgcolor=ft.Colors.RED),
                    on_dismiss=lambda _, index=i: set_items(
                        [item for item in items if item != index]
                    ),
                    dismiss_thresholds={
                        ft.DismissDirection.HORIZONTAL: 0.1,
                        ft.DismissDirection.START_TO_END: 0.1,
                    },
                    content=ft.ListTile(title=ft.Text(f"Item {i}")),
                )
                for i in items
            ],
        ),
    )


def main(page: ft.Page):
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
