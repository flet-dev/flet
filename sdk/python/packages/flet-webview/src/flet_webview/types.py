from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

import flet as ft

if TYPE_CHECKING:
    from flet_webview.webview import WebView  # noqa

__all__ = [
    "JavaScriptMode",
    "LogLevelSeverity",
    "RequestMethod",
    "WebViewConsoleMessageEvent",
    "WebViewJavaScriptEvent",
    "WebViewScrollEvent",
]


class RequestMethod(Enum):
    """Defines the supported HTTP methods for loading a page in a `WebView`."""

    GET = "get"
    """HTTP GET method."""

    POST = "post"
    """HTTP POST method."""


class LogLevelSeverity(Enum):
    """Represents the severity of a JavaScript log message."""

    ERROR = "error"
    """
    Indicates an error message was logged via an "error" event of the
    `console.error` method.
    """

    WARNING = "warning"
    """Indicates a warning message was logged using the `console.warning` method."""

    DEBUG = "debug"
    """Indicates a debug message was logged using the `console.debug` method."""

    INFO = "info"
    """Indicates an informational message was logged using the `console.info` method."""

    LOG = "log"
    """Indicates a log message was logged using the `console.log` method."""


class JavaScriptMode(Enum):
    """Defines the state of JavaScript support in the `WebView`."""

    UNRESTRICTED = "unrestricted"
    """JavaScript execution is unrestricted."""

    DISABLED = "disabled"
    """JavaScript execution is disabled."""


@dataclass
class WebViewScrollEvent(ft.Event["WebView"]):
    x: float
    """
    The value of the horizontal offset with the origin being at the
    leftmost of the `WebView`.
    """

    y: float
    """
    The value of the vertical offset with the origin being at the
    topmost of the `WebView`.
    """


@dataclass
class WebViewConsoleMessageEvent(ft.Event["WebView"]):
    message: str
    """The message written to the console."""

    severity_level: LogLevelSeverity
    """The severity of a JavaScript log message."""


@dataclass
class WebViewJavaScriptEvent(ft.Event["WebView"]):
    message: str
    """The message to be displayed in the window."""

    url: str
    """The URL of the page requesting the dialog."""
