import flet as ft

name = "Assist chips"


def example():
    def save_to_favorites_clicked(e):
        save_to_favourites.label.value = "Saved to favorites"
        save_to_favourites.leading = ft.Icon(ft.Icons.FAVORITE_OUTLINED)
        save_to_favourites.disabled = True
        save_to_favourites.update()

    async def open_google_maps(e):
        await e.control.page.launch_url_async("https://maps.google.com")

    save_to_favourites = ft.Chip(
        label=ft.Text("Save to favourites"),
        leading=ft.Icon(ft.Icons.FAVORITE_BORDER_OUTLINED),
        on_click=save_to_favorites_clicked,
    )

    open_in_maps = ft.Chip(
        label=ft.Text("9 min walk"),
        leading=ft.Icon(ft.Icons.MAP_SHARP),
        on_click=open_google_maps,
    )

    return ft.Row([save_to_favourites, open_in_maps])
