from typing import Any

__all__ = ["SessionStore"]


class SessionStore:
    """In-memory key-value storage scoped to a user session.

    Note:
        In its current implementation, the data stored in a session store
        is transient and is not preserved between app restarts.

    Example:
    ```python
    page.session.store.set("user_name", "Alice")
    user_name = page.session.store.get("user_name")
    ```
    """

    def __init__(self):
        """Initialize an empty session store."""
        self.__store: dict[str, Any] = {}

    def set(self, key: str, value: Any):
        """Store a value under a key.

        Args:
            key: Key to store the value under.
            value: Value to store.
        """
        self.__store[key] = value

    def get(self, key: str):
        """Return the value for a key, or ``None`` if missing.

        Args:
            key: Key to look up.

        Returns:
            The stored value or ``None`` if the key does not exist.
        """
        return self.__store.get(key)

    def contains_key(self, key: str) -> bool:
        """Check whether a key exists in the store.

        Args:
            key: Key to check.

        Returns:
            ``True`` if the key exists, otherwise ``False``.
        """
        return key in self.__store

    def remove(self, key: str):
        """Remove a key from the store.

        Args:
            key: Key to remove.
        """
        self.__store.pop(key)

    def get_keys(self) -> list[str]:
        """Return all keys currently stored.

        Returns:
            A list of keys.
        """
        return list(self.__store.keys())

    def clear(self):
        """Remove all keys and values from the store."""
        self.__store.clear()
