---
class_name: flet.FilePicker
examples: ../../examples/services/file_picker
example_images: ../examples/services/file_picker/media
---

{{ class_summary(class_name) }}

## Usage

Create an instance of `FilePicker`:

```python
import flet as ft

file_picker = ft.FilePicker()
```

To open the file picker dialog call one of these three methods:
[`pick_files()`][flet.FilePicker.pick_files], [`save_file()`][flet.FilePicker.save_file]
or [`get_directory_path()`][flet.FilePicker.get_directory_path], depending on the use case.

In most cases you can use a lambda function for that:

```python
ft.Button(
    content="Pick files,
    on_click=lambda _: file_picker.pick_files(allow_multiple=True)
)
```

### Uploading files

To upload one or more files, call [`FilePicker.pick_files()`][flet.FilePicker.pick_files]
to let the user select files, then pass the returned list to
[`FilePicker.upload()`][flet.FilePicker.upload] to perform the upload.

/// admonition | Separate uploads per user
    type: note
If you need to separate uploads for each user you can specify a filename
prepended with any number of directories in
[`page.get_upload_url()`][flet.Page.get_upload_url] call, for example:

```python
upload_url = page.get_upload_url(f"/{username}/pictures/{f.name}", 600)
```

`/{username}/pictures` directories will be automatically created inside `upload_dir` if non-existent.
///

### Upload storage

Notice the usage of [`page.get_upload_url()`][flet.Page.get_upload_url] method –
it generates a presigned upload URL for Flet's internal upload storage.

/// admonition | Use any storage for file uploads
    type: note
You can [generate presigned upload URL](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html#generating-a-presigned-url-to-upload-a-file)
for AWS S3 storage using boto3 library.

The same technique should work for [Wasabi](https://wasabi.com/), [Backblaze](https://www.backblaze.com/),
[MinIO](https://min.io/) and any other storage providers with S3-compatible API.
///

To enable Flet saving uploaded files to a directory provide a full or
relative path to that directory in `flet.run()` call:

```python
ft.run(main, upload_dir="uploads")
```

You can even put uploads inside [assets](../cookbook/assets.md) directory,
so uploaded files, e.g. pictures, docs, or other media,
can be accessed from a Flet client right away:

```python
ft.run(main, assets_dir="assets", upload_dir="assets/uploads")
```

and in your app you can display the uploaded picture with:

```python
ft.Image(src="/uploads/<some-uploaded-picture.png>")
```

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/filepicker)

### Pick, save, and get directory paths

```python
--8<-- "{{ examples }}/pick_save_and_get_directory_path.py"
```

{{ image(example_images + "/pick_save_and_get_directory_path.png", width="80%") }}


### Pick and upload files

The following example demonstrates multi-file [pick][flet.FilePicker.pick_files]
and [upload][flet.FilePicker.upload] app.

```python
--8<-- "{{ examples }}/pick_and_upload.py"
```

{{ image(example_images + "/pick_and_upload.png", width="80%") }}

### Pick text content and save/download it

Use [`pick_files()`][flet.FilePicker.pick_files] with `with_data=True` when
you need file contents directly, such as in web apps where
[`FilePickerFile.path`][flet.FilePickerFile.path] is not available.

```python
--8<-- "{{ examples }}/pick_and_save_text_content.py"
```


{{ class_members(class_name) }}
