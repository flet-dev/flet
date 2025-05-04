import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEvent
from flet.controls.services.service import Service
from flet.controls.types import OptionalEventCallable

__all__ = [
    "FilePicker",
    "FilePickerUploadEvent",
    "FilePickerFileType",
    "FilePickerUploadFile",
    "FilePickerFile",
]


class FilePickerFileType(Enum):
    ANY = "any"
    MEDIA = "media"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    CUSTOM = "custom"


@dataclass
class FilePickerUploadFile:
    upload_url: str
    method: str = field(default="PUT")
    id: Optional[int] = None
    name: Optional[str] = None


@dataclass
class FilePickerFile:
    id: int
    name: str
    size: int
    path: Optional[str] = None


@dataclass
class FilePickerUploadEvent(ControlEvent):
    file_name: str
    progress: Optional[float] = None
    error: Optional[str] = None


@control("FilePicker")
class FilePicker(Service):
    """
    A control that allows you to use the native file explorer to pick single
    or multiple files, with extensions filtering support and upload.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def pick_files_result(e: ft.FilePickerResultEvent):
            selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files
                else "Cancelled!"
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
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=True
                        ),
                    ),
                    selected_files,
                ]
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/filepicker
    """

    on_upload: OptionalEventCallable[FilePickerUploadEvent] = None

    def upload_async(self, files: list[FilePickerUploadFile]):
        return self._invoke_method_async(
            "upload",
            {"files": files},
        )

    def upload(self, files: list[FilePickerUploadFile]):
        asyncio.create_task(self.upload_async(files))

    def get_directory_path_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ):
        return self._invoke_method_async(
            "get_directory_path",
            {
                "dialog_title": dialog_title,
                "initial_directory": initial_directory,
            },
            timeout=3600,  # 1 hour
        )

    def save_file_async(
        self,
        dialog_title: Optional[str] = None,
        file_name: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[list[str]] = None,
    ):
        return self._invoke_method_async(
            "save_file",
            {
                "dialog_title": dialog_title,
                "file_name": file_name,
                "initial_directory": initial_directory,
                "file_type": file_type,
                "allowed_extensions": allowed_extensions,
            },
            timeout=3600,  # 1 hour
        )

    async def pick_files_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[list[str]] = None,
        allow_multiple: bool = False,
    ):
        files = await self._invoke_method_async(
            "pick_files",
            {
                "dialog_title": dialog_title,
                "initial_directory": initial_directory,
                "file_type": file_type,
                "allowed_extensions": allowed_extensions,
                "allow_multiple": allow_multiple,
            },
            timeout=3600,  # 1 hour
        )
        return [FilePickerFile(**file) for file in files]
