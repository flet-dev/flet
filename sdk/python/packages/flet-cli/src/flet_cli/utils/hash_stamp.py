import hashlib
from pathlib import Path


class HashStamp:
    def __init__(self, path) -> None:
        self._path = path
        self._hash = hashlib.sha256()

    def update(self, data):
        if data is not None:
            self._hash.update(str(data).encode())

    def has_changed(self):
        hash_file = Path(self._path)
        last_hash = hash_file.read_text() if hash_file.exists() else ""
        return self._hash.hexdigest() != last_hash

    def commit(self):
        hash_file = Path(self._path)
        hash_file.parent.mkdir(parents=True, exist_ok=True)
        hash_file.write_text(self._hash.hexdigest())
