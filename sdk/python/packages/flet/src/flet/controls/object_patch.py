#
# python-json-patch - An implementation of the JSON Patch format
# https://github.com/stefankoegl/python-json-patch
#
# Copyright (c) 2011 Stefan Kögl <stefan@skoegl.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import dataclasses
import weakref
from typing import Any

_ST_ADD = 0
_ST_REMOVE = 1


class ObjectPatchException(Exception):
    """Base Object Patch exception"""


class InvalidObjectPatch(ObjectPatchException):
    """Raised if an invalid Object Patch is created"""


class PatchOperation:
    """A single operation inside a Object Patch."""

    def __init__(self, operation):
        if not operation.__contains__("path"):
            raise InvalidObjectPatch("Operation must have a 'path' member")

        self.location = operation["path"]
        self.operation = operation

    def __hash__(self):
        return hash(frozenset(self.operation.items()))

    def __eq__(self, other):
        if not isinstance(other, PatchOperation):
            return False
        return self.operation == other.operation

    def __ne__(self, other):
        return not (self == other)

    @property
    def path(self):
        return self.location[:-1]

    @property
    def key(self):
        return self.location[-1]

    @key.setter
    def key(self, value):
        self.location[-1] = value
        self.operation["path"] = self.location

    def walk(self, doc, part):
        """Walks one step in doc and returns the referenced part"""

        if isinstance(doc, list):
            try:
                return doc[part]

            except IndexError:
                raise ObjectPatchException(f"index '{part}' is out of bounds") from None

        # Else the object is a mapping or supports __getitem__
        # (so assume custom indexing)
        try:
            if hasattr(doc, "__getitem__"):
                return doc[part]
            else:
                return getattr(doc, str(part))

        except KeyError:
            raise ObjectPatchException(f"member '{part}' not found in {doc}") from None

    def to_last(self, doc):
        """Resolves ptr until the last step, returns (sub-doc, last-step)"""

        if not self.location:
            return doc

        for part in self.location[:-1]:
            doc = self.walk(doc, part)

        return doc


class RemoveOperation(PatchOperation):
    """Removes an object property or an array element."""

    def _on_undo_remove(self, path, key):
        if self.path == path:
            if self.key >= key:
                self.key += 1
            else:
                key -= 1
        return key

    def _on_undo_add(self, path, key):
        if self.path == path:
            if self.key > key:
                self.key -= 1
            else:
                key -= 1
        return key


class AddOperation(PatchOperation):
    """Adds an object property or an array element."""

    def _on_undo_remove(self, path, key):
        if self.path == path:
            if self.key > key:
                self.key += 1
            else:
                key += 1
        return key

    def _on_undo_add(self, path, key):
        if self.path == path:
            if self.key > key:
                self.key -= 1
            else:
                key += 1
        return key


class ReplaceOperation(PatchOperation):
    """Replaces an object property or an array element by a new value."""

    def _on_undo_remove(self, path, key):
        return key

    def _on_undo_add(self, path, key):
        return key


class MoveOperation(PatchOperation):
    """Moves an object property or an array element to a new location."""

    @property
    def from_path(self):
        return self.operation["from"][:-1]

    @property
    def from_key(self):
        return self.operation["from"][-1]

    @from_key.setter
    def from_key(self, value):
        self.operation["from"][-1] = value

    def _on_undo_remove(self, path, key):
        if self.from_path == path:
            if self.from_key >= key:
                self.from_key += 1
            else:
                key -= 1
        if self.path == path:
            if self.key > key:
                self.key += 1
            else:
                key += 1
        return key

    def _on_undo_add(self, path, key):
        if self.from_path == path:
            if self.from_key > key:
                self.from_key -= 1
            else:
                key -= 1
        if self.path == path:
            if self.key > key:
                self.key -= 1
            else:
                key += 1
        return key


