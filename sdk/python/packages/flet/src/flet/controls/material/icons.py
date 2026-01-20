from __future__ import annotations

import json
import time
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
    __slots__ = ("_map",)

    def __init__(self) -> None:
        self._map: dict[str, int] | None = None

    def _load(self) -> None:
        if self._map is not None:
            return
        t0 = time.perf_counter()
        data = (
            resources.files(__package__)
            .joinpath("icons.json")
            .read_text(encoding="utf-8")
        )
        self._map = json.loads(data)
        t1 = time.perf_counter()
        print(f"Loaded icons.json in {t1 - t0:.4f} seconds")

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


Icons = _IconsProxy()
