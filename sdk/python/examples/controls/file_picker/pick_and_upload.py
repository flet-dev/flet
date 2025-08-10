import flet as ft

state = {"picked_files": []}


def main(page: ft.Page):
    prog_bars: dict[str, ft.ProgressRing] = {}

    def on_upload_progress(e: ft.FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress

    # add to services
    page.services.append(file_picker := ft.FilePicker(on_upload=on_upload_progress))

    async def handle_files_pick(e: ft.Event[ft.ElevatedButton]):
        files = await file_picker.pick_files(allow_multiple=True)
        print("Picked files:", files)
        state["picked_files"] = files

        # update progress bars
        upload_button.disabled = len(files) == 0
        prog_bars.clear()
        upload_progress.controls.clear()
        for f in files:
            prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
            prog_bars[f.name] = prog
            upload_progress.controls.append(ft.Row([prog, ft.Text(f.name)]))

    async def handle_file_upload(e: ft.Event[ft.ElevatedButton]):
        upload_button.disabled = True
        await file_picker.upload(
            files=[
                ft.FilePickerUploadFile(
                    name=file.name,
                    upload_url=page.get_upload_url(f"dir/{file.name}", 60),
                )
                for file in state["picked_files"]
            ]
        )

    page.add(
        ft.Text("test"),
        ft.ElevatedButton(
            content="Select files...",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=handle_files_pick,
        ),
        upload_progress := ft.Column(),
        upload_button := ft.ElevatedButton(
            content="Upload",
            icon=ft.Icons.UPLOAD,
            on_click=handle_file_upload,
            disabled=True,
        ),
    )


ft.run(main, upload_dir="examples")
