"""CrocoDocs config loading."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


@dataclass
class AssetMapping:
    ref_root: str
    source_path: Path
    static_subpath: str
    include_exts: set[str] | None


@dataclass
class CrocoDocsConfig:
    project_root: Path
    docs_path: Path
    manifest_output: Path
    api_output: Path
    partials_output_dir: Path
    sidebars_source: Path
    sidebars_output: Path
    examples_root: Path
    asset_mappings: dict[str, AssetMapping]
    base_url: str
    extensions: list[str]
    packages: dict[str, Path]
    member_filters: dict[str, set[str]]


def _resolve_path(project_root: Path, value: str) -> Path:
    """Join project_root with value and return the resolved absolute path."""
    return (project_root / value).resolve()


def load_config(project_root: Path) -> CrocoDocsConfig:
    """Read [tool.crocodocs] from pyproject.toml and return a CrocoDocsConfig instance."""
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(f"CrocoDocs config not found: {pyproject_path}")

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    tool = data.get("tool", {})
    raw = tool.get("crocodocs", {})
    raw_packages = raw.get("packages", {})
    raw_member_filters = raw.get("member_filters", {})
    raw_asset_mappings = raw.get("asset_mappings", {})
    asset_mappings = {
        ref_root: AssetMapping(
            ref_root=ref_root,
            source_path=_resolve_path(project_root, mapping["source_path"]),
            static_subpath=str(mapping["static_subpath"]).strip("/"),
            include_exts=set(mapping["include_exts"])
            if "include_exts" in mapping
            else None,
        )
        for ref_root, mapping in raw_asset_mappings.items()
    }
    examples_root_value = raw.get("examples_root")
    if examples_root_value is None:
        raise KeyError("CrocoDocs config requires 'examples_root'.")
    examples_root = _resolve_path(project_root, examples_root_value)

    return CrocoDocsConfig(
        project_root=project_root,
        docs_path=_resolve_path(project_root, raw["docs_path"]),
        manifest_output=_resolve_path(project_root, raw["manifest_output"]),
        api_output=_resolve_path(project_root, raw["api_output"]),
        partials_output_dir=_resolve_path(project_root, raw["partials_output_dir"]),
        sidebars_source=_resolve_path(project_root, raw["sidebars_source"]),
        sidebars_output=_resolve_path(project_root, raw["sidebars_output"]),
        examples_root=examples_root,
        asset_mappings=asset_mappings,
        base_url=str(raw["base_url"]),
        extensions=list(raw.get("extensions", [])),
        packages={
            name: _resolve_path(project_root, path)
            for name, path in raw_packages.items()
        },
        member_filters={
            key: {str(item) for item in values}
            for key, values in raw_member_filters.items()
            if isinstance(values, list)
        },
    )


def apply_path_override(
    config: CrocoDocsConfig, field_name: str, value: str | None
) -> None:
    """Set a Path field on config from a CLI string value, resolving it relative to project_root.

    Does nothing when value is None.
    """
    if value is None:
        return
    setattr(config, field_name, (config.project_root / value).resolve())


def apply_value_override(
    config: CrocoDocsConfig, field_name: str, value: Any | None
) -> None:
    """Set a scalar field on config to value. Does nothing when value is None."""
    if value is None:
        return
    setattr(config, field_name, value)


def apply_package_overrides(
    config: CrocoDocsConfig, overrides: list[str] | None
) -> None:
    """Apply NAME:PATH package entries from CLI --package flags to config.packages.

    Each override must have the form 'NAME:PATH'; raises ArgumentTypeError otherwise.
    """
    if not overrides:
        return
    for item in overrides:
        if ":" not in item:
            raise argparse.ArgumentTypeError(
                f"Invalid --package value '{item}'. Expected NAME:PATH."
            )
        name, path = item.split(":", 1)
        config.packages[name] = (config.project_root / path).resolve()
