import flet as ft


@ft.control
class MyContainer(ft.Container):
    text: str = ""
    height: int = 100
    alignment: ft.Alignment = ft.Alignment.CENTER

    def init(self):
        self.bgcolor = ft.Colors.random()
        self.content = ft.Text(self.text)


def main(page: ft.Page):
    def handle_new_tab(e: ft.Event[ft.CupertinoFilledButton]):
        tab_count = len(tab_bar.tabs) + 1
        tab_bar.tabs.append(ft.Tab(label=ft.Text(f"Tab {tab_count}")))
        tab_view.controls.append(MyContainer(text=f"Tab {tab_count} content"))
        tabs.length = len(tab_bar.tabs)

    tabs = ft.Tabs(
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

    page.add(
        ft.SafeArea(
            expand=True,
            content=tabs,
        )
    )


if __name__ == "__main__":
    ft.run(main)
