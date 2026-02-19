from typing import _eval_type

__all__ = ["eval_type"]

_EMPTY_TYPE_PARAMS = ()


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
