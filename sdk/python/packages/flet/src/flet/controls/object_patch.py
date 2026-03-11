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
import itertools
import logging
import weakref
from enum import Enum
from typing import Any, Optional

from flet.controls.keys import Key

logger = logging.getLogger("flet_object_patch")
logger.setLevel(logging.INFO)

_ST_ADD = 0
_ST_REMOVE = 1


class Operation(Enum):
    Replace = 0
    Add = 1
    Remove = 2
    Move = 3


class ObjectPatchException(Exception):
    """Base Object Patch exception"""


class InvalidObjectPatch(ObjectPatchException):
    """Raised if an invalid Object Patch is created"""


class PatchOperation:
    """A single operation inside an Object Patch."""

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


def _control_setattr(obj, name, value):
    # For plain dataclasses (no Prop tracking), this hook records the old
    # value in __changes so _compare_dataclasses can detect the change.
    # Prop-managed fields (on @control/@value types) are fully handled by
    # Prop.__set__ and do not go through this path.
    control_cls = getattr(type(obj), "__flet_control_cls__", None)
    if not name.startswith("_") and (
        name != "data" or not control_cls or not isinstance(obj, control_cls)
    ):
        prop_defaults = getattr(type(obj), "_prop_defaults", None)
        if prop_defaults is not None and name in prop_defaults:
            # Prop field: delegate entirely to Prop.__set__ via normal setattr.
            pass
        else:
            if hasattr(obj, "_frozen"):
                raise RuntimeError("Frozen controls cannot be updated.") from None
            # Track first-write old value for plain-dataclass scalar fields.
            changes = getattr(obj, "__changes", None)
            if changes is not None and name not in changes:
                changes[name] = getattr(obj, name, None)
            if hasattr(obj, "_notify"):
                obj._notify(name, value)
    object.__setattr__(obj, name, value)


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
        parent: Any = None,
        path: Optional[list[Any]] = None,
        frozen: bool = False,
    ):
        builder = DiffBuilder(
            src,
            dst,
            control_cls=control_cls,
        )
        builder._compare_values(parent, path or [], None, src, dst, frozen=frozen)

        ops = list(builder.execute())
        added = list(builder.get_added_controls())
        removed = list(builder.get_removed_controls())

        builder.teardown()

        return cls(ops), added, removed

    def to_message(self):
        state = {"i": 0}
        paths = [state["i"]]
        state["i"] += 1

        def encode_path(path):
            node = paths
            parent = paths
            parts = path
            len_parts = len(parts)
            if len_parts == 0:
                return [0, 0]  # root object
            n = 0
            while n < len_parts - 1:
                if len(parent) == 1:
                    parent.append({})
                node = parent[1].get(parts[n], None)
                if node is None:
                    node = [state["i"]]
                    parent[1][parts[n]] = node
                    state["i"] += 1
                parent = node
                n += 1
            return [node[0], parts[n]]

        ops = []
        for op in self.patch:
            if op["op"] == "remove":
                ops.append(
                    [
                        Operation.Remove,
                        *encode_path(op["path"]),
                    ]
                )
            elif op["op"] == "replace":
                ops.append(
                    [
                        Operation.Replace,
                        *encode_path(op["path"]),
                        op["value"],
                    ]
                )
            elif op["op"] == "add":
                ops.append(
                    [
                        Operation.Add,
                        *encode_path(op["path"]),
                        op["value"],
                    ]
                )
            elif op["op"] == "move":
                ops.append(
                    [
                        Operation.Move,
                        *encode_path(op["from"]),
                        *encode_path(op["path"]),
                    ]
                )
            else:
                raise ObjectPatchException(f"Unknown operation: {op['op']}")

        return [paths, *ops]


