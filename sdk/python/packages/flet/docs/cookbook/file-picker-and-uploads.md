[`FilePicker`][flet.FilePicker] control opens a native OS dialog for selecting files and directories.

It works on all platforms: Web, macOS, Window, Linux, iOS and Android.

![File picker all modes demo](https://raw.githubusercontent.com/flet-dev/flet/main/sdk/python/examples/controls/file-picker/media/pick-save-and-get-directory-path.png){width="80%"}
/// caption
///

Check out [source code of the demo above](https://github.com/flet-dev/examples/blob/main/python/controls/file-picker/file-picker-all-modes.py).

File picker allows opening three dialogs:

* **Pick files** - one or multiple, any files or only specific types.
* **Save file** - choose directory and file name.
* **Get directory** - select directory.

When running Flet app in a browser only "Pick files" option is available and it's used for
uploads only as it, obviously, doesn't return a full path to a selected file.

Where file picker really shines is a desktop! All three dialogs return full paths to selected
files and directories - great assistance to your users!

/// admonition
    type: info
In Linux, the FilePicker control depends on [Zenity](https://help.gnome.org/users/zenity/stable/)  when running Flet as an app.
This is not a requirement when running Flet in a browser.

To install Zenity on Ubuntu/Debian run the following commands:
```bash
sudo apt-get install zenity
```
///

## Using file picker in your app

Add file picker to [`Page.services`][flet.Page.services] collection,
so it doesn't affect the layout of your app. Despite file picker has 0x0 size it is still considered as a control when put into `Row` or `Column`.

```python
import flet as ft

file_picker = ft.FilePicker()
page.services.append(file_picker)
page.update()
```

To open file picker dialog call one of the three methods:

* `pick_files_async()`
* `save_file()`
* `get_directory_path()`

Lambda works pretty nice for that:

```python
ft.ElevatedButton(
    content="Choose files...",
    on_click=lambda _: file_picker.pick_files_async(allow_multiple=True)
)
```

When dialog is closed `FilePicker.on_result` event handler is called which event object has one of the following properties set:

* `files` - "Pick files" dialog only, a list of selected files or `None` if dialog was cancelled.
* `path` - "Save file" and "Get directory" dialogs, a full path to a file or directory or `None` if dialog was cancelled.

```python
import flet as ft

def on_dialog_result(e: ft.FilePickerResultEvent):
    print("Selected files:", e.files)
    print("Selected file or directory:", e.path)

file_picker = ft.FilePicker(on_result=on_dialog_result)
```

The last result is always available in `FilePicker.result` property.

Check [`FilePicker`][flet.FilePicker] control docs for all available dialog methods and their parameters.

## Uploading files

File picker has built-in upload capabilities that work on all platforms and the web.

To upload one or more files you should call `FilePicker.pick_files_async()` first.
When the files are selected by the user they are not automatically uploaded anywhere, but instead their references are kept in the file picker state.

To perform an actual upload you should call `FilePicker.upload()` method and pass the list of files that need to be uploaded along with their upload URLs and upload method (`PUT` or `POST`):

```python
import flet as ft

def upload_files(e):
    upload_list = []
    if file_picker.result != None and file_picker.result.files != None:
        for f in file_picker.result.files:
            upload_list.append(
                FilePickerUploadFile(
                    f.name,
                    upload_url=page.get_upload_url(f.name, 600),
                )
            )
        file_picker.upload(upload_list)

ft.ElevatedButton("Upload", on_click=upload_files)
```

/// admonition
    type: note
If you need to separate uploads for each user you can specify a filename prepended with any number of directories in `page.get_upload_url()` call, for example:

```python
upload_url = page.get_upload_url(f"/{username}/pictures/{f.name}", 600)
```

`/{username}/pictures` directories will be automatically created inside `upload_dir` if not exist.
///

### Upload storage

Notice the usage of `page.get_upload_url()` method - it generates a presigned upload URL for Flet's internal upload storage.

/// admonition | Use any storage for file uploads
    type: note
You can [generate presigned upload URL](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html#generating-a-presigned-url-to-upload-a-file) for AWS S3 storage using boto3 library.

The same technique should work for [Wasabi](https://wasabi.com/), [Backblaze](https://www.backblaze.com/), [MinIO](https://min.io/) and any other  storage providers with S3-compatible API.
///

To enable Flet saving uploaded files to a directory provide full or relative path to that directory in `flet.app()` call:

```python
ft.run(main, upload_dir="uploads")
```

You can even put uploads inside "assets" directory, so uploaded files, e.g. pictures, docs or other media, can be accessed from a Flet client right away:

```python
ft.run(main, assets_dir="assets", upload_dir="assets/uploads")
```

and somewhere in your app you can display uploaded picture with:

```python
page.add(ft.Image(src="/uploads/<some-uploaded-picture.png>"))
```

### Upload progress

Once `FilePicker.upload()` method is called Flet client asynchronously starts uploading selected files one-by-one
and reports the progress via `FilePicker.on_upload` callback.

Event object of `on_upload` event is an instance of `FilePickerUploadEvent` class with the following fields:

* `file_name`
* `progress` - a value from `0.0` to `1.0`.
* `error`

The callback is called at least twice for every uploaded file: with `0` progress before upload begins
and with `1.0` progress when upload is finished. For files larger than 1 MB a progress is additionally
reported for every 10% uploaded.

The following example demonstrates multiple file uploads:

```python
--8<-- https://raw.githubusercontent.com/flet-dev/flet/refs/heads/main/sdk/python/examples/controls/file-picker/pick-and-upload.py
```

![File picker multiple uploads](https://raw.githubusercontent.com/flet-dev/flet/main/sdk/python/examples/controls/file-picker/media/pick-and-upload.png){width="80%"}
/// caption
///

See [`FilePicker`][flet.FilePicker] control docs for all its properties and examples.
