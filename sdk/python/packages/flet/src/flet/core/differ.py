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
            if sub_patch or (old_value is not None and new_value is None):
                patch[field.name] = sub_patch if sub_patch else None
            setattr(updated, field.name, updated_value)
        return patch, updated

    elif isinstance(old, dict) and isinstance(new, dict):
        patch = {}
        updated = old.copy()
        for key in old.keys() | new.keys():
            if key in old and key in new:
                # ley exists in both dicts
                sub_patch, updated[key] = generate_patch(
                    old[key], new[key], path + [key]
                )
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
        return patch, updated

    elif isinstance(old, list) and isinstance(new, list):
        patch = {}
        updated = old[:]
        min_len = min(len(old), len(new))

        for i in range(min_len):
            sub_patch, updated[i] = generate_patch(old[i], new[i], path + [i])
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

        return patch, updated

    elif type(old) != type(new) or old != new or (old is not None and new is None):
        return new, new  # Explicitly track None changes

    return {}, old
