from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from flet.auth.group import Group

__all__ = ["User"]


class User(dict):
    """
    Authenticated user profile used by Flet authorization flows.

    The instance is a mutable mapping with provider-specific user fields and
    normalized attributes such as [`id`][(c).] and [`groups`][(c).].

    Args:
        kwargs: Provider-specific user fields to store in the mapping.
        id: Stable user identifier.
    """

    id: str
    """
    Provider user identifier represented as a string.
    """

    groups: list["Group"]
    """
    Groups loaded for this user when group retrieval is enabled.
    """

    def __init__(self, kwargs: dict[str, Any], id: str) -> None:
        super().__init__(kwargs)
        self.id = id
        self.groups = []
