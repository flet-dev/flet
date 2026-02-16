import os
import subprocess
import sys
import tempfile
from pathlib import Path

import flet as ft


def open_file(_, path: str):
    """Open a desktop file in the default application."""
    if os.path.isfile(path):
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", path])
        elif sys.platform == "win32":  # Windows
            os.startfile(path)
        else:  # Linux / BSD
            subprocess.run(["xdg-open", path])


async def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # supported-platform checkers
    supports_set_files = not page.web and page.platform.is_desktop()
    supports_get_files = not page.web and (
        page.platform.is_desktop() or page.platform == ft.PagePlatform.ANDROID
    )

    def get_sample_files() -> list[str]:
        # create temporary files
        sample_dir = Path(tempfile.gettempdir()) / "flet_clipboard_files_example"
        sample_dir.mkdir(parents=True, exist_ok=True)
        sample_files = [
            sample_dir / "sample_1.txt",
            sample_dir / "sample_2.txt",
        ]
        sample_files[0].write_text("Clipboard sample file #1\n", encoding="utf-8")
        sample_files[1].write_text("Clipboard sample file #2\n", encoding="utf-8")
        return [str(p) for p in sample_files]

    async def set_files_to_clipboard(e: ft.Event[ft.Button]):
        files = get_sample_files()
        ok = await ft.Clipboard().set_files(files)
        status.value = (
            f"Set {len(files)} file references to clipboard (result: {ok})."
            if ok
            else "Failed to set file references to clipboard."
        )

    async def get_files_from_clipboard(e: ft.Event[ft.Button]):
        files = await ft.Clipboard().get_files()
        if files:
            files_lv.controls = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(f, selectable=True),
                        ft.IconButton(
                            icon=ft.Icons.OPEN_IN_NEW,
                            icon_size=15,
                            on_click=lambda e, f=f: open_file(e, f),
                            tooltip="Open file",
                        ),
                    ],
                )
                for f in files
            ]
        else:
            files_lv.controls = []
        status.value = f"Read {len(files)} file reference(s) from clipboard."

    page.add(
        ft.SafeArea(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Button(
                        "Set example files to clipboard",
                        on_click=set_files_to_clipboard,
                        disabled=not supports_set_files,
                        tooltip="Supported on desktop platforms only."
                        if not supports_set_files
                        else None,
                    ),
                    ft.Button(
                        "Get files from clipboard",
                        on_click=get_files_from_clipboard,
                        disabled=not supports_get_files,
                        tooltip="Supported on Android and desktop platforms only."
                        if not supports_get_files
                        else None,
                    ),
                    status := ft.Text(),
                    files_lv := ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                        controls=[],
                    ),
                ],
            )
        )
    )


ft.run(main)
