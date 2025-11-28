import importlib.util
import logging
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
from mkdocs.plugins import BasePlugin

logger = logging.getLogger("flet.docs.examples_gallery")


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
    logger.info("Installing pip in the current environment for `flet publish`.")
    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)


def _web_path_ready(path: Path) -> bool:
    """Return True when ``path`` points to a usable web client."""
    return path.is_dir() and path.joinpath("index.html").is_file()


def _locate_existing_web_client(env: Mapping[str, str]) -> Optional[Path]:
    """Check configured env or installed packages for a usable web client."""
    configured = env.get("FLET_WEB_PATH")
    if configured:
        candidate = Path(configured).expanduser()
        if _web_path_ready(candidate):
            return candidate
        logger.warning(
            "FLET_WEB_PATH is set to %s but no web client was found.", candidate
        )

    try:
        from flet_web import get_package_web_dir
    except Exception as exc:  # noqa: BLE001
        logger.debug("Unable to import flet_web: %s", exc)
        return None

    try:
        package_web = Path(get_package_web_dir())
    except Exception as exc:  # noqa: BLE001
        logger.debug("Unable to resolve packaged web client: %s", exc)
        return None

    return package_web if _web_path_ready(package_web) else None


def _download_packaged_web_client(version: str) -> Optional[Path]:
    """Download the pre-built flet-web wheel and expose its web folder."""
    cache_root = Path(tempfile.gettempdir()) / "flet-web"
    target_root = cache_root / version
    web_dir = target_root / "flet_web" / "web"

    if _web_path_ready(web_dir):
        return web_dir

    if target_root.exists():
        shutil.rmtree(target_root, ignore_errors=True)

    target_root.mkdir(parents=True, exist_ok=True)
    _ensure_pip_available()

    logger.info("Downloading flet-web==%s into %s", version, target_root)
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
        logger.warning("Unable to download flet-web==%s: %s", version, exc)
        return None

    return web_dir if _web_path_ready(web_dir) else None


def _ensure_web_client(env: dict[str, str]) -> Path:
    """Ensure a web client exists and return the path to use for publishing."""
    existing = _locate_existing_web_client(env)
    if existing:
        return existing

    try:
        from flet import version as flet_version
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "FLET_WEB_PATH is not set and the flet version could not be determined to "
            "download a packaged web client. Set FLET_WEB_PATH manually to a built "
            "client (e.g. client/build/web)."
        ) from exc

    target_version = flet_version.version or getattr(
        flet_version, "DEFAULT_VERSION", ""
    )
    downloaded = _download_packaged_web_client(target_version)
    if downloaded:
        return downloaded

    raise RuntimeError(
        "FLET_WEB_PATH is not set and no packaged web client could be downloaded "
        f"(tried flet-web=={target_version}). Provide FLET_WEB_PATH pointing to a "
        "built client or ensure network access to download the flet-web wheel."
    )


def _latest_mtime(root: Path, ignored: Optional[Iterable[Path]] = None) -> float:
    """Return the newest mtime under ``root`` ignoring any ``ignored`` directories."""
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
    - Finds the examples gallery entry point (default: docs/apps/examples-gallery/src/main.py).
    - Runs `flet publish` (via `uv run --active`) into the configured dist folder.
    - Skips the build when the dist/index.html is newer than the source tree.

    Env opts:
    - FLET_SKIP_EXAMPLES_GALLERY=1 — skip building (useful for fast local docs iteration).
    - FLET_WEB_PATH — optional path to a built Flet web client; if unset the plugin
      downloads the matching flet-web wheel into a temp cache.

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
        ("src", config_options.Type(str, default="apps/examples-gallery/src/main.py")),
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
        - Runs the configured command (or the default `uv run --active flet publish ...`)
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

        src_mtime = _latest_mtime(src_root, ignore_roots)
        dist_mtime = dist_index.stat().st_mtime if dist_index.exists() else 0.0
        if dist_mtime >= src_mtime:
            return

        cmd: Optional[list[str]] = self.config.get("command")
        if not cmd:
            cmd = [
                "uv",
                "run",
                "--active",
                "flet",
                "publish",
                str(src),
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

        web_client_path = _ensure_web_client(env)
        env["FLET_WEB_PATH"] = str(web_client_path)

        _ensure_pip_available()
        subprocess.run(cmd, cwd=docs_dir, check=True, env=env)
