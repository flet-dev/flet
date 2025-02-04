# TODO
# - when serializing dataclass in msgpack skip fields with 'None' values
# - create dataclasses index (using hashes) for partial tree updates
# - optimize deletions for lists and dicts, like "$d": {2, 4, 5} or "$d": {"key1", "key2", "key3"}
# - implement weakref index of dataclasses having event handlers
# - controls should have weak ref to a parent control or page

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


def generate_patch(
    index: dict, old: Any, new: Any, path: Optional[List[Any]] = None
) -> Dict:
    if path is None:
        path = []

    if type(old) != type(new):
        return new

    elif is_dataclass_instance(old) and is_dataclass_instance(new):
        patch = {}
        updated = {}
        for field in dataclasses.fields(old):
            old_value = getattr(old, field.name)
            new_value = getattr(new, field.name)
            sub_patch = generate_patch(index, old_value, new_value, path + [field.name])
            if sub_patch or (old_value is not None and new_value is None):
                patch[field.name] = sub_patch if sub_patch else None
            updated[field.name] = new_value
        index[new] = updated
        return patch

    elif isinstance(old, dict) and isinstance(new, dict):
        patch = {}
        updated = old.copy()
        for key in old.keys() | new.keys():
            if key in old and key in new:
                # ley exists in both dicts
                updated[key] = new[key]
                sub_patch = generate_patch(index, old[key], new[key], path + [key])
                if sub_patch or (old[key] is not None and new[key] is None):
                    patch[key] = sub_patch if sub_patch else None
            elif key in new:
                # new key
                patch[key] = new[key]  # Addition
                updated[key] = new[key]
            else:
                # deleted key
                deleted_keys = patch.get("$d")
                if deleted_keys is None:
                    deleted_keys = []
                    patch["$d"] = deleted_keys
                deleted_keys.append(key)
                del updated[key]
        index[new] = updated
        return patch

    elif isinstance(old, list) and isinstance(new, list):
        patch = {}
        updated = old[:]
        min_len = min(len(old), len(new))

        for i in range(min_len):
            updated[i] = new[i]
            sub_patch = generate_patch(old[i], new[i], path + [i])
            if sub_patch or (old[i] is not None and new[i] is None):
                patch[i] = sub_patch if sub_patch else None

        if len(new) > len(old):
            for i in range(len(old), len(new)):
                patch[i] = {"$a": new[i]}
                updated.append(new[i])
        elif len(old) > len(new):
            deleted_keys = patch.get("$d")
            if deleted_keys is None:
                deleted_keys = []
                patch["$d"] = deleted_keys
            for i in range(len(new), len(old)):
                deleted_keys.append(i)
                updated.pop()
        index[new] = updated
        return patch

    elif old != new or (old is not None and new is None):
        return new

    return {}
