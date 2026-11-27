"""`flet publish` must honor `tool.flet.web.pwa_short_name`.

`flet build` already reads that setting for the PWA `short_name`. `flet
publish` documented the same key but skipped it and wrote `project.name`
into `dist/manifest.json` instead. The CLI flag must still win.
"""

from argparse import Namespace
from pathlib import Path

from flet_cli.commands.publish import resolve_app_short_name
from flet_cli.utils.pyproject_toml import load_pyproject_toml


def _options(app_short_name=None):
    return Namespace(app_short_name=app_short_name)


def _project(tmp_path: Path, body: str) -> Path:
    (tmp_path / "pyproject.toml").write_text(body, encoding="utf-8")
    return tmp_path


def test_pyproject_pwa_short_name_wins_over_project_name(tmp_path):
    project_dir = _project(
        tmp_path,
        """
[project]
name = "cool_counter"

[tool.flet.web]
pwa_short_name = "Short"
""",
    )

    assert (
        resolve_app_short_name(_options(), load_pyproject_toml(project_dir), project_dir)
        == "Short"
    )


def test_cli_app_short_name_wins_over_pyproject(tmp_path):
    project_dir = _project(
        tmp_path,
        """
[project]
name = "cool_counter"

[tool.flet.web]
pwa_short_name = "Short"
""",
    )

    assert (
        resolve_app_short_name(
            _options(app_short_name="FromCli"),
            load_pyproject_toml(project_dir),
            project_dir,
        )
        == "FromCli"
    )


def test_falls_back_to_project_name_when_pwa_short_name_is_absent(tmp_path):
    project_dir = _project(
        tmp_path,
        """
[project]
name = "cool_counter"
""",
    )

    assert (
        resolve_app_short_name(_options(), load_pyproject_toml(project_dir), project_dir)
        == "cool_counter"
    )
