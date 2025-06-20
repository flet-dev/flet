import asyncio
from typing import Any, List

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["SharedPreferences"]


@control("SharedPreferences")
class SharedPreferences(Service):
    def set(self, key: str, value: Any) -> None:
        asyncio.create_task(self.set_async(key, value))

    async def set_async(self, key: str, value: Any) -> bool:
        assert value is not None
        return await self._invoke_method_async("set", {"key": key, "value": value})

    async def get_async(self, key: str):
        return await self._invoke_method_async("get", {"key": key})

    async def contains_key_async(self, key: str) -> bool:
        return await self._invoke_method_async("contains_key", {"key": key})

    def remove(self, key: str) -> None:
        asyncio.create_task(self.remove_async(key))

    async def remove_async(self, key: str) -> bool:
        return await self._invoke_method_async("remove", {"key": key})

    async def get_keys_async(self, key_prefix: str) -> List[str]:
        return await self._invoke_method_async("get_keys", {"key_prefix": key_prefix})

    def clear(self) -> None:
        asyncio.create_task(self.clear_async())

    async def clear_async(self) -> bool:
        return await self._invoke_method_async("clear")
