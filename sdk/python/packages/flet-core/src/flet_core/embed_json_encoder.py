import enum
import json
from typing import Dict

from flet_core.border import Border, BorderSide
from flet_core.border_radius import BorderRadius
from flet_core.buttons import ButtonStyle
from flet_core.margin import Margin
from flet_core.padding import Padding


class EmbedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BorderSide):
            return {
                "w": obj.width,
                "c": obj.color,
            }
        elif isinstance(obj, Border):
            return {
                "l": obj.left,
                "t": obj.top,
                "r": obj.right,
                "b": obj.bottom,
            }
        elif isinstance(obj, BorderRadius):
            return {
                "bl": obj.bottomLeft,
                "br": obj.bottomRight,
                "tl": obj.topLeft,
                "tr": obj.topRight,
            }
        elif isinstance(obj, (Margin, Padding)):
            return {
                "l": obj.left,
                "t": obj.top,
                "r": obj.right,
                "b": obj.bottom,
            }
        elif isinstance(obj, ButtonStyle):
            for k, v in obj.__dict__.items():
                if v is not None:
                    if not isinstance(v, Dict):
                        obj.__dict__[k] = {"": v}
                    if k != "animation_duration":
                        obj.__dict__[k] = self._cleanup_dict(obj.__dict__[k])
            return self._cleanup_dict(obj.__dict__)
        elif isinstance(obj, object):
            return self._cleanup_dict(obj.__dict__)
        return json.JSONEncoder.default(self, obj)

    def encode(self, o):
        if isinstance(o, Dict):
            o = self._cleanup_dict(o)
        return super().encode(o)

    def _cleanup_dict(self, d):
        return dict(
            map(
                lambda item: (
                    item[0] if not isinstance(item[0], enum.Enum) else item[0].value,
                    item[1] if not isinstance(item[1], enum.Enum) else item[1].value,
                ),
                filter(lambda item: item[1] is not None, d.items()),
            )
        )
