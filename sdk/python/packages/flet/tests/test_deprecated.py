"""Unit tests for runtime deprecation helpers in `flet.utils.deprecated`."""

import inspect
import re
import warnings
from dataclasses import dataclass
from types import ModuleType

import pytest

from flet.utils.deprecated import deprecated, deprecated_class, deprecated_warning


def test_deprecated_decorator_warns_and_returns_original_result():
    """`@deprecated` should warn and preserve wrapped function behavior."""

    @deprecated(
        reason="Use new_function instead.",
        version="1.0.0",
        delete_version="2.0.0",
    )
    def old_function(value: int) -> int:
        return value + 1

    with pytest.warns(
        DeprecationWarning,
        match=re.escape(
            "old_function is deprecated since version 1.0.0 and will be removed in "
            "version 2.0.0. Use new_function instead."
        ),
    ):
        assert old_function(2) == 3


def test_deprecated_decorator_respects_show_parentheses():
    """`show_parentheses=True` should render `name()` in warning text."""

    @deprecated(
        reason="Use new_function instead.",
        show_parentheses=True,
    )
    def old_function() -> str:
        return "ok"

    with pytest.warns(
        DeprecationWarning,
        match=re.escape("old_function() is deprecated. Use new_function instead."),
    ):
        assert old_function() == "ok"


def test_deprecated_decorator_uses_runtime_reason_not_docs_reason():
    """`docs_reason` is docs-only metadata and must not leak into runtime warnings."""

    @deprecated(
        reason="Runtime guidance only.",
        docs_reason="Use [`new_function`][(m).new_function] instead.",
        version="1.0.0",
    )
    def old_function() -> None:
        return None

    with pytest.warns(DeprecationWarning) as captured:
        old_function()

    warning_text = str(captured[0].message)
    assert "Runtime guidance only." in warning_text
    assert "new_function" not in warning_text


def test_deprecated_class_warns_on_init_and_post_init():
    """`@deprecated_class` should warn on both init and post-init hooks."""

    @deprecated_class(
        reason="Use NewClass instead.",
        docs_reason="Use [`NewClass`][(m).NewClass] instead.",
        version="1.0.0",
        delete_version="2.0.0",
    )
    @dataclass
    class OldClass:
        value: int

        def __post_init__(self):
            self.value += 1

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        obj = OldClass(1)

    assert obj.value == 2
    # __init__ and __post_init__ are both wrapped in deprecated_class.
    assert len(captured) == 2
    for warning in captured:
        warning_text = str(warning.message)
        assert "OldClass is deprecated since version 1.0.0" in warning_text
        assert "Use NewClass instead." in warning_text
        assert "NewClass" in warning_text
        assert "[`NewClass`]" not in warning_text


def test_deprecated_warning_formats_message_with_and_without_delete_version():
    """`deprecated_warning()` should render message variants deterministically."""
    with pytest.warns(
        DeprecationWarning,
        match=re.escape(
            "Sample.old_value property is deprecated since version 1.0.0 and will be "
            "removed in version 2.0.0. Use new_value instead."
        ),
    ):
        deprecated_warning(
            name="Sample.old_value",
            reason="Use new_value instead.",
            version="1.0.0",
            delete_version="2.0.0",
            type="property",
        )

    with pytest.warns(
        DeprecationWarning,
        match=re.escape(
            "Sample.old_value property is deprecated since version 1.0.0. "
            "Use new_value instead."
        ),
    ):
        deprecated_warning(
            name="Sample.old_value",
            reason="Use new_value instead.",
            version="1.0.0",
            delete_version=None,
            type="property",
        )


def test_deprecated_warning_points_to_user_code_through_flet_frames():
    """
    Ensure stacklevel skips internal `flet.*` frames and targets user call site.
    """

    flet_internal = ModuleType("flet.fake_internal")
    flet_internal.deprecated_warning = deprecated_warning
    exec(
        (
            "def emit_warning():\n"
            "    deprecated_warning(\n"
            "        name='Sample.old_value',\n"
            "        reason='Use new_value instead.',\n"
            "        version='0.80.0',\n"
            "    )\n"
        ),
        flet_internal.__dict__,
    )

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        expected_line = inspect.currentframe().f_lineno + 1
        flet_internal.emit_warning()

    assert len(captured) == 1
    warning = captured[0]
    assert warning.filename == __file__
    assert warning.lineno == expected_line
