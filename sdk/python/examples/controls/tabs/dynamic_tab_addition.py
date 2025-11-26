import flet as ft


class MyContainer(ft.Container):
    def __init__(self, text):
        super().__init__(
            height=100,
            bgcolor=ft.Colors.random(),
            alignment=ft.Alignment.CENTER,
        )
        self.content = ft.Text(text)


def main(page: ft.Page):
    def handle_new_tab(e: ft.Event[ft.CupertinoFilledButton]):
        tab_count = len(tab_bar.tabs) + 1
        tab_bar.tabs.append(ft.Tab(label=ft.Text(f"Tab {tab_count}")))
        tab_view.controls.append(MyContainer(text=f"Tab {tab_count} content"))
        tabs.length = len(tab_bar.tabs)

    page.add(
        tabs := ft.Tabs(
            length=2,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    tab_bar := ft.TabBar(
                        tab_alignment=ft.TabAlignment.CENTER,
                        tabs=[
                            ft.Tab(label=ft.Text("Tab 1")),
                            ft.Tab(label=ft.Text("Tab 2")),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.CupertinoFilledButton(
                                content="Add New Tab",
                                icon=ft.Icons.ADD,
                                on_click=handle_new_tab,
                            ),
                        ],
                    ),
                    tab_view := ft.TabBarView(
                        expand=True,
                        controls=[
                            MyContainer(text="Tab 1 content"),
                            MyContainer(text="Tab 2 content"),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
