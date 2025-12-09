import flet as ft


async def main(page: ft.Page):
    storage_paths = ft.StoragePaths()

    items = []
    for label, method in [
        ("Application cache directory", storage_paths.get_application_cache_directory),
        (
            "Application documents directory",
            storage_paths.get_application_documents_directory,
        ),
        (
            "Application support directory",
            storage_paths.get_application_support_directory,
        ),
        ("Downloads directory", storage_paths.get_downloads_directory),
        ("External cache directories", storage_paths.get_external_cache_directories),
        (
            "External storage directories",
            storage_paths.get_external_storage_directories,
        ),
        ("Library directory", storage_paths.get_library_directory),
        ("External storage directory", storage_paths.get_external_storage_directory),
        ("Temporary directory", storage_paths.get_temporary_directory),
        ("Console log filename", storage_paths.get_console_log_filename),
    ]:
        try:
            value = await method()
        except ft.FletUnsupportedPlatformException as e:
            value = f"Not supported: {e}"
        except Exception as e:
            value = f"Error: {e}"
        else:
            if isinstance(value, list):
                value = ", ".join(value)
            elif value is None:
                value = "Unavailable"

        items.append(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        f"{label}: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)
                    ),
                    ft.TextSpan(value),
                ]
            )
        )

    page.add(ft.Column(items, spacing=5))


ft.run(main)
