from dataclasses import MISSING, dataclass, field
from typing import TYPE_CHECKING, Any, Optional, TypeVar, Union

from flet.controls.context import context
from flet.controls.services.service import Service
from flet.controls.types import Url, UrlTarget

if TYPE_CHECKING:
    from flet.controls.services.file_picker import FilePicker, FilePickerFileType

__all__ = [
    "ClientAction",
    "CopyToClipboard",
    "OpenUrl",
    "PickFiles",
    "ShareText",
]

S = TypeVar("S", bound=Service)


def _shared_service(service_type: type[S]) -> S:
    """
    Returns the page's single instance of `service_type`, creating it on first use.

    Client actions are attached to controls, so a page can easily hold dozens of
    them. Instantiating a service per action would register a service per action
    with the client for no benefit, since these services carry no per-action
    state.
    """
    page = context.page
    services = page._internals.setdefault("client_action_services", {})
    service = services.get(service_type)
    if service is None:
        service = service_type()
        services[service_type] = service
    return service


def _action_field(default: Any = MISSING):
    """
    Declares a field that configures an action but is not sent to the client.

    Only `service_id`, `method` and `args` cross the wire; the properties users
    set are kept readable on the Python object without duplicating them into the
    payload. Omit `default` to make the field required.
    """
    if default is MISSING:
        return field(metadata={"skip": True})
    return field(default=default, metadata={"skip": True})


@dataclass
class ClientAction:
    """
    Base class for actions performed by the client, without a round trip to your
    Python code.

    Assign one - or a list of them - to the `action` property of a control such
    as :class:`~flet.Button`, and it runs the moment the control is activated.

    Browsers only allow a page to open a file picker, write to the clipboard,
    show a share sheet or open a new tab while the user's click or key press is
    still being handled. Sending the click to your Python code and acting on the
    reply takes longer than that permission lasts, so on iOS Safari those
    operations are silently ignored, while Android and desktop browsers let them
    through. Client actions close that gap by performing the operation on the
    client, inside the original gesture.

    Because an action runs before your code sees the click, its arguments have to
    be known in advance. To act on a value that is only computed at click time,
    set it on the control ahead of the click instead.

    Note:
        Actions are not constructed directly - use one of the subclasses, such as
        :class:`~flet.OpenUrl`.
    """

    service_id: int = field(init=False, default=0)
    """
    Internal id of the service that performs this action on the client.
    """

    method: str = field(init=False, default="")
    """
    Name of the service method invoked on the client.
    """

    args: dict[str, Any] = field(init=False, default_factory=dict)
    """
    Arguments passed to :attr:`method`.
    """

    _service: Optional[Service] = field(
        init=False, default=None, repr=False, metadata={"skip": True}
    )

    def _bind(self, service: Service, method: str, args: dict[str, Any]) -> None:
        """
        Targets this action at `method` of `service`.

        Holding on to `service` matters: the page drops services that nothing
        references any more, and an action outlives the call that created it.
        """
        self._service = service
        self.service_id = service._i
        self.method = method
        self.args = {k: v for k, v in args.items() if v is not None}


@dataclass
class OpenUrl(ClientAction):
    """
    Opens a URL when the control is activated.

    Equivalent to :meth:`flet.UrlLauncher.launch_url`, but performed by the
    client inside the user's gesture, so that opening a new tab is not blocked as
    an unsolicited popup.

    Example:
        ```python
        ft.Button(
            "Open flet.dev",
            action=ft.OpenUrl("https://flet.dev", target=ft.UrlTarget.BLANK),
        )
        ```
    """

    url: str = _action_field()
    """
    The URL to open.
    """

    target: Optional[Union[UrlTarget, str]] = _action_field(None)
    """
    Where to open the URL, for example :attr:`flet.UrlTarget.BLANK` for a new tab.

    Web-only; ignored on other platforms.
    """

    def __post_init__(self) -> None:
        from flet.controls.services.url_launcher import UrlLauncher

        self._bind(
            _shared_service(UrlLauncher),
            "launch_url",
            {"url": Url(url=self.url, target=self.target)},
        )


