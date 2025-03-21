import json
from typing import Any, List

from flet.core.control import Service, control
from flet.utils.json_utils import to_json


@control("SharedPreferences")
class SharedPreferences(Service):
    # breaking change: no JSON conversion for value
    def set(self, key: str, value: Any) -> bool:
        assert value is not None
        return self.invoke_method("set", {"key": key, "value": value})

    async def set_async(self, key: str, value: Any) -> bool:
        assert value is not None
        return await self.invoke_method_async("set", {"key": key, "value": value})

    def get(self, key: str):
        return self.invoke_method("get", {"key": key})

    async def get_async(self, key: str):
        return await self.invoke_method_async("get", {"key": key})

    def contains_key(self, key: str) -> bool:
        return self.invoke_method("contains_key", {"key": key})

    async def contains_key_async(self, key: str) -> bool:
        return await self.invoke_method_async("contains_key", {"key": key})

    def remove(self, key: str) -> bool:
        return self.invoke_method("remove", {"key": key}, wait_for_result=True)

    async def remove_async(self, key: str) -> bool:
        return await self.invoke_method_async("remove", {"key": key})

    def get_keys(self, key_prefix: str) -> List[str]:
        return self.invoke_method("get_keys", {"key_prefix": key_prefix})

    async def get_keys_async(self, key_prefix: str) -> List[str]:
        return await self.invoke_method_async("get_keys", {"key_prefix": key_prefix})

    def clear(self) -> bool:
        return self.invoke_method("clear")

    async def clear_async(self) -> bool:
        return await self.invoke_method_async("clear")
