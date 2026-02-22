from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

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
    Defines the file types that can be selected using the [`FilePicker`][flet.].
    """

    ANY = "any"
    """
    Allows any file type.
    """

    MEDIA = "media"
    """
    A combination of [`VIDEO`][(c).] and [`IMAGE`][(c).].
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
    """
    Upload descriptor for one file selected by [`FilePicker`][flet.].

    Instances are passed to [`FilePicker.upload()`][flet.FilePicker.upload].
    During upload, Flet resolves the selected file by [`id`][(c).] first and,
    when `id` is absent or not found, falls back to [`name`][(c).].

    At least one of [`id`][(c).] or [`name`][(c).] should be provided.
    """

    upload_url: str
    """
    Upload destination URL.

    Can be an absolute URL or a page-relative URL returned by
    [`Page.get_upload_url()`][flet.Page.get_upload_url].
    """

    method: str = "PUT"
    """
    HTTP method used for the upload request, usually `PUT` or `POST`.
    """

    id: Optional[int] = None
    """
    Selected file identifier returned by
    [`FilePicker.pick_files()`][flet.FilePicker.pick_files].

    This is the preferred lookup key when both `id` and `name` are specified.
    """

    name: Optional[str] = None
    """
    Selected file name used as fallback lookup when [`id`][(c).] is missing
    or does not match any currently selected file.
    """


@dataclass
class FilePickerFile:
    """
    Metadata for a file selected via
    [`FilePicker.pick_files()`][flet.FilePicker.pick_files].

    Returned by [`FilePicker.pick_files()`][flet.FilePicker.pick_files] and
    used as input context for [`FilePickerUploadFile`][flet.FilePickerUploadFile]
    when uploading selected files.
    """

    id: int
    """
    Selection-scoped file identifier assigned by Flet.

    This value is stable for the current picker selection and is preferred for
    upload matching in [`FilePickerUploadFile`][flet.FilePickerUploadFile].
    """

    name: str
    """
    File name (basename), without directory path.
    """

    size: int
    """
    File size in bytes.
    """

    path: Optional[str] = None
    """
    Absolute path to the selected file, when available.

    Note:
        - Web mode always returns `None`.
        - On native platforms, this can still be `None` if the platform picker
            does not expose a filesystem path.
    """

    bytes: Optional[bytes] = None
    """
    File contents.

    Returned only when [`pick_files()`][flet.FilePicker.pick_files] is called with
    `with_data=True`. Otherwise this value is `None`.
    """


@dataclass
class FilePickerUploadEvent(Event["FilePicker"]):
    """
    Event emitted when a file is uploaded via \
    [`FilePicker.upload()`][flet.FilePicker.upload] method.
    """

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
    A control that allows you to use the native file explorer to pick single or \
    multiple files, with extensions filtering support and upload.

    Danger: Important
        On Linux, this control requires
        [Zenity](https://help.gnome.org/users/zenity/stable/) when running Flet
        as a desktop app. It is not required when running Flet in a browser.

        To install Zenity on Ubuntu/Debian run the following commands:
        ```bash
        sudo apt-get install zenity
        ```
    """

    on_upload: Optional[EventHandler[FilePickerUploadEvent]] = None
    """
    Called when a file is uploaded via [`upload()`][(c).upload] method.

    This callback is invoked at least twice for each uploaded file: once with `0.0`
    [`progress`][flet.FilePickerUploadEvent.] before the upload starts, and once with
    `1.0` [`progress`][flet.FilePickerUploadEvent.] when the upload completes.

    For files larger than 1 MB, additional progress events are emitted
    at every 10% increment (for example, `0.1`, `0.2`, ...).
    """

    async def upload(self, files: list[FilePickerUploadFile]):
        """
        Uploads picked files to specified upload URLs.

        Before calling this method, [`pick_files()`][(c).pick_files] first has to be
        called to ensure the internal file picker selection is not empty.

        Once called, Flet asynchronously starts uploading selected files
        one-by-one and reports the progress via [`on_upload`][(c).] event.

        Args:
            files: A list of [`FilePickerUploadFile`][flet.], where
                each item specifies which file to upload, and where
                (with `PUT` or `POST`).
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

        Returns:
            The selected directory path or `None` if the dialog was cancelled.

        Raises:
            FletUnsupportedPlatformException: If called in web mode.
        """
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_directory_path is not supported in web mode"
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
        Opens a save file dialog which lets the user select a file path and a file \
        name to save a file.

        Note:
            - On desktop this method only opens a dialog for the user to select
                a location and file name, and returns the chosen path. The file
                itself is not created or saved.

        Args:
            dialog_title: The title of the dialog window.
            file_name: The default file name.
            initial_directory: The initial directory where the dialog should open.
            file_type: The file types allowed to be selected.
            src_bytes: The contents of a file. Must be provided in web,
                iOS or Android modes.
            allowed_extensions: The allowed file extensions. Has effect only if
                `file_type` is
                [`FilePickerFileType.CUSTOM`][flet.].

        Raises:
            ValueError: If `src_bytes` is not provided, when called in web mode,
                on iOS or Android.
            ValueError: If `file_name` is not provided in web mode.
        """

        if (self.page.web or self.page.platform.is_mobile()) and not src_bytes:
            raise ValueError(
                '"src_bytes" is required when saving a file in web mode,'
                "or on mobile (Android & iOS)."
            )
        if self.page.web and not file_name:
            raise ValueError('"file_name" is required when saving a file in web mode.')

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
        with_data: bool = False,
    ) -> list[FilePickerFile]:
        """
        Opens a pick file dialog.

        Tip:
            To upload the picked files, pass them to [`upload()`][(c).upload] method,
            along with their upload URLs.

        Args:
            dialog_title: The title of the dialog window.
            initial_directory: The initial directory where the dialog should open.
            file_type: The file types allowed to be selected.
            allow_multiple: Allow the selection of multiple files at once.
            with_data: Read selected file contents into
                [`bytes`][flet.FilePickerFile.].
            allowed_extensions: The allowed file extensions. Has effect only if
                `file_type` is [`FilePickerFileType.CUSTOM`][flet.].

        Returns:
            A list of selected files.
        """
        files = await self._invoke_method(
            "pick_files",
            {
                "dialog_title": dialog_title,
                "initial_directory": initial_directory,
                "file_type": file_type,
                "allowed_extensions": allowed_extensions,
                "allow_multiple": allow_multiple,
                "with_data": with_data,
            },
            timeout=3600,
        )
        return [FilePickerFile(**self._normalize_file(file)) for file in files]

    def _normalize_file(self, file: dict[str, Any]) -> dict[str, Any]:
        value = file.get("bytes")
        if isinstance(value, list):
            file["bytes"] = bytes(value)
        return file
