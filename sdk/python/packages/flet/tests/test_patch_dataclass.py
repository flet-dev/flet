from dataclasses import dataclass

from flet.core.padding import Padding
from flet.core.page import Page, PageMediaData
from flet.core.types import Brightness
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.utils import patch_dataclass


def test_simple_patch_dataclass():
    @dataclass
    class Config:
        retries: int
        timeout: float

    @dataclass
    class AppSettings:
        debug: bool
        config: Config

    settings = AppSettings(debug=False, config=Config(retries=3, timeout=1.0))

    patch = {"debug": True, "config": {"timeout": 2.5}}

    patch_dataclass(settings, patch)

    assert settings.debug == True
    assert isinstance(settings.config, Config)
    assert settings.config.timeout == 2.5


def test_page_patch_dataclass():
    page = Page(sess=Session(conn=Connection()))

    assert page.window.width is None
    assert page.window.height is None
    assert page.debug is False

    patch_dataclass(
        page,
        {
            "pwa": False,
            "web": False,
            "debug": True,
            "window": {
                "maximized": False,
                "minimized": False,
                "full_screen": False,
                "always_on_top": False,
                "focused": True,
                "visible": True,
                "width": 800.0,
                "height": 628.0,
                "top": 232.0,
                "left": -1360.0,
                "opacity": 1.0,
            },
            "platform_brightness": "light",
            "media": {
                "padding": {"top": 0.0, "right": 0.0, "bottom": 0.0, "left": 0.0},
                "view_padding": {"top": 0.0, "right": 0.0, "bottom": 0.0, "left": 0.0},
                "view_insets": {"top": 0.0, "right": 0.0, "bottom": 0.0, "left": 0.0},
            },
            "width": 800.0,
            "height": 600.0,
            "route": "/",
            "platform": "macos",
        },
    )
    print(page)
    assert page.window.width == 800.0
    assert page.window.height == 628.0
    assert page.debug is True
    assert page._prev_debug is True
    assert page.platform_brightness == Brightness.LIGHT
    assert page._prev_platform_brightness == Brightness.LIGHT
    assert isinstance(page.media, PageMediaData)
    assert isinstance(page.media.padding, Padding)
    assert isinstance(page.media.view_insets, Padding)
    assert isinstance(page.media.view_padding, Padding)
    assert page.media.padding._prev_left == 0
    assert page.media.view_insets._prev_top == 0
