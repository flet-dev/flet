__all__ = [
    "FletException",
    "FletPageDisconnectedException",
    "FletUnimplementedPlatformException",
    "FletUnsupportedPlatformException",
    "HostRequestError",
    "HostRequestRefused",
]


class FletException(Exception):
    """
    Base class for all Flet exceptions.

    See these subclasses/implementations:

    - :class:`~flet.FletUnsupportedPlatformException`
    - :class:`~flet.FletUnimplementedPlatformException`
    - :class:`~flet.FletPageDisconnectedException`
    - :class:`~flet.HostRequestError`
    - :class:`~flet.HostRequestRefused`
    """


class FletUnsupportedPlatformException(FletException):
    """
    Thrown by operations that are not supported on the current platform.
    """


class FletUnimplementedPlatformException(FletUnsupportedPlatformException):
    """
    Thrown by operations that have not been implemented yet.
    """


class FletPageDisconnectedException(FletException):
    """
    Thrown when the page is disconnected.
    """


class HostRequestError(FletException):
    """
    Raised by :meth:`Page.request_host() <flet.Page.request_host>` when the
    host app doesn't answer a request with a result.
    """

    def __init__(self, kind: str, message: str = ""):
        super().__init__(message or kind)
        self.kind = kind
        """
        What went wrong:

        - `"not_embedded"`: the app isn't embedded in another app;
        - `"unhandled"`: the host app doesn't handle requests, or not this one;
        - `"refused"`: the host app declined the request, for example because
          its user said no (it raised :class:`~flet.HostRequestRefused`);
        - `"failed"`: the host app failed to answer it, or the request was
          too large or one of too many;
        - `"timeout"`: the host app didn't answer in time.
        """
        self.message = message
        """
        A message from the host app, or about the failure. Never the host's
        traceback.
        """


class HostRequestRefused(FletException):
    """
    Raise from a [`FletApp.on_guest_request`][flet.FletApp.on_guest_request]
    handler to decline a request, for example when the user said no. The
    embedded app's :meth:`Page.request_host() <flet.Page.request_host>` raises
    :class:`~flet.HostRequestError` with `kind` `"refused"` and this message.
    """
