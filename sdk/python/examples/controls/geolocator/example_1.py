from typing import Callable

import flet as ft
import flet_geolocator as ftg


async def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.appbar = ft.AppBar(title=ft.Text("Geolocator Tests"))

    def handle_position_change(e: ftg.GeolocatorPositionChangeEvent):
        page.add(ft.Text(f"New position: {e.position.latitude} {e.position.longitude}"))

    def get_dialog(handler: Callable):
        return ft.AlertDialog(
            adaptive=True,
            title="Opening Location Settings...",
            content=ft.Text(
                "You are about to be redirected to the location/app settings. "
                "Please locate this app and grant it location permissions."
            ),
            actions=[ft.TextButton("Take me there", on_click=handler)],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

    def show_snackbar(message):
        page.show_dialog(ft.SnackBar(ft.Text(message)))

    async def handle_permission_request(e: ft.Event[ft.OutlinedButton]):
        p = await geo.request_permission()
        page.add(ft.Text(f"request_permission: {p}"))
        show_snackbar(f"Permission request sent: {p}")

    async def handle_get_permission_status(e: ft.Event[ft.OutlinedButton]):
        p = await geo.get_permission_status()
        show_snackbar(f"Permission status: {p}")

    async def handle_get_current_position(e: ft.Event[ft.OutlinedButton]):
        p = await geo.get_current_position()
        show_snackbar(f"Current position: ({p.latitude}, {p.longitude})")

    async def handle_get_last_known_position(e):
        p = await geo.get_last_known_position()
        show_snackbar(f"Last known position: ({p.latitude}, {p.longitude})")

    async def handle_location_service_enabled(e):
        p = await geo.is_location_service_enabled()
        show_snackbar(f"Location service enabled: {p}")

    async def handle_open_location_settings(e: ft.Event[ft.OutlinedButton]):
        p = await geo.open_location_settings()
        page.pop_dialog()
        if p:
            show_snackbar("Location settings opened successfully.")
        else:
            show_snackbar("Location settings could not be opened.")

    async def handle_open_app_settings(e: ft.Event[ft.OutlinedButton]):
        p = await geo.open_app_settings()
        page.pop_dialog()
        if p:
            show_snackbar("App settings opened successfully.")
        else:
            show_snackbar("App settings could not be opened.")

    location_settings_dlg = get_dialog(handle_open_location_settings)
    app_settings_dlg = get_dialog(handle_open_app_settings)

    geo = ftg.Geolocator(
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.LOW
        ),
        on_position_change=handle_position_change,
        on_error=lambda e: page.add(ft.Text(f"Error: {e.data}")),
    )

    page.add(
        ft.Row(
            wrap=True,
            controls=[
                ft.OutlinedButton(
                    content="Request Permission",
                    on_click=handle_permission_request,
                ),
                ft.OutlinedButton(
                    content="Get Permission Status",
                    on_click=handle_get_permission_status,
                ),
                ft.OutlinedButton(
                    content="Get Current Position",
                    on_click=handle_get_current_position,
                ),
                ft.OutlinedButton(
                    content="Get Last Known Position",
                    disabled=page.web,
                    on_click=handle_get_last_known_position,
                ),
                ft.OutlinedButton(
                    content="Is Location Service Enabled",
                    on_click=handle_location_service_enabled,
                ),
                ft.OutlinedButton(
                    content="Open Location Settings",
                    disabled=page.web,  # (1)!
                    on_click=lambda e: page.show_dialog(location_settings_dlg),
                ),
                ft.OutlinedButton(
                    content="Open App Settings",
                    disabled=page.web,  # (1)!
                    on_click=lambda e: page.show_dialog(app_settings_dlg),
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
