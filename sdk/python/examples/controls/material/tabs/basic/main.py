import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Tabs(
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
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Text("This is Tab 1"),
                                ),
                                ft.Container(
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Text("This is Tab 2"),
                                ),
                                ft.Container(
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Text("This is Tab 3"),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
