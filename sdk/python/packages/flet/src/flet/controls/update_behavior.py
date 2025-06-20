import contextvars


class UpdateBehavior:
    _auto_update_enabled: bool = True

    @classmethod
    def reset(cls):
        """Copies parent state into current context."""
        current = _update_behavior_context_var.get()
        new = UpdateBehavior()
        new._auto_update_enabled = current._auto_update_enabled
        _update_behavior_context_var.set(new)

    @classmethod
    def enable_auto_update(cls):
        _update_behavior_context_var.get()._auto_update_enabled = True

    @classmethod
    def disable_auto_update(cls):
        _update_behavior_context_var.get()._auto_update_enabled = False

    @classmethod
    def auto_update_enabled(cls):
        return _update_behavior_context_var.get()._auto_update_enabled


_update_behavior_context_var = contextvars.ContextVar(
    "update_behavior", default=UpdateBehavior()
)
