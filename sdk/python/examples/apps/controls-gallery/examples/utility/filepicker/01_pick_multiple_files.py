import flet as ft

name = "Pick multiple files"


def example():
    class Example(ft.Row):
        def __init__(self):
            super().__init__()
            self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
            self.selected_files = ft.Text()

            def pick_files(_):
                self.pick_files_dialog.pick_files(allow_multiple=True)

            self.controls = [
                ft.Button(
                    "Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=pick_files,
                ),
                self.selected_files,
            ]

        def pick_files_result(self, e: ft.FilePickerResultEvent):
            self.selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )
            self.selected_files.update()

        # happens when example is added to the page (when user chooses
        # the FilePicker control from the grid)
        def did_mount(self):
            self.page.overlay.append(self.pick_files_dialog)
            self.page.update()

        # happens when example is removed from the page (when user chooses
        # different control group on the navigation rail)
        def will_unmount(self):
            self.page.overlay.remove(self.pick_files_dialog)
            self.page.update()

    filepicker_example = Example()

    return filepicker_example