class ObjectPatch:
    """An Object Patch is a list of Patch Operations."""

    def __init__(self, patch):
        self.patch = patch

    def __str__(self):
        return str(self.patch)

    @classmethod
    def from_diff(
        cls,
        src,
        dst,
        control_cls,
    ):
        builder = DiffBuilder(
            src,
            dst,
            control_cls=control_cls,
        )
        builder._compare_values(None, [], None, src, dst, False)
        ops = list(builder.execute())
        return cls(ops), builder.added_controls, builder.removed_controls

    def to_graph(self) -> Any:
        root = {}
        for op in self.patch:
            prev = root
            node = root
            parts = op["path"]
            len_parts = len(parts)
            if len_parts == 0 and op["op"] == "replace":
                return {"": op["value"]}  # root object
            for i in range(0, len_parts):
                node = prev.get(parts[i], None)
                if node is None:
                    node = {}
                if i == len_parts - 1:
                    if op["op"] == "remove":
                        indices = prev.get("$d", None)
                        if indices is None:
                            indices = []
                            prev["$d"] = indices
                        indices.append(parts[-1])
                        break
                    elif op["op"] == "replace":
                        prev[parts[-1]] = op["value"]
                    elif op["op"] == "add":
                        prev[parts[-1]] = {"$a": op["value"]}
                    elif op["op"] == "move":
                        prev[parts[-1]] = {"$m": op["from"]}
                    else:
                        raise ObjectPatchException(f"Unknown operation: {op['op']}")
                else:
                    prev[parts[i]] = node
                prev = node
        return root


