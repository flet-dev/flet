import flet as ft


def main(page: ft.Page) -> None:
    page.title = "Device orientation lock"
    page.appbar = ft.AppBar(
        title=ft.Text("Device orientation Playground"),
        center_title=True,
        bgcolor=ft.Colors.BLUE,
    )

    def handle_media_change(e: ft.PageMediaData) -> None:
        page.show_dialog(
            ft.SnackBar(
                f"I see you rotated the device to {e.orientation.name} orientation. 👀",
                action="Haha!",
                duration=ft.Duration(seconds=3),
            )
        )

    page.on_media_change = handle_media_change

    async def on_checkbox_change(e: ft.Event[ft.Checkbox]) -> None:
        # get selection
        selected = [o for o, checkbox in checkboxes.items() if checkbox.value]
        # apply selection
        await page.set_allowed_device_orientations(selected)

    checkboxes: dict[ft.DeviceOrientation, ft.Checkbox] = {
        orientation: ft.Checkbox(
            label=orientation.name,
            value=True,
            on_change=on_checkbox_change,
            disabled=not page.platform.is_mobile(),  # disabled on non-mobile platforms
        )
        for orientation in list(ft.DeviceOrientation)
    }

    page.add(
        ft.Text(
            spans=[
                # shown only on mobile platforms
                ft.TextSpan(
                    "Select the orientations that should remain enabled for the app. "
                    "If no orientation is selected, the system defaults will be used.",
                    visible=page.platform.is_mobile(),
                ),
                # shown only on non-mobile platforms
                ft.TextSpan(
                    "Please open this example on a mobile device instead.",
                    visible=not page.platform.is_mobile(),
                    style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                ),
            ],
        ),
        ft.Column(controls=list(checkboxes.values())),
    )


if __name__ == "__main__":
    ft.run(main)
