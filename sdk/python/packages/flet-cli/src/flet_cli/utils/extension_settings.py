"""
Build settings that installed Flet extensions contribute to the app.

An extension ships a `flet-extension.toml` file anywhere in its wheel. The file
uses the keys of the app's `[tool.flet]` table, without the `tool.flet` prefix,
and only the keys in `ALLOWED_SETTINGS`. Its values are defaults under the
app's own settings: the app has the last word.
"""

import csv
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

EXTENSION_SETTINGS_FILE = "flet-extension.toml"

ALLOWED_SETTINGS = (
    "android.compile_options",
    "android.gradle_dependencies",
)
"""Dotted keys, relative to `[tool.flet]`, an extension may set."""


@dataclass
class ExtensionSettings:
    """The `flet-extension.toml` of one installed distribution."""

    name: str
    """Distribution name, as in its metadata."""

    version: str
    """Distribution version, as in its metadata."""

    path: Path
    """Location of the file in the build."""

    settings: dict[str, Any] = field(default_factory=dict)
    """Allowed settings by dotted key, such as `"android.compile_options"`."""

    @property
    def label(self) -> str:
        """The distribution name and version, for messages."""
        return f"{self.name} {self.version}"


def find_extension_settings(
    site_packages_dir: Path, flutter_packages_dir: Optional[Path]
) -> tuple[list[ExtensionSettings], list[str]]:
    """
    Read the `flet-extension.toml` of every distribution installed for the app.

    Files are found through each distribution's `RECORD`, so they can be
    anywhere in the wheel. The `flutter/` folders of installed packages are
    moved to `flutter_packages_dir` before this runs, so files listed under
    `flutter/` are read from there. A distribution installed for several
    architectures is read once.

    Args:
        site_packages_dir: Directory the app's packages were installed into,
            directly or in one subdirectory per architecture.
        flutter_packages_dir: Directory the `flutter/` folders were moved to.

    Returns:
        The settings of each distribution that has the file, ordered by
            distribution name, and warnings about files that could not be read.

    Raises:
        ValueError: When a file is invalid or a distribution lists more than one.
    """

    found: dict[str, ExtensionSettings] = {}
    warnings: list[str] = []
    records = sorted(site_packages_dir.glob("*.dist-info/RECORD")) + sorted(
        site_packages_dir.glob("*/*.dist-info/RECORD")
    )
    if not records and site_packages_dir.is_dir() and any(site_packages_dir.iterdir()):
        warnings.append(
            f"No package metadata (.dist-info) found in {site_packages_dir}, so "
            f"extensions' {EXTENSION_SETTINGS_FILE} build settings were not "
            "applied. Do the app's cleanup settings remove .dist-info directories?"
        )

    # Flutter packages whose distribution metadata is installed.
    owned_flutter_packages: set[str] = set()
    for record in records:
        dist_info = record.parent
        name, version = _distribution_name_version(dist_info)
        with record.open(newline="", encoding="utf-8") as f:
            paths = [Path(row[0]) for row in csv.reader(f) if row]
        owned_flutter_packages.update(
            p.parts[1] for p in paths if len(p.parts) > 2 and p.parts[0] == "flutter"
        )
        if name.lower() in found:
            continue
        entries = [str(p) for p in paths if p.name == EXTENSION_SETTINGS_FILE]
        if not entries:
            continue
        if len(entries) > 1:
            raise ValueError(
                f"{name} {version} contains more than one "
                f"{EXTENSION_SETTINGS_FILE}: {', '.join(entries)}."
            )

        entry = Path(entries[0])
        if ".." in entry.parts:
            warnings.append(
                f"{name} {version} installs {EXTENSION_SETTINGS_FILE} outside its "
                "packages, for example with setuptools data-files, so its build "
                "settings were not applied. The file must be inside a package of "
                "the wheel."
            )
            continue
        if entry.parts[0] == "flutter" and flutter_packages_dir is not None:
            path = flutter_packages_dir.joinpath(*entry.parts[1:])
        else:
            path = dist_info.parent / entry
        if not path.is_file():
            warnings.append(
                f"{name} {version} lists {entry} but the file is missing, so its "
                "build settings were not applied. Do the app's cleanup settings "
                "remove it?"
            )
            continue

        extension = ExtensionSettings(name=name, version=version, path=path)
        extension.settings, unsupported = _read_settings(extension)
        warnings.extend(
            f"{extension.label}: {EXTENSION_SETTINGS_FILE} setting {key!r} is not "
            "supported and was ignored."
            for key in unsupported
        )
        found[name.lower()] = extension

    if records and flutter_packages_dir is not None and flutter_packages_dir.is_dir():
        warnings.extend(
            f"The package that installed the Flutter package {package.name} has no "
            f"metadata (.dist-info) in {site_packages_dir}, so build settings in "
            f"its {EXTENSION_SETTINGS_FILE}, if any, were not applied. Do the "
            "app's cleanup settings remove .dist-info directories?"
            for package in sorted(flutter_packages_dir.iterdir())
            if (package / "pubspec.yaml").is_file()
            and package.name not in owned_flutter_packages
        )

    return sorted(found.values(), key=lambda e: e.name.lower()), warnings


