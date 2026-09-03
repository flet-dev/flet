from dataclasses import MISSING, dataclass, field
from typing import Any, Optional, TypeVar
from weakref import WeakKeyDictionary

from flet.controls.context import context
from flet.controls.services.service import Service

__all__ = ["ClientAction"]

S = TypeVar("S", bound=Service)


_shared_services: "WeakKeyDictionary[Any, dict[type, Service]]" = WeakKeyDictionary()
"""
Per-page cache of the services client actions target, keyed weakly so it does
not keep a finished page alive.

Deliberately not stored on the page itself: `BaseControl._internals` is sent to
the client (it is how `Button` ships its resolved style), and a cache keyed by
class would put a class object on the wire.
"""


def shared_service(service_type: type[S]) -> S:
    """
    Returns the page's single instance of `service_type`, creating it on first use.

    Internal, but shared: each action lives in its own service's module and calls
    this to reach a service the user never instantiated.

    Client actions are attached to controls, so a page can easily hold dozens of
    them. Instantiating a service per action would register a service per action
    with the client for no benefit, since these services carry no per-action
    state.
    """
    page = context.page
    services = _shared_services.setdefault(page, {})
    service = services.get(service_type)
    if service is None:
        service = service_type()
        services[service_type] = service
    return service


def action_field(default: Any = MISSING):
    """
    Declares a field that configures an action but is not sent to the client.

    Internal, but shared: used by the `ClientAction` subclasses, which live in
    the modules of the services they drive.

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
        Actions are not constructed directly - use one of the subclasses, each of
        which lives alongside the service it drives:
        :class:`~flet.OpenUrl`, :class:`~flet.CopyToClipboard`,
        :class:`~flet.PickFiles` and :class:`~flet.ShareText`.
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
