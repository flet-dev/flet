from typing import Optional, TypeAlias, Union

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["SharedPreferences", "SharedPreferencesValueType"]

SharedPreferencesValueType: TypeAlias = Union[str, int, float, bool, list[str]]
"""Supported types for [`SharedPreferences`][flet.] values."""


@control("SharedPreferences")
class SharedPreferences(Service):
    """
    Provides access to persistent key-value storage.
    """

    async def set(self, key: str, value: SharedPreferencesValueType) -> bool:
        """
        Sets a value for the given key.

        Note:
            Due to limitations on Android, it is not possible to set values that start
            with any of the following: `VGhpcyBpcyB0aGUgcHJlZml4IGZvciBhIGxpc3Qu`,
            `VGhpcyBpcyB0aGUgcHJlZml4IGZvciBCaWdJbnRlZ2Vy`, and
            `VGhpcyBpcyB0aGUgcHJlZml4IGZvciBEb3VibGUu`.

        Args:
            key: The key to store the value under.
            value: The value to store.

        Returns:
            `True` if the value was set successfully, `False` otherwise.

        Raises:
            ValueError: If `value` is of an unsupported type
                (`str`, `int`, `float`, `bool`, and `list[str]`).
        """
        if not (
            isinstance(value, (str, int, float, bool))
            or (isinstance(value, list) and all(isinstance(x, str) for x in value))
        ):
            raise ValueError(
                f"Unsupported value type: {type(value)}. "
                "Supported types are: str, int, float, bool, list[str]."
            )
        return await self._invoke_method("set", {"key": key, "value": value})

    async def get(self, key: str) -> Optional[SharedPreferencesValueType]:
        """
        Gets the value for the given key.

        Args:
            key: The key to retrieve the value for.

        Returns:
            The value for the given key, or `None` if the key doesn't exist.
        """
        return await self._invoke_method("get", {"key": key})

    async def contains_key(self, key: str) -> bool:
        """
        Checks if the given key exists.

        Args:
            key: The key to check for existence.

        Returns:
            `True` if the key exists, `False` otherwise.
        """
        return await self._invoke_method("contains_key", {"key": key})

    async def remove(self, key: str) -> bool:
        """
        Removes the value for the given key.

        Args:
            key: The key to remove.

        Returns:
            `True` if the key was removed, `False` if the key didn't exist.
        """
        return await self._invoke_method("remove", {"key": key})

    async def get_keys(self, key_prefix: str) -> list[str]:
        """
        Gets all keys with the given prefix.

        Args:
            key_prefix: The prefix to filter keys by.

        Returns:
            A list of keys that start with the given prefix.
        """
        return await self._invoke_method("get_keys", {"key_prefix": key_prefix})

    async def clear(self) -> bool:
        """
        Clears all keys and values.

        Returns:
            `True` if the preferences were cleared successfully, `False` otherwise.
        """
        return await self._invoke_method("clear")
