import ast
import importlib.metadata
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

_PACKAGE_URI = re.compile(rb"package:([a-z][a-z0-9_]*)/")

# Directories that hold no app code, skipped when looking for the app's imports.
_SKIPPED_DIRS = {"__pycache__", "build", "dist", "node_modules", "site-packages"}


@dataclass
class InstalledExtension:
    """
    A Flet extension installed in the current environment.
    """

    package: str
    """
    Name of the extension's Flutter package.
    """

    distribution: Optional[str]
    """
    Name of the distribution that installed it, if known.
    """

    modules: set[str]
    """
    Top-level Python modules the extension provides.
    """


def get_client_extensions(snapshot_path: str) -> Optional[set[str]]:
    """
    Return the Flutter packages compiled into a prebuilt Flet client.

    Release builds keep the `package:<name>/` URI of every Dart library in the
    app's AOT snapshot: `data/app.so` on Windows, `lib/libapp.so` on Linux and
    `Contents/Frameworks/App.framework/App` in a macOS app bundle.

    Args:
        snapshot_path: Path to the client's AOT snapshot.

    Returns:
        Names of the packages, or `None` when the snapshot is missing or names no
            `flet` library, so the client's extensions can't be told.
    """

    path = Path(snapshot_path)
    if not path.is_file():
        return None
    packages = {m.decode() for m in _PACKAGE_URI.findall(path.read_bytes())}
    return packages if "flet" in packages else None


def find_extension_packages() -> set[str]:
    """
    Return the Flutter package names of the extensions on `sys.path`.

    Extensions install a `flutter/<package>/pubspec.yaml` file next to their
    Python modules, so this only lists those folders, without reading any
    distribution's metadata. Use `find_installed_extensions()` to learn which
    distribution and modules a package comes with.
    """

    packages: set[str] = set()
    for entry in sys.path:
        flutter_dir = Path(entry or ".") / "flutter"
        try:
            packages.update(p.parent.name for p in flutter_dir.glob("*/pubspec.yaml"))
        except OSError:
            continue
    return packages


def find_installed_extensions() -> list[InstalledExtension]:
    """
    Return the Flet extensions installed in the current environment.

    An extension is a distribution that installs a `flutter/<package>/pubspec.yaml`
    file. Editable installs list no such file in their `RECORD`, so a
    `flutter/<package>` folder on `sys.path` that no distribution owns is reported
    too when the same `sys.path` entry has a Python module named `<package>`.
    """

    extensions: dict[str, InstalledExtension] = {}
    for dist in importlib.metadata.distributions():
        files = dist.files or []
        packages = {
            f.parts[1]
            for f in files
            if len(f.parts) == 3
            and f.parts[0] == "flutter"
            and f.parts[2] == "pubspec.yaml"
        }
        if not packages:
            continue
        modules = {
            Path(f.parts[0]).stem
            for f in files
            if f.parts[0] not in ("flutter", "..", "__pycache__")
            and not f.parts[0].endswith((".dist-info", ".data", ".pth"))
            and (len(f.parts) > 1 or f.suffix == ".py")
        }
        for package in packages:
            extensions.setdefault(
                package,
                InstalledExtension(package, dist.metadata["Name"], modules),
            )

    for entry in sys.path:
        entry_dir = Path(entry or ".")
        if not (entry_dir / "flutter").is_dir():
            continue
        for pubspec in sorted((entry_dir / "flutter").glob("*/pubspec.yaml")):
            package = pubspec.parent.name
            if (entry_dir / package).is_dir() or (
                entry_dir / f"{package}.py"
            ).is_file():
                extensions.setdefault(
                    package, InstalledExtension(package, None, {package})
                )

    return sorted(extensions.values(), key=lambda e: e.package)


def find_imported_modules(app_dir: Path) -> set[str]:
    """
    Return the top-level modules the app's Python files import.

    Virtual environments, hidden folders, build output and symlinked folders in
    `app_dir` are skipped, as are files that can't be read or don't parse.

    Args:
        app_dir: Directory of the app's main script.
    """

    modules: set[str] = set()
    for path in _iter_app_files(app_dir):
        try:
            tree = ast.parse(path.read_bytes(), filename=str(path))
        except (OSError, SyntaxError, ValueError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                modules.add(node.module.split(".")[0])
    return modules


def find_missing_extensions(
    app_dir: Path, client_extensions: set[str]
) -> list[InstalledExtension]:
    """
    Return the installed extensions the app imports but the client lacks.

    Args:
        app_dir: Directory of the app's main script.
        client_extensions: Flutter packages compiled into the client, as
            returned by `get_client_extensions()`.
    """

    candidates = [
        e for e in find_installed_extensions() if e.package not in client_extensions
    ]
    if not candidates:
        return []
    imported = find_imported_modules(app_dir)
    return [e for e in candidates if e.modules & imported]


def _iter_app_files(directory: Path):
    """
    Yield the Python files of an app folder, recursively.
    """

    try:
        paths = sorted(directory.iterdir())
    except OSError:
        return
    for path in paths:
        if path.is_dir():
            if (
                path.is_symlink()
                or path.name.startswith(".")
                or path.name in _SKIPPED_DIRS
                or (path / "pyvenv.cfg").exists()
            ):
                continue
            yield from _iter_app_files(path)
        elif path.suffix == ".py":
            yield path
