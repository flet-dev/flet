from dataclasses import field
from typing import Any

import flet as ft
from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet_secure_storage.options import (
    AndroidOptions,
    IOSOptions,
    MacOsOptions,
    WebOptions,
    WindowsOptions,
)
from flet_secure_storage.types import SecureStorageEvent


@control("SecureStorage")
class SecureStorage(Service):
    ios_options: IOSOptions = field(default_factory=lambda: IOSOptions())
    android_options: AndroidOptions = field(default_factory=lambda: AndroidOptions())
    windows_options: WindowsOptions = field(default_factory=lambda: WindowsOptions())
    macos_options: MacOsOptions = field(default_factory=lambda: MacOsOptions())
    web_options: WebOptions = field(default_factory=lambda: WebOptions())
    on_change: ft.EventHandler["SecureStorageEvent"] | None = None

    @property
    async def is_availability(self) -> bool | None:
        return await self._get_availability()

    async def _get_availability(self) -> bool | None:
        return self._invoke_method("get_availability")

    async def set(
        self,
        key: str,
        value: Any,
        web: WebOptions | None = None,
        ios: IOSOptions | None = None,
        macos: MacOsOptions | None = None,
        android: AndroidOptions | None = None,
        windows: WindowsOptions | None = None,
    ) -> None:
        if value is None:
            raise ValueError("value can't be None")
        return await self._invoke_method(
            method_name="set",
            arguments={
                "key": key,
                "value": value,
                "web": web,
                "ios": ios,
                "macos": macos,
                "android": android,
                "windows": windows,
            },
        )

    async def get(
        self,
        key: str,
        web: WebOptions | None = None,
        ios: IOSOptions | None = None,
        macos: MacOsOptions | None = None,
        android: AndroidOptions | None = None,
        windows: WindowsOptions | None = None,
    ) -> str | None:
        return await self._invoke_method(
            method_name="get",
            arguments={
                "key": key,
                "web": web,
                "ios": ios,
                "macos": macos,
                "android": android,
                "windows": windows,
            },
        )

    async def get_all(
        self,
        web: WebOptions | None = None,
        ios: IOSOptions | None = None,
        macos: MacOsOptions | None = None,
        android: AndroidOptions | None = None,
        windows: WindowsOptions | None = None,
    ) -> dict[str, Any]:
        return await self._invoke_method(
            method_name="get_all",
            arguments={
                "web": web,
                "ios": ios,
                "macos": macos,
                "android": android,
                "windows": windows,
            },
        )

    async def contains_key(
        self,
        key: str,
        web: WebOptions | None = None,
        ios: IOSOptions | None = None,
        macos: MacOsOptions | None = None,
        android: AndroidOptions | None = None,
        windows: WindowsOptions | None = None,
    ) -> bool:
        return await self._invoke_method(
            method_name="contains_key",
            arguments={
                "key": key,
                "web": web,
                "ios": ios,
                "macos": macos,
                "android": android,
                "windows": windows,
            },
        )

    async def remove(
        self,
        key: str,
        web: WebOptions | None = None,
        ios: IOSOptions | None = None,
        macos: MacOsOptions | None = None,
        android: AndroidOptions | None = None,
        windows: WindowsOptions | None = None,
    ) -> None:
        return await self._invoke_method(
            method_name="remove",
            arguments={
                "key": key,
                "web": web,
                "ios": ios,
                "macos": macos,
                "android": android,
                "windows": windows,
            },
        )

    async def clear(
        self,
        web: WebOptions | None = None,
        ios: IOSOptions | None = None,
        macos: MacOsOptions | None = None,
        android: AndroidOptions | None = None,
        windows: WindowsOptions | None = None,
    ) -> None:
        return await self._invoke_method(
            method_name="clear",
            arguments={
                "web": web,
                "ios": ios,
                "macos": macos,
                "android": android,
                "windows": windows,
            },
        )
