"""Private receipt photos: native app documents, small browser-storage fallback."""

import base64
import os
import re
from uuid import uuid4

import flet as ft

PREFIX = "expense_tracker.receipt."
MAX_WEB_BYTES = 1_500_000
MAX_NATIVE_BYTES = 15_000_000


class ReceiptError(Exception):
    """An attachment problem with a user-facing explanation."""


class ReceiptPhotos:
    def __init__(self):
        page = ft.context.page
        self.web = page.web
        self.mobile = page.platform in (ft.PagePlatform.ANDROID, ft.PagePlatform.IOS)
        self.picker = ft.FilePicker()
        self.prefs = ft.SharedPreferences()
        self.paths = ft.StoragePaths()

    def can_take_photo(self) -> bool:
        return self.mobile and not self.web

    def validate(self, data: bytes) -> bytes:
        if not data:
            raise ReceiptError("The selected photo was empty. Choose another photo.")
        if len(data) > (MAX_WEB_BYTES if self.web else MAX_NATIVE_BYTES):
            raise ReceiptError(
                "Choose a photo smaller than 1.5 MB in the browser preview. "
                "Larger photos work in the installed phone app."
                if self.web
                else "Choose a photo smaller than 15 MB."
            )
        return data

    async def pick(self) -> bytes | None:
        files = await self.picker.pick_files(
            dialog_title="Choose receipt photo",
            file_type=ft.FilePickerFileType.IMAGE,
            allow_multiple=False,
            with_data=True,
            compression_quality=80,
            cancel_upload_on_window_blur=False,
        )
        if not files:
            return None
        file = files[0]
        limit = MAX_WEB_BYTES if self.web else MAX_NATIVE_BYTES
        if file.size > limit and file.bytes is None:
            raise ReceiptError("This photo is too large. Choose a smaller photo.")
        data = file.bytes
        if data is None and file.path and not self.web:
            with open(file.path, "rb") as source:
                data = source.read(limit + 1)
        if data is None:
            raise ReceiptError("Couldn't read that photo. Please choose it again.")
        return self.validate(data)

    async def _folder(self) -> str:
        folder = os.path.join(
            await self.paths.get_application_documents_directory(), "receipts"
        )
        os.makedirs(folder, exist_ok=True)
        return folder

    def _key(self, ref: str) -> str:
        kind, _, key = ref.partition(":")
        if kind not in ("file", "prefs") or not re.fullmatch(r"[0-9a-f]{32}", key):
            raise ReceiptError("This receipt reference is invalid.")
        return key

    async def save(self, data: bytes) -> str:
        self.validate(data)
        key = uuid4().hex
        if self.web:
            if not await self.prefs.set(
                PREFIX + key, base64.b64encode(data).decode("ascii")
            ):
                raise ReceiptError("There isn't enough browser storage for this photo.")
            return "prefs:" + key
        path = os.path.join(await self._folder(), key + ".receipt")
        try:
            with open(path, "wb") as target:
                target.write(data)
        except Exception:
            if os.path.exists(path):
                os.remove(path)
            raise
        return "file:" + key

    async def load(self, ref: str) -> bytes | None:
        key = self._key(ref)
        if ref.startswith("prefs:"):
            raw = await self.prefs.get(PREFIX + key)
            return base64.b64decode(raw) if raw else None
        if self.web:
            return None
        path = os.path.join(await self._folder(), key + ".receipt")
        if os.path.exists(path):
            with open(path, "rb") as source:
                return source.read(MAX_NATIVE_BYTES + 1)
        return None

    async def delete(self, ref: str):
        key = self._key(ref)
        if ref.startswith("prefs:"):
            await self.prefs.remove(PREFIX + key)
        elif not self.web:
            path = os.path.join(await self._folder(), key + ".receipt")
            if os.path.exists(path):
                os.remove(path)

    async def collect_unused(self, keep: set[str]):
        # Run only on startup: photos of deleted expenses stay available for Undo
        # until the app restarts.
        if self.web:
            for key in await self.prefs.get_keys(PREFIX):
                ref = "prefs:" + key.removeprefix(PREFIX)
                if ref not in keep:
                    await self.delete(ref)
        else:
            folder = await self._folder()
            for name in os.listdir(folder):
                if re.fullmatch(r"[0-9a-f]{32}\.receipt", name):
                    ref = "file:" + name.removesuffix(".receipt")
                    if ref not in keep:
                        await self.delete(ref)
