import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Optional

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from packaging.requirements import Requirement

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - fallback for 3.10
    import tomli as tomllib  # type: ignore[no-redef]

log = get_plugin_logger("examples_gallery")


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def _has_pip() -> bool:
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return importlib.util.find_spec("pip") is not None


def _ensure_pip_available() -> None:
    """Bootstrap pip into the active virtualenv when it's missing."""
    if _has_pip():
        return
    log.info("Installing pip...")
    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)


def _web_path_ready(path: Path) -> bool:
    """Return True when `path` points to a usable web client."""
    return path.is_dir() and path.joinpath("index.html").is_file()


def _find_pyproject(start: Path, stop: Optional[Path] = None) -> Optional[Path]:
    """Walk up from start looking for pyproject.toml, stopping at `stop` if provided."""
    current = start.resolve()
    stop = stop.resolve() if stop else None
    while True:
        candidate = current / "pyproject.toml"
        if candidate.is_file():
            return candidate
        if current == current.parent or (stop and current == stop):
            return None
        current = current.parent


def _version_from_specifiers(specifiers) -> tuple[Optional[str], bool]:
    """Extract a deterministic version from a SpecifierSet.

    Returns (version, lower_only_flag).
    - If an exact pin or upper bound exists, returns that version and False.
    - If only lower bounds exist (>=, >, ~=), returns (None, True) so callers
        can opt for a fallback (e.g., latest pre-release) instead of trying a
        nonexistent lower bound.
    """
    for operator in ("==", "==="):
        for spec in specifiers:
            if spec.operator == operator:
                return spec.version, False

    for operator in ("<", "<="):
        for spec in specifiers:
            if spec.operator == operator:
                return spec.version, False

    for operator in ("~=", ">=", ">"):
        for spec in specifiers:
            if spec.operator == operator:
                return None, True

    return None, False


def _version_from_pyproject(pyproject: Path) -> tuple[Optional[str], bool]:
    """
    Read the flet dependency from pyproject.toml
    and return a version plus lower-only flag.
    """
    try:
        data = tomllib.loads(pyproject.read_text())
    except Exception as exc:  # noqa: BLE001
        log.debug("Unable to parse %s: %s", pyproject, exc)
        return None, False

    deps = data.get("project", {}).get("dependencies") or []
    for raw in deps:
        try:
            req = Requirement(raw)
        except Exception:  # noqa: BLE001
            continue
        if req.name != "flet":
            continue
        candidate, lower_only = _version_from_specifiers(req.specifier)
        if candidate or lower_only:
            return candidate, lower_only
    return None, False


def _resolve_flet_version(
    env: Mapping[str, str], src_root: Path, docs_dir: Path
) -> tuple[Optional[str], bool]:
    """Resolve the Flet version similar to `flet publish`.

    Order:
    - Explicit override: FLET_WEB_VERSION.
    - Version pinned in the gallery's pyproject.toml (walk up from src).
    - The version exposed by the local flet package
        (patched in releases or derived from git tags).
    - DEFAULT_VERSION from flet.version.

    This keeps docs builds reproducible for historical commits and avoids
    pulling newer incompatible clients.
    """
    default_version: Optional[str] = None
    try:
        from flet import version as flet_version

        default_version = getattr(flet_version, "DEFAULT_VERSION", None)
    except Exception as exc:  # noqa: BLE001
        log.debug("Unable to preload flet version defaults: %s", exc)

    if env.get("FLET_WEB_VERSION"):
        return str(env["FLET_WEB_VERSION"]), False

    pyproject = _find_pyproject(src_root, stop=docs_dir.parent)
    pinned, lower_only = (
        _version_from_pyproject(pyproject) if pyproject else (None, False)
    )
    if pinned:
        return pinned, False
    if lower_only:
        return None, True

    try:
        from flet import version as flet_version

        resolved = flet_version.version or getattr(
            flet_version, "DEFAULT_VERSION", None
        )
        resolved = resolved or default_version
        if resolved:
            return str(resolved), False
    except Exception as exc:  # noqa: BLE001
        log.debug("Unable to resolve flet version from package: %s", exc)

    if default_version:
        return str(default_version), False

    raise RuntimeError(
        "FLET_WEB_PATH is not set and Flet version could not be determined. "
        "Set FLET_WEB_VERSION or provide FLET_WEB_PATH pointing to a built client."
    )