def merge_compile_options(app_options: Any, extensions: list[ExtensionSettings]) -> Any:
    """
    Layer extensions' `android.compile_options` under the app's.

    Options are merged, and the app's value of an option wins. Two extensions
    setting an option to different values is a conflict, which fails the build;
    the app resolves it by setting that option itself.

    Args:
        app_options: The app's `[tool.flet.android.compile_options]` value.
        extensions: Settings found by `find_extension_settings()`.

    Returns:
        The merged table, or `app_options` unchanged when no extension sets
            options or the app's value is not a table, for the setting's own
            validation to report.

    Raises:
        ValueError: When extensions conflict on an option the app does not set.
    """

    if app_options is not None and not isinstance(app_options, dict):
        return app_options
    merged: dict[str, Any] = {}
    owners: dict[str, ExtensionSettings] = {}
    for extension in extensions:
        options = extension.settings.get("android.compile_options", {})
        for name, expression in options.items():
            owner = owners.get(name)
            if (
                owner is not None
                and merged[name] != expression
                and name not in (app_options or {})
            ):
                raise ValueError(
                    f"Conflicting android compile option {name}: {owner.label} "
                    f"sets {merged[name]!r} and {extension.label} sets "
                    f"{expression!r}. To resolve the conflict, set {name} in the "
                    "app's [tool.flet.android.compile_options]."
                )
            merged.setdefault(name, expression)
            owners.setdefault(name, extension)
    if not merged:
        return app_options
    return {**merged, **(app_options or {})}


def merge_gradle_dependencies(
    app_dependencies: Any, extensions: list[ExtensionSettings]
) -> Any:
    """
    Combine extensions' `android.gradle_dependencies` with the app's.

    Extensions' declarations come first, then the app's. A declaration is added
    once, and an extension's is left out when the app's declarations already
    contain it as a whole, ignoring whitespace and the app's comments.

    Args:
        app_dependencies: The app's `[tool.flet.android].gradle_dependencies`.
        extensions: Settings found by `find_extension_settings()`.

    Returns:
        The combined declarations, or `app_dependencies` unchanged when no
            extension adds any or the app's value is not a string, for the setting's
            own validation to report.
    """

    if app_dependencies is not None and not isinstance(app_dependencies, str):
        return app_dependencies
    app = re.sub(r"/\*.*?\*/", " ", app_dependencies or "", flags=re.DOTALL)
    app = _compact(re.sub(r"(^|\s)//[^\n]*", r"\1", app))
    declarations: list[str] = []
    for extension in extensions:
        declaration = extension.settings.get("android.gradle_dependencies")
        if declaration is None or any(
            _compact(declaration) == _compact(d) for d in declarations
        ):
            continue
        # Preceded by no identifier character, so `implementation(...)` is not
        # found inside `debugImplementation(...)`.
        if re.search(r"(?<![\w.])" + re.escape(_compact(declaration)), app):
            continue
        declarations.append(declaration)
    if not declarations:
        return app_dependencies
    if app_dependencies is not None:
        declarations.append(textwrap.dedent(app_dependencies).strip())
    return "\n".join(declarations)


