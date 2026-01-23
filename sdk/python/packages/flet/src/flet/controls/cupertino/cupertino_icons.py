from __future__ import annotations

import json
import random
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


_CupertinoIconData.__name__ = "CupertinoIcons"
_CupertinoIconData.__qualname__ = "CupertinoIcons"


class _CupertinoIconsProxy:
    __slots__ = ("_map", "_values")

    def __init__(self) -> None:
        self._map: dict[str, int] | None = None
        self._values: list[_CupertinoIconData] | None = None

    def _load(self) -> None:
        if self._map is not None:
            return
        data = (
            resources.files(__package__)
            .joinpath("cupertino_icons.json")
            .read_text(encoding="utf-8")
        )
        self._map = json.loads(data)

    def _get_member(self, name: str) -> _CupertinoIconData:
        self._load()
        assert self._map is not None
        cls = _CupertinoIconData
        existing = cls._member_map_.get(name)
        if existing is not None:
            return existing
        value = self._map[name]
        member = int.__new__(cls, value)
        member._value_ = value
        member._name_ = name
        cls._member_map_[name] = member
        cls._value2member_map_[value] = member
        cls._member_names_.append(name)
        return member

    def _get_values(self) -> list[_CupertinoIconData]:
        self._load()
        if self._values is None:
            assert self._map is not None
            self._values = [self._get_member(name) for name in self._map]
        return self._values

    def __getattr__(self, name: str) -> IconData:
        try:
            return self._get_member(name)
        except KeyError:
            raise AttributeError(name) from None

    def __dir__(self) -> list[str]:
        self._load()
        assert self._map is not None
        return sorted(self._map.keys())

    def __iter__(self):
        return iter(self._get_values())

    def __len__(self) -> int:
        self._load()
        assert self._map is not None
        return len(self._map)

    def random(
        self,
        exclude: list[IconData] | None = None,
        weights: dict[IconData, int] | None = None,
    ) -> IconData | None:
        choices = list(self._get_values())
        if exclude:
            excluded = set(exclude)
            choices = [icon for icon in choices if icon not in excluded]
            if not choices:
                return None
        if weights:
            weights_list = [weights.get(icon, 1) for icon in choices]
            return random.choices(choices, weights=weights_list)[0]
        return random.choice(choices)


CupertinoIcons = _CupertinoIconsProxy()
