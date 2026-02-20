import flet as ft


async def main(page: ft.Page):
    def format_locales(locales: list[ft.Locale]) -> str:
        """Format locale list for display."""
        return ", ".join(str(loc) for loc in locales)

    def handle_locale_change(e: ft.LocaleChangeEvent):
        page.add(ft.Text(f"Locales changed: {format_locales(e.locales)}"))

    page.on_locale_change = handle_locale_change
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    initial_locales = (await page.get_device_info()).locales
    page.add(
        ft.Text(f"Initial locales: {format_locales(initial_locales)}"),
        ft.Text(
            "Change your system or browser language to trigger on_locale_change.",
            color=ft.Colors.BLUE,
        ),
    )


ft.run(main)
