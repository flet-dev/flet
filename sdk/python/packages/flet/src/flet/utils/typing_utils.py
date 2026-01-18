from typing import _eval_type

__all__ = ["eval_type"]

_EMPTY_TYPE_PARAMS = ()


def eval_type(annotation, globalns, localns, type_params=_EMPTY_TYPE_PARAMS):
    try:
        return _eval_type(annotation, globalns, localns, type_params=type_params)
    except TypeError:
        # Older Python versions don't accept type_params.
        return _eval_type(annotation, globalns, localns)
