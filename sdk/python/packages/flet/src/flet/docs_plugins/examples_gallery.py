import os
import subprocess
from pathlib import Path
from typing import Optional

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin


def _latest_mtime(root: Path) -> float:
    """Return the latest modification time for all files under a directory."""
    mtimes = []
    for path in root.rglob("*"):
        if path.is_file():
            mtimes.append(path.stat().st_mtime)
    return max(mtimes) if mtimes else 0.0


class ExamplesGalleryPlugin(BasePlugin):
    """Build the examples gallery Flet app before MkDocs runs.

    This plugin:
    - Finds the examples gallery entry point (default: docs/apps/examples-gallery/src/main.py).
    - Runs `flet publish` (via `uv run --active`) into the configured dist folder.
    - Skips the build when the dist/index.html is newer than the source tree.

    Env opts:
    - FLET_SKIP_EXAMPLES_GALLERY=1 — skip building (useful for fast local docs iteration).

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

        src_mtime = _latest_mtime(src.parent)
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

        subprocess.run(cmd, cwd=docs_dir, check=True, env=env)
