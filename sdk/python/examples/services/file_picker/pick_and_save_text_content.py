#
# Example of picking and saving text content with FilePicker.
#
# Run this example with:
#    uv run flet run --web examples/services/file_picker/pick_and_save_text_content.py
#
import flet as ft


def main(page: ft.Page):
    selected_file_name = ft.Text("No file selected")
    selected_file_content = ft.TextField(
        label="Selected file content",
        multiline=True,
        min_lines=8,
        max_lines=14,
    )
    save_status = ft.Text()

    async def pick_text_file(_: ft.Event[ft.Button]):
        files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt", "md"],
        )
        if not files:
            selected_file_name.value = "Selection cancelled"
            selected_file_content.value = ""
            page.update()
            return

        selected = files[0]
        selected_file_name.value = f"Selected: {selected.name} ({selected.size} bytes)"
        selected_file_content.value = (
            selected.bytes.decode("utf-8", errors="replace") if selected.bytes else ""
        )
        save_status.value = ""
        page.update()

    async def save_text_file(_: ft.Event[ft.Button]):
        file_name = "flet_text_content.txt"
        file_path = await ft.FilePicker().save_file(
            file_name=file_name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"],
            src_bytes=selected_file_content.value.encode("utf-8"),
        )
        if page.web:
            save_status.value = f"Downloaded as {file_name}"
        else:
            save_status.value = (
                f"Saved to: {file_path}" if file_path else "Save cancelled"
            )
        page.update()

    page.add(
        ft.Text("Pick a .txt/.md file and load its text from FilePickerFile.bytes"),
        ft.Button(
            content="Pick text file",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=pick_text_file,
        ),
        selected_file_name,
        selected_file_content,
        ft.Button(
            content="Save / Download text",
            icon=ft.Icons.DOWNLOAD,
            on_click=save_text_file,
        ),
        save_status,
    )


ft.run(main)
