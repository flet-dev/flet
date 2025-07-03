::: flet.FilePicker

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/filepicker)

### Pick multiple files



```python
import flet as ft

def main(page: ft.Page):
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                selected_files,
            ]
        )
    )

ft.run(main)
```


### All dialog modes

<img src="/img/docs/controls/file-picker/file-picker-all-modes-demo.png" className="screenshot-70" />

[Source code](https://github.com/flet-dev/examples/blob/main/python/controls/file-picker/file-picker-all-modes.py)

### Upload multiple files

<img src="/img/docs/controls/file-picker/file-picker-multiple-uploads.png" className="screenshot-40" />

[Source code](https://github.com/flet-dev/examples/blob/main/python/controls/file-picker/file-picker-upload-progress.py)
