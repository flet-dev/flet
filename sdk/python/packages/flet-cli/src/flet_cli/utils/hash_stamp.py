import hashlib
from pathlib import Path


class HashStamp:
    """
    Track a SHA-256 digest and persist it to a stamp file.

    A `HashStamp` instance is typically used to detect whether a set of values
    has changed since the last run.
    """

    def __init__(self, path) -> None:
        self._path = path
        self._hash = hashlib.sha256()

    def update(self, data):
        """
        Add a value to the current digest state.

        Args:
            data: Value to include in the hash. `None` values are ignored.
        """

        if data is not None:
            self._hash.update(str(data).encode())

    def has_changed(self):
        """
        Check whether the current digest differs from the stored stamp.

        Returns:
            `True` if the current digest does not match the stamp file content;
            otherwise `False`.
        """

        hash_file = Path(self._path)
        last_hash = hash_file.read_text() if hash_file.exists() else ""
        return self._hash.hexdigest() != last_hash

    def commit(self):
        """
        Persist the current digest value to the stamp file.

        Parent directories are created automatically when needed.
        """

        hash_file = Path(self._path)
        hash_file.parent.mkdir(parents=True, exist_ok=True)
        hash_file.write_text(self._hash.hexdigest())
