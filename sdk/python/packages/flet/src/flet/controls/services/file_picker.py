import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
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
    Defines the file types that can be selected using the [`FilePicker`][flet.FilePicker].
    """

    ANY = "any"
    """
    Allows any file type.
    """

    MEDIA = "media"
    """
    A combination of [`VIDEO`][flet.FilePickerFileType.VIDEO] and [`IMAGE`][flet.FilePickerFileType.IMAGE].
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
    Allows only the custom file types specified in the `allowed_extensions` list.
    """


@dataclass
class FilePickerUploadFile:
    upload_url: str
    method: str = "PUT"
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
    Full path to a file.

    Note:
        Works for desktop and mobile only. Will be `None` on web.
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

    Danger: Important
        In Linux, the FilePicker control depends on
        [Zenity](https://help.gnome.org/users/zenity/stable/) when running Flet
        as an app. This is not a requirement when running Flet in a browser.

        To install Zenity on Ubuntu/Debian run the following commands:
        ```bash
        sudo apt-get install zenity
        ```
    """

    on_upload: Optional[EventHandler[FilePickerUploadEvent]] = None
    """
    Called when a file upload progress is updated.
    """

    async def upload_async(self, files: list[FilePickerUploadFile]):
        """
        Uploads selected files to specified upload URLs.

        Before calling this method, [`pick_files_async()`][flet.FilePicker.pick_files_async]
        must be called, so that the internal file picker selection is not empty.

        Args:
            files: A list of [`FilePickerUploadFile`][flet.FilePickerUploadFile], where
                each item specifies which file to upload, and where (with PUT or POST).
        """
        await self._invoke_method_async(
            "upload",
            {"files": files},
        )

    def upload(self, files: list[FilePickerUploadFile]):
        """
        Uploads selected files to specified upload URLs.

        Before calling this method, [`pick_files_async()`][flet.FilePicker.pick_files_async]
        must be called, so that the internal file picker selection is not empty.

        Args:
            files: A list of [`FilePickerUploadFile`][flet.FilePickerUploadFile], where
                each item specifies which file to upload, and where (with PUT or POST).
        """
        asyncio.create_task(self.upload_async(files))

    async def get_directory_path_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ) -> Optional[str]:
        """
        Selects a directory and returns its absolute path.

        Args:
            dialog_title: The title of the dialog window. Defaults to [`FilePicker.
            initial_directory: The initial directory where the dialog should open.
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

        Args:
            dialog_title: The title of the dialog window.
            file_name: The default file name.
            initial_directory: The initial directory where the dialog should open.
            file_type: The file types allowed to be selected.
            src_bytes: TBA
            allowed_extensions: The allowed file extensions. Has effect only if
                `file_type` is [`FilePickerFileType.CUSTOM`][flet.FilePickerFileType.CUSTOM].

        Note:
            - This method only opens a dialog for the user to select a location and file name,
            and returns the chosen path. The file itself is not created or saved.
            - This method is only available on desktop platforms (Linux, macOS & Windows).

        Info: Saving a file on web
            To save a file from the web, you actually don't need to use a `FilePicker`.

            You can instead provide an API endpoint `/download/:filename` that returns the
            file content, and then use
            [`page.launch_url`][flet.Page.launch_url] to open the url, which
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

        Args:
            dialog_title: The title of the dialog window.
            initial_directory: The initial directory where the dialog should open.
            file_type: The file types allowed to be selected.
            allow_multiple: Allow the selection of multiple files at once.
            allowed_extensions: The allowed file extensions. Has effect only if
                `file_type` is [`FilePickerFileType.CUSTOM`][flet.FilePickerFileType.CUSTOM].
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