@dataclass
class CopyToClipboard(ClientAction):
    """
    Copies text to the clipboard when the control is activated.

    Equivalent to :meth:`flet.Clipboard.set`, but performed by the client inside
    the user's gesture, which is the only time Safari permits a page to write to
    the clipboard.

    Example:
        ```python
        ft.Button("Copy token", action=ft.CopyToClipboard(token))
        ```
    """

    data: str = _action_field()
    """
    The text to copy.

    Must be known before the control is activated. To copy something computed at
    click time, assign it to this action ahead of the click.
    """

    def __post_init__(self) -> None:
        from flet.controls.services.clipboard import Clipboard

        self._bind(_shared_service(Clipboard), "set", {"data": self.data})


@dataclass
class PickFiles(ClientAction):
    """
    Opens a file picker dialog when the control is activated.

    Equivalent to :meth:`flet.FilePicker.pick_files`, but performed by the
    client inside the user's gesture, which is the only time a browser opens a
    file picker. This is what makes file picking work in a web app on iOS.

    Unlike `pick_files()`, the selection is not returned to the caller - it
    arrives at :attr:`flet.FilePicker.on_result`. The files stay associated with
    `file_picker`, so they can be passed straight to
    :meth:`flet.FilePicker.upload`.

    Example:
        ```python
        picker = ft.FilePicker(on_result=handle_result)
        page.services.append(picker)

        ft.Button("Upload", action=ft.PickFiles(picker, allow_multiple=True))
        ```
    """

    file_picker: "FilePicker" = _action_field()
    """
    The :class:`~flet.FilePicker` that opens the dialog and reports the result
    through its :attr:`~flet.FilePicker.on_result` event.
    """

    dialog_title: Optional[str] = _action_field(None)
    """
    The title of the dialog window.
    """

    initial_directory: Optional[str] = _action_field(None)
    """
    The initial directory where the dialog should open.
    """

    file_type: Optional["FilePickerFileType"] = _action_field(None)
    """
    The file types allowed to be selected.
    """

    allowed_extensions: Optional[list[str]] = _action_field(None)
    """
    The allowed file extensions. Has effect only if :attr:`file_type` is
    :attr:`flet.FilePickerFileType.CUSTOM`.
    """

    allow_multiple: bool = _action_field(False)
    """
    Allow the selection of multiple files at once.
    """

    with_data: bool = _action_field(False)
    """
    Read selected file contents into :attr:`flet.FilePickerFile.bytes`.
    """

    compression_quality: int = _action_field(0)
    """
    Image compression quality from `0` to `100`. `0` disables compression.
    """

    cancel_upload_on_window_blur: bool = _action_field(True)
    """
    Web-only. Whether to treat browser window blur as a cancelled selection.
    """

    def __post_init__(self) -> None:
        from flet.controls.services.file_picker import FilePickerFileType

        self._bind(
            self.file_picker,
            "pick_files",
            {
                "dialog_title": self.dialog_title,
                "initial_directory": self.initial_directory,
                "file_type": self.file_type or FilePickerFileType.ANY,
                "allowed_extensions": self.allowed_extensions,
                "allow_multiple": self.allow_multiple,
                "with_data": self.with_data,
                "compression_quality": self.compression_quality,
                "cancel_upload_on_window_blur": self.cancel_upload_on_window_blur,
            },
        )


@dataclass
class ShareText(ClientAction):
    """
    Opens the platform share sheet with text when the control is activated.

    Equivalent to :meth:`flet.Share.share_text`, but performed by the client
    inside the user's gesture, which is the only time a browser permits
    `navigator.share`.

    The share result is not reported back - use
    :meth:`flet.Share.share_text` if you need it, keeping in mind that it does
    not work on the web on iOS.

    Example:
        ```python
        ft.Button(
            "Share",
            action=ft.ShareText("Check out Flet", subject="Flet"),
        )
        ```
    """

    text: str = _action_field()
    """
    The text to share.
    """

    title: Optional[str] = _action_field(None)
    """
    Title shown in the share sheet.
    """

    subject: Optional[str] = _action_field(None)
    """
    Subject used by targets that support one, such as email.
    """

    def __post_init__(self) -> None:
        from flet.controls.services.share import Share, _share_args

        self._bind(
            _shared_service(Share),
            "share_text",
            _share_args(text=self.text, title=self.title, subject=self.subject),
        )