def _locate_existing_web_client(env: Mapping[str, str]) -> Optional[Path]:
    """Check configured env or installed packages for a usable web client."""
    configured = env.get("FLET_WEB_PATH")
    if configured:
        candidate = Path(configured).expanduser()
        if _web_path_ready(candidate):
            return candidate
        log.warning(
            "FLET_WEB_PATH is set to %s but no web client was found.", candidate
        )

    try:
        from flet_web import get_package_web_dir
    except Exception as exc:  # noqa: BLE001
        log.debug("Unable to import flet_web: %s", exc)
        return None

    try:
        package_web = Path(get_package_web_dir())
    except Exception as exc:  # noqa: BLE001
        log.debug("Unable to resolve packaged web client: %s", exc)
        return None

    return package_web if _web_path_ready(package_web) else None


def _download_packaged_web_client(
    version: Optional[str], pre_only: bool = False
) -> Optional[Path]:
    """Download the pre-built flet-web wheel and expose its web folder.

    Uses a temp/versioned cache to avoid repeated downloads during local dev.
    When `pre_only` is True (or version is None), skip the exact-version attempt
    and go straight to the latest available pre-release wheel.
    """
    cache_root = Path(tempfile.gettempdir()) / "flet-web"
    cache_key = version or "latest-pre"
    target_root = cache_root / cache_key
    web_dir = target_root / "flet_web" / "web"

    if _web_path_ready(web_dir):
        return web_dir

    if target_root.exists():
        shutil.rmtree(target_root, ignore_errors=True)

    target_root.mkdir(parents=True, exist_ok=True)
    _ensure_pip_available()

    def _install_latest_pre() -> bool:
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "--only-binary",
                    ":all:",
                    "--pre",
                    "flet-web",
                    "--target",
                    str(target_root),
                ],
                check=True,
            )
            return True
        except subprocess.CalledProcessError as exc2:
            log.warning("Unable to download a fallback flet-web wheel: %s", exc2)
            return False

    if not pre_only and version:
        log.info("Downloading flet-web==%s into %s", version, target_root)
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "--only-binary",
                    ":all:",
                    f"flet-web=={version}",
                    "--target",
                    str(target_root),
                ],
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            log.warning("Unable to download flet-web==%s: %s", version, exc)
            log.info("Falling back to latest available pre-release flet-web wheel.")
            if not _install_latest_pre():
                return None
    else:
        log.info("No exact flet-web version to install; using latest pre-release.")
        if not _install_latest_pre():
            return None

    return web_dir if _web_path_ready(web_dir) else None


def _ensure_web_client(env: dict[str, str], src_root: Path, docs_dir: Path) -> Path:
    """Ensure a web client exists and return the path to use for publishing.

    Prefers an already-available client (env or packaged). If none exists,
    resolves a version and downloads the wheel into a temp cache.
    """
    existing = _locate_existing_web_client(env)
    if existing:
        return existing

    target_version, lower_only = _resolve_flet_version(env, src_root, docs_dir)
    downloaded = _download_packaged_web_client(target_version, pre_only=lower_only)
    if downloaded:
        return downloaded

    raise RuntimeError(
        "FLET_WEB_PATH is not set and no packaged web client could be downloaded "
        f"(tried flet-web=={target_version} and latest pre-release). Provide "
        "FLET_WEB_PATH pointing to a built client or ensure network access to "
        "download the flet-web wheel."
    )


def _latest_mtime(root: Path, ignored: Optional[Iterable[Path]] = None) -> float:
    """Return the newest mtime under `root` ignoring any `ignored` directories."""
    root = root.resolve()
    ignore_roots = tuple(p.resolve() for p in ignored or ())
    latest = 0.0
    for dirpath, dirnames, filenames in os.walk(root):
        current_dir = Path(dirpath)
        if any(_is_relative_to(current_dir, skipped) for skipped in ignore_roots):
            dirnames[:] = []
            continue
        for name in filenames:
            file_path = current_dir / name
            if any(_is_relative_to(file_path, skipped) for skipped in ignore_roots):
                continue
            try:
                latest = max(latest, file_path.stat().st_mtime)
            except FileNotFoundError:
                continue
    return latest


