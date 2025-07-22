import flet as ft


def example(page):
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=20,
        expand=True,
        # alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(
                [
                    ft.Text("Common buttons"),
                    ft.IconButton(
                        ft.Icons.INFO_OUTLINED,
                        tooltip="There are five types of common buttons: elevated, filled, filled tonal, outlined, and text",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="Elevated", expand=1),
                    ft.ElevatedButton(text="Elevated", disabled=True, expand=1),
                ],
            ),
            ft.Row(
                controls=[
                    ft.FilledButton(text="Filled", expand=1),
                    ft.FilledButton(text="Filled", disabled=True, expand=1),
                ],
            ),
            ft.Row(
                controls=[
                    ft.FilledTonalButton(text="Filled tonal", expand=1),
                    ft.FilledTonalButton(text="Filled tonal", disabled=True, expand=1),
                ],
            ),
            ft.Row(
                controls=[
                    ft.OutlinedButton(text="Outlined", expand=1),
                    ft.OutlinedButton(text="Outlined", disabled=True, expand=1),
                ],
            ),
            ft.Row(
                controls=[
                    ft.TextButton(text="Text", expand=1),
                    ft.TextButton(text="Text", disabled=True, expand=1),
                ],
            ),
            ft.Row(
                [
                    ft.Text("Icon buttons"),
                    ft.IconButton(
                        ft.Icons.INFO_OUTLINED,
                        tooltip="Icon buttons help people take supplementary actions with a single tap",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.IconButton(icon=ft.Icons.BOOKMARK),
                    ft.IconButton(
                        icon=ft.Icons.BOOKMARK,
                        disabled=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Text("Floating action buttons"),
                    ft.IconButton(
                        ft.Icons.INFO_OUTLINED,
                        tooltip="The FAB represents the most important action on a screen. It puts key actions within reach",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.FloatingActionButton(icon=ft.Icons.ADD, tooltip="Standard"),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, text="Extended", tooltip="Extended"
                    ),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, mini=True, tooltip="Mini"
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )


def main(page: ft.Page):
    page.title = "Flet buttons example"
    page.window_width = 390
    page.window_height = 844
    page.add(example(page))


if __name__ == "__main__":
    ft.app(target=main)
