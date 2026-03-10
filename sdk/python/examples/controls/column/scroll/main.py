import flet as ft


def main(page: ft.Page):
    def add_text_box(e: ft.Event[ft.Button]):
        text_field = ft.TextField(
            label=f"Text Box {len(left_column.controls)}",
            label_style=ft.TextStyle(color=ft.Colors.GREEN),
            color=ft.Colors.GREEN,
            value=str(len(left_column.controls)),
        )
        left_column.controls.append(text_field)
        page.update()

    def remove_text_box(e: ft.Event[ft.Button]):
        if left_column.controls:
            left_column.controls.pop()
        page.update()

    def scroll_generator(scroll_mode_list: list):
        while True:
            yield from scroll_mode_list

    def change_scroll(_):
        left_column.scroll = next(scroll_mode)
        scroll_mode_text.value = str(left_column.scroll)
        page.update()

    add_text_box_button = ft.Button("Add TextBox", on_click=add_text_box)
    remove_text_box_button = ft.Button(
        content="Remove TextBox",
        on_click=remove_text_box,
    )
    scroll_change_button = ft.Button(
        content="Change Scroll Mode",
        on_click=change_scroll,
    )

    scroll_mode = scroll_generator(
        [
            None,
            ft.ScrollMode.AUTO,
            ft.ScrollMode.ADAPTIVE,
            ft.ScrollMode.ALWAYS,
            ft.ScrollMode.HIDDEN,
        ]
    )

    left_column = ft.Column(
        controls=[ft.Text("THIS IS COL 1", color=ft.Colors.RED_400)],
        scroll=next(scroll_mode),
    )
    scroll_mode_text = ft.Text(str(left_column.scroll))

    page.add(
        ft.Row(
            expand=True,
            controls=[
                ft.Container(
                    content=left_column,
                    expand=True,
                    margin=10,
                    padding=10,
                    bgcolor=ft.Colors.AMBER_100,
                    border_radius=10,
                    alignment=ft.Alignment.TOP_CENTER,
                ),
                ft.Container(
                    margin=10,
                    padding=10,
                    bgcolor=ft.Colors.CYAN_500,
                    border_radius=10,
                    expand=True,
                    alignment=ft.Alignment.TOP_LEFT,
                    content=ft.Column(
                        controls=[
                            add_text_box_button,
                            remove_text_box_button,
                            scroll_change_button,
                            scroll_mode_text,
                        ],
                    ),
                ),
            ],
        )
    )


ft.run(main)
