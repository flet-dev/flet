import flet as ft
import flet_local_auth as auth


def main(page: ft.Page):
    status = ft.Text(theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    local_auth = auth.LocalAuthentication()

    async def refresh_capabilities(_):
        supported = await local_auth.is_device_supported()
        can_check = await local_auth.can_check_biometrics()
        biometrics = await local_auth.get_available_biometrics()
        status.value = (
            f"Device supported: {supported}\n"
            f"Biometric hardware: {can_check}\n"
            f"Enrolled biometrics: {', '.join(b.value for b in biometrics) or 'none'}"
        )

    async def authenticate(_):
        try:
            ok = await local_auth.authenticate(
                "Authenticate to continue",
                android_messages=auth.AndroidAuthMessages(
                    sign_in_title="Unlock",
                    cancel_button="Not now",
                ),
            )
            status.value = f"Authenticated: {ok}"
        except auth.LocalAuthException as e:
            status.value = f"Authentication failed: {e.code.value}"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Container(
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=12,
                        padding=16,
                        content=status,
                    ),
                    ft.Button("Check capabilities", on_click=refresh_capabilities),
                    ft.Button("Authenticate", on_click=authenticate),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
