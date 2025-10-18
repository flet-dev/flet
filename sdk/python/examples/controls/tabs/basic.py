import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Tabs(
            selected_index=1,
            length=3,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Tab 1", icon=ft.Icons.SETTINGS_PHONE),
                            ft.Tab(label="Tab 2", icon=ft.Icons.SETTINGS),
                            ft.Tab(
                                label=ft.CircleAvatar(
                                    foreground_image_src="https://avatars.githubusercontent.com/u/102273996?s=200&amp;v=4",
                                ),
                            ),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Text("This is Tab 1"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("This is Tab 2"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("This is Tab 3"),
                                alignment=ft.Alignment.CENTER,
                            ),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