class DiffBuilder:
    def __init__(
        self,
        src_doc,
        dst_doc,
        control_cls=None,
    ):
        self.control_cls = control_cls
        self._added_dataclasses = {}
        self._removed_dataclasses = {}
        self.index_storage = [{}, {}]
        self.index_storage2 = [[], []]
        self.__root = root = []
        self.src_doc = src_doc
        self.dst_doc = dst_doc
        root[:] = [root, root, None]

    @staticmethod
    def _update_list_snapshot(
        snapshots: dict[Any, list[Any]], key: Any, value: list[Any]
    ) -> None:
        snap = snapshots.get(key)
        if snap is None:
            snapshots[key] = value[:]
            return
        snap[:] = value

    @staticmethod
    def _update_dict_snapshot(
        snapshots: dict[Any, dict[Any, Any]], key: Any, value: dict[Any, Any]
    ) -> None:
        snap = snapshots.get(key)
        if snap is None:
            snapshots[key] = value.copy()
            return
        snap.clear()
        snap.update(value)

    def teardown(self):
        """Break cycles and release strong references to allow GC."""
        # clear indexes
        self.index_storage = [{}, {}]
        self.index_storage2 = [[], []]
        self._added_dataclasses.clear()
        self._removed_dataclasses.clear()

        # break the doubly linked list cycle
        root = self.__root
        if root:
            root[:] = [root, root, None]

        # drop references to source/target docs
        self.src_doc = None
        self.dst_doc = None

    def get_added_controls(self):
        for key, dc in self._added_dataclasses.items():
            configure_setattr_only = key in self._removed_dataclasses
            yield from self._configure_dataclass(
                dc, None, False, configure_setattr_only
            )

    def get_removed_controls(self):
        for key, dc in self._removed_dataclasses.items():
            recurse = key not in self._added_dataclasses
            yield from self._removed_controls(dc, recurse)

    def store_index(self, value, index, st):
        value_type = type(value)
        try:
            storage = self.index_storage[st]
            typed_storage = storage.get(value_type)
            if typed_storage is None:
                typed_storage = {}
                storage[value_type] = typed_storage
            stored = typed_storage.get(value)
            if stored is None:
                typed_storage[value] = [index]
            else:
                stored.append(index)

        except TypeError:
            self.index_storage2[st].append([value_type, value, index])

    def take_index(self, value, st):
        value_type = type(value)
        try:
            typed_storage = self.index_storage[st].get(value_type)
            if typed_storage is None:
                return None
            stored = typed_storage.get(value)
            if stored:
                return stored.pop()

        except TypeError:
            storage = self.index_storage2[st]
            for i in range(len(storage) - 1, -1, -1):
                item_type, item_value, item_index = storage[i]
                if item_type is value_type and item_value == value:
                    storage.pop(i)
                    return item_index

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

    def _index_key(self, item, item_key, path):
        """
        Return the composite key used to pair add/remove (by control key if present).
        """
        return item_key if item_key is not None else item

    def _maybe_compare_dataclasses(self, parent, path, src, dst, frozen):
        """
        Compare dataclasses only when both are dataclasses and identity/"frozen" rules \
        allow it.
        """
        if not (dataclasses.is_dataclass(src) and dataclasses.is_dataclass(dst)):
            return
        if not frozen and src is dst:
            # Non-frozen in-place: same Python object, use __changes tracking.
            self._compare_dataclasses(parent, path, src, dst, False)
        elif src is not dst and type(src) is type(dst):
            # Different Python objects of the same type.
            # Frozen diff always applies; non-frozen applies when they share an
            # explicit key (rebuilt object scenario – treat as frozen comparison).
            same_explicit_key = (
                not frozen
                and get_control_key(src) is not None
                and get_control_key(src) == get_control_key(dst)
            )
            if frozen or same_explicit_key:
                self._compare_dataclasses(parent, path, src, dst, True)

    def _affected_is_list(self, op):
        """
        Return True if the item the op affects lives in a list in the destination doc.
        We must not rely on op.key’s type because PatchOperation coerces to int.
        """
        container = op.to_last(self.dst_doc)
        return isinstance(container, list)

    def _emit_move(self, from_loc, to_loc):
        """Create and insert a move operation."""
        self.insert(MoveOperation({"op": "move", "from": from_loc, "path": to_loc}))

    def _item_added(self, parent, path, key, item, item_key=None, frozen=False):
        logger.debug(
            f"_item_added: path={path} key={key} item={item} item_key={item_key}"
        )

        index_key = self._index_key(item, item_key, path)
        paired_idx = self.take_index(index_key, _ST_REMOVE)

        # A matching 'remove' exists: it's a move (or an in-place update)
        if paired_idx is not None:
            rem_op: RemoveOperation = paired_idx[2]  # the earlier remove
            src = rem_op.operation["value"]
            dst = item

            # undo bookkeeping for the removed dataclass (it’s coming back)
            self._undo_dataclass_removed(src)

            # If the affected sequence is a list, adjust later op indices after removal
            if isinstance(rem_op.key, int) and isinstance(key, int):
                for v in self.iter_from(paired_idx):
                    rem_op.key = v._on_undo_remove(rem_op.path, rem_op.key)

            # Drop the paired remove from the chain: we’re going to emit either
            # compares or a move
            self.remove(paired_idx)

            src_loc = rem_op.location
            dst_loc = _path_join(path, key)

            # Compare first (for dataclasses), anchored at source or dest depending
            # on whether we move
            if src_loc != dst_loc:
                # Compare on the source location before we move (matches your tests’
                # expectations)
                self._maybe_compare_dataclasses(parent, src_loc, src, dst, frozen)
                # Then emit the move
                self._emit_move(src_loc, dst_loc)
                return
            else:
                # No move, just in-place updates
                self._maybe_compare_dataclasses(parent, dst_loc, src, dst, frozen)
                return

        # No matching remove: this is a plain add
        add_op = AddOperation(
            {"op": "add", "path": _path_join(path, key), "value": item}
        )
        add_idx = self.insert(add_op)
        self.store_index(index_key, add_idx, _ST_ADD)
        self._dataclass_added(item, parent, frozen)

    def _item_removed(self, path, key, item, item_key=None, frozen=False):
        logger.debug(
            f"_item_removed: path={path} key={key} item={item} item_key={item_key}"
        )

        index_key = self._index_key(item, item_key, path)
        rem_op = RemoveOperation(
            {"op": "remove", "path": _path_join(path, key), "value": item}
        )
        rem_idx = self.insert(rem_op)

        paired_idx = self.take_index(index_key, _ST_ADD)

        # A matching 'add' exists: it's a move (or an in-place update)
        if paired_idx is not None:
            add_op: AddOperation = paired_idx[2]  # the earlier add
            src = item
            dst = add_op.operation["value"]

            # undo bookkeeping for the added dataclass (it’s being consumed by the move)
            self._undo_dataclass_added(dst)

            # If the added op affects a list, adjust later ops after that add
            if self._affected_is_list(add_op):
                for v in self.iter_from(paired_idx):
                    add_op.key = v._on_undo_add(add_op.path, add_op.key)

            src_loc = rem_op.location
            dst_loc = add_op.location

            # The earlier add no longer stands on its own
            self.remove(paired_idx)

            if src_loc != dst_loc:
                # If we’re moving, compare anchored at the source BEFORE the move
                # (matches your tests)
                self._maybe_compare_dataclasses(
                    dst.parent if hasattr(dst, "parent") else None,
                    src_loc,
                    src,
                    dst,
                    frozen,
                )
                # Turn the just-inserted remove into a move (reuse node)
                rem_idx[2] = MoveOperation(
                    {"op": "move", "from": src_loc, "path": dst_loc}
                )
                return
            else:
                # No move after all; drop the remove from the chain (pair consumed)
                self.remove(rem_idx)
                # In-place updates only
                self._maybe_compare_dataclasses(
                    dst.parent if hasattr(dst, "parent") else None,
                    _path_join(add_op.path, add_op.key),
                    src,
                    dst,
                    frozen,
                )
                return

        # No matching add: keep the remove and remember this dataclass
        self.store_index(index_key, rem_idx, _ST_REMOVE)
        self._dataclass_removed(item)

    def _item_replaced(self, path, key, item):
        logger.debug("_item_replaced: %s %s %s:", path, key, item)
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
        logger.debug("\n_compare_dicts: %s %s %s", path, src, dst)

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
        logger.debug("\n_compare_lists: %s %s %s", path, src, dst)

        # Decide algorithm based on whether any dataclasses are present.
        # Pure-primitive / pure-dict lists use the simpler positional algorithm which
        # produces minimal diffs for insertion/deletion.  Lists that contain at least
        # one dataclass use the hybrid keyed algorithm which preserves identity across
        # reorders and across Python-object rebuilds (when explicit keys are provided).
        has_any_dataclass = any(
            dataclasses.is_dataclass(obj) for obj in itertools.chain(src, dst)
        )

        if not has_any_dataclass:
            # ----- Positional diff for pure-primitive / pure-dict lists -----
            len_src, len_dst = len(src), len(dst)
            max_len = max(len_src, len_dst)
            min_len = min(len_src, len_dst)
            for key in range(max_len):
                if key < min_len:
                    old, new = src[key], dst[key]
                    logger.debug(
                        f"\n\nCOMPARE LIST ITEM: {key}\n\nOLD: {old}\n\nNEW: {new}"
                    )
                    if isinstance(old, dict) and isinstance(new, dict):
                        self._compare_dicts(
                            parent, _path_join(path, key), old, new, frozen
                        )
                    elif isinstance(old, list) and isinstance(new, list):
                        self._compare_lists(
                            parent, _path_join(path, key), old, new, frozen
                        )
                    elif type(old) is not type(new) or old != new:
                        self._item_removed(path, key, old, frozen=frozen)
                        self._item_added(parent, path, key, new, frozen=frozen)
                elif len_src > len_dst:
                    self._item_removed(path, len_dst, src[key], frozen=frozen)
                else:
                    self._item_added(parent, path, key, dst[key], frozen=frozen)
            return

        # ----- Hybrid keyed algorithm for lists containing dataclasses -----
        #
        # Composite key assignment:
        #   frozen mode:
        #     explicit key  → ("k", key)       – user-provided logical identity
        #     unkeyed dc    → ("pos", n)        – positional among unkeyed items
        #   non-frozen mode:
        #     explicit key  → ("k", key)        – allows matching rebuilt objects
        #     no explicit   → ("id", id(obj))   – Python-object identity
        #   non-dataclass items (primitives):
        #     always        → ("prim", n)       – positional among non-dc items
        #
        # Using tuple-namespaced keys prevents collisions between the four classes.

        def build_keys(items):
            keys = []
            unkeyed_pos = 0
            prim_pos = 0
            for obj in items:
                if dataclasses.is_dataclass(obj):
                    ek = get_control_key(obj)
                    if ek is not None:
                        keys.append(("k", ek))
                    elif frozen:
                        keys.append(("pos", unkeyed_pos))
                        unkeyed_pos += 1
                    else:
                        keys.append(("id", id(obj)))
                else:
                    keys.append(("prim", prim_pos))
                    prim_pos += 1
            return keys

        src_keys = build_keys(src)
        dst_keys = build_keys(dst)

        # Helper: determine effective frozen flag for a matched (old, new) pair.
        # A non-frozen pair matched by explicit key (different Python objects) must
        # be diffed like a frozen pair since the new object has no __changes log.
        def _effective_frozen(old_item, new_item):
            if frozen:
                return True
            if old_item is not new_item:
                old_ck = get_control_key(old_item)
                if old_ck is not None and old_ck == get_control_key(new_item):
                    return True
            return False

        if src_keys == dst_keys:
            # Keys identical and in the same order: positional diff (fast path).
            for idx, (old, new) in enumerate(zip(src, dst)):
                if isinstance(old, dict) and isinstance(new, dict):
                    self._compare_dicts(parent, _path_join(path, idx), old, new, frozen)
                elif isinstance(old, list) and isinstance(new, list):
                    self._compare_lists(parent, _path_join(path, idx), old, new, frozen)
                elif dataclasses.is_dataclass(old) and dataclasses.is_dataclass(new):
                    same_type = type(old) is type(new)
                    same_component_fn = True
                    if (
                        getattr(old, "_c", None) == "C"
                        and getattr(new, "_c", None) == "C"
                    ):
                        same_component_fn = getattr(old, "fn", None) is getattr(
                            new, "fn", None
                        )
                    if same_type and same_component_fn:
                        frozen_eff = _effective_frozen(old, new)
                        self._compare_dataclasses(
                            parent, _path_join(path, idx), old, new, frozen_eff
                        )
                    else:
                        # Different types or different component function: use
                        # remove+add so controls are registered in added/removed
                        # sets; execute() collapses same-path pairs to replace.
                        self._item_removed(path, idx, old, frozen=frozen)
                        self._item_added(parent, path, idx, new, frozen=frozen)
                elif type(old) is not type(new) or old != new:
                    self._item_replaced(path, idx, new)
            return

        # -------- Keyed, React-style reconciliation --------
        # We’ll mutate a working copy of the old list so emitted indices are "live".
        work = list(src)
        work_keys = src_keys[:]
        # Map key -> current index in `work`
        pos = {key: i for i, key in enumerate(work_keys)}
        new_index_by_key = {key: i for i, key in enumerate(dst_keys)}
        new_keys_set = set(new_index_by_key.keys())

        def _reindex(start_idx: int) -> None:
            for j in range(start_idx, len(work_keys)):
                pos[work_keys[j]] = j

        def _remove_from_work(idx: int):
            removed_item = work.pop(idx)
            removed_key = work_keys.pop(idx)
            pos.pop(removed_key, None)
            if idx < len(work_keys):
                _reindex(idx)
            return removed_item, removed_key

        def _insert_into_work(idx: int, item, key):
            work.insert(idx, item)
            work_keys.insert(idx, key)
            pos[key] = idx
            if idx + 1 <= len(work_keys):
                _reindex(idx + 1)

        def emit_replace_at(idx, old_item, new_item):
            # Keying by identity means old_item is often new_item, so we explicitly run
            # the dataclass diff even when the instance pointer matches to surface
            # property mutations captured by __changes.
            if dataclasses.is_dataclass(old_item) and dataclasses.is_dataclass(
                new_item
            ):
                frozen_local = (
                    (old_item is not None and hasattr(old_item, "_frozen"))
                    or (new_item is not None and hasattr(new_item, "_frozen"))
                    or _effective_frozen(old_item, new_item)
                )
                old_control_key = get_control_key(old_item)
                new_control_key = get_control_key(new_item)

                def _keys_match():
                    return (
                        old_control_key is None
                        or new_control_key is None
                        or old_control_key == new_control_key
                    )

                same_type = type(old_item) is type(new_item)
                same_component_fn = True
                # Component controls (type "C") must only be diffed/migrated when
                # their underlying component function is the same. Otherwise we
                # need a replace to force remount and fresh hook state.
                if (
                    getattr(old_item, "_c", None) == "C"
                    and getattr(new_item, "_c", None) == "C"
                ):
                    same_component_fn = getattr(old_item, "fn", None) is getattr(
                        new_item, "fn", None
                    )

                if (not frozen_local and old_item is new_item) or (
                    frozen_local
                    and old_item is not new_item
                    and same_type
                    and same_component_fn
                    and _keys_match()
                ):
                    self._compare_dataclasses(
                        parent, _path_join(path, idx), old_item, new_item, frozen_local
                    )
                    return

            if type(old_item) is not type(new_item) or old_item != new_item:
                if dataclasses.is_dataclass(old_item) or dataclasses.is_dataclass(
                    new_item
                ):
                    # Controls must go through remove+add so the added/removed
                    # registries stay consistent; execute() folds adjacent
                    # same-path pairs into a replace op.
                    self._item_removed(path, idx, old_item, frozen=frozen)
                    self._item_added(parent, path, idx, new_item, frozen=frozen)
                else:
                    self._item_replaced(path, idx, new_item)

        # Scan forward through desired new order.
        i = 0
        while i < len(dst):
            target_key = dst_keys[i]

            # First, delete any items currently at position i that should NOT be here:
            # - keys that don't exist anymore
            # - or keys that exist but must appear BEFORE i in the new order
            #   (they are out of place here)
            while i < len(work):
                cur_key = work_keys[i]
                if cur_key not in new_keys_set:
                    # remove disappearing item at i
                    self._item_removed(
                        path, i, work[i], item_key=(cur_key, path), frozen=frozen
                    )
                    _remove_from_work(i)
                    continue
                desired_pos = new_index_by_key[cur_key]
                if desired_pos < i:
                    # this item belongs earlier; it should have already been moved
                    # before.
                    # remove it here; it will be re-inserted (moved) where needed.
                    self._item_removed(
                        path, i, work[i], item_key=(cur_key, path), frozen=frozen
                    )
                    _remove_from_work(i)
                    continue
                break  # current slot is ok to fill with target

            if target_key in pos:
                cur_idx = pos[target_key]
                old_item = work[cur_idx]
                new_item = dst[i]

                if cur_idx == i:
                    # in place: just emit updates
                    emit_replace_at(i, old_item, new_item)
                else:
                    # move from cur_idx -> i
                    # Emit updates anchored at SOURCE (cur_idx) before the move
                    # (matches your tests)
                    emit_replace_at(cur_idx, old_item, new_item)

                    # Emit move
                    move_op = MoveOperation(
                        {
                            "op": "move",
                            "from": _path_join(path, cur_idx),
                            "path": _path_join(path, i),
                        }
                    )
                    self.insert(move_op)

                    # Apply the move in our working model
                    moved_item, _ = _remove_from_work(cur_idx)
                    insert_idx = i if cur_idx >= i else i
                    _insert_into_work(insert_idx, moved_item, target_key)
            else:
                # brand-new key: add at i
                self._item_added(
                    parent,
                    path,
                    i,
                    dst[i],
                    item_key=(target_key, path),
                    frozen=frozen,
                )
                _insert_into_work(i, dst[i], target_key)

            i += 1

        # Finally, remove any trailing leftovers (present in old but not in new)
        # We remove from the end so indices stay valid.
        j = len(work) - 1
        while j >= 0:
            key_j = work_keys[j]
            if key_j not in new_keys_set:
                self._item_removed(
                    path, j, work[j], item_key=(key_j, path), frozen=frozen
                )
                _remove_from_work(j)
            j -= 1

    def _compare_dataclasses(self, parent, path, src, dst, frozen):
        logger.debug("\n_compare_dataclasses: %s\n\n%s\n%s\n", path, src, dst)

        if (
            self.control_cls
            and isinstance(parent, self.control_cls)
            and parent.is_isolated()
            and parent != self.dst_doc
        ):
            return  # do not update isolated control's children

        if self.control_cls and isinstance(dst, self.control_cls):
            if frozen and hasattr(src, "_i"):
                dst._migrate_state(src)
                if not hasattr(dst, "_initialized"):
                    orig_frozen = getattr(dst, "_frozen", None)
                    if orig_frozen is not None:
                        del dst._frozen
                    dst.build()
                    if orig_frozen is not None:
                        object.__setattr__(dst, "_frozen", orig_frozen)
                    object.__setattr__(dst, "_initialized", True)
            dst._before_update_safe()

        if not frozen:
            # In-place (non-frozen) comparison.
            #
            # Prop-managed scalar/event fields: _dirty (populated by
            # Prop.__set__) records which fields changed.  Emit a replace with
            # the current _values entry — no old-value needed for scalars.
            #
            # Structural fields (lists, dicts, nested dataclasses): __prev_*
            # snapshots from the last protocol serialisation cover both
            # reassignment and in-place mutation, so __changes is not needed.
            dirty = getattr(dst, "_dirty", None)
            prev_lists = getattr(dst, "__prev_lists", {})
            prev_dicts = getattr(dst, "__prev_dicts", {})
            prev_classes = getattr(dst, "__prev_classes", {})

            if dirty:
                _values = getattr(dst, "_values", None)
                prop_defaults = getattr(type(dst), "_prop_defaults", None)
                fields_map = {f.name: f for f in dataclasses.fields(dst)}
                for field_name in dirty:  # dict → insertion order preserved
                    f = fields_map.get(field_name)
                    if f is None or f.metadata.get("skip", False):
                        continue
                    raw = getattr(dst, field_name, None)

                    # Structural fields use _compare_values with the old
                    # snapshot from __prev_*, then update the snapshot.
                    # They are popped from __prev_* so the loops below do not
                    # re-process them.
                    if isinstance(raw, list):
                        old = prev_lists.pop(field_name, [])
                        self._compare_values(dst, path, field_name, old, raw, frozen)
                        self._update_list_snapshot(prev_lists, field_name, raw)
                        continue
                    if isinstance(raw, dict):
                        old = prev_dicts.pop(field_name, {})
                        self._compare_values(dst, path, field_name, old, raw, frozen)
                        self._update_dict_snapshot(prev_dicts, field_name, raw)
                        continue
                    if dataclasses.is_dataclass(raw):
                        old = prev_classes.pop(field_name, None)
                        self._compare_values(dst, path, field_name, old, raw, frozen)
                        prev_classes[field_name] = raw
                        continue
                    if raw is None:
                        # Structural → None transition.
                        if field_name in prev_classes:
                            old = prev_classes.pop(field_name)
                            self._compare_values(
                                dst, path, field_name, old, None, frozen
                            )
                            continue
                        if field_name in prev_lists:
                            old = prev_lists.pop(field_name)
                            self._compare_values(
                                dst, path, field_name, old, None, frozen
                            )
                            continue
                        if field_name in prev_dicts:
                            old = prev_dicts.pop(field_name)
                            self._compare_values(
                                dst, path, field_name, old, None, frozen
                            )
                            continue

                    # Scalar / event field.
                    new = (
                        _values.get(field_name, prop_defaults[field_name])
                        if (_values is not None and prop_defaults is not None)
                        else raw
                    )
                    if f.name.startswith("on_") and f.metadata.get("event", True):
                        new = new is not None
                    logger.debug("\n\n_compare_values:dirty %s %s", field_name, new)
                    self._item_replaced(path, field_name, new)
                dst._dirty.clear()

            # Plain-dataclass scalar changes recorded by _control_setattr.
            changes = getattr(dst, "__changes", None)
            if changes:
                fields_map = (
                    fields_map
                    if dirty
                    else {f.name: f for f in dataclasses.fields(dst)}
                )
                for field_name in list(changes):
                    f = fields_map.get(field_name)
                    if f is None or f.metadata.get("skip", False):
                        continue
                    new = getattr(dst, field_name)
                    if f.name.startswith("on_") and f.metadata.get("event", True):
                        new = new is not None
                    self._item_replaced(path, field_name, new)
                changes.clear()

            # compare lists
            for field_name, old in list(prev_lists.items()):
                new = getattr(dst, field_name)
                if not isinstance(new, list):
                    del prev_lists[field_name]
                self._compare_values(dst, path, field_name, old, new, frozen)
                if isinstance(new, list):
                    self._update_list_snapshot(prev_lists, field_name, new)

            # compare dicts
            for field_name, old in list(prev_dicts.items()):
                new = getattr(dst, field_name)
                if not isinstance(new, dict):
                    del prev_dicts[field_name]
                self._compare_values(dst, path, field_name, old, new, frozen)
                if isinstance(new, dict):
                    self._update_dict_snapshot(prev_dicts, field_name, new)

            # compare dataclasses
            for field_name, old in list(prev_classes.items()):
                new = getattr(dst, field_name)
                if not dataclasses.is_dataclass(new):
                    del prev_classes[field_name]
                else:
                    prev_classes[field_name] = new
                self._compare_values(dst, path, field_name, old, new, frozen)
        else:
            # frozen comparison
            logger.debug(
                "\nfrozen dataclass compare:%s\n\n    dst:%s\n\n    parent:%s",
                src,
                dst,
                parent,
            )
            src_vals = getattr(src, "_values", None)
            dst_vals = getattr(dst, "_values", None)
            if src_vals is not None and dst_vals is not None:
                # Fast path: two focused loops, each proportional to the
                # number of fields that actually need comparing.
                #
                # 1. Structural fields (_i, _c, controls, …) — always compare;
                #    typically just a handful per control type.
                # 2. Active Prop fields — only those non-default on at least
                #    one side; read directly from _values to skip Prop.__get__.
                structural = getattr(type(dst), "_structural_fields", frozenset())
                prop_defaults = getattr(type(dst), "_prop_defaults", {})
                event_fields = getattr(type(dst), "_event_fields", frozenset())

                for fname in structural:
                    old = getattr(src, fname)
                    new = getattr(dst, fname)
                    self._compare_values(dst, path, fname, old, new, frozen)

                for fname in {**src_vals, **dst_vals}:
                    default = prop_defaults.get(fname)
                    old = src_vals.get(fname, default)
                    new = dst_vals.get(fname, default)
                    if old is new or old == new:
                        continue
                    if fname in event_fields:
                        old = old is not None
                        new = new is not None
                    self._compare_values(dst, path, fname, old, new, frozen)
            else:
                # Slow path: full field scan (objects without _values).
                for field in dataclasses.fields(dst):
                    if not field.metadata.get("skip", False):
                        old = getattr(src, field.name)
                        new = getattr(dst, field.name)
                        if field.name.startswith("on_") and field.metadata.get(
                            "event", True
                        ):
                            old = old is not None
                            new = new is not None
                        self._compare_values(dst, path, field.name, old, new, frozen)
            self._dataclass_removed(src)
            self._dataclass_added(dst, parent, frozen)

    def _compare_values(self, parent, path, key, src, dst, frozen):
        logger.debug(
            "\n_compare_values: %s %s (Frozen: %s)\n\n%s\n%s\n",
            path,
            key,
            frozen,
            src,
            dst,
        )

        if isinstance(src, dict) and isinstance(dst, dict):
            if (len(src) == 0 and len(dst) > 0) or (len(src) > 0 and len(dst) == 0):
                self._item_replaced(path, key, dst)
                self._dataclass_removed(src)
                self._dataclass_added(dst, parent, frozen)
            else:
                self._compare_dicts(parent, _path_join(path, key), src, dst, frozen)

        elif isinstance(src, list) and isinstance(dst, list):
            if (len(src) == 0 and len(dst) > 0) or (len(src) > 0 and len(dst) == 0):
                self._item_replaced(path, key, dst)
                self._dataclass_removed(src)
                self._dataclass_added(dst, parent, frozen)
            else:
                self._compare_lists(parent, _path_join(path, key), src, dst, frozen)

        elif dataclasses.is_dataclass(src) and dataclasses.is_dataclass(dst):
            frozen = (
                (src is not None and hasattr(src, "_frozen"))
                or (dst is not None and hasattr(dst, "_frozen"))
                or frozen
            )

            logger.debug(
                "\n_compare_values:dataclasses (Frozen: %s) %s %s", frozen, src, dst
            )

            if (not frozen and src is dst) or (
                frozen and src is not dst and type(src) is type(dst)
            ):
                self._compare_dataclasses(
                    parent, _path_join(path, key), src, dst, frozen
                )
            elif (not frozen and src is not dst) or (
                frozen and type(src) is not type(dst)
            ):
                self._item_replaced(path, key, dst)
                self._dataclass_removed(src)
                self._dataclass_added(dst, parent, frozen)

        elif type(src) is not type(dst) or src != dst:
            logger.debug(
                "\n_compare_values:replaced %s %s %s\n\n%s %s",
                path,
                key,
                src,
                dst,
                frozen,
            )
            self._item_replaced(path, key, dst)
            self._dataclass_removed(src)
            self._dataclass_added(dst, parent, frozen)

            if not frozen:
                prev_lists = getattr(dst, "__prev_lists", {})
                prev_dicts = getattr(dst, "__prev_dicts", {})
                prev_classes = getattr(dst, "__prev_classes", {})

                if isinstance(src, list) and key in prev_lists:
                    del prev_lists[key]
                if isinstance(src, dict) and key in prev_dicts:
                    del prev_dicts[key]
                if dataclasses.is_dataclass(src) and key in prev_classes:
                    del prev_classes[key]
                if isinstance(dst, list) and key is not None:
                    self._update_list_snapshot(prev_lists, key, dst)
                if isinstance(dst, dict) and key is not None:
                    self._update_dict_snapshot(prev_dicts, key, dst)
                if dataclasses.is_dataclass(dst) and key is not None:
                    prev_classes[key] = dst

    def _dataclass_added(self, item, parent, frozen):
        logger.debug("\n\nDataclass added: %s %s %s", item, parent, frozen)
        if dataclasses.is_dataclass(item):
            if parent:
                logger.debug("\n\nAdding parent %s to item: %s", parent, item)
                if parent is item:
                    raise ObjectPatchException(f"Parent is the same as item: {item}")
                item._parent = weakref.ref(parent)
            else:
                logger.debug("\n\nSkip adding parent to item: %s", item)
            if frozen:
                item._frozen = frozen

            logger.debug("\n_dataclass_added: %s", self._get_dataclass_key(item))
            self._added_dataclasses[self._get_dataclass_key(item)] = item

        elif isinstance(item, dict):
            for v in item.values():
                self._dataclass_added(v, parent, frozen)

        elif isinstance(item, list):
            for v in item:
                self._dataclass_added(v, parent, frozen)

    def _undo_dataclass_added(self, item):
        self._added_dataclasses.pop(self._get_dataclass_key(item), None)

    def _dataclass_removed(self, item):
        logger.debug("\n\nDataclass removed: %s", item)
        if dataclasses.is_dataclass(item):
            self._removed_dataclasses[self._get_dataclass_key(item)] = item

        elif isinstance(item, dict):
            for v in item.values():
                self._dataclass_removed(v)

        elif isinstance(item, list):
            for v in item:
                self._dataclass_removed(v)

    def _undo_dataclass_removed(self, item):
        if dataclasses.is_dataclass(item):
            self._removed_dataclasses.pop(self._get_dataclass_key(item), None)

    def _get_dataclass_key(self, item):
        return (
            item._i
            if self.control_cls and isinstance(item, self.control_cls)
            else str(id(item))
        )

    def _configure_dataclass(self, item, parent, frozen, configure_setattr_only=False):
        if dataclasses.is_dataclass(item):
            logger.debug(
                "\n_configure_dataclass: %s %s %s", item, frozen, configure_setattr_only
            )

            if parent:
                if parent is item:
                    raise ObjectPatchException(f"Parent is the same as item: {item}")
                item._parent = weakref.ref(parent)

            if hasattr(item, "_frozen"):
                frozen = item._frozen
            elif frozen:
                item._frozen = frozen

            item_cls = item.__class__
            if getattr(item_cls, "__flet_control_cls__", None) is None:
                item_cls.__flet_control_cls__ = self.control_cls

            if self.control_cls and isinstance(item, self.control_cls):
                if not configure_setattr_only:
                    item.build()
                    item._before_update_safe()
                    object.__setattr__(item, "_initialized", True)
                yield item

            # recurse through fields
            if not configure_setattr_only:
                for field in dataclasses.fields(item):
                    if not field.metadata.get("skip", False):
                        yield from self._configure_dataclass(
                            getattr(item, field.name), item, frozen
                        )

            if not frozen:
                # Clear _dirty so post-configuration mutations are tracked
                # incrementally from a clean baseline.
                dst_dirty = getattr(item, "_dirty", None)
                if dst_dirty is not None:
                    dst_dirty.clear()
                else:
                    # Plain dataclass without Prop tracking: install
                    # _control_setattr to capture scalar changes in __changes.
                    item_cls = type(item)
                    if item_cls.__setattr__ is not _control_setattr:
                        item_cls.__setattr__ = _control_setattr
                    object.__setattr__(item, "__changes", {})

        elif isinstance(item, dict):
            for v in item.values():
                yield from self._configure_dataclass(v, parent, frozen)

        elif isinstance(item, list):
            for v in item:
                yield from self._configure_dataclass(v, parent, frozen)

    def _removed_controls(self, item, recurse):
        if self.control_cls and isinstance(item, self.control_cls):
            if hasattr(item, "__prev_lists"):
                # recurse through list props
                for item_list in getattr(item, "__prev_lists", {}).values():
                    yield from self._removed_controls(item_list, recurse)

                # recurse through dict props
                for item_dict in getattr(item, "__prev_dicts", {}).values():
                    yield from self._removed_controls(item_dict, recurse)

                # recurse through dataclass props
                for item_class in getattr(item, "__prev_classes", {}).values():
                    yield from self._removed_controls(item_class, recurse)
            elif recurse:
                # recurse through fields
                for field in dataclasses.fields(item):
                    if not field.metadata.get("skip", False):
                        yield from self._removed_controls(
                            getattr(item, field.name),
                            recurse,
                        )

            yield item

        elif isinstance(item, dict):
            for v in item.values():
                yield from self._removed_controls(v, recurse)

        elif isinstance(item, list):
            for v in item:
                yield from self._removed_controls(v, recurse)


def get_control_key(obj):
    # Fast path: read from _values directly to avoid Prop.__get__ overhead.
    _values = getattr(obj, "_values", None)
    key = _values.get("key") if _values is not None else getattr(obj, "key", None)
    return key.value if isinstance(key, Key) else key


def _path_join(path, key):
    if key is None:
        return path
    return path + [key]
