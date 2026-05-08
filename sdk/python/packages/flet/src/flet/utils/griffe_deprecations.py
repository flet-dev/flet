"""
Griffe extension for rendering deprecation details in API docs.

This extension centralizes deprecation detection for Flet docs. It supports:
- class/function decorators:
  - `warnings.deprecated(...)`
  - `typing_extensions.deprecated(...)`
  - `flet.utils.deprecated(...)`
  - `flet.utils.deprecated_class(...)`
- property getters decorated as `@property` and `flet.utils.deprecated(...)`
- attribute metadata:
  - `typing.Annotated[..., V.deprecated(...)]`

Detected deprecations are inserted as a docstring admonition and labeled with
`deprecated`.
"""

import ast
from typing import Any, Optional, Union

from griffe import (
    Attribute,
    Class,
    Docstring,
    DocstringSectionAdmonition,
    ExprCall,
    ExprKeyword,
    ExprName,
    ExprSubscript,
    ExprTuple,
    Extension,
    Function,
)

__all__ = ["FletDeprecationsExtension"]

_ANNOTATED_PATHS = {"typing.Annotated", "typing_extensions.Annotated"}
_V_DEPRECATED_PATH = "flet.utils.validation.V.deprecated"
_PEP702_DECORATORS = {"warnings.deprecated", "typing_extensions.deprecated"}
_FLET_FUNCTION_DECORATORS = {
    "flet.utils.deprecated",
    "flet.utils.deprecated.deprecated",
    "deprecated",
}
_FLET_CLASS_DECORATORS = {
    "flet.utils.deprecated_class",
    "flet.utils.deprecated.deprecated_class",
}


def _text(expr: Any) -> Optional[str]:
    """Best-effort extraction of readable text from a Griffe expression."""
    if expr is None:
        return None
    if isinstance(expr, ExprName):
        return expr.name
    raw = expr.strip() if isinstance(expr, str) else str(expr).strip()

    if raw == "":
        return None

    try:
        return str(ast.literal_eval(raw))
    except Exception:
        return raw


def _split_call_arguments(call: ExprCall) -> tuple[list[Any], dict[str, Any]]:
    """Split call arguments into positional and keyword dictionaries."""
    positional: list[Any] = []
    keywords: dict[str, Any] = {}
    for arg in call.arguments:
        if isinstance(arg, ExprKeyword):
            keywords[arg.name] = arg.value
        else:
            positional.append(arg)
    return positional, keywords


def _compose_message(
    *,
    reason: Optional[str],
    version: Optional[str],
    delete_version: Optional[str],
) -> str:
    """
    Compose a concise deprecation summary suitable for a docs admonition.
    """
    prefix = "Deprecated."
    if version and delete_version:
        prefix = (
            f"Deprecated since version `{version}` and scheduled for removal in "
            f"`{delete_version}`."
        )
    elif version:
        prefix = f"Deprecated since version `{version}`."
    elif delete_version:
        prefix = f"Scheduled for removal in version `{delete_version}`."

    if reason:
        return f"{prefix} {reason}".strip()
    return prefix


def _extract_deprecation_from_decorators(obj: Union[Class, Function]) -> Optional[str]:
    """Extract deprecation details from supported class/function decorators."""
    for decorator in obj.decorators or []:
        call = decorator.value
        path = decorator.callable_path
        if not path or not isinstance(call, ExprCall):
            continue

        positional, keywords = _split_call_arguments(call)
        reason: Optional[str] = None
        version: Optional[str] = None
        delete_version: Optional[str] = None

        if path in _PEP702_DECORATORS:
            if positional:
                reason = _text(positional[0])
            if reason is None:
                reason = "This API is deprecated."
            return _compose_message(
                reason=reason, version=version, delete_version=delete_version
            )

        if path in _FLET_FUNCTION_DECORATORS:
            reason = _text(keywords.get("reason"))
            if reason is None and positional:
                reason = _text(positional[0])
            docs_reason = _text(keywords.get("docs_reason"))

            version = _text(keywords.get("version"))
            if version is None and len(positional) > 1:
                version = _text(positional[1])

            delete_version = _text(keywords.get("delete_version"))
            if delete_version is None and len(positional) > 2:
                delete_version = _text(positional[2])

            return _compose_message(
                reason=docs_reason or reason,
                version=version,
                delete_version=delete_version,
            )

        if path in _FLET_CLASS_DECORATORS:
            reason = _text(keywords.get("reason"))
            if reason is None and positional:
                reason = _text(positional[0])
            docs_reason = _text(keywords.get("docs_reason"))

            version = _text(keywords.get("version"))
            if version is None and len(positional) > 1:
                version = _text(positional[1])

            delete_version = _text(keywords.get("delete_version"))
            if delete_version is None and len(positional) > 2:
                delete_version = _text(positional[2])

            return _compose_message(
                reason=docs_reason or reason,
                version=version,
                delete_version=delete_version,
            )

    return None


def _extract_v_deprecated_call(attribute: Attribute) -> Optional[ExprCall]:
    """
    Return the `V.deprecated(...)` call from `Annotated[...]` metadata, if present.
    """
    annotation = attribute.annotation
    if not isinstance(annotation, ExprSubscript):
        return None
    if annotation.canonical_path not in _ANNOTATED_PATHS:
        return None
    if not isinstance(annotation.slice, ExprTuple):
        return None

    for metadata in annotation.slice.elements[1:]:
        if isinstance(metadata, ExprCall) and (
            metadata.canonical_path == _V_DEPRECATED_PATH
            or metadata.canonical_path.endswith(".V.deprecated")
        ):
            return metadata
    return None


