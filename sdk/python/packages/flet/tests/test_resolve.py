import builtins
import importlib
import typing


def resolve_type(
    type_str: str, globalns: dict = None, localns: dict = None
) -> typing.Any:
    """
    Resolve a type from a string.

    :param type_str: The type as a string (e.g. "int", "list", "typing.List[int]", etc.)
    :param globalns: Optional dict of globals for resolving custom types.
    :param localns: Optional dict of locals for resolving custom types.
    :return: The resolved type object.
    """
    # First check if it's a built-in type
    if hasattr(builtins, type_str):
        return getattr(builtins, type_str)

    # Try using eval with typing and builtins in scope
    ns = {
        **vars(typing),
        **vars(builtins),
    }

    if globalns:
        ns.update(globalns)
    if localns:
        ns.update(localns)

    try:
        return eval(type_str, ns)
    except (NameError, SyntaxError):
        # Fallback: assume it's a fully qualified path
        if "." in type_str:
            module_path, _, attr = type_str.rpartition(".")
            try:
                module = importlib.import_module(module_path)
                return getattr(module, attr)
            except (ModuleNotFoundError, AttributeError):
                pass

    raise TypeError(f"Could not resolve type from string: '{type_str}'")


def test_resolve_type():
    assert resolve_type("OnScrollEvent")
