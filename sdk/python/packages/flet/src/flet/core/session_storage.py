from typing import Any, Dict, List

__all__ = ["SessionStorage"]


class SessionStorage:
    def __init__(self):
        self.__store: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.__store[key] = value

    def get(self, key: str):
        return self.__store.get(key)

    def contains_key(self, key: str) -> bool:
        return key in self.__store

    def remove(self, key: str):
        self.__store.pop(key)

    def get_keys(self) -> List[str]:
        return list(self.__store.keys())

    def clear(self):
        self.__store.clear()
