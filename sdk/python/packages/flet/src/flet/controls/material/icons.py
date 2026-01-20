from __future__ import annotations

import json
import random
from importlib import resources

from flet.controls.icon_data import IconData

__all__ = ["Icons"]


class _MaterialIconData(IconData, package_name="flet", class_name="Icons"):
    _DUMMY = -1

    @classmethod
    def _missing_(cls, value):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._name_ = f"_ICON_{value}"
        cls._value2member_map_[value] = obj
        return obj


class _IconsProxy:
    __slots__ = ("_map", "_values")

    def __init__(self) -> None:
        self._map: dict[str, int] | None = None
        self._values: list[_MaterialIconData] | None = None

    def _load(self) -> None:
        if self._map is not None:
            return
        data = (
            resources.files(__package__)
            .joinpath("icons.json")
            .read_text(encoding="utf-8")
        )
        self._map = json.loads(data)

    def _get_values(self) -> list[_MaterialIconData]:
        self._load()
        if self._values is None:
            assert self._map is not None
            self._values = [_MaterialIconData(v) for v in self._map.values()]
        return self._values

    def __getattr__(self, name: str) -> IconData:
        self._load()
        assert self._map is not None
        try:
            return _MaterialIconData(self._map[name])
        except KeyError:
            raise AttributeError(name) from None

    def __dir__(self) -> list[str]:
        self._load()
        assert self._map is not None
        return sorted(self._map.keys())

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


Icons = _IconsProxy()
