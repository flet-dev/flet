import enum
import json
from typing import Dict

from flet.core.border import Border, BorderSide
from flet.core.border_radius import BorderRadius
from flet.core.box import BoxConstraints
from flet.core.margin import Margin
from flet.core.padding import Padding


class EmbedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BorderSide):
            obj_as_dict = {
                "w": obj.width,
                "c": obj.color,
                "sa": obj.stroke_align,
            }
        elif isinstance(obj, Border):
            obj_as_dict = {
                "l": obj.left,
                "t": obj.top,
                "r": obj.right,
                "b": obj.bottom,
            }
        elif isinstance(obj, BorderRadius):
            obj_as_dict = {
                "bl": obj.bottom_left,
                "br": obj.bottom_right,
                "tl": obj.top_left,
                "tr": obj.top_right,
            }
        elif isinstance(obj, (Margin, Padding)):
            obj_as_dict = {
                "l": obj.left,
                "t": obj.top,
                "r": obj.right,
                "b": obj.bottom,
            }
        elif isinstance(obj, BoxConstraints):
            obj_as_dict = {
                "min_width": obj.min_width,
                "max_width": obj.max_width,
                "min_height": obj.min_height,
                "max_height": obj.max_height,
            }
        else:
            obj_as_dict = self._convert_enums(obj.__dict__)

        # Convert inf to string "inf" to avoid JSON serialization error
        for key, value in obj_as_dict.items():
            if value == float("inf"):
                obj_as_dict[key] = "inf"

        return obj_as_dict

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
