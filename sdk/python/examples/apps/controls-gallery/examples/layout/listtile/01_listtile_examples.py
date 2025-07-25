import flet as ft

name = "ListTile Examples"


def example():
    return ft.Card(
        content=ft.Container(
            width=500,
            content=ft.Column(
                [
                    ft.ListTile(
                        title=ft.Text("One-line list tile"),
                    ),
                    ft.ListTile(title=ft.Text("One-line dense list tile"), dense=True),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SETTINGS),
                        title=ft.Text("One-line selected list tile"),
                        selected=True,
                    ),
                    ft.ListTile(
                        leading=ft.Image(src="/logo.svg", fit=ft.BoxFit.CONTAIN),
                        title=ft.Text("One-line with leading control"),
                    ),
                    ft.ListTile(
                        title=ft.Text("One-line with trailing control"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(text="Item 1"),
                                ft.PopupMenuItem(text="Item 2"),
                            ],
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ALBUM),
                        title=ft.Text("One-line with leading and trailing controls"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(text="Item 1"),
                                ft.PopupMenuItem(text="Item 2"),
                            ],
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SNOOZE),
                        title=ft.Text("Two-line with leading and trailing controls"),
                        subtitle=ft.Text("Here is a second title."),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(text="Item 1"),
                                ft.PopupMenuItem(text="Item 2"),
                            ],
                        ),
                    ),
                ],
                spacing=0,
            ),
            padding=ft.Padding.symmetric(vertical=10),
        )
    )
