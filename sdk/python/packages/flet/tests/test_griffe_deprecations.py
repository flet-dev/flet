"""Tests for docs-facing deprecation extraction via Griffe extension."""

from textwrap import dedent

import pytest

griffe = pytest.importorskip("griffe")
from griffe import (  # noqa: E402
    DocstringSectionAdmonition,
    load_extensions,
    temporary_visited_module,
)


def _first_deprecation_admonition(obj):
    """Return the first `Deprecated` admonition section from an object docstring."""
    if not obj.docstring:
        return None
    for section in obj.docstring.parsed:
        if (
            isinstance(section, DocstringSectionAdmonition)
            and section.title == "Deprecated"
        ):
            return section
    return None


def _admonition_text(admonition):
    """Extract admonition body text from a Griffe admonition section."""
    return admonition.value.contents


def test_extension_adds_attribute_admonition_for_v_deprecated():
    """Ensure that `V.deprecated` attributes get a Deprecated admonition."""
    code = dedent(
        """
        from typing import Annotated, Optional
        from flet.utils.validation import V

        class Control:
            old_prop: Annotated[
                Optional[int],
                V.deprecated("new_prop", version="0.81.0", delete_version="0.90.0"),
            ] = None
        """
    )
    with temporary_visited_module(
        code, extensions=load_extensions("flet.utils.griffe_deprecations")
    ) as module:
        attr = module["Control"]["old_prop"]
        admonition = _first_deprecation_admonition(attr)
        assert admonition is not None
        text = _admonition_text(admonition)
        assert "Deprecated since version `0.81.0`" in text
        assert "removal in `0.90.0`" in text
        assert "Use `new_prop` instead." in text
        assert "deprecated" in attr.labels


def test_extension_prefers_docs_reason_for_v_deprecated():
    """Ensure that `docs_reason` overrides `reason` for `V.deprecated` attributes."""
    code = dedent(
        """
        from typing import Annotated, Optional
        from flet.utils.validation import V

        class Control:
            old_prop: Annotated[
                Optional[int],
                V.deprecated(
                    "new_prop",
                    version="0.81.0",
                    reason="Use plain text.",
                    docs_reason="Use [`new_prop`][(c).] instead.",
                ),
            ] = None
        """
    )
    with temporary_visited_module(
        code, extensions=load_extensions("flet.utils.griffe_deprecations")
    ) as module:
        attr = module["Control"]["old_prop"]
        admonition = _first_deprecation_admonition(attr)
        assert admonition is not None
        text = _admonition_text(admonition)
        assert "Use [`new_prop`][(c).] instead." in text
        assert "Use plain text." not in text


def test_extension_adds_function_admonition_for_flet_decorator():
    """Ensure that `@deprecated` functions get a Deprecated admonition."""
    code = dedent(
        """
        from flet.utils.deprecated import deprecated

        @deprecated(
            reason="Use `new_func()` instead.",
            version="0.80.0",
            delete_version="0.90.0",
        )
        def old_func():
            return None
        """
    )
    with temporary_visited_module(
        code, extensions=load_extensions("flet.utils.griffe_deprecations")
    ) as module:
        func = module["old_func"]
        admonition = _first_deprecation_admonition(func)
        assert admonition is not None
        text = _admonition_text(admonition)
        assert "Deprecated since version `0.80.0`" in text
        assert "removal in `0.90.0`" in text
        assert "Use `new_func()` instead." in text
        assert "deprecated" in func.labels


def test_extension_prefers_docs_reason_for_flet_decorator():
    """Ensure that `docs_reason` overrides `reason` for `@deprecated` functions."""
    code = dedent(
        """
        from flet.utils.deprecated import deprecated

        @deprecated(
            reason="Use plain text.",
            docs_reason="Use [`new_func()`][(m).new_func] instead.",
            version="0.80.0",
            delete_version="0.90.0",
        )
        def old_func():
            return None
        """
    )
    with temporary_visited_module(
        code, extensions=load_extensions("flet.utils.griffe_deprecations")
    ) as module:
        func = module["old_func"]
        admonition = _first_deprecation_admonition(func)
        assert admonition is not None
        text = _admonition_text(admonition)
        assert "Use [`new_func()`][(m).new_func] instead." in text
        assert "Use plain text." not in text


