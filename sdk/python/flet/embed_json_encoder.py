import json

from flet.border import Border, BorderSide
from flet.border_radius import BorderRadius
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
        elif isinstance(obj, object):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
