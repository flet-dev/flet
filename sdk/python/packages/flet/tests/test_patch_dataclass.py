from dataclasses import dataclass

import msgpack

from flet.controls.base_control import BaseControl
from flet.controls.base_page import PageMediaData
from flet.controls.object_patch import ObjectPatch
from flet.controls.padding import Padding
from flet.controls.page import Page
from flet.controls.types import Brightness, PagePlatform
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub
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

    assert settings.debug
    assert isinstance(settings.config, Config)
    assert settings.config.timeout == 2.5


def test_page_patch_dataclass():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))

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

    # 1 -calculate diff
    patch, added_controls, removed_controls = ObjectPatch.from_diff(
        None, page, control_cls=BaseControl
    )

    # 2 - convert patch to hierarchy
    graph_patch = patch.to_message()
    print("Patch 1:", graph_patch)

    msg = msgpack.packb(
        graph_patch, default=configure_encode_object_for_msgpack(BaseControl)
    )

    print("Message 1:", msg)

    # print(page)
    assert page.window.width == 800.0
    assert page.window.height == 628.0
    assert page.debug is True
    # assert page._prev_debug is True
    assert page.platform_brightness == Brightness.LIGHT
    # assert page._prev_platform_brightness == Brightness.LIGHT
    print("page.media:", page.media)
    assert isinstance(page.media, PageMediaData)
    assert isinstance(page.media.padding, Padding)
    assert isinstance(page.media.view_insets, Padding)
    assert isinstance(page.media.view_padding, Padding)
    # assert page.media.padding._prev_left == 0.0
    # assert page.media.view_insets._prev_top == 0.0
    assert page.platform == PagePlatform.MACOS

    # 1 -calculate diff
    patch, _, _ = ObjectPatch.from_diff(page, page, control_cls=BaseControl)

    # 2 - convert patch to hierarchy
    graph_patch = patch.to_message()
    print("PATCH 1:", graph_patch)

    assert graph_patch == [[0]]

    page.media.padding.left = 1
    page.platform_brightness = Brightness.DARK
    page.window.width = 1024
    page.window.height = 768

    # 1 -calculate diff
    patch, _, _ = ObjectPatch.from_diff(page, page, control_cls=BaseControl)

    # 2 - convert patch to hierarchy
    graph_patch = patch.to_message()
    print("PATCH 2:", graph_patch)

    # TODO - fix tests
    # assert graph_patch["window"]["width"] == 1024
    # assert graph_patch["platform_brightness"] == Brightness.DARK
    # assert graph_patch["media"]["padding"]["left"] == 1

    msg = msgpack.packb(
        graph_patch, default=configure_encode_object_for_msgpack(BaseControl)
    )

    print("Message 2:", msg)
