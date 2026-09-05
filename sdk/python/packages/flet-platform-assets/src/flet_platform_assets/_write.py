"""Persisting a render into a Flutter project."""

from __future__ import annotations

from pathlib import Path

from ._imaging import save_ico, save_png
from ._models import RenderResult

__all__ = ["write"]


def write(
    result: RenderResult,
    project_dir: str | Path,
    *,
    declared_only: bool = True,
) -> list[Path]:
    """Write a render into a Flutter project.

    Args:
        result: What :func:`render_icons` or :func:`render_splash` produced.
        project_dir: Root of the Flutter project.
        declared_only: Only overwrite files that already exist. A rendered
            project declares which icons it uses - through its asset catalogs
            and web manifest - so this keeps generation from inventing files
            nothing references. Pass `False` for outputs a project is
            expected to gain, such as Android's adaptive layers.

    Returns:
        The paths written, in the order they were produced.
    """

    root = Path(project_dir)
    written: list[Path] = []

    for asset in result.assets:
        path = root / asset.relative_path
        if declared_only and not path.exists():
            continue
        save_png(asset.image, path)
        written.append(path)

    for relative, images in result.ico.items():
        path = root / relative
        if declared_only and not path.exists():
            continue
        save_ico(path, images)
        written.append(path)

    return written
