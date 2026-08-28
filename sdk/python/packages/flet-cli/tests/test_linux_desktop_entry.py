"""Rendering of the Linux desktop entry template (issue #2269).

The build template ships `linux/{{cookiecutter.bundle_id}}.desktop`, installed
into the bundle at `share/applications/` so Wayland desktops can resolve the
app's launcher name and icon. `Exec` and `Categories` have escaping rules of
their own and are prepared by `flet build` (see `escape_desktop_exec` and
`escape_desktop_categories`); the rest is escaped in the template.
"""

from pathlib import Path

import pytest
from jinja2 import Environment

from flet_cli.commands.build_base import BaseBuildCommand

TEMPLATE_PATH = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
    / "linux"
    / "{{cookiecutter.bundle_id}}.desktop"
)


def _render(**overrides: str) -> str:
    """
    Render the desktop entry template with a cookiecutter-like context.

    Args:
        overrides: cookiecutter context values to override.

    Returns:
        The rendered desktop entry text.
    """
    context = {
        "product_name": "My App",
        "project_description": "",
        "desktop_exec": "my_app",
        "linux_categories": "Utility;",
        "bundle_id": "com.example.my_app",
        **overrides,
    }
    env = Environment(keep_trailing_newline=True)
    return env.from_string(TEMPLATE_PATH.read_text()).render(cookiecutter=context)


def test_desktop_entry_fields():
    content = _render(project_description="Does great things.")
    assert "[Desktop Entry]" in content
    assert "Type=Application" in content
    assert "Name=My App" in content
    assert "Comment=Does great things." in content
    # Exec is quoted: artifact names may contain spaces, and an unquoted
    # value would word-split into the wrong program.
    assert 'Exec="my_app" %U' in content
    # Icon and StartupWMClass must both equal the bundle id: the runner sets
    # its program name to the bundle id, and Wayland/X11 match the running app
    # to this entry (and its themed icon) through that name.
    assert "Icon=com.example.my_app" in content
    assert "StartupWMClass=com.example.my_app" in content
    assert "Categories=Utility;" in content
    assert "{{" not in content and "{%" not in content


def test_comment_omitted_without_description():
    content = _render(project_description="")
    assert "Comment=" not in content
    # The conditional must not leave a blank line behind.
    assert 'Name=My App\nExec="my_app" %U' in content


def test_multiline_description_flattened():
    # A newline inside Comment= would make the entry fail
    # desktop-file-validate and get ignored by the desktop environment.
    content = _render(project_description="Line one.\nLine two.")
    assert "Comment=Line one. Line two." in content


def test_control_characters_flattened_in_name_and_comment():
    content = _render(
        product_name="My\tApp\nName", project_description="Tabbed\tdescription"
    )
    assert "Name=My App Name" in content
    assert "Comment=Tabbed description" in content


def test_backslashes_escaped():
    # Desktop entry values use backslash escape sequences, so a literal
    # backslash must be doubled.
    content = _render(project_description=r"Uses C:\path\now")
    assert r"Comment=Uses C:\\path\\now" in content


def test_prepared_values_are_interpolated_verbatim():
    # Exec and Categories arrive already escaped; the template must not
    # escape them a second time.
    content = _render(desktop_exec=r"weird\\\"name", linux_categories="Game;Fun;")
    assert 'Exec="weird\\\\\\"name" %U' in content
    assert "Categories=Game;Fun;" in content


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("my_app", "my_app"),
        ("my app", "my app"),
        # " ` $ \ are reserved inside the quoted Exec value; each gets a
        # backslash, and every backslash is then doubled for the entry file.
        ('mid"dle', 'mid\\\\"dle'),
        ("my$app", "my\\\\$app"),
        ("a\\b", "a\\\\\\\\b"),
        ("tick`s", "tick\\\\`s"),
    ],
)
def test_escape_desktop_exec(raw, expected):
    assert BaseBuildCommand.escape_desktop_exec(raw) == expected


def test_escape_desktop_categories():
    escape = BaseBuildCommand.escape_desktop_categories
    assert escape(["Game", "Education"]) == "Game;Education;"
    assert escape("Development") == "Development;"
    # A literal semicolon would split one category into two.
    assert escape(["Ut;ility"]) == "Ut\\;ility;"
    assert escape(["back\\slash"]) == "back\\\\slash;"
    # Blanks are dropped, and an all-blank list keeps the default.
    assert escape(["Game", "  ", ""]) == "Game;"
    assert escape([]) == "Utility;"


@pytest.mark.parametrize("bad", [5, None, ["ok", 7], {"a": 1}])
def test_escape_desktop_categories_rejects_non_strings(bad):
    # A bad pyproject value must surface as a clear error rather than a
    # jinja TypeError that wipes the build directory.
    with pytest.raises(ValueError):
        BaseBuildCommand.escape_desktop_categories(bad)
