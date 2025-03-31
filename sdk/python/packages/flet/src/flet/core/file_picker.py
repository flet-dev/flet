import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, List, Optional

from flet.core.control import Control
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.types import OptionalEventCallable

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class FilePickerState(Enum):
    PICK_FILES = "pickFiles"
    SAVE_FILE = "saveFile"
    GET_DIRECTORY_PATH = "getDirectoryPath"


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


class FilePickerResultEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.path: Optional[str] = d.get("path")
        self.files: Optional[List[FilePickerFile]] = None
        files = d.get("files")
        if files is not None and isinstance(files, List):
            self.files = []
            for fd in files:
                self.files.append(FilePickerFile(**fd))


class FilePickerUploadEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.file_name: str = d.get("file_name")
        self.progress: Optional[float] = d.get("progress")
        self.error: Optional[str] = d.get("error")


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
        on_result: Optional[Callable[[FilePickerResultEvent], None]] = None,
        on_upload: Optional[Callable[[FilePickerUploadEvent], None]] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            data=data,
        )

        def convert_result_event_data(e):
            self.__result = FilePickerResultEvent(e)
            return self.__result

        self.__on_result = EventHandler(convert_result_event_data)
        self._add_event_handler("result", self.__on_result.get_handler())

        self.__on_upload = EventHandler(lambda e: FilePickerUploadEvent(e))
        self._add_event_handler("upload", self.__on_upload.get_handler())

        self.__result: Optional[FilePickerResultEvent] = None
        self.__upload: List[FilePickerUploadFile] = []
        self.__allowed_extensions: Optional[List[str]] = None
        self.__state = None
        self.__file_type = None
        self.on_result = on_result
        self.on_upload = on_upload

    def _get_control_name(self):
        return "filepicker"

    def before_update(self):
        super().before_update()
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
        self.state = FilePickerState.PICK_FILES
        self.dialog_title = dialog_title
        self.initial_directory = initial_directory
        self.file_type = file_type
        self.allowed_extensions = allowed_extensions
        self.allow_multiple = allow_multiple
        self.update()

    def save_file(
        self,
        dialog_title: Optional[str] = None,
        file_name: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: FilePickerFileType = FilePickerFileType.ANY,
        allowed_extensions: Optional[List[str]] = None,
    ):
        self.state = FilePickerState.SAVE_FILE
        self.dialog_title = dialog_title
        self.file_name = file_name
        self.initial_directory = initial_directory
        self.file_type = file_type
        self.allowed_extensions = allowed_extensions
        self.update()

    def get_directory_path(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ):
        self.state = FilePickerState.GET_DIRECTORY_PATH
        self.dialog_title = dialog_title
        self.initial_directory = initial_directory
        self.update()

    def upload(self, files: List[FilePickerUploadFile]):
        self.__upload = files
        self.update()

    # state
    @property
    def state(self) -> Optional[FilePickerState]:
        return self.__state

    @state.setter
    def state(self, value: Optional[FilePickerState]):
        self.__state = value
        self._set_enum_attr("state", value, FilePickerState)

    # result
    @property
    def result(self) -> Optional[FilePickerResultEvent]:
        return self.__result

    # dialog_title
    @property
    def dialog_title(self) -> Optional[str]:
        return self._get_attr("dialogTitle")

    @dialog_title.setter
    def dialog_title(self, value: Optional[str]):
        self._set_attr("dialogTitle", value)

    # file_name
    @property
    def file_name(self) -> Optional[str]:
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
        self._set_enum_attr("fileType", value, FilePickerFileType)

    # allowed_extensions
    @property
    def allowed_extensions(self) -> Optional[List[str]]:
        return self.__allowed_extensions

    @allowed_extensions.setter
    def allowed_extensions(self, value: Optional[List[str]]):
        self.__allowed_extensions = value

    # allow_multiple
    @property
    def allow_multiple(self) -> bool:
        return self._get_attr("allowMultiple", data_type="bool", def_value=False)

    @allow_multiple.setter
    def allow_multiple(self, value: Optional[bool]):
        self._set_attr("allowMultiple", value)

    # on_result
    @property
    def on_result(self) -> OptionalEventCallable[FilePickerResultEvent]:
        return self.__on_result.handler

    @on_result.setter
    def on_result(self, handler: OptionalEventCallable[FilePickerResultEvent]):
        self.__on_result.handler = handler

    # on_upload
    @property
    def on_upload(self):
        return self.__on_upload.handler

    @on_upload.setter
    def on_upload(self, handler: OptionalEventCallable[FilePickerUploadEvent]):
        self.__on_upload.handler = handler
