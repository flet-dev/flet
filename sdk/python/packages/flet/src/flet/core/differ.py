# TODO
# - when serializing dataclass in msgpack skip fields with 'None' values
# - track updated fields in dataclasses
# - create dataclasses index (using hashes) for partial tree updates

"""
[
  {"op": "replace", "path": ["controls", 0, "controls", 0, "text"], "value": "Updated Button"},
  {"op": "replace", "path": ["controls", 0, "controls", 1, "text"], "value": "Updated Span"},
  {"op": "add", "path": ["controls", 2], "value": {"id": "sidebar", "cls": "sidebar", "controls": []}},
  {"op": "add", "path": ["controls", 2, "controls", 0], "value": {"id": "btn3", "text": "New Button"}},
  {"op": "add", "path": ["controls", 2, "controls", 1], "value": {"id": "span3", "text": "New Span"}}
]
"""

a = {
    "": {
        "controls": {
            0: {
                "controls": {
                    0: {
                        "$replace": {
                            "text": "Updated button",
                            "cls": "new-button-class",
                        }
                    },
                    "$add": {1: {"id": "sidebar", "cls": "sidebar", "controls": []}},
                },
            },
            "$add": {
                1: {"id": "btn3", "text": "New Button"},
                2: {"id": "span3", "text": "New span"},
            },
            "$remove": [3, 4, 5],
        },
        "$replace": {"id": "div_2", "cls": "div-class"},
    }
}

import dataclasses
from typing import Any, Dict, List, Optional, Tuple


def is_dataclass_instance(obj):
    return dataclasses.is_dataclass(obj) and not isinstance(obj, type)


@dataclasses.dataclass
class Patch:
    op: str
    path: List[Any]
    value: Any


def generate_patch(
    old: Any, new: Any, path: Optional[List[Any]] = None
) -> Tuple[Dict, Any]:
    if path is None:
        path = []

    if is_dataclass_instance(old) and is_dataclass_instance(new):
        patch = {}
        updated = dataclasses.replace(old)
        for field in dataclasses.fields(old):
            old_value = getattr(old, field.name)
            new_value = getattr(new, field.name)
            sub_patch, updated_value = generate_patch(
                old_value, new_value, path + [field.name]
            )
            if sub_patch:
                patch[field.name] = sub_patch
            setattr(updated, field.name, updated_value)
        return patch, updated

    elif isinstance(old, dict) and isinstance(new, dict):
        patch = {}
        updated = old.copy()
        for key in old.keys() | new.keys():
            if key in old and key in new:
                sub_patch, updated[key] = generate_patch(
                    old[key], new[key], path + [key]
                )
                if sub_patch:
                    patch[key] = sub_patch
            elif key in new:
                patch[key] = {"$a": new[key]}  # Addition
                updated[key] = new[key]
            else:
                patch[key] = {"$d": None}  # Deletion marker
                del updated[key]
        return patch, updated

    elif isinstance(old, list) and isinstance(new, list):
        patch = {}
        updated = old[:]
        min_len = min(len(old), len(new))

        for i in range(min_len):
            sub_patch, updated[i] = generate_patch(old[i], new[i], path + [i])
            if sub_patch:
                patch[i] = sub_patch

        if len(new) > len(old):
            for i in range(len(old), len(new)):
                patch[i] = {"$a": new[i]}
                updated.append(new[i])
        elif len(old) > len(new):
            for i in range(len(new), len(old)):
                patch[i] = {"$d": None}
                updated.pop()

        return patch, updated

    elif old != new:
        return new, new  # Implicit replace

    return {}, old
