import sys
from typing import _eval_type

__all__ = ["eval_type"]

_EMPTY_TYPE_PARAMS = ()


def eval_type(annotation, globalns, localns, type_params=_EMPTY_TYPE_PARAMS):
    if sys.version_info >= (3, 12):
        return _eval_type(annotation, globalns, localns, type_params=type_params)
    return _eval_type(annotation, globalns, localns)
