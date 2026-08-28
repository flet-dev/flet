#
# Picking and uploading files in a way that also works in a web app on iOS.
#
# Run this example with:
#    export FLET_SECRET_KEY=<some_secret_key>
#    uv run flet run --web examples/services/file_picker/pick_files_action/main.py
#
from dataclasses import dataclass, field

import flet as ft


@dataclass
class State:
    picked_files: list[ft.FilePickerFile] = field(default_factory=list)


state = State()


def main(page: ft.Page):
    prog_bars: dict[str, ft.ProgressRing] = {}

    def handle_upload_progress(e: ft.FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress

    def handle_result(e: ft.FilePickerResultEvent):
        # A PickFiles action opens the dialog before Python sees the click, so
        # the selection arrives here instead of being returned to a caller.
        state.picked_files = e.files

        prog_bars.clear()
        upload_progress.controls.clear()
        for f in e.files:
            prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
            prog_bars[f.name] = prog
            upload_progress.controls.append(
                ft.Row([prog, ft.Text(f"{f.name} ({f.size} bytes)")])
            )
        upload_button.disabled = len(e.files) == 0

    async def handle_file_upload(e: ft.Event[ft.Button]):
        upload_button.disabled = True
        # The picked files stay on the FilePicker, so upload() takes them as-is.
        await file_picker.upload(
            files=[
                ft.FilePickerUploadFile(
                    name=file.name,
                    upload_url=page.get_upload_url(f"dir/{file.name}", 60),
                )
                for file in state.picked_files
            ]
        )

    file_picker = ft.FilePicker(
        on_result=handle_result,
        on_upload=handle_upload_progress,
    )
    page.services.append(file_picker)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Button(
                        content="Select files...",
                        icon=ft.Icons.FOLDER_OPEN,
                        # Attaching the pick to the control - rather than
                        # calling file_picker.pick_files() from an on_click
                        # handler - is what makes the dialog open on iOS.
                        action=ft.PickFiles(file_picker, allow_multiple=True),
                    ),
                    upload_progress := ft.Column(),
                    upload_button := ft.Button(
                        content="Upload",
                        icon=ft.Icons.UPLOAD,
                        on_click=handle_file_upload,
                        disabled=True,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main, upload_dir="examples")