class DiffBuilder:
    def __init__(
        self,
        src_doc,
        dst_doc,
        control_cls=None,
    ):
        self.added_controls = []
        self.removed_controls = []
        self.control_cls = control_cls
        self.index_storage = [{}, {}]
        self.index_storage2 = [[], []]
        self.__root = root = []
        self.src_doc = src_doc
        self.dst_doc = dst_doc
        root[:] = [root, root, None]

    def store_index(self, value, index, st):
        typed_key = (value, type(value))
        try:
            storage = self.index_storage[st]
            stored = storage.get(typed_key)
            if stored is None:
                storage[typed_key] = [index]
            else:
                storage[typed_key].append(index)

        except TypeError:
            self.index_storage2[st].append((typed_key, index))

    def take_index(self, value, st):
        typed_key = (value, type(value))
        try:
            stored = self.index_storage[st].get(typed_key)
            if stored:
                return stored.pop()

        except TypeError:
            storage = self.index_storage2[st]
            for i in range(len(storage) - 1, -1, -1):
                if storage[i][0] == typed_key:
                    return storage.pop(i)[1]

    def insert(self, op):
        root = self.__root
        last = root[0]
        last[1] = root[0] = [last, root, op]
        return root[0]

    def remove(self, index):
        link_prev, link_next, _ = index
        link_prev[1] = link_next
        link_next[0] = link_prev
        index[:] = []

    def iter_from(self, start):
        root = self.__root
        curr = start[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def __iter__(self):
        root = self.__root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def execute(self):
        root = self.__root
        curr = root[1]
        while curr is not root:
            if curr[1] is not root:
                op_first, op_second = curr[2], curr[1][2]
                if (
                    op_first.location == op_second.location
                    and isinstance(op_first, RemoveOperation)
                    and isinstance(op_second, AddOperation)
                ):
                    yield ReplaceOperation(
                        {
                            "op": "replace",
                            "path": op_second.location,
                            "value": op_second.operation["value"],
                        }
                    ).operation
                    curr = curr[1][1]
                    continue

            yield curr[2].operation
            curr = curr[1]

    def _item_added(
        self,
        parent,
        path,
        key,
        item,
        item_key=None,
        configure_dataclass=True,
        frozen=False,
    ):
        # print("_item_added:", path, key, item, item_key)
        if configure_dataclass:
            self._configure_dataclass(item, parent, frozen)
        index_key = item_key if item_key is not None else item
        index = self.take_index(index_key, _ST_REMOVE)
        if index is not None:
            op = index[2]
            if isinstance(op.key, int) and isinstance(key, int):
                for v in self.iter_from(index):
                    op.key = v._on_undo_remove(op.path, op.key)

            self.remove(index)
            if op.location != _path_join(path, key):
                new_op = MoveOperation(
                    {
                        "op": "move",
                        "from": op.location,
                        "path": _path_join(path, key),
                    }
                )
                self.insert(new_op)
        else:
            new_op = AddOperation(
                {
                    "op": "add",
                    "path": _path_join(path, key),
                    "value": item,
                }
            )
            new_index = self.insert(new_op)
            self.store_index(index_key, new_index, _ST_ADD)

    def _item_removed(self, path, key, item, item_key=None, frozen=False):
        # print("_item_removed:", path, key, item, item_key)
        new_op = RemoveOperation(
            {
                "op": "remove",
                "path": _path_join(path, key),
            }
        )
        index_key = item_key if item_key is not None else item
        index = self.take_index(index_key, _ST_ADD)
        new_index = self.insert(new_op)
        if index is not None:
            op = index[2]
            # We can't rely on the op.key type since PatchOperation casts
            # the .key property to int and this path wrongly ends up being taken
            # for numeric string dict keys while the intention is to only handle lists.
            # So we do an explicit check on the item affected by the op instead.
            added_item = op.to_last(self.dst_doc)
            if isinstance(added_item, list):
                for v in self.iter_from(index):
                    op.key = v._on_undo_add(op.path, op.key)

            self.remove(index)
            if new_op.location != op.location:
                new_op = MoveOperation(
                    {
                        "op": "move",
                        "from": new_op.location,
                        "path": op.location,
                    }
                )
                new_index[2] = new_op

            else:
                self.remove(new_index)

        else:
            self.store_index(index_key, new_index, _ST_REMOVE)
            self._remove_control(item, frozen)

    def _item_replaced(self, parent, path, key, item, frozen=False):
        print("_item_replaced:", path, key, item, frozen)
        self._configure_dataclass(item, parent, frozen)
        self.insert(
            ReplaceOperation(
                {
                    "op": "replace",
                    "path": _path_join(path, key),
                    "value": item,
                }
            )
        )

    def _compare_dicts(self, parent, path, src, dst, frozen):
        # print("\n_compare_dicts:", path, src, dst)

        src_keys = set(src.keys())
        dst_keys = set(dst.keys())
        added_keys = dst_keys - src_keys
        removed_keys = src_keys - dst_keys

        for key in removed_keys:
            self._item_removed(path, str(key), src[key], frozen=frozen)

        for key in added_keys:
            self._item_added(parent, path, str(key), dst[key], frozen=frozen)

        for key in src_keys & dst_keys:
            self._compare_values(parent, path, key, src[key], dst[key], frozen)

    def _compare_lists(self, parent, path, src, dst, frozen):
        # print("\n_compare_lists:", path, src, dst)

        len_src, len_dst = len(src), len(dst)
        max_len = max(len_src, len_dst)
        min_len = min(len_src, len_dst)
        for key in range(max_len):
            if key < min_len:
                old, new = src[key], dst[key]

                if isinstance(old, dict) and isinstance(new, dict):
                    self._compare_dicts(parent, _path_join(path, key), old, new, frozen)

                elif isinstance(old, list) and isinstance(new, list):
                    self._compare_lists(parent, _path_join(path, key), old, new, frozen)

                elif dataclasses.is_dataclass(old) and dataclasses.is_dataclass(new):
                    frozen = (
                        (old is not None and hasattr(old, "_frozen"))
                        or (new is not None and hasattr(new, "_frozen"))
                        or frozen
                    )

                    old_list_key = getattr(old, "list_key", None)
                    new_list_key = getattr(new, "list_key", None)

                    if (not frozen and old is new) or (
                        frozen
                        and old is not new  # not a cached control tree
                        and type(old) is type(new)  # iteams are of the same type
                        and (
                            old_list_key is None
                            or new_list_key is None
                            or old_list_key == new_list_key
                        )  # same list key or both None
                    ):
                        # print("\n\ncompare list dataclasses:", new)
                        self._compare_dataclasses(
                            parent, _path_join(path, key), old, new, frozen
                        )
                    elif frozen and old is not new:
                        # print(
                        #     "\n\ndataclass removed and added:",
                        #     "\n\nOLD:",
                        #     old,
                        #     "\n\nNEW:",
                        #     new,
                        # )
                        self._item_removed(
                            path,
                            key,
                            old,
                            item_key=(old_list_key, path)
                            if old_list_key is not None
                            else old,
                            frozen=frozen,
                        )
                        self._item_added(
                            parent,
                            path,
                            key,
                            new,
                            item_key=(new_list_key, path)
                            if new_list_key is not None
                            else new,
                            configure_dataclass=False,
                            frozen=frozen,
                        )

                elif type(old) is not type(new) or old != new:
                    # print("removed and added:", old, new)
                    self._item_removed(path, key, old, frozen=frozen)
                    self._item_added(
                        parent, path, key, new, configure_dataclass=False, frozen=frozen
                    )

            elif len_src > len_dst:
                list_key = getattr(src[key], "list_key", None)
                self._item_removed(
                    path,
                    len_dst,
                    src[key],
                    item_key=(list_key, path) if list_key is not None else src[key],
                    frozen=frozen,
                )

            else:
                list_key = getattr(dst[key], "list_key", None)
                self._item_added(
                    parent,
                    path,
                    key,
                    dst[key],
                    item_key=(list_key, path) if list_key is not None else dst[key],
                    frozen=frozen,
                )

    def _compare_dataclasses(self, parent, path, src, dst, frozen):
        # print("\n_compare_dataclasses:", path, src, dst, frozen)

        if (
            self.control_cls
            and isinstance(parent, self.control_cls)
            and parent.is_isolated()
            and parent != self.dst_doc
        ):
            return  # do not update isolated control's children

        if self.control_cls and isinstance(dst, self.control_cls):
            parent = dst
            dst.before_update()

        if not frozen:
            # in-place comparison
            changes = getattr(dst, "__changes", {})
            prev_lists = getattr(dst, "__prev_lists", {})
            prev_dicts = getattr(dst, "__prev_dicts", {})
            prev_classes = getattr(dst, "__prev_classes", {})

            for field_name, change in changes.items():
                old = change[0]
                new = change[1]

                # print("_compare_values:changes", old, new)

                self._compare_values(parent, path, field_name, old, new, frozen)

                # update prev value
                if isinstance(new, list):
                    new = new[:]
                    prev_lists[field_name] = new
                elif isinstance(new, dict):
                    new = new.copy()
                    prev_dicts[field_name] = new
                elif dataclasses.is_dataclass(new):
                    prev_classes[field_name] = new

            # compare lists
            for field_name, old in list(prev_lists.items()):
                if field_name in changes:
                    if new is None:
                        del prev_lists[field_name]
                    continue
                new = getattr(dst, field_name)
                self._compare_values(parent, path, field_name, old, new, frozen)
                prev_lists[field_name] = new[:]

            # compare dicts
            for field_name, old in list(prev_dicts.items()):
                if field_name in changes:
                    if new is None:
                        del prev_dicts[field_name]
                    continue
                new = getattr(dst, field_name)
                self._compare_values(parent, path, field_name, old, new, frozen)
                prev_dicts[field_name] = new.copy()

            # compare dataclasses
            for field_name, old in list(prev_classes.items()):
                if field_name in changes:
                    if new is None:
                        del prev_classes[field_name]
                    continue
                new = getattr(dst, field_name)
                self._compare_values(parent, path, field_name, old, new, frozen)
                prev_classes[field_name] = new

            changes.clear()
        else:
            # frozen comparison
            # print("\nfrozen dataclass compare:", src, dst)
            for field in dataclasses.fields(dst):
                if field.compare:
                    old = getattr(src, field.name)
                    new = getattr(dst, field.name)
                    self._compare_values(parent, path, field.name, old, new, frozen)
            self._configure_dataclass(
                dst, parent, frozen=frozen, configure_setattr_only=True
            )

    def _compare_values(self, parent, path, key, src, dst, frozen):
        # print("\n_compare_values:", path, key, src, dst, frozen)

        if isinstance(src, dict) and isinstance(dst, dict):
            self._compare_dicts(parent, _path_join(path, key), src, dst, frozen)

        elif isinstance(src, list) and isinstance(dst, list):
            if (len(src) == 0 and len(dst) > 0) or (len(src) > 0 and len(dst) == 0):
                self._item_replaced(parent, path, key, dst, frozen=frozen)
                self._remove_control(src, frozen)
            else:
                self._compare_lists(parent, _path_join(path, key), src, dst, frozen)

        elif dataclasses.is_dataclass(src) and dataclasses.is_dataclass(dst):
            frozen = (
                (src is not None and hasattr(src, "_frozen"))
                or (dst is not None and hasattr(dst, "_frozen"))
                or frozen
            )

            # print("\n_compare_values:dataclasses", src, dst, frozen)

            if (not frozen and src is dst) or (
                frozen and src is not dst and type(src) is type(dst)
            ):
                self._compare_dataclasses(
                    parent, _path_join(path, key), src, dst, frozen
                )
            elif (not frozen and src is not dst) or (
                frozen and type(src) is not type(dst)
            ):
                self._item_replaced(parent, path, key, dst, frozen=frozen)
                self._remove_control(src, frozen)

        elif type(src) is not type(dst) or src != dst:
            self._item_replaced(parent, path, key, dst, frozen=frozen)
            self._remove_control(src, frozen)

    def _configure_dataclass(self, item, parent, frozen, configure_setattr_only=False):
        if dataclasses.is_dataclass(item):
            # print("\n_configure_dataclass:", item, frozen)
            # set parent
            if parent:
                # print(
                #     f"\n*** _configure_control: ***\n\nitem: {item._c}({item._i})""
                # "\nparent: {parent._c}({parent._i})"
                # )
                # if hasattr(item, "_parent"):
                #     raise Exception(
                #         f"Control {item._c}({item._i}) is already a part of "
                # "{item.parent._c}({item.parent._i})."
                #     )
                item._parent = weakref.ref(parent)

            if frozen:
                item._frozen = frozen

            def control_setattr(obj, name, value):
                if not name.startswith("_") and (
                    name != "data"
                    or not self.control_cls
                    or not isinstance(obj, self.control_cls)
                ):
                    if hasattr(obj, "_frozen"):
                        raise Exception(
                            "Controls inside data view cannot be updated."
                        ) from None

                    if hasattr(obj, "__changes"):
                        old_value = getattr(obj, name, None)
                        if name.startswith("on_"):
                            old_value = old_value is not None
                        new_value = (
                            value if not name.startswith("on_") else value is not None
                        )
                        if old_value != new_value:
                            # print(
                            #     f"set_attr: {obj.__class__.__name__}.{name} = "
                            #     f"{new_value}, old: {old_value}"
                            # )
                            changes = getattr(obj, "__changes")
                            changes[name] = (old_value, new_value)
                object.__setattr__(obj, name, value)

            item.__class__.__setattr__ = control_setattr  # type: ignore

            if not configure_setattr_only:
                if self.control_cls and isinstance(item, self.control_cls):
                    item.init()

                # recurse through fields
                for field in dataclasses.fields(item):
                    if "skip" not in field.metadata:
                        self._configure_dataclass(
                            getattr(item, field.name), item, frozen
                        )

                if self.control_cls and isinstance(item, self.control_cls):
                    # register new control
                    self.added_controls.append(item)

                    # call Control.before_update()
                    item.before_update()

                if not frozen:
                    setattr(item, "__changes", {})

        elif isinstance(item, dict):
            for v in item.values():
                self._configure_dataclass(v, parent, frozen)

        elif isinstance(item, list):
            for v in item:
                self._configure_dataclass(v, parent, frozen)

    def _remove_control(self, item, frozen):
        if self.control_cls and isinstance(item, self.control_cls):
            if not frozen:
                # recurse through list props
                for item_list in getattr(item, "__prev_lists", {}).values():
                    self._remove_control(item_list, frozen)

                # recurse through dict props
                for item_dict in getattr(item, "__prev_dicts", {}).values():
                    self._remove_control(item_dict, frozen)

                # recurse through dataclass props
                for item_class in getattr(item, "__prev_classes", {}).values():
                    self._remove_control(item_class, frozen)
            else:
                # recurse through fields
                for field in dataclasses.fields(item):
                    if "skip" not in field.metadata:
                        self._remove_control(getattr(item, field.name), frozen)

            self.removed_controls.append(item)

        elif isinstance(item, dict):
            for v in item.values():
                self._remove_control(v, frozen)

        elif isinstance(item, list):
            for v in item:
                self._remove_control(v, frozen)


def _path_join(path, key):
    if key is None:
        return path
    return path + [key]
