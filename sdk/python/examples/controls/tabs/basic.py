import flet as ft


def main(page: ft.Page):
    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                label="Tab 1",
                content=ft.Container(
                    content=ft.Text("This is Tab 1"), alignment=ft.Alignment.CENTER
                ),
            ),
            ft.Tab(
                label="Tab 2",
                icon=ft.Icons.SETTINGS,
                content=ft.Container(
                    content=ft.Text("This is Tab 2"), alignment=ft.Alignment.CENTER
                ),
            ),
            ft.Tab(
                label=ft.CircleAvatar(
                    foreground_image_src="https://avatars.githubusercontent.com/u/7119543?s=88&v=4"
                ),
                content=ft.Container(
                    content=ft.Text("This is Tab 3"), alignment=ft.Alignment.CENTER
                ),
            ),
        ],
        expand=1,
    )

    page.add(t)


ft.run(main)
