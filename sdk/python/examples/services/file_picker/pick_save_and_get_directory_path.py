import flet as ft


def main(page: ft.Page):
    async def handle_pick_files(e: ft.Event[ft.Button]):
        files = await ft.FilePicker().pick_files(allow_multiple=True)
        selected_files.value = (
            ", ".join(map(lambda f: f.name, files)) if files else "Cancelled!"
        )

    async def handle_save_file(e: ft.Event[ft.Button]):
        save_file_path.value = await ft.FilePicker().save_file()

    async def handle_get_directory_path(e: ft.Event[ft.Button]):
        directory_path.value = await ft.FilePicker().get_directory_path()

    page.add(
        ft.Row(
            controls=[
                ft.Button(
                    content="Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=handle_pick_files,
                ),
                selected_files := ft.Text(),
            ]
        ),
        ft.Row(
            controls=[
                ft.Button(
                    content="Save file",
                    icon=ft.Icons.SAVE,
                    on_click=handle_save_file,
                    disabled=page.web,  # disable this button in web mode
                ),
                save_file_path := ft.Text(),
            ]
        ),
        ft.Row(
            controls=[
                ft.Button(
                    content="Open directory",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=handle_get_directory_path,
                    disabled=page.web,  # disable this button in web mode
                ),
                directory_path := ft.Text(),
            ]
        ),
    )


ft.run(main)