def test_extension_adds_class_admonition_for_deprecated_class():
    """Ensure that `@deprecated_class` classes get a Deprecated admonition."""
    code = dedent(
        """
        from flet.utils.deprecated import deprecated_class

        @deprecated_class(
            reason="Use `NewControl` instead.",
            version="0.80.0",
            delete_version="0.90.0",
        )
        class OldControl:
            pass
        """
    )
    with temporary_visited_module(
        code, extensions=load_extensions("flet.utils.griffe_deprecations")
    ) as module:
        cls = module["OldControl"]
        admonition = _first_deprecation_admonition(cls)
        assert admonition is not None
        text = _admonition_text(admonition)
        assert "Deprecated since version `0.80.0`" in text
        assert "removal in `0.90.0`" in text
        assert "Use `NewControl` instead." in text
        assert "deprecated" in cls.labels


def test_extension_prefers_docs_reason_for_deprecated_class():
    """Ensure that `docs_reason` overrides `reason` for `@deprecated_class` classes."""
    code = dedent(
        """
        from flet.utils.deprecated import deprecated_class

        @deprecated_class(
            reason="Use plain text.",
            docs_reason="Use [`NewControl`][(m).NewControl] instead.",
            version="0.80.0",
            delete_version="0.90.0",
        )
        class OldControl:
            pass
        """
    )
    with temporary_visited_module(
        code, extensions=load_extensions("flet.utils.griffe_deprecations")
    ) as module:
        cls = module["OldControl"]
        admonition = _first_deprecation_admonition(cls)
        assert admonition is not None
        text = _admonition_text(admonition)
        assert "Use [`NewControl`][(m).NewControl] instead." in text
        assert "Use plain text." not in text


def test_extension_adds_attribute_admonition_for_property_getter_deprecated():
    """Ensure that deprecated property getters get a Deprecated admonition."""
    code = dedent(
        """
        from flet.utils.deprecated import deprecated

        class Control:
            @property
            @deprecated(
                reason="Use plain text.",
                docs_reason="Use :attr:`new_prop` instead.",
                version="0.80.0",
                delete_version="0.90.0",
            )
            def old_prop(self) -> int:
                \"\"\"Deprecated property getter.\"\"\"
                return 1
        """
    )
    with temporary_visited_module(
        code, extensions=load_extensions("flet.utils.griffe_deprecations")
    ) as module:
        attr = module["Control"]["old_prop"]
        admonition = _first_deprecation_admonition(attr)
        assert admonition is not None
        text = _admonition_text(admonition)
        assert "Deprecated since version `0.80.0`" in text
        assert "removal in `0.90.0`" in text
        assert "Use :attr:`new_prop` instead." in text
        assert "Use plain text." not in text
        assert "deprecated" in attr.labels
        assert "property" in attr.labels


def test_extension_adds_function_admonition_for_typing_extensions_deprecated():
    """
    Ensure that `typing_extensions.deprecated` functions get a Deprecated admonition.
    """
    code = dedent(
        """
        from typing_extensions import deprecated

        @deprecated("Use `new_function` instead.")
        def old_function():
            return None
        """
    )
    with temporary_visited_module(
        code, extensions=load_extensions("flet.utils.griffe_deprecations")
    ) as module:
        func = module["old_function"]
        admonition = _first_deprecation_admonition(func)
        assert admonition is not None
        text = _admonition_text(admonition)
        assert "Deprecated." in text
        assert "Use `new_function` instead." in text
        assert "deprecated" in func.labels
