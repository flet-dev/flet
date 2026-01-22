from dataclasses import dataclass, field
from typing import Any, Optional

import flet as ft
from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet_secure_storage.types import (
    AndroidOptions,
    IOSOptions,
    MacOsOptions,
    WebOptions,
    WindowsOptions,
)


@dataclass
class SecureStorageEvent(ft.Event["SecureStorage"]):
    """
    The event fired by SecureStorage when availability changes.
    """

    available: Optional[bool]
    """
    The availability of secure storage. True if secure storage is available,
    False if not, None if unknown.
    """


@control("SecureStorage")
class SecureStorage(Service):
    """
    A class to manage secure storage in a Flet application across multiple platforms.
    """

    ios_options: IOSOptions = field(default_factory=lambda: IOSOptions())
    """
    iOS-specific configuration for secure storage.
    """

    android_options: AndroidOptions = field(default_factory=lambda: AndroidOptions())
    """
    Android-specific configuration for secure storage.
    """

    windows_options: WindowsOptions = field(default_factory=lambda: WindowsOptions())
    """
    Windows-specific configuration for secure storage.
    """

    macos_options: MacOsOptions = field(default_factory=lambda: MacOsOptions())
    """
    macOS-specific configuration for secure storage.
    """

    web_options: WebOptions = field(default_factory=lambda: WebOptions())
    """
    Web-specific configuration for secure storage.
    """

    on_change: Optional[ft.EventHandler["SecureStorageEvent"]] = None
    """
    Fires when secure storage availability changes.

    iOS only feature. For unsupported platforms, this event will never fire.
    The payload is a `SecureStorageEvent` object with the `available` field.
    """

    async def get_availability(self) -> Optional[bool]:
        """
        Gets the current availability status of secure storage.

        iOS and macOS only. On macOS, available only on macOS 12+.
        On older macOS versions, always returns True.
        On unsupported platforms, returns None.

        Returns:
            A boolean indicating storage availability, or None if unsupported.
        """
        return await self._invoke_method("get_availability")

    async def set(
        self,
        key: str,
        value: Any,
        *,
        web: Optional[WebOptions] = None,
        ios: Optional[IOSOptions] = None,
        macos: Optional[MacOsOptions] = None,
        android: Optional[AndroidOptions] = None,
        windows: Optional[WindowsOptions] = None,
    ) -> None:
        """
        Stores a value in secure storage under the given key.

        Args:
            key: The key to store the value under.
            value: The value to store (cannot be None).
            web: Optional web-specific configuration.
            ios: Optional iOS-specific configuration.
            macos: Optional macOS-specific configuration.
            android: Optional Android-specific configuration.
            windows: Optional Windows-specific configuration.

        Raises:
            ValueError: If `value` is None.
        """
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
        *,
        web: Optional[WebOptions] = None,
        ios: Optional[IOSOptions] = None,
        macos: Optional[MacOsOptions] = None,
        android: Optional[AndroidOptions] = None,
        windows: Optional[WindowsOptions] = None,
    ) -> Optional[str]:
        """
        Retrieves the value stored under the given key in secure storage.

        Args:
            key: The key to retrieve.
            web: Optional web-specific configuration.
            ios: Optional iOS-specific configuration.
            macos: Optional macOS-specific configuration.
            android: Optional Android-specific configuration.
            windows: Optional Windows-specific configuration.

        Returns:
            The stored string value, or None if the key does not exist.
        """
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
        *,
        web: Optional[WebOptions] = None,
        ios: Optional[IOSOptions] = None,
        macos: Optional[MacOsOptions] = None,
        android: Optional[AndroidOptions] = None,
        windows: Optional[WindowsOptions] = None,
    ) -> dict[str, str]:
        """
        Retrieves all key-value pairs from secure storage.

        Args:
            web: Optional web-specific configuration.
            ios: Optional iOS-specific configuration.
            macos: Optional macOS-specific configuration.
            android: Optional Android-specific configuration.
            windows: Optional Windows-specific configuration.

        Returns:
            A dictionary with all stored key-value pairs.
        """
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
        *,
        web: Optional[WebOptions] = None,
        ios: Optional[IOSOptions] = None,
        macos: Optional[MacOsOptions] = None,
        android: Optional[AndroidOptions] = None,
        windows: Optional[WindowsOptions] = None,
    ) -> bool:
        """
        Checks whether the given key exists in secure storage.

        Args:
            key: The key to check.
            web: Optional web-specific configuration.
            ios: Optional iOS-specific configuration.
            macos: Optional macOS-specific configuration.
            android: Optional Android-specific configuration.
            windows: Optional Windows-specific configuration.

        Returns:
            True if the key exists, False otherwise.
        """
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
        *,
        web: Optional[WebOptions] = None,
        ios: Optional[IOSOptions] = None,
        macos: Optional[MacOsOptions] = None,
        android: Optional[AndroidOptions] = None,
        windows: Optional[WindowsOptions] = None,
    ) -> None:
        """
        Removes the value stored under the given key in secure storage.

        Args:
            key: The key to remove.
            web: Optional web-specific configuration.
            ios: Optional iOS-specific configuration.
            macos: Optional macOS-specific configuration.
            android: Optional Android-specific configuration.
            windows: Optional Windows-specific configuration.
        """
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
        *,
        web: Optional[WebOptions] = None,
        ios: Optional[IOSOptions] = None,
        macos: Optional[MacOsOptions] = None,
        android: Optional[AndroidOptions] = None,
        windows: Optional[WindowsOptions] = None,
    ) -> None:
        """
        Clears all key-value pairs from secure storage.

        Args:
            web: Optional web-specific configuration.
            ios: Optional iOS-specific configuration.
            macos: Optional macOS-specific configuration.
            android: Optional Android-specific configuration.
            windows: Optional Windows-specific configuration.
        """
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
