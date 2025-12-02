import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_change(e: ft.Event[ft.ExpansionPanelList]):
        print(f"change on panel with index {e.data}")

    def handle_delete(e: ft.Event[ft.IconButton]):
        icon_button = e.control
        tile = icon_button.parent
        panel = tile.parent

        panel_list.controls.remove(panel)
        page.update()

    panel_list = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.AMBER,
        elevation=8,
        divider_color=ft.Colors.AMBER,
        on_change=handle_change,
        controls=[
            ft.ExpansionPanel(
                # has no header and content - placeholders will be used
                bgcolor=ft.Colors.BLUE_400,
                expanded=True,
            ),
        ],
    )

    colors = [
        ft.Colors.GREEN_500,
        ft.Colors.BLUE_800,
        ft.Colors.RED_800,
    ]

    for i in range(len(colors)):
        bgcolor = colors[i % len(colors)]
        panel_list.controls.append(
            ft.ExpansionPanel(
                bgcolor=bgcolor,
                header=ft.ListTile(title=ft.Text(f"Panel {i}"), bgcolor=bgcolor),
                content=ft.ListTile(
                    bgcolor=bgcolor,
                    title=ft.Text(f"This is in Panel {i}"),
                    subtitle=ft.Text(f"Press the icon to delete panel {i}"),
                    trailing=ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=handle_delete,
                    ),
                ),
            )
        )

    page.add(panel_list)


if __name__ == "__main__":
    ft.run(main)
