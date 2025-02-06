# -*- coding: utf-8 -*-
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

""" Apply JSON-Patches (RFC 6902) """

import dataclasses

_ST_ADD = 0
_ST_REMOVE = 1


class JsonPatchException(Exception):
    """Base Json Patch exception"""


class InvalidJsonPatch(JsonPatchException):
    """Raised if an invalid JSON Patch is created"""


class PatchOperation(object):
    """A single operation inside a JSON Patch."""

    def __init__(self, operation):

        if not operation.__contains__("path"):
            raise InvalidJsonPatch("Operation must have a 'path' member")

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


class JsonPatch(object):
    """A JSON Patch is a list of Patch Operations.

    >>> patch = JsonPatch([
    ...     {'op': 'add', 'path': '/foo', 'value': 'bar'},
    ...     {'op': 'add', 'path': '/baz', 'value': [1, 2, 3]},
    ...     {'op': 'remove', 'path': '/baz/1'},
    ...     {'op': 'test', 'path': '/baz', 'value': [1, 3]},
    ...     {'op': 'replace', 'path': '/baz/0', 'value': 42},
    ...     {'op': 'remove', 'path': '/baz/1'},
    ... ])
    >>> doc = {}
    >>> result = patch.apply(doc)
    >>> expected = {'foo': 'bar', 'baz': [42]}
    >>> result == expected
    True
    """

    def __init__(self, patch):
        self.patch = patch

    def __str__(self):
        return str(self.patch)

    @classmethod
    def from_diff(
        cls,
        src,
        dst,
        in_place=False,
    ):
        builder = DiffBuilder(src, dst, in_place=in_place)
        builder._compare_values([], None, src, dst)
        ops = list(builder.execute())
        return cls(ops)


class DiffBuilder(object):

    def __init__(self, src_doc, dst_doc, in_place=False):
        self.in_place = in_place
        self.index_storage = [{}, {}]
        self.index_storage2 = [[], []]
        self.__root = root = []
        self.src_doc = src_doc
        self.dst_doc = dst_doc
        root[:] = [root, root, None]
        self.dt_cls = []  # stack of dataclasses to save "previous" state

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
                    and type(op_first) == RemoveOperation
                    and type(op_second) == AddOperation
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

    def _item_added(self, path, key, item):
        index = self.take_index(item, _ST_REMOVE)
        if index is not None:
            op = index[2]
            if type(op.key) == int and type(key) == int:
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
            self.store_index(item, new_index, _ST_ADD)

    def _item_removed(self, path, key, item):
        new_op = RemoveOperation(
            {
                "op": "remove",
                "path": _path_join(path, key),
            }
        )
        index = self.take_index(item, _ST_ADD)
        new_index = self.insert(new_op)
        if index is not None:
            op = index[2]
            # We can't rely on the op.key type since PatchOperation casts
            # the .key property to int and this path wrongly ends up being taken
            # for numeric string dict keys while the intention is to only handle lists.
            # So we do an explicit check on the item affected by the op instead.
            added_item = op.pointer.to_last(self.dst_doc)[0]
            if type(added_item) == list:
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
            self.store_index(item, new_index, _ST_REMOVE)

    def _item_replaced(self, path, key, item):
        self.insert(
            ReplaceOperation(
                {
                    "op": "replace",
                    "path": _path_join(path, key),
                    "value": item,
                }
            )
        )

    def _compare_dicts(self, path, src, dst):
        # print("\n_compare_dicts:", path, src, dst)

        src_keys = set(src.keys())
        dst_keys = set(dst.keys())
        added_keys = dst_keys - src_keys
        removed_keys = src_keys - dst_keys

        for key in removed_keys:
            self._item_removed(path, str(key), src[key])

        for key in added_keys:
            self._item_added(path, str(key), dst[key])

        for key in src_keys & dst_keys:
            self._compare_values(path, key, src[key], dst[key])

    def _compare_lists(self, path, src, dst):
        # print("\n_compare_lists:", path, src, dst)

        len_src, len_dst = len(src), len(dst)
        max_len = max(len_src, len_dst)
        min_len = min(len_src, len_dst)
        for key in range(max_len):
            if key < min_len:
                old, new = src[key], dst[key]

                if isinstance(old, dict) and isinstance(new, dict):
                    self._compare_dicts(_path_join(path, key), old, new)

                elif isinstance(old, list) and isinstance(new, list):
                    self._compare_lists(_path_join(path, key), old, new)

                elif (
                    dataclasses.is_dataclass(old)
                    and dataclasses.is_dataclass(new)
                    and (
                        (self.in_place and old == new)
                        or (not self.in_place and type(old) == type(new))
                    )
                ):
                    self._compare_dataclasses(_path_join(path, key), old, new)

                elif type(old) != type(new) or old != new:
                    self._item_removed(path, key, old)
                    self._item_added(path, key, new)

            elif len_src > len_dst:
                self._item_removed(path, len_dst, src[key])

            else:
                self._item_added(path, key, dst[key])

    def _compare_dataclasses(self, path, src, dst):
        # print("\n_compare_dataclasses:", path, src, dst)

        # push dataclass on stack
        self.dt_cls.append(dst)

        for field in dataclasses.fields(dst):
            old = (
                getattr(src, field.name)
                if not self.in_place
                else getattr(src, f"_prev_{field.name}")
            )
            new = getattr(dst, field.name)
            self._compare_values(path, field.name, old, new)

            # update prev value
            if isinstance(new, list):
                new = new[:]
            elif isinstance(new, dict):
                new = new.copy()
            setattr(dst, f"_prev_{field.name}", new)

    def _compare_values(self, path, key, src, dst):
        # print("\n_compare_values:", path, key, src, dst)

        if isinstance(src, dict) and isinstance(dst, dict):
            self._compare_dicts(_path_join(path, key), src, dst)

        elif isinstance(src, list) and isinstance(dst, list):
            self._compare_lists(_path_join(path, key), src, dst)

        elif (
            dataclasses.is_dataclass(src)
            and dataclasses.is_dataclass(dst)
            and (
                (self.in_place and src == dst)
                or (not self.in_place and type(src) == type(dst))
            )
        ):
            self._compare_dataclasses(_path_join(path, key), src, dst)

        elif type(src) != type(dst) or src != dst:
            self._item_replaced(path, key, dst)


def _path_join(path, key):
    if key is None:
        return path
    return path + [key]
