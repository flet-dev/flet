from typing import Any

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["SharedPreferences"]


@control("SharedPreferences")
class SharedPreferences(Service):
    """
    Provides access to persistent key-value storage.
    """

    async def set(self, key: str, value: Any) -> bool:
        """
        Sets a value for the given key.
        """
        if value is None:
            raise ValueError("value can't be None")
        return await self._invoke_method("set", {"key": key, "value": value})

    async def get(self, key: str):
        """
        Gets the value for the given key.
        """
        return await self._invoke_method("get", {"key": key})

    async def contains_key(self, key: str) -> bool:
        """
        Checks if the given key exists.
        """
        return await self._invoke_method("contains_key", {"key": key})

    async def remove(self, key: str) -> bool:
        """
        Removes the value for the given key.
        """
        return await self._invoke_method("remove", {"key": key})

    async def get_keys(self, key_prefix: str) -> list[str]:
        """
        Gets all keys with the given prefix.
        """
        return await self._invoke_method("get_keys", {"key_prefix": key_prefix})

    async def clear(self) -> bool:
        """
        Clears all keys and values.
        """
        return await self._invoke_method("clear")
