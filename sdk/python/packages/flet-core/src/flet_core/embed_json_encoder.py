import enum
import json
from typing import Dict

from flet_core.border import Border, BorderSide
from flet_core.border_radius import BorderRadius
from flet_core.margin import Margin
from flet_core.padding import Padding


class EmbedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BorderSide):
            return {
                "w": obj.width,
                "c": obj.color,
                "sa": obj.stroke_align,
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
                "bl": obj.bottom_left,
                "br": obj.bottom_right,
                "tl": obj.top_left,
                "tr": obj.top_right,
            }
        elif isinstance(obj, (Margin, Padding)):
            return {
                "l": obj.left,
                "t": obj.top,
                "r": obj.right,
                "b": obj.bottom,
            }
        else:
            return self._convert_enums(obj.__dict__)

    def encode(self, o):
        return super().encode(self._convert_enums(o))

    def _convert_enums(self, obj):
        if isinstance(obj, Dict):
            return dict(
                map(
                    lambda item: (
                        self._convert_enums(
                            item[0]
                            if not isinstance(item[0], enum.Enum)
                            else item[0].value
                        ),
                        self._convert_enums(
                            item[1]
                            if not isinstance(item[1], enum.Enum)
                            else item[1].value
                        ),
                    ),
                    filter(lambda item: item[1] is not None, obj.items()),
                )
            )
        else:
            return obj
