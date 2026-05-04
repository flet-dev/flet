import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.ExpansionPanelList(
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
                spacing=8,
                controls=[
                    ft.ExpansionPanel(
                        can_tap_header=True,
                        header=ft.ListTile(title=ft.Text(f"Panel {i}")),
                        content=ft.ListTile(
                            title=ft.Text(f"Details for panel {i}"),
                            subtitle=ft.Text(
                                "This content can be expanded or collapsed."
                            ),
                        ),
                    )
                    for i in range(1, 41)
                ],
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
