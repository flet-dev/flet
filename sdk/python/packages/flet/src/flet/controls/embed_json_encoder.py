import enum
import json

__all__ = ["EmbedJsonEncoder"]


class EmbedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        obj_as_dict = self._convert_enums(obj.__dict__)

        # Convert inf to string "inf" to avoid JSON serialization error
        for key, value in obj_as_dict.items():
            if value == float("inf"):
                obj_as_dict[key] = "inf"

        return obj_as_dict

    def encode(self, o):
        return super().encode(self._convert_enums(o))

    def _convert_enums(self, obj):
        if isinstance(obj, dict):
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
