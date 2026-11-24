"""Fixtures shared by the notifications tests."""

from types import SimpleNamespace

import pytest

import flet as ft
from flet_notifications import Notifications


@pytest.fixture(autouse=True)
def client_platform(monkeypatch):
    """
    Platform of the client for services that aren't on a page.

    Android supports every platform-specific method except
    `update_windows_progress()`. Tests can change `platform` and `web`.
    """
    client = SimpleNamespace(web=False, platform=ft.PagePlatform.ANDROID)
    get_page = Notifications.page.fget

    def page(self):
        try:
            return get_page(self)
        except RuntimeError:
            return client

    monkeypatch.setattr(Notifications, "page", property(page))
    return client