class ExamplesGalleryPlugin(BasePlugin):
    """Build the examples gallery Flet app before MkDocs runs.

    This plugin:
    - Finds the examples gallery entry point
        (default: docs/apps/examples-gallery/src/main.py).
    - Runs `flet publish` (via `uv run --active`) into the configured dist folder.
    - Skips the build when the dist/index.html is newer than the source tree.

    Env opts:
    - FLET_SKIP_EXAMPLES_GALLERY=1 — skip building
        (useful for fast local docs iteration).
    - FLET_WEB_PATH — optional path to a built Flet web client; if unset the plugin
        downloads the matching flet-web wheel into a temp cache.
    - FLET_WEB_VERSION — optional version override for the wheel download.

    Config options (mkdocs.yml):
    - enabled: bool (default True)
    - src: path to the gallery main.py relative to docs_dir
    - dist: output folder relative to docs_dir
    - base_url: base URL passed to `--base-url`
    - command: optional custom command list to run instead of the default
    - env: optional extra env vars to inject into the command
    """

    config_scheme = (
        ("enabled", config_options.Type(bool, default=True)),
        ("src", config_options.Type(str, default="apps/examples-gallery/src")),
        ("dist", config_options.Type(str, default="apps/examples-gallery/dist")),
        ("base_url", config_options.Type(str, default="apps/examples-gallery/dist")),
        ("command", config_options.Type(list, default=None)),
        ("env", config_options.Type(dict, default=None)),
    )

    def on_pre_build(self, config: MkDocsConfig) -> None:
        """
        Optionally publish the examples gallery before the docs build.

        - Honours `enabled` and `FLET_SKIP_EXAMPLES_GALLERY`.
        - Skips when the existing dist/index.html is newer than the source tree.
        - Runs the configured command (or the default `uv run flet publish ...`)
            with `docs_dir` as the working directory and merged env vars.
        """
        if not self.config.get("enabled", True):
            return
        if os.environ.get("FLET_SKIP_EXAMPLES_GALLERY"):
            return

        docs_dir = Path(config["docs_dir"])
        src = docs_dir / self.config["src"]
        dist_dir = docs_dir / self.config["dist"]
        dist_index = dist_dir / "index.html"
        strict_mode = bool(config.get("strict", False))

        if not src.exists():
            return

        # Accept either a specific entry file or a folder and consistently inspect
        # the directory that actually contains the source files.
        src_root = src if src.is_dir() else src.parent
        ignore_roots: list[Path] = []
        if _is_relative_to(dist_dir, src_root):
            # Publishing into the source tree dirties files for every build, so
            # ignore the generated dist folder when computing the latest mtime.
            ignore_roots.append(dist_dir)

        # Skip rebuild if dist/index.html is already as new as the newest source file.
        src_mtime = _latest_mtime(src_root, ignore_roots)
        dist_mtime = dist_index.stat().st_mtime if dist_index.exists() else 0.0
        if dist_mtime >= src_mtime:
            log.info("Skipping build; dist is up-to-date at %s", dist_index)
            return

        staging_dir: Optional[Path] = None
        try:
            # Prepare a staging directory to ease bundling
            # external examples alongside the app.
            staging_dir = Path(tempfile.mkdtemp(prefix="flet-examples-gallery-"))
            log.info("Staging examples gallery into %s", staging_dir)
            source_root = src_root.parent
            shutil.copytree(
                source_root,
                staging_dir,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    "build", "dist", "__pycache__", ".venv", ".git"
                ),
            )

            staged_src_root = staging_dir / src_root.name

            # Copy examples/controls to the staged app
            # so imports work in the packaged build.
            repo_examples_controls = (
                docs_dir.resolve().parents[2] / "examples" / "controls"
            )
            if repo_examples_controls.is_dir():
                dest_controls = staged_src_root / "controls"
                if dest_controls.exists():
                    shutil.rmtree(dest_controls)
                shutil.copytree(repo_examples_controls, dest_controls)

            staged_entry = staging_dir / src.relative_to(source_root)

            cmd: Optional[list[str]] = self.config.get("command")
            if not cmd:
                cmd = [
                    "uv",
                    "run",
                    "--active",
                    "flet",
                    "publish",
                    str(staged_entry or src),
                    "--distpath",
                    str(dist_dir),
                    "--base-url",
                    self.config["base_url"],
                    "--route-url-strategy",
                    "hash",
                    "--pre",
                ]

            env: dict[str, str] = dict(os.environ)
            extra_env = self.config.get("env") or {}
            env.update({k: str(v) for k, v in extra_env.items()})

            web_client_path = _ensure_web_client(env, src_root, docs_dir)
            env["FLET_WEB_PATH"] = str(web_client_path)

            _ensure_pip_available()
            log.info("Running publish: %s", " ".join(cmd))
            subprocess.run(cmd, cwd=docs_dir, check=True, env=env)
        except Exception as exc:
            if strict_mode:
                raise
            log.warning(
                "Build failed; skipping because mkdocs strict mode is off. Reason: %s",
                exc,
            )
            return
        finally:
            # cleanup
            if staging_dir:
                shutil.rmtree(staging_dir, ignore_errors=True)
