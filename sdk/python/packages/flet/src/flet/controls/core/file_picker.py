import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEvent
from flet.controls.types import OptionalEventCallable

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
__all__ = [
    "FilePicker",
    "FilePickerResultEvent",
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
    name: str
    upload_url: str
    id: int = None
    method: str = field(default="PUT")


@dataclass
class FilePickerFile:
    name: str
    path: str
    size: int
    id: int


@dataclass
class FilePickerResultEvent(ControlEvent):
    path: Optional[str]
    files: Optional[List[FilePickerFile]] = None


@dataclass
class FilePickerUploadEvent(ControlEvent):
    file_name: str
    progress: Optional[float] = None
    error: Optional[str] = None


@control("FilePicker")
class FilePicker(Control):
    """
    A control that allows you to use the native file explorer to pick single or multiple files, with extensions filtering support and upload.

    Example:
    ```
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

    on_result: OptionalEventCallable[FilePickerResultEvent] = None
    on_upload: OptionalEventCallable[FilePickerUploadEvent] = None

    # _result: Optional[FilePickerResultEvent] = field(init=False, repr=False)

    def before_update(self):
        super().before_update()

    # @property
    # def result(self) -> Optional[FilePickerResultEvent]:
    #     return self._result

    async def upload_async(self, files: List[FilePickerUploadFile]):
        await self._invoke_method_async(
            "upload",
            {
                # "files": [
                #     {
                #         "name": file.name,
                #         "upload_url": file.upload_url,
                #         "id": file.id,
                #         "method": file.method,
                #     }
                #     for file in files
                # ],
                "files": files
            },
        )

    def upload(self, files: List[FilePickerUploadFile]):
        asyncio.create_task(self.upload_async(files))

    async def get_directory_path_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ):
        await self._invoke_method_async(
            "get_directory_path",
            {
                "dialog_title": dialog_title,
                "initial_directory": initial_directory,
            },
        )

    def get_directory_path(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ):
        asyncio.create_task(
            self.get_directory_path_async(dialog_title, initial_directory)
        )

    async def save_file_async(
        self,
        dialog_title: Optional[str] = None,
        file_name: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
    ):
        await self._invoke_method_async(
            "save_file",
            {
                "dialog_title": dialog_title,
                "file_name": file_name,
                "initial_directory": initial_directory,
                "file_type": file_type,
                "allowed_extensions": allowed_extensions,
            },
        )

    def save_file(
        self,
        dialog_title: Optional[str] = None,
        file_name: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
    ):
        asyncio.create_task(
            self.save_file_async(
                dialog_title,
                file_name,
                initial_directory,
                file_type,
                allowed_extensions,
            )
        )

    async def pick_files_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
        allow_multiple: bool = False,
    ):
        await self._invoke_method_async(
            "pick_files",
            {
                "dialog_title": dialog_title,
                "initial_directory": initial_directory,
                "file_type": file_type,
                "allowed_extensions": allowed_extensions,
                "allow_multiple": allow_multiple,
            },
        )

    def pick_files(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
        allow_multiple: bool = False,
    ):
        asyncio.create_task(
            self.pick_files_async(
                dialog_title,
                initial_directory,
                file_type,
                allowed_extensions,
                allow_multiple,
            )
        )