def contributed_settings(extension: ExtensionSettings) -> list[str]:
    """
    Describe what an extension contributes, for build output.

    Args:
        extension: Settings of one extension.

    Returns:
        Dotted keys under `[tool.flet]`, with property names for tables.
    """

    described = []
    for key, value in extension.settings.items():
        if isinstance(value, dict):
            described.extend(f"{key}.{name}" for name in value)
        else:
            described.append(key)
    return described


def _compact(code: str) -> str:
    """
    Remove whitespace outside string literals, so declarations that differ only in
    formatting compare equal while ones with different paths or names don't.
    """
    return re.sub(
        r"(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')|\s+",
        lambda m: m.group(1) or "",
        code,
    )


def _read_settings(extension: ExtensionSettings) -> tuple[dict[str, Any], list[str]]:
    """Parse and validate a file, returning allowed settings and other keys."""

    try:
        document = tomllib.loads(extension.path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as e:
        raise ValueError(
            f"{extension.label}: cannot read {EXTENSION_SETTINGS_FILE}: {e}"
        ) from e

    if "tool" in document:
        raise ValueError(
            f"{extension.label}: {EXTENSION_SETTINGS_FILE} uses a [tool] table. "
            "Write its settings without the tool.flet prefix, for example "
            "[android] instead of [tool.flet.android]."
        )

    settings: dict[str, Any] = {}
    unsupported: list[str] = []
    for key, value in _flatten(document):
        if key in ALLOWED_SETTINGS:
            settings[key] = value
        else:
            unsupported.append(key)

    compile_options = settings.get("android.compile_options")
    if compile_options is not None and (
        not isinstance(compile_options, dict)
        or not all(isinstance(v, str) and v.strip() for v in compile_options.values())
    ):
        raise ValueError(
            f"{extension.label}: android.compile_options in "
            f"{EXTENSION_SETTINGS_FILE} must be a table of nonempty Kotlin "
            "expression strings."
        )
    if compile_options is not None:
        settings["android.compile_options"] = {
            name: expression.strip() for name, expression in compile_options.items()
        }
    dependencies = settings.get("android.gradle_dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, str) or not dependencies.strip():
            raise ValueError(
                f"{extension.label}: android.gradle_dependencies in "
                f"{EXTENSION_SETTINGS_FILE} must be a nonempty string of Kotlin "
                "declarations."
            )
        settings["android.gradle_dependencies"] = textwrap.dedent(dependencies).strip()
    return settings, unsupported


def _flatten(document: dict[str, Any], prefix: str = ""):
    """Yield `(dotted key, value)` pairs, stopping at allowed settings."""

    for key, value in document.items():
        dotted = f"{prefix}{key}"
        if isinstance(value, dict) and dotted not in ALLOWED_SETTINGS:
            yield from _flatten(value, f"{dotted}.")
        else:
            yield dotted, value


def _distribution_name_version(dist_info: Path) -> tuple[str, str]:
    """Read a distribution's name and version from its metadata."""

    name, _, version = dist_info.name[: -len(".dist-info")].partition("-")
    metadata = dist_info / "METADATA"
    if metadata.is_file():
        for line in metadata.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line:
                break
            if line.startswith("Name:"):
                name = line[len("Name:") :].strip()
            elif line.startswith("Version:"):
                version = line[len("Version:") :].strip()
    return name, version
