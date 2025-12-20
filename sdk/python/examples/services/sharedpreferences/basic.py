import flet as ft


async def main(page: ft.Page):
    async def set_value():
        await ft.SharedPreferences().set(store_key.value, store_value.value)
        get_key.value = store_key.value
        store_key.value = ""
        store_value.value = ""
        page.show_dialog(ft.SnackBar("Value saved to SharedPreferences"))

    async def get_value():
        contents = await ft.SharedPreferences().get(get_key.value)
        page.add(ft.Text(f"SharedPreferences contents: {contents}"))

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        store_key := ft.TextField(label="Key"),
                        store_value := ft.TextField(label="Value"),
                        ft.Button("Set", on_click=set_value),
                    ]
                ),
                ft.Row(
                    [
                        get_key := ft.TextField(label="Key"),
                        ft.Button("Get", on_click=get_value),
                    ]
                ),
            ],
        )
    )


ft.run(main)
