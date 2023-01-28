import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional, Union

from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.dropdown import Option
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

FileTypeString = Literal["any", "media", "image", "video", "audio", "custom"]
FilePickerState = Literal["pickFiles", "saveFile", "getDirectoryPath"]


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
    method: str = field(default="PUT")


@dataclass
class FilePickerFile:
    name: str
    path: str
    size: int


class FilePickerResultEvent(ControlEvent):
    def __init__(self, path, files) -> None:
        self.path: Optional[str] = path
        self.files: Optional[List[FilePickerFile]] = None
        if files is not None and isinstance(files, List):
            self.files = []
            for fd in files:
                self.files.append(FilePickerFile(**fd))


@dataclass
class FilePickerUploadEvent(ControlEvent):
    file_name: str
    progress: Optional[float]
    error: Optional[str]


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

    def __init__(
        self,
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        on_result=None,
        on_upload=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        def convert_result_event_data(e):
            d = json.loads(e.data)
            self.__result = FilePickerResultEvent(**d)
            return self.__result

        self.__on_result = EventHandler(convert_result_event_data)
        self._add_event_handler("result", self.__on_result.get_handler())

        def convert_upload_event_data(e):
            d = json.loads(e.data)
            return FilePickerUploadEvent(**d)

        self.__on_upload = EventHandler(convert_upload_event_data)
        self._add_event_handler("upload", self.__on_upload.get_handler())

        self.__result: Optional[FilePickerResultEvent] = None
        self.__upload: List[FilePickerUploadFile] = []
        self.__allowed_extensions: Optional[List[str]] = None
        self.on_result = on_result
        self.on_upload = on_upload

    def _get_control_name(self):
        return "filepicker"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("allowedExtensions", self.__allowed_extensions)
        self._set_attr_json("upload", self.__upload)

    def pick_files(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
        allow_multiple: Optional[bool] = False,
    ):
        self.state = "pickFiles"
        self.dialog_title = dialog_title
        self.initial_directory = initial_directory
        self.file_type = file_type
        self.allowed_extensions = allowed_extensions
        self.allow_multiple = allow_multiple
        self.update()

    async def pick_files_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
        allow_multiple: Optional[bool] = False,
    ):
        self.state = "pickFiles"
        self.dialog_title = dialog_title
        self.initial_directory = initial_directory
        self.file_type = file_type
        self.allowed_extensions = allowed_extensions
        self.allow_multiple = allow_multiple
        await self.update_async()

    def save_file(
        self,
        dialog_title: Optional[str] = None,
        file_name: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
    ):
        self.state = "saveFile"
        self.dialog_title = dialog_title
        self.file_name = file_name
        self.initial_directory = initial_directory
        self.file_type = file_type
        self.allowed_extensions = allowed_extensions
        self.update()

    async def save_file_async(
        self,
        dialog_title: Optional[str] = None,
        file_name: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
    ):
        self.state = "saveFile"
        self.dialog_title = dialog_title
        self.file_name = file_name
        self.initial_directory = initial_directory
        self.file_type = file_type
        self.allowed_extensions = allowed_extensions
        await self.update_async()

    def get_directory_path(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ):
        self.state = "getDirectoryPath"
        self.dialog_title = dialog_title
        self.initial_directory = initial_directory
        self.update()

    async def get_directory_path_async(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ):
        self.state = "getDirectoryPath"
        self.dialog_title = dialog_title
        self.initial_directory = initial_directory
        await self.update_async()

    def upload(self, files: List[FilePickerUploadFile]):
        self.__upload = files
        self.update()

    async def upload_async(self, files: List[FilePickerUploadFile]):
        self.__upload = files
        await self.update_async()

    # state
    @property
    def state(self) -> Optional[FilePickerState]:
        return self._get_attr("state")

    @state.setter
    def state(self, value: Optional[FilePickerState]):
        self._set_attr("state", value)

    # result
    @property
    def result(self) -> Optional[FilePickerResultEvent]:
        return self.__result

    # dialog_title
    @property
    def dialog_title(self):
        return self._get_attr("dialogTitle")

    @dialog_title.setter
    def dialog_title(self, value):
        self._set_attr("dialogTitle", value)

    # file_name
    @property
    def file_name(self):
        return self._get_attr("fileName")

    @file_name.setter
    def file_name(self, value: Optional[str]):
        self._set_attr("fileName", value)

    # initial_directory
    @property
    def initial_directory(self):
        return self._get_attr("initialDirectory")

    @initial_directory.setter
    def initial_directory(self, value: Optional[str]):
        self._set_attr("initialDirectory", value)

    # file_type
    @property
    def file_type(self) -> FilePickerFileType:
        return self.__file_type

    @file_type.setter
    def file_type(self, value: FilePickerFileType):
        self.__file_type = value
        if isinstance(value, FilePickerFileType):
            self._set_attr("fileType", value.value)
        else:
            self.__set_file_type(value)

    def __set_file_type(self, value: FileTypeString):
        self._set_attr("fileType", value)

    # allowed_extensions
    @property
    def allowed_extensions(self) -> Optional[List[str]]:
        return self.__allowed_extensions

    @allowed_extensions.setter
    def allowed_extensions(self, value: Optional[List[str]]):
        self.__allowed_extensions = value

    # allow_multiple
    @property
    def allow_multiple(self) -> Optional[bool]:
        return self._get_attr("allowMultiple", data_type="bool", def_value=False)

    @allow_multiple.setter
    def allow_multiple(self, value: Optional[bool]):
        self._set_attr("allowMultiple", value)

    # on_result
    @property
    def on_result(self):
        return self.__on_result

    @on_result.setter
    def on_result(self, handler):
        self.__on_result.subscribe(handler)

    # on_upload
    @property
    def on_upload(self):
        return self.__on_upload

    @on_upload.setter
    def on_upload(self, handler):
        self.__on_upload.subscribe(handler)
