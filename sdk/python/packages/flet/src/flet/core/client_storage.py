import json
import weakref
from typing import Any, List


class ClientStorage:
    def __init__(self, page):
        self.__page = weakref.ref(page)

    def set(self, key: str, value: Any) -> bool:
        if page := self.__page():
            jv = page._convert_attr_json(value)
            assert jv is not None
            return (
                page._invoke_method(
                    "clientStorage:set", {"key": key, "value": jv}, wait_for_result=True
                )
                == "true"
            )
        return False

    async def set_async(self, key: str, value: Any) -> bool:
        if page := self.__page():
            jv = page._convert_attr_json(value)
            assert jv is not None
            return (
                await page._invoke_method_async(
                    "clientStorage:set", {"key": key, "value": jv}, wait_for_result=True
                )
            ) == "true"
        return False

    def get(self, key: str):
        if page := self.__page():
            jv = page._invoke_method(
                "clientStorage:get", {"key": key}, wait_for_result=True
            )
            if jv:
                return json.loads(json.loads(jv))
        return None

    async def get_async(self, key: str):
        if page := self.__page():
            jv = await page._invoke_method_async(
                "clientStorage:get", {"key": key}, wait_for_result=True
            )
            if jv:
                return json.loads(json.loads(jv))
        return None

    def contains_key(self, key: str) -> bool:
        if page := self.__page():
            return (
                page._invoke_method(
                    "clientStorage:containskey", {"key": key}, wait_for_result=True
                )
                == "true"
            )
        return False

    async def contains_key_async(self, key: str) -> bool:
        if page := self.__page():
            return (
                await page._invoke_method_async(
                    "clientStorage:containskey", {"key": key}, wait_for_result=True
                )
                == "true"
            )
        return False

    def remove(self, key: str) -> bool:
        if page := self.__page():
            return (
                page._invoke_method(
                    "clientStorage:remove", {"key": key}, wait_for_result=True
                )
                == "true"
            )
        return False

    async def remove_async(self, key: str) -> bool:
        if page := self.__page():
            return (
                await page._invoke_method_async(
                    "clientStorage:remove", {"key": key}, wait_for_result=True
                )
            ) == "true"
        return False

    def get_keys(self, key_prefix: str) -> List[str]:
        if page := self.__page():
            jr = page._invoke_method(
                "clientStorage:getkeys",
                {"key_prefix": key_prefix},
                wait_for_result=True,
            )
            assert jr is not None
            return json.loads(jr)
        return []

    async def get_keys_async(self, key_prefix: str) -> List[str]:
        if page := self.__page():
            jr = await page._invoke_method_async(
                "clientStorage:getkeys",
                {"key_prefix": key_prefix},
                wait_for_result=True,
            )
            assert jr is not None
            return json.loads(jr)
        return []

    def clear(self) -> bool:
        if page := self.__page():
            return (
                page._invoke_method("clientStorage:clear", wait_for_result=True)
                == "true"
            )
        return False

    async def clear_async(self) -> bool:
        if page := self.__page():
            return (
                await page._invoke_method_async(
                    "clientStorage:clear", wait_for_result=True
                )
                == "true"
            )
        return False
