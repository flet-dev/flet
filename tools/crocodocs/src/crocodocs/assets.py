"""Asset discovery and syncing helpers."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from .config import AssetMapping


@dataclass(frozen=True)
class AssetResolution:
    ref: str
    source_path: Path
    static_destination: Path
    public_url: str


def iter_referenced_local_assets(
    front_matter: dict, content: str, refs: set[str]
) -> set[str]:
    out = set(refs)
    for key in ("example_media", "example_images", "example_images_examples"):
        value = front_matter.get(key)
        if isinstance(value, str) and value.startswith(".."):
            out.add(value)
    return out


def _parse_virtual_asset_ref(
    ref: str,
    asset_mappings: dict[str, AssetMapping],
) -> tuple[AssetMapping, str] | None:
    match = re.match(r"^(?:(?:\.\./)+)?([^/]+)/(.*)$", ref)
    if not match:
        return None
    ref_root, remainder = match.groups()
    mapping = asset_mappings.get(ref_root)
    if mapping is None:
        return None
    return mapping, remainder


def resolve_local_asset_source(
    ref: str,
    asset_mappings: dict[str, AssetMapping],
) -> Path | None:
    parsed = _parse_virtual_asset_ref(ref, asset_mappings)
    if parsed is None:
        return None
    mapping, remainder = parsed
    return mapping.source_path / remainder


def resolve_static_asset_url(
    ref: str,
    asset_mappings: dict[str, AssetMapping],
) -> str | None:
    parsed = _parse_virtual_asset_ref(ref, asset_mappings)
    if parsed is None:
        return None
    mapping, remainder = parsed
    return "/" + "/".join([mapping.static_subpath.strip("/"), remainder])


def resolve_asset_copy_targets(
    ref: str,
    static_root: Path,
    asset_mappings: dict[str, AssetMapping],
) -> AssetResolution | None:
    parsed = _parse_virtual_asset_ref(ref, asset_mappings)
    if parsed is None:
        return None
    mapping, remainder = parsed
    return AssetResolution(
        ref=ref,
        source_path=mapping.source_path / remainder,
        static_destination=(static_root / mapping.static_subpath / remainder).resolve(),
        public_url="/" + "/".join([mapping.static_subpath.strip("/"), remainder]),
    )


def _ext_ignore(include_exts: set[str]):
    """Return an ignore callback for shutil.copytree that skips files
    whose suffix is not in *include_exts*."""

    def _ignore(directory: str, contents: list[str]) -> list[str]:
        ignored: list[str] = []
        for name in contents:
            path = Path(directory) / name
            if path.is_file() and path.suffix.lower() not in include_exts:
                ignored.append(name)
        return ignored

    return _ignore


def bulk_copy_assets(
    source_root: Path,
    dest_root: Path,
    include_exts: set[str] | None = None,
) -> int:
    """Copy all matching files from *source_root* to *dest_root*.

    Returns the number of files copied.
    """
    copied = 0
    for source_path in sorted(source_root.rglob("*")):
        if not source_path.is_file():
            continue
        if include_exts and source_path.suffix.lower() not in include_exts:
            continue
        relative = source_path.relative_to(source_root)
        dest_path = dest_root / relative
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        copied += 1
    return copied
