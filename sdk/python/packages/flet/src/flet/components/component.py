from __future__ import annotations

import logging
import weakref
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar

from flet.components.hooks.hook import Hook
from flet.components.hooks.use_effect import EffectHook
from flet.components.observable import Observable, ObservableSubscription
from flet.components.utils import (
    _CURRENT_RENDERER,
    shallow_compare_args_and_kwargs,
)
from flet.controls.base_control import BaseControl, control
from flet.controls.context import context

logger = logging.getLogger("flet_components")
logger.setLevel(logging.INFO)


@dataclass
class _ComponentState:
    hooks: list[Hook] = field(default_factory=list)
    hook_cursor: int = 0
    mounted: bool = False
    is_dirty: bool = False
    observable_subscriptions: list[ObservableSubscription] = field(default_factory=list)
    last_args: tuple[Any, ...] = field(default_factory=tuple)
    last_kwargs: dict[str, Any] = field(default_factory=dict)
    last_b: Any = None

    def change_owner(self, new_owner: Any):
        for hook in self.hooks:
            hook.component = new_owner
        for sub in self.observable_subscriptions:
            sub.component = new_owner


HookTypeT = TypeVar("HookTypeT", bound=Hook)


@control("C")
class Component(BaseControl):
    fn: Callable[..., Any] = field(metadata={"skip": True})
    args: tuple[Any, ...] = field(default_factory=tuple, metadata={"skip": True})
    kwargs: dict[str, Any] = field(default_factory=dict, metadata={"skip": True})
    _parent_component: weakref.ref[Component] | None = field(
        default=None, metadata={"skip": True}
    )
    _state: _ComponentState = field(
        default_factory=_ComponentState, metadata={"skip": True}
    )
    _contexts: dict[object, Any] = field(default_factory=dict, metadata={"skip": True})
    memoized: bool = field(default=False, metadata={"skip": True})
    _stale: bool = field(default=False, metadata={"skip": True})

    _b: Any = None  # body

    def _migrate_state(self, other: BaseControl):
        super()._migrate_state(other)
        logger.debug("%s._migrate_state(%s)", self, other)
        if not isinstance(other, Component):
            return
        self._state = other._state
        self._state.change_owner(self)
        other._stale = True

    def update(self):
        if self._stale:
            logger.debug("%s.update(): skipping (stale)", self)
            return

        logger.debug(
            "%s.update(), memoized: %s",
            self,
            self.memoized,
        )

        self._state.is_dirty = False

        # new rendering
        self._state.hook_cursor = 0
        self._detach_observable_subscriptions()
        self._subscribe_observable_args(self.args, self.kwargs)

        b = Renderer(self).render(self.fn, *self.args, **self.kwargs)

        for item in b if isinstance(b, list) else [b] if b is not None else []:
            object.__setattr__(item, "_frozen", True)

        if self.memoized and b is not None:
            logger.debug("%s.update(): memoizing", self)
            self._state.last_b = b
            self._state.last_args = self.args
            self._state.last_kwargs = self.kwargs

        # patch component
        if b is not None:
            context.page.session.patch_control(
                prev_control={"_b": self._b},
                control={"_b": b},
                parent=self,
                path=[],
                frozen=True,
            )

        self._b = b
        self._run_render_effects()

    def before_update(self):
        logger.debug("%s.before_update(), memoized: %s", self, self.memoized)
        is_dirty = self._state.is_dirty
        self._state.is_dirty = False

        if (
            self.memoized
            and not is_dirty
            and shallow_compare_args_and_kwargs(
                self._state.last_args, self._state.last_kwargs, self.args, self.kwargs
            )
            and self._state.last_b is not None
        ):
            logger.debug("%s.before_update(): skipping (memo)", self)
            self._b = self._state.last_b

            # fix parent
            for item in self._b if isinstance(self._b, list) else [self._b]:
                object.__setattr__(item, "_parent", weakref.ref(self))
            return

        self._state.hook_cursor = 0
        self._detach_observable_subscriptions()
        self._subscribe_observable_args(self.args, self.kwargs)
        b = Renderer(self).render(self.fn, *self.args, **self.kwargs)

        for item in b if isinstance(b, list) else [b] if b is not None else []:
            object.__setattr__(item, "_frozen", True)

        if self.memoized and b is not None:
            logger.debug("%s.before_update(): memoizing", self)
            self._state.last_b = b
            self._state.last_args = self.args
            self._state.last_kwargs = self.kwargs
        self._b = b
        self._run_render_effects()

    def _schedule_update(self):
        logger.debug("%s.schedule_update()", self)
        self._state.is_dirty = True
        context.page.session.schedule_update(self)

    def _schedule_effect(self, hook: EffectHook, is_cleanup: bool = False):
        logger.debug("%s.schedule_effect(%s, %s)", self, hook, is_cleanup)
        context.page.session.schedule_effect(hook, is_cleanup)

    def _subscribe_observable_args(self, args: tuple[Any, ...], kwargs: dict[str, Any]):
        for a in args:
            if isinstance(a, Observable):
                self._attach_observable_subscription(a)
        for v in kwargs.values():
            if isinstance(v, Observable):
                self._attach_observable_subscription(v)

    def _attach_observable_subscription(self, observable: Observable):
        # Use weak refs to avoid cycles
        logger.debug("%s._attach_observable_subscription(%s)", self, observable)

        self._state.observable_subscriptions.append(
            ObservableSubscription(owner=self, observable=observable)
        )
        return self._state.observable_subscriptions[-1]

    def _detach_observable_subscription(self, subscription: ObservableSubscription):
        if subscription in self._state.observable_subscriptions:
            subscription.dispose()
            self._state.observable_subscriptions.remove(subscription)

    def _detach_observable_subscriptions(self):
        for subscription in self._state.observable_subscriptions:
            subscription.dispose()
        self._state.observable_subscriptions.clear()

    def use_hook(self, default: Callable[[], HookTypeT]) -> HookTypeT:
        hook_cursor = self._state.hook_cursor

        i = hook_cursor
        hook_cursor += 1

        if i >= len(self._state.hooks):
            self._state.hooks.append(default())

        self._state.hook_cursor = hook_cursor
        return self._state.hooks[i]  # type: ignore

    def _run_mount_effects(self):
        if self._state.hooks:
            logger.debug("%s._run_mount_effects()", self)
        for hook in self._state.hooks:
            if isinstance(hook, EffectHook):
                # all effects are running on mount
                self._schedule_effect(hook, is_cleanup=False)

    def _run_render_effects(self):
        if not self._state.mounted:
            return
        if self._state.hooks:
            logger.debug("%s._run_render_effects()", self)
        for hook in self._state.hooks:
            if isinstance(hook, EffectHook) and hook.deps != []:
                if callable(hook.cleanup):
                    self._schedule_effect(hook, is_cleanup=False)
                if (
                    hook.deps is None
                    or hook.prev_deps is None
                    or hook.deps != hook.prev_deps
                ):
                    self._schedule_effect(hook, is_cleanup=False)

    def _run_unmount_effects(self):
        if self._state.hooks:
            logger.debug("%s._run_unmount_effects()", self)
        for hook in self._state.hooks:
            # all effects are running on unmount
            if isinstance(hook, EffectHook) and callable(hook.cleanup):
                self._schedule_effect(hook, is_cleanup=True)
        self._state.hooks.clear()

    def did_mount(self):
        super().did_mount()
        self._state.mounted = True
        self._run_mount_effects()

    def will_unmount(self):
        super().will_unmount()
        self._state.mounted = False
        self._detach_observable_subscriptions()
        self._run_unmount_effects()

    def __str__(self):
        return f"{self._c}:{self.fn.__name__}({self._i} - {id(self)})"