def _extract_deprecation_from_attribute(attribute: Attribute) -> Optional[str]:
    """
    Extract deprecation details from `Annotated[..., V.deprecated(...)]`.
    """
    call = _extract_v_deprecated_call(attribute)
    if call is None:
        return None

    positional, keywords = _split_call_arguments(call)
    replacement = _text(keywords.get("replacement"))
    if replacement is None and positional:
        replacement = _text(positional[0])

    reason = _text(keywords.get("reason"))
    docs_reason = _text(keywords.get("docs_reason"))
    selected_reason = docs_reason or reason
    if selected_reason is None:
        selected_reason = (
            f"Use `{replacement}` instead."
            if replacement is not None
            else "This property is deprecated."
        )

    version = _text(keywords.get("version"))
    delete_version = _text(keywords.get("delete_version"))

    return _compose_message(
        reason=selected_reason,
        version=version,
        delete_version=delete_version,
    )


def _ast_decorator_name(expr: ast.AST) -> Optional[str]:
    """Return the dotted callable name for a decorator AST node when possible."""
    if isinstance(expr, ast.Call):
        return _ast_decorator_name(expr.func)
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        parent = _ast_decorator_name(expr.value)
        return f"{parent}.{expr.attr}" if parent else expr.attr
    return None


def _ast_text(expr: Optional[ast.AST]) -> Optional[str]:
    """Best-effort extraction of readable text from a Python AST expression."""
    if expr is None:
        return None
    try:
        return str(ast.literal_eval(expr))
    except Exception:
        try:
            return ast.unparse(expr)
        except Exception:
            return None


def _extract_deprecation_from_property_decorators(node: ast.AST) -> Optional[str]:
    """
    Extract deprecation details from a `@property` getter
    AST node decorated with `@deprecated`.

    Griffe exposes `@property` getters as `Attribute` objects in the final
    object model, so the getter decorators are no longer available there. The
    original `FunctionDef` is still passed into `on_attribute_instance`,
    which lets us recover the deprecation arguments and transfer them onto the
    resulting attribute for docs rendering.
    """
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return None

    has_property = False
    deprecated_call: Optional[ast.Call] = None
    for decorator in node.decorator_list:
        name = _ast_decorator_name(decorator)
        if name == "property":
            has_property = True
            continue
        if isinstance(decorator, ast.Call) and name in _FLET_FUNCTION_DECORATORS:
            deprecated_call = decorator

    if not has_property or deprecated_call is None:
        return None

    positional = list(deprecated_call.args)
    keywords = {
        keyword.arg: keyword.value
        for keyword in deprecated_call.keywords
        if keyword.arg is not None
    }

    reason = _ast_text(keywords.get("reason"))
    if reason is None and positional:
        reason = _ast_text(positional[0])
    docs_reason = _ast_text(keywords.get("docs_reason"))

    version = _ast_text(keywords.get("version"))
    if version is None and len(positional) > 1:
        version = _ast_text(positional[1])

    delete_version = _ast_text(keywords.get("delete_version"))
    if delete_version is None and len(positional) > 2:
        delete_version = _ast_text(positional[2])

    return _compose_message(
        reason=docs_reason or reason,
        version=version,
        delete_version=delete_version,
    )


class FletDeprecationsExtension(Extension):
    """
    Add deprecation admonitions for supported Flet and PEP 702 patterns.
    """

    def __init__(
        self,
        kind: str = "warning",
        title: str = "Deprecated",
        label: Optional[str] = "deprecated",
    ) -> None:
        super().__init__()
        self.kind = kind
        self.title = title
        self.label = label

    def _insert_message(self, obj: Any, message: str) -> None:
        """
        Insert deprecation admonition/label on a Griffe object once.

        The method is idempotent for identical admonition payloads.
        """
        if not obj.docstring:
            obj.docstring = Docstring("", parent=obj)

        sections = obj.docstring.parsed
        for section in sections:
            if (
                isinstance(section, DocstringSectionAdmonition)
                and section.title == self.title
                and getattr(section.value, "contents", None) == message
                and getattr(section.value, "kind", None) == self.kind
            ):
                break
        else:
            sections.insert(
                0,
                DocstringSectionAdmonition(
                    kind=self.kind,
                    title=self.title,
                    text=message,
                ),
            )

        if self.label:
            obj.labels.add(self.label)
        if hasattr(obj, "deprecated"):
            obj.deprecated = message

    def on_class_instance(self, *, cls: Class, **kwargs: Any) -> None:  # noqa: ARG002
        if message := _extract_deprecation_from_decorators(cls):
            self._insert_message(cls, message)

    def on_function_instance(self, *, func: Function, **kwargs: Any) -> None:  # noqa: ARG002
        if message := _extract_deprecation_from_decorators(func):
            self._insert_message(func, message)

    def on_attribute_instance(
        self, *, node: ast.AST, attr: Attribute, **kwargs: Any
    ) -> None:  # noqa: ARG002
        if message := _extract_deprecation_from_attribute(attr):
            self._insert_message(attr, message)
            return
        # Property getters arrive here as Attributes, so decorator-based
        # deprecations must be recovered from the original getter AST node.
        if message := _extract_deprecation_from_property_decorators(node):
            self._insert_message(attr, message)
