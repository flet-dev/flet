import enum
import json

__all__ = ["EmbedJsonEncoder"]


class EmbedJsonEncoder(json.JSONEncoder):
    """
    JSON encoder that embeds control-like objects by serializing their `__dict__`.
    """

    def default(self, obj):
        """
        Serialize an object by converting its attribute dictionary to JSON-safe values.

        Enum keys/values are converted to their raw values and `float("inf")` is
        normalized to `"inf"` to avoid JSON serialization failures.
        """
        obj_as_dict = self._convert_enums(obj.__dict__)

        # Convert inf to string "inf" to avoid JSON serialization error
        for key, value in obj_as_dict.items():
            if value == float("inf"):
                obj_as_dict[key] = "inf"

        return obj_as_dict

    def encode(self, o):
        """
        Encode an object after recursively converting enum instances in mappings.
        """
        return super().encode(self._convert_enums(o))

    def _convert_enums(self, obj):
        """
        Recursively convert enum keys/values to `.value` and drop `None` values.
        """
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
