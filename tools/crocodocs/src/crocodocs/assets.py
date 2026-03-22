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
    should_copy: bool


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
    phase: str,
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
        should_copy=phase in mapping.copy_during,
    )


def copy_referenced_asset(
    ref: str,
    static_root: Path,
    asset_mappings: dict[str, AssetMapping],
    phase: str,
) -> bool:
    resolution = resolve_asset_copy_targets(ref, static_root, asset_mappings, phase)
    if resolution is None:
        return False
    if not resolution.should_copy:
        return False
    if not resolution.source_path.exists():
        return False
    resolution.static_destination.parent.mkdir(parents=True, exist_ok=True)
    if resolution.source_path.is_dir():
        shutil.copytree(
            resolution.source_path, resolution.static_destination, dirs_exist_ok=True
        )
    else:
        shutil.copy2(resolution.source_path, resolution.static_destination)
    return True
