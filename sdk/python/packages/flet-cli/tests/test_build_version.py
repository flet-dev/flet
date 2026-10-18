"""
The version and build number `flet build` passes to Flutter, which embeds them
in the app, where `page.get_package_info()` returns them.
"""

from pathlib import Path
from typing import Optional

import pytest
import yaml

from flet_cli.cli import parse_command_line


def flutter_version_args(
    cli_args: list[str], pyproject: Optional[dict] = None
) -> dict[str, Optional[str]]:
    """
    Build the `flutter build` arguments of `flet build apk`.

    Args:
        cli_args: Options given to `flet build apk`.
        pyproject: `pyproject.toml` settings, keyed by dotted path.

    Returns:
        The values of `--build-name` and `--build-number`, `None` when the
            argument is not passed and Flutter falls back to the template's
            `pubspec.yaml` version, `1.0.0+1`.
    """
    options = parse_command_line(["build", "apk", *cli_args])
    cmd = options.handler.__self__
    cmd.options = options
    cmd.build_dir = cmd.flutter_dir = "."
    cmd.template_data = {"options": {"target_arch": None}, "split_per_abi": False}
    values = pyproject or {}
    cmd.get_pyproject = lambda key=None: values.get(key)
    cmd.target_platform = "apk"
    cmd.config_platform = cmd.platforms["apk"]["config_platform"]

    args = []
    cmd.add_flutter_command_args(args)

    def value(name):
        return args[args.index(name) + 1] if name in args else None

    return {"version": value("--build-name"), "build_number": value("--build-number")}


@pytest.mark.parametrize(
    ("cli_args", "pyproject", "expected"),
    [
        pytest.param(
            [],
            {},
            {"version": None, "build_number": None},
            id="neither",
        ),
        pytest.param(
            [],
            {"project.version": "1.2.3", "tool.flet.build_number": 42},
            {"version": "1.2.3", "build_number": "42"},
            id="pyproject",
        ),
        pytest.param(
            [],
            {"tool.poetry.version": "2.0.0"},
            {"version": "2.0.0", "build_number": None},
            id="poetry-version",
        ),
        pytest.param(
            [],
            {"project.version": "1.2.3", "tool.poetry.version": "2.0.0"},
            {"version": "1.2.3", "build_number": None},
            id="project-version-over-poetry",
        ),
        pytest.param(
            ["--build-version", "3.0.0", "--build-number", "7"],
            {},
            {"version": "3.0.0", "build_number": "7"},
            id="cli",
        ),
        pytest.param(
            ["--build-version", "3.0.0", "--build-number", "7"],
            {
                "project.version": "1.2.3",
                "tool.poetry.version": "2.0.0",
                "tool.flet.build_number": 42,
            },
            {"version": "3.0.0", "build_number": "7"},
            id="cli-over-pyproject",
        ),
        pytest.param(
            ["--build-version", "3.0.0"],
            {"project.version": "1.2.3", "tool.flet.build_number": 42},
            {"version": "3.0.0", "build_number": "42"},
            id="cli-version-only",
        ),
        pytest.param(
            ["--build-number", "7"],
            {"project.version": "1.2.3", "tool.flet.build_number": 42},
            {"version": "1.2.3", "build_number": "7"},
            id="cli-build-number-only",
        ),
    ],
)
def test_version_and_build_number(cli_args, pyproject, expected):
    assert flutter_version_args(cli_args, pyproject) == expected


def test_template_default_version():
    """Without a version or build number, the app gets the template's."""
    pubspec = (
        Path(__file__).parents[3]
        / "templates"
        / "build"
        / "{{cookiecutter.out_dir}}"
        / "pubspec.yaml"
    )
    assert yaml.safe_load(pubspec.read_text())["version"] == "1.0.0+1"
