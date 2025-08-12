from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.service import Service

__all__ = [
    "FilePicker",
    "FilePickerFile",
    "FilePickerFileType",
    "FilePickerUploadEvent",
    "FilePickerUploadFile",
]


class FilePickerFileType(Enum):
    """
    Defines the file types that can be selected using the
    [`FilePicker`][flet.FilePicker].
    """

    ANY = "any"
    """
    Allows any file type.
    """

    MEDIA = "media"
    """
    A combination of [`VIDEO`][flet.FilePickerFileType.VIDEO] and
    [`IMAGE`][flet.FilePickerFileType.IMAGE].
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

    async def upload(self, files: list[FilePickerUploadFile]):
        """
        Uploads selected files to specified upload URLs.

        Before calling this method,
        [`pick_files()`][flet.FilePicker.pick_files]
        must be called, so that the internal file picker selection is not empty.

        Args:
            files: A list of [`FilePickerUploadFile`][flet.FilePickerUploadFile], where
                each item specifies which file to upload, and where
                (with PUT or POST).
        """
        await self._invoke_method(
            "upload",
            {"files": files},
        )

    async def get_directory_path(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ) -> Optional[str]:
        """
        Selects a directory and returns its absolute path.

        Args:
            dialog_title: The title of the dialog window. Defaults to [`FilePicker.
            initial_directory: The initial directory where the dialog should open.

        Raises:
            NotImplementedError: if called in web app.
        """
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_directory_path is not supported on web"
            )

        return await self._invoke_method(
            "get_directory_path",
            {
                "dialog_title": dialog_title,
                "initial_directory": initial_directory,
            },
            timeout=3600,
        )

    async def save_file(
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
            src_bytes: The contents of a file. Must be provided in web,
                iOS or Android modes.
            allowed_extensions: The allowed file extensions. Has effect only if
                `file_type` is
                [`FilePickerFileType.CUSTOM`][flet.FilePickerFileType.CUSTOM].

        Note:
            - On desktop this method only opens a dialog for the user to select
              a location and file name, and returns the chosen path. The file
              itself is not created or saved.

        Raises:
            ValueError: if `src_bytes` is not provided in web, iOS or Android modes.
            ValueError: if `file_name` is not provided in web mode.
        """

        if (self.page.web or self.page.platform.is_mobile()) and not src_bytes:
            raise ValueError(
                '"src_bytes" is required when saving a file on Web, Android and iOS.'
            )
        if self.page.web and not file_name:
            raise ValueError('"file_name" is required when saving a file on Web.')

        return await self._invoke_method(
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

    async def pick_files(
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
                `file_type` is
                [`FilePickerFileType.CUSTOM`][flet.FilePickerFileType.CUSTOM].
        """
        files = await self._invoke_method(
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
