from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["FileStorage"]


@control("FileStorage")
class FileStorage(Service):
    """
    Files an app keeps between runs, in a folder of its own.

    The Flet client stores them for the app: on web in the browser's origin
    private file system (OPFS), on desktop and mobile in a folder under the app
    support directory. Use it for data that outgrows
    [`SharedPreferences`][flet.SharedPreferences], such as a SQLite database
    (`sqlite3.Connection.serialize()` / `sqlite3.Connection.deserialize()`),
    images or JSON documents.

    It matters most on web, where an app's Python has no persistent file
    system of its own. On desktop and mobile, an app can also use regular
    files (see [`StoragePaths`][flet.StoragePaths]), which is faster for large
    or frequently written data; `FileStorage` works there too, so the same code
    runs on every platform.

    Names are paths relative to the app's folder, such as `"notes.json"` or
    `"db/app.sqlite"`: parts are separated by `/`, and none may be empty,
    `.` or `..`, contain `\\ : * ? " < > |` or control characters, or end with a
    space or a dot. The same rules apply on every platform.

    A write replaces the whole file atomically: a reader sees the old contents
    or the new ones, never a mix.

    Note:
        An app embedded in another with [`FletApp`][flet.FletApp] gets its own
        folder, named from its
        [`FletApp.storage_prefix`][flet.FletApp.storage_prefix], and can't read,
        list or change its host's files or another embedded app's. It can keep
        up to [`FletApp.file_storage_quota`][flet.FletApp.file_storage_quota]
        bytes (50 MB unless the host sets another limit). A top-level app has
        no limit beyond the platform's own.

    Note:
        On web, writing needs `FileSystemWritableFileStream`: Chrome 86+,
        Firefox 111+ or Safari 26+. Older browsers raise an error.
    """

    async def read(self, name: str) -> Optional[bytes]:
        """
        Reads a file.

        Args:
            name: The file's name, such as `"db/app.sqlite"`.

        Returns:
            The file's contents, or `None` if there's no such file.
        """
        return await self._invoke_method("read", {"name": name})

    async def write(self, name: str, data: bytes) -> None:
        """
        Creates or replaces a file, atomically. Folders in its name are created
        as needed.

        Args:
            name: The file's name, such as `"db/app.sqlite"`.
            data: The file's new contents.

        Raises:
            TypeError: If `data` isn't `bytes`, `bytearray` or `memoryview`.
            RuntimeError: If the write would take an embedded app past its
                [`FletApp.file_storage_quota`][flet.FletApp.file_storage_quota].
        """
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError(
                f"FileStorage.write() takes bytes, not {type(data).__name__}."
            )
        await self._invoke_method("write", {"name": name, "data": bytes(data)})

    async def delete(self, name: str) -> bool:
        """
        Deletes a file.

        Args:
            name: The file's name.

        Returns:
            `True` if a file was deleted, `False` if there was none.
        """
        return await self._invoke_method("delete", {"name": name})

    async def exists(self, name: str) -> bool:
        """
        Checks whether a file exists.

        Args:
            name: The file's name.
        """
        return await self._invoke_method("exists", {"name": name})

    async def list(self, prefix: str = "") -> list[str]:
        """
        Lists the app's files, including those in folders.

        Args:
            prefix: Only names starting with this, such as `"db/"`.

        Returns:
            The files' names, sorted, such as `["db/app.sqlite", "notes.json"]`.
        """
        return await self._invoke_method("list", {"prefix": prefix})

    async def size(self) -> int:
        """
        Returns the total size of the app's files, in bytes.
        """
        return await self._invoke_method("size")

    async def lock(self, name: str, timeout: float = 5.0) -> bool:
        """
        Takes an exclusive lock, so two copies of the app don't write the same
        file at once - on web, the app open in two tabs.

        Locks are named like files and belong to the app; they don't stop
        anything by themselves, so take the lock before reading a file you'll
        write back, and [`unlock()`][(c).unlock] it after. A lock the app
        still holds is released when it closes.

        Args:
            name: The lock's name, usually the file's.
            timeout: Seconds to wait for another copy to release it. `0`
                doesn't wait.

        Returns:
            `True` if the app now holds the lock (or already did), `False` if
                another copy still held it after `timeout`.
        """
        return await self._invoke_method("lock", {"name": name, "timeout": timeout})

    async def unlock(self, name: str) -> None:
        """
        Releases a lock taken with [`lock()`][(c).lock].

        Args:
            name: The lock's name.
        """
        await self._invoke_method("unlock", {"name": name})
