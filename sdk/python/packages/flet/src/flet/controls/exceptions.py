__all__ = [
    "FletException",
    "FletUnsupportedPlatformException",
    "FletUnimplementedPlatformException",
    "FletPageDisconnectedException",
]


class FletException(Exception):
    """
    Base class for all Flet exceptions.

    See these subclasses/implementations:

    - [`FletUnsupportedPlatformException`][flet.FletUnsupportedPlatformException]
    - [`FletUnimplementedPlatformException`][flet.FletUnimplementedPlatformException]
    - [`FletPageDisconnectedException`][flet.FletPageDisconnectedException]
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
