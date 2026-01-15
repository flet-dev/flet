import base64
import os

import flet as ft
import flet_secure_storage as fss


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    storage = fss.SecureStorage(
        web_options=fss.WebOptions(
            db_name="customstorage",
            public_key="publickey",
            wrap_key=base64.urlsafe_b64encode(os.urandom(32)).decode(),
            wrap_key_iv=base64.urlsafe_b64encode(os.urandom(16)).decode(),
        ),
        android_options=fss.AndroidOptions(
            reset_on_error=True,
            migrate_on_algorithm_change=True,
            enforce_biometrics=True,
            key_cipher_algorithm=fss.KeyCipherAlgorithm.AES_GCM_NO_PADDING,
            storage_cipher_algorithm=fss.StorageCipherAlgorithm.AES_GCM_NO_PADDING,
        ),
    )

    key = ft.TextField(label="Key", value="example_key")
    value = ft.TextField(label="Value", value="secret_value")
    result = ft.Text(theme_style=ft.TextThemeStyle.TITLE_LARGE)

    async def set_value(e):
        await storage.set(key.value, value.value)
        result.value = "Value saved"
        page.update()

    async def get_value(e):
        result.value = await storage.get(key.value)
        page.update()

    async def remove_value(e):
        await storage.remove(key.value)
        result.value = "Value removed"
        page.update()

    async def clear_storage(e):
        await storage.clear()
        result.value = "Storage cleared"
        page.update()

    async def contains_key(e):
        exists = await storage.contains_key(key.value)
        result.value = f"Key exists: {exists}"
        page.update()

    async def get_availability(e):
        is_availability = await storage.get_availability()
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    value=f"Protected data available: {is_availability}"
                    if is_availability
                    else "Protected data available: None"
                )
            )
        )
        page.update()

    page.add(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                result,
                key,
                value,
                ft.Row(
                    width=300,
                    wrap=True,
                    controls=[
                        ft.Button("Set", on_click=set_value),
                        ft.Button("Get", on_click=get_value),
                        ft.Button("Contains key", on_click=contains_key),
                        ft.Button("Remove", on_click=remove_value),
                        ft.Button("Clear", on_click=clear_storage),
                        ft.Button("Check Data Availability", on_click=get_availability),
                    ],
                ),
            ],
        ),
    )


ft.run(main)
