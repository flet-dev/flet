from typing import Any

__all__ = ["Group"]


class Group(dict):
    """
    Group or role entry associated with an authenticated [`User`][(p).].

    The instance behaves like a mutable mapping with provider-specific metadata,
    while exposing a normalized [`name`][(c).] attribute commonly used by app logic.

    Args:
        kwargs: Provider-specific group fields to store in the mapping.
        name: Group name used for display and matching.
    """

    name: str
    """
    Human-readable group name.
    """

    def __init__(self, kwargs: dict[str, Any], name: str) -> None:
        super().__init__(kwargs)
        self.name = name
