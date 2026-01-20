from __future__ import annotations

import json
from importlib import resources

from flet.controls.icon_data import IconData

__all__ = ["CupertinoIcons"]


class _CupertinoIconData(IconData, package_name="flet", class_name="CupertinoIcons"):
    _DUMMY = -1

    @classmethod
    def _missing_(cls, value):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._name_ = f"_ICON_{value}"
        cls._value2member_map_[value] = obj
        return obj


class _CupertinoIconsProxy:
    __slots__ = ("_map",)

    def __init__(self) -> None:
        self._map: dict[str, int] | None = None

    def _load(self) -> None:
        if self._map is not None:
            return
        data = (
            resources.files(__package__)
            .joinpath("cupertino_icons.json")
            .read_text(encoding="utf-8")
        )
        self._map = json.loads(data)

    def __getattr__(self, name: str) -> IconData:
        self._load()
        assert self._map is not None
        try:
            return _CupertinoIconData(self._map[name])
        except KeyError:
            raise AttributeError(name) from None

    def __dir__(self) -> list[str]:
        self._load()
        assert self._map is not None
        return sorted(self._map.keys())


CupertinoIcons = _CupertinoIconsProxy()
