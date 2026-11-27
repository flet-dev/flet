import sys
from dataclasses import Field
from typing import Any, _eval_type

__all__ = ["eval_type", "field_annotation"]

_EMPTY_TYPE_PARAMS = ()


def field_annotation(cls: type, field: Field) -> Any:
    """Resolve one field's annotation independently, preserving its metadata."""
    hint = field.type
    if isinstance(hint, str):
        # Postponed annotations use the imports of the class that declared the
        # field. Dataclasses reuse that same Field object when it is inherited.
        owner = next(
            base
            for base in reversed(cls.__mro__)
            if vars(base).get("__dataclass_fields__", {}).get(field.name) is field
        )
        try:
            return eval(hint, vars(sys.modules[owner.__module__]), dict(vars(owner)))
        except (NameError, AttributeError):
            pass  # An unresolved forward reference may become available later.
    return hint


def eval_type(annotation, globalns, localns, type_params=_EMPTY_TYPE_PARAMS):
    """
    Evaluates a type annotation using runtime namespaces.

    This helper prefers calling `typing._eval_type()` with `type_params` support and
    falls back to the older call signature for Python versions that do not accept
    `type_params`.

    Args:
        annotation: The type annotation object to evaluate.
        globalns: Global namespace used to resolve forward references.
        localns: Local namespace used to resolve forward references.
        type_params: Generic type parameters used by newer Python versions.

    Returns:
        The evaluated type annotation.
    """
    try:
        return _eval_type(annotation, globalns, localns, type_params=type_params)
    except TypeError:
        # Older Python versions don't accept type_params.
        return _eval_type(annotation, globalns, localns)
