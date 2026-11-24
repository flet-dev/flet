import flet as ft


async def main(page: ft.Page):
    info = await page.get_package_info()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text(info.app_name, theme_style=ft.TextThemeStyle.TITLE_LARGE),
                    ft.Text(f"Version {info.version} (build {info.build_number})"),
                    ft.Text(f"Package: {info.package_name}"),
                    ft.Text(f"Installed from: {info.installer_store or 'unknown'}"),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
