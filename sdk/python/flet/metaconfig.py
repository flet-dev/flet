from typing import List, Any, Dict, Tuple


class Meta(type):

    _exclude_attrs: List[str] = ["__module__", "__qualname__"]
    _include_attrs: Dict[Dict[str, Any], Any] = {}

    def __new__(cls, name: str, bases: Tuple[type], attrs: Dict[str, Any]) -> type:
        class_attributes = {i: attrs[i] for i in attrs if i not in cls._exclude_attrs}
        cls._include_attrs[name] = class_attributes
        return super().__new__(cls, name, bases, attrs)

    def __init__(self, name: str, bases: Tuple[type], attrs: Dict[str, Any]) -> None:
        self.name = name
        self.bases = bases
        self.attrs = attrs
        setattr(
            self, "_set_page_attrs", self._set_page_attrs
        )  # Add _set_page_attrs method to every child class to be called from Page class

    def _set_page_attrs(self, obj: Any, config: str) -> None:
        for key, value in self._include_attrs[config].items():
            if key not in self._exclude_attrs:
                setattr(obj, key, value)


class BaseConfig(metaclass=Meta):
    pass
