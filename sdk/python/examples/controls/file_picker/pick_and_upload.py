#
# Example of picking and uploading files with progress indication
#
# Run this example with:
#    export FLET_SECRET_KEY=<some_secret_key>
#    uv run flet run --web examples/controls/file_picker/pick_and_upload.py
#
from dataclasses import dataclass, field

import flet as ft


@dataclass
class State:
    file_picker: ft.FilePicker | None = None
    picked_files: list[ft.FilePickerFile] = field(default_factory=list)


state = State()


def main(page: ft.Page):
    if not page.web:
        page.add(
            ft.Text(
                "This example is only available in Flet Web mode.\n"
                "\n"
                "Run this example with:\n"
                "    export FLET_SECRET_KEY=<some_secret_key>\n"
                "    flet run --web "
                "examples/controls/file_picker/pick_and_upload.py",
                color=ft.Colors.RED,
                selectable=True,
            )
        )
        return

    prog_bars: dict[str, ft.ProgressRing] = {}

    def on_upload_progress(e: ft.FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress

    async def handle_files_pick(e: ft.Event[ft.Button]):
        state.file_picker = ft.FilePicker(on_upload=on_upload_progress)
        files = await state.file_picker.pick_files(allow_multiple=True)
        print("Picked files:", files)
        state.picked_files = files

        # update progress bars
        upload_button.disabled = len(files) == 0
        prog_bars.clear()
        upload_progress.controls.clear()
        for f in files:
            prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
            prog_bars[f.name] = prog
            upload_progress.controls.append(ft.Row([prog, ft.Text(f.name)]))

    async def handle_file_upload(e: ft.Event[ft.Button]):
        upload_button.disabled = True
        await state.file_picker.upload(
            files=[
                ft.FilePickerUploadFile(
                    name=file.name,
                    upload_url=page.get_upload_url(f"dir/{file.name}", 60),
                )
                for file in state.picked_files
            ]
        )

    page.add(
        ft.Button(
            content="Select files...",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=handle_files_pick,
        ),
        upload_progress := ft.Column(),
        upload_button := ft.Button(
            content="Upload",
            icon=ft.Icons.UPLOAD,
            on_click=handle_file_upload,
            disabled=True,
        ),
    )


ft.run(main, upload_dir="examples")
