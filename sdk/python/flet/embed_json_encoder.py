import json
from typing import Dict

from flet.border import Border, BorderSide
from flet.border_radius import BorderRadius
from flet.buttons import ButtonStyle
from flet.margin import Margin
from flet.padding import Padding


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
                if v != None and not isinstance(v, Dict):
                    obj.__dict__[k] = {"": v}
            return self._cleanup_dict(obj.__dict__)
        elif isinstance(obj, object):
            return self._cleanup_dict(obj.__dict__)
        return json.JSONEncoder.default(self, obj)

    def _cleanup_dict(self, d):
        return dict(filter(lambda item: item[1] != None, d.items()))
