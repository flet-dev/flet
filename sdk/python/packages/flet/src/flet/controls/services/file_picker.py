import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, OptionalEventHandler
from flet.controls.services.service import Service

__all__ = [
    "FilePicker",
    "FilePickerUploadEvent",
    "FilePickerFileType",
    "FilePickerUploadFile",
    "FilePickerFile",
]


class FilePickerFileType(Enum):
    """
    Defines the file types that can be selected using the
    [FilePicker](https://flet.dev/docs/controls/filepicker).
    """

    ANY = "any"
    """
    Allows any file type.
    """

    MEDIA = "media"
    """
    A combination of `VIDEO` and `IMAGE`.
    """

    IMAGE = "image"
    """
    Allows only image files.
    """

    VIDEO = "video"
    """
    Allows only video files.
    """

    AUDIO = "audio"
    """
    Allows only audio files.
    """

    CUSTOM = "custom"
    """
    Allows only the custom file types specified in the
    [allowed_extensions](https://flet.dev/docs/controls/filepicker) list.
    """


@dataclass
class FilePickerUploadFile:
    upload_url: str
    method: str = field(default="PUT")
    id: Optional[int] = None
    name: Optional[str] = None


@dataclass
class FilePickerFile:
    id: int
    """
    TBD
    """

    name: str
    """
    File name without a path.
    """

    size: int
    """
    File size in bytes.
    """

    path: Optional[str] = None
    """
    Full path to a file. Works for desktop and mobile only. `None` on web.
    """


@dataclass
class FilePickerUploadEvent(Event["FilePicker"]):
    file_name: str
    """
    The name of the uploaded file.
    """

    progress: Optional[float] = None
    """
    A value from `0.0` to `1.0` representing the progress of the upload.
    """

    error: Optional[str] = None
    """
    An error message if the upload failed.
    """


@control("FilePicker")
class FilePicker(Service):
    """
    A control that allows you to use the native file explorer to pick single
    or multiple files, with extensions filtering support and upload.

    Online docs: https://flet.dev/docs/controls/filepicker
    """

    on_upload: OptionalEventHandler[FilePickerUploadEvent] = None
    """
    Fires when a file upload progress is updated.

    Event object is an instance of 
    [FilePickerUploadEvent](https://flet.dev/docs/reference/types/filepickeruploadevent).
    """

    async def upload_async(self, files: list[FilePickerUploadFile]):
        """
        Uploads selected files to specified upload URLs.

        Before calling `upload()` [pick_files()](https://flet.dev/docs/controls/filepicker#pick_files)
        must be called, so the internal file picker selection is not empty.

        Method arguments:
        - `files` - a list of
        [FilePickerUploadFile](https://flet.dev/docs/reference/types/filepickeruploadfile).
        Each item specifies which file to upload, and where (with PUT or POST).
        """
        await self._invoke_method_async(
            "upload",
            {"files": files},
        )

    def upload(self, files: list[FilePickerUploadFile]):
        """
        Uploads selected files to specified upload URLs.

        Before calling `upload()` [pick_files()](https://flet.dev/docs/controls/filepicker#pick_files)
        must be called, so the internal file picker selection is not empty.

        Method arguments:
        - `files` - a list of
        [FilePickerUploadFile](https://flet.dev/docs/reference/types/filepickeruploadfile).
        Each item specifies which file to upload, and where (with PUT or POST).
        """
        asyncio.create_task(self.upload_async(files))

    async def get_directory_path_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ) -> Optional[str]:
        """
        Selects a directory and returns its absolute path.

        You could either set the following file picker properties or provide their
        values in the method call:

        * `dialog_title` - the title of the dialog window.
        * `initial_directory` - the initial directory where the dialog should open.
        """
        return await self._invoke_method_async(
            "get_directory_path",
            {
                "dialog_title": dialog_title,
                "initial_directory": initial_directory,
            },
            timeout=3600,
        )

    async def save_file_async(
        self,
        dialog_title: Optional[str] = None,
        file_name: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[list[str]] = None,
        src_bytes: Optional[bytes] = None,
    ) -> Optional[str]:
        """
        Opens a save file dialog which lets the user select a file path and a file name
        to save a file.

        This function does not actually save a file. It only opens the dialog to let
        the user choose a location and file name. This function only returns the path
        to this (non-existing) file in `FilePicker.result.path` property.

        This method is only available on desktop platforms (Linux, macOS & Windows).

        You could either set the following file picker properties or provide their
        values in the method call:

        * `dialog_title` - the title of the dialog window.
        * `file_name` - the default file name.
        * `initial_directory` - the initial directory where the dialog should open.
        * `file_type` - the allowed
        [`FilePickerFileType`](https://flet.dev/docs/reference/types/filepickerfiletype).
        * `allowed_extensions` - the allowed file extensions. Has effect only if
        `file_type` is `FilePickerFileType.CUSTOM`.

        Info:
            To save a file from the web, you don't need to use the FilePicker object.

            You can instead provides an API endpoint `/download/:filename` that returns the
            file content, and then use
            [`page.launch_url`](/docs/controls/page#launch_urlurl) to open the url, which
            will trigger the browser's save file dialog.

            Take [FastAPI](https://flet.dev/docs/publish/web/dynamic-website#advanced-fastapi-scenarios)
            as an example, you can use the following code to implement the endpoint:

            ```python
            from fastapi import FastAPI, Response
            from fastapi.responses import FileResponse

            app = flet_fastapi.app(main)

            @app.get("/download/{filename}")
            def download(filename: str):
                path = prepare_file(filename)
                return FileResponse(path)
            ```

            and then use `page.launch_url("/download/myfile.txt")` to open the url, for
            instance, when a button is clicked.

            ```python
            ft.ElevatedButton(
                "Download myfile",
                on_click=lambda _: page.launch_url("/download/myfile.txt"),
            )
            ```
        """
        return await self._invoke_method_async(
            "save_file",
            {
                "dialog_title": dialog_title,
                "file_name": file_name,
                "initial_directory": initial_directory,
                "file_type": file_type,
                "allowed_extensions": allowed_extensions,
                "src_bytes": src_bytes,
            },
            timeout=3600,
        )

    async def pick_files_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[list[str]] = None,
        allow_multiple: bool = False,
    ) -> list[FilePickerFile]:
        """
        Retrieves the file(s) from the underlying platform.

        You could either set the following file picker properties or provide their
        values in the method call:

        * `dialog_title` - the title of the dialog window.
        * `initial_directory` - the initial directory where the dialog should open.
        * `file_type` - the allowed
        [`FilePickerFileType`](https://flet.dev/docs/reference/types/filepickerfiletype).
        * `allowed_extensions` - the allowed file extensions. Has effect only if
        `file_type` is `FilePickerFileType.CUSTOM`.
        * `allow_multiple` - allow selecting multiple files.
        """
        files = await self._invoke_method_async(
            "pick_files",
            {
                "dialog_title": dialog_title,
                "initial_directory": initial_directory,
                "file_type": file_type,
                "allowed_extensions": allowed_extensions,
                "allow_multiple": allow_multiple,
            },
            timeout=3600,
        )
        return [FilePickerFile(**file) for file in files]
