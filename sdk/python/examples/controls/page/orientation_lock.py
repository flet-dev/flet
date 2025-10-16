from typing import Optional

import flet as ft


def main(page: ft.Page) -> None:
    page.title = "Device orientation lock"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    def describe(selected: list[ft.DeviceOrientation] | None) -> str:
        if not selected:
            return "Allowed orientations: All (system default)"
        names = ", ".join(o.name.replace("_", " ").title() for o in selected)
        return f"Allowed orientations: {names}"

    def current_orientations() -> list[ft.DeviceOrientation]:
        value = page.device_orientations
        return list(value) if value else []

    orientations = list(ft.DeviceOrientation)
    initial_selection = current_orientations()
    status = ft.Text(describe(initial_selection), text_align=ft.TextAlign.CENTER)

    def on_checkbox_change(_):
        selected = [o for o, checkbox in checkboxes.items() if checkbox.value]
        if selected:
            page.device_orientations = selected
            status.value = describe(selected)
        else:
            page.device_orientations = None
            status.value = describe(None)
        page.update()

    def label_for(orientation: ft.DeviceOrientation) -> str:
        return orientation.name.replace("_", " ").title()

    def format_orientation(value: Optional[ft.Orientation]) -> str:
        return value.name.title() if value else "Unknown"

    orientation_info = ft.Text(
        f"Current orientation: {format_orientation(page.orientation)}",
        text_align=ft.TextAlign.CENTER,
    )

    def handle_orientation_change(e: ft.OrientationChangeEvent) -> None:
        orientation_info.value = (
            f"Current orientation: {format_orientation(e.orientation)}"
        )
        page.update()

    page.on_orientation_change = handle_orientation_change

    checkboxes: dict[ft.DeviceOrientation, ft.Checkbox] = {
        orientation: ft.Checkbox(
            label=label_for(orientation),
            value=orientation in initial_selection if initial_selection else True,
            on_change=on_checkbox_change,
        )
        for orientation in orientations
    }

    page.add(
        ft.Text(
            "Select the orientations that should remain enabled for the app. "
            "Try opening this example on a mobile device to observe the effect.",
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Column(list(checkboxes.values()), tight=True),
        status,
        orientation_info,
    )

    # Ensure the initial device orientations reflect the default checkbox state.
    on_checkbox_change(None)


if __name__ == "__main__":
    ft.app(target=main)