#
# Renderer
#


class Renderer:
    _ROOT_TOKEN = ("__root__",)

    def __init__(self, root_component=None):
        self._root_component = root_component
        self._render_stack: list[Component] = []
        self._is_memo = False
        self._contexts: dict[object, list[object]] = defaultdict(list)

    def set_memo(self):
        self._is_memo = True

    def push_context(self, key: object, value: object) -> None:
        logger.debug("Renderer._push_context(%s, %s)", key, value)
        self._contexts[key].append(value)

    def pop_context(self, key: object) -> None:
        logger.debug("Renderer._pop_context(%s)", key)
        stack = self._contexts.get(key)
        if stack:
            stack.pop()
            if not stack:
                del self._contexts[key]

    def _snapshot_contexts(self) -> dict[object, object]:
        # take top of each stack
        return {k: v[-1] for k, v in self._contexts.items() if v}

    def with_context(self):
        """Context manager to make this renderer the 'current' one."""

        class _C:
            def __init__(_s, r: Renderer):
                _s._tok = None
                _s._r = r

            def __enter__(_s):
                _s._tok = _CURRENT_RENDERER.set(_s._r)
                return _s._r

            def __exit__(_s, exc_type, exc, tb):
                if _s._tok is not None:
                    _CURRENT_RENDERER.reset(_s._tok)

        return _C(self)

    def render(self, root_fn: Callable[..., Any], *args, **kwargs):
        # run with this renderer bound as current
        with self.with_context(), self._Frame(self, self._root_component):
            return root_fn(*args, **kwargs)

    def render_component(
        self,
        fn: Callable[..., Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        key=None,
    ):
        logger.debug(
            "Renderer._render_component(%s, %s, %s, %s)", fn, args, kwargs, key
        )
        parent_component = len(self._render_stack) and self._render_stack[-1]

        if not hasattr(fn, "__is_component__"):
            raise ValueError(f"Function {fn} is not a component (missing @component?)")

        c = Component(
            fn=fn,
            args=args,
            kwargs=kwargs,
            _parent_component=weakref.ref(parent_component)
            if parent_component
            else None,
            memoized=self._is_memo,
            key=key,
        )
        c._contexts = self._snapshot_contexts()
        c._frozen = True

        self._is_memo = False

        return c

    class _Frame:
        """Context around entering a component; pushes/pops on renderer's stack."""

        def __init__(self, renderer: Renderer, c: Component | None = None):
            self.r = renderer
            self.c = c

        def __enter__(self):
            if self.c:
                self.r._render_stack.append(self.c)
            return self.c

        def __exit__(self, exc_type, exc, tb):
            if self.c:
                self.r._render_stack.pop()
