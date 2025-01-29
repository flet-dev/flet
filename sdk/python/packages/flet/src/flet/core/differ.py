from dataclasses import fields, is_dataclass, replace
from typing import Any, Dict, List, Optional, Union

# TODO
# - when serializing dataclass in msgpack skip fields with 'None' values
# - track updated fields in dataclasses
# - create dataclasses index (using hashes) for partial tree updates


def diff_and_patch(
    old: Any, new: Any, path: Optional[list[Union[int, str]]] = None
) -> tuple[list[Dict], Any]:
    """Entry point to calculate differences and update."""
    if path is None:
        path = []

    # Handle dataclasses
    if is_dataclass(old) and is_dataclass(new):
        return diff_and_patch_dataclass(old, new, path)

    # Handle lists
    if isinstance(old, list) and isinstance(new, list):
        return diff_and_patch_list(old, new, path)

    # Handle dicts
    if isinstance(old, dict) and isinstance(new, dict):
        return diff_and_patch_dict(old, new, path)

    # Handle literals or mismatched types
    if old != new:
        return [{"op": "replace", "path": path, "value": new}], new

    return [], old  # No changes for identical literals


def diff_and_patch_dataclass(
    old: Any, new: Any, path: List[Union[int, str]]
) -> tuple[list[Dict], Any]:
    patches = []
    updated = replace(old)  # Copy the old dataclass

    for field in fields(old):
        field_name = field.name
        field_path = path + [field_name]

        old_value = getattr(old, field_name)
        new_value = getattr(new, field_name)

        child_patches, updated_value = diff_and_patch(old_value, new_value, field_path)
        patches.extend(child_patches)
        setattr(updated, field_name, updated_value)

    return patches, updated


def diff_and_patch_list(
    old: List[Any], new: List[Any], path: List[Union[int, str]]
) -> tuple[list[Dict], Any]:
    """Diffs and patches lists, always including index in the 'add' operation."""
    patches = []
    updated = []

    max_len = max(len(old), len(new))
    for i in range(max_len):
        item_path = path + [i]  # Always use index for 'add'
        if i >= len(old):  # Additions
            patches.append({"op": "add", "path": item_path, "value": new[i]})
            updated.append(new[i])
        elif i >= len(new):  # Removals
            patches.append({"op": "remove", "path": item_path})
        else:  # Compare elements
            child_patches, updated_item = diff_and_patch(old[i], new[i], item_path)
            patches.extend(child_patches)
            updated.append(updated_item)

    return patches, updated


def diff_and_patch_dict(
    old: Dict[Any, Any], new: Dict[Any, Any], path: List[Union[int, str]]
) -> tuple[list[Dict], Any]:
    patches = []
    updated = old.copy()

    for key in set(old.keys()).union(new.keys()):
        item_path = path + [key]

        if key not in old:  # New key added
            patches.append({"op": "add", "path": item_path, "value": new[key]})
            updated[key] = new[key]
        elif key not in new:  # Old key removed
            patches.append({"op": "remove", "path": item_path})
            del updated[key]
        else:  # Compare existing keys
            child_patches, updated_value = diff_and_patch(old[key], new[key], item_path)
            patches.extend(child_patches)
            updated[key] = updated_value

    return patches, updated
