"""Rendering of the Linux desktop entry template (issue #2269).

The build template ships `linux/{{cookiecutter.bundle_id}}.desktop`, installed
into the bundle at `share/applications/` so Wayland desktops can resolve the
app's launcher name and icon. These tests render that single template file
with jinja the way cookiecutter would (including the `get_pyproject` global
registered by the template's `FletExtension`).
"""

from pathlib import Path
from typing import Any, Optional

from jinja2 import Environment

TEMPLATE_PATH = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
    / "linux"
    / "{{cookiecutter.bundle_id}}.desktop"
)


def _render(pyproject: Optional[dict] = None, **overrides: str) -> str:
    """
    Render the desktop entry template with a cookiecutter-like context.

    Args:
        pyproject: fake parsed pyproject.toml served through the
            `get_pyproject` jinja global.
        overrides: cookiecutter context values to override.

    Returns:
        The rendered desktop entry text.
    """
    context = {
        "product_name": "My App",
        "project_description": "",
        "artifact_name": "my_app",
        "bundle_id": "com.example.my_app",
        **overrides,
    }

    def get_pyproject(setting: str) -> Any:
        d: Any = pyproject or {}
        for key in setting.split("."):
            d = d.get(key)
            if d is None:
                return None
        return d

    env = Environment(keep_trailing_newline=True)
    env.globals["get_pyproject"] = get_pyproject
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


def test_exec_quotes_artifact_with_spaces():
    content = _render(artifact_name="My App")
    assert 'Exec="My App" %U' in content


def test_categories_from_pyproject_list():
    content = _render(
        pyproject={"tool": {"flet": {"linux": {"categories": ["Game", "Education"]}}}}
    )
    assert "Categories=Game;Education;" in content


def test_categories_from_pyproject_string():
    content = _render(
        pyproject={"tool": {"flet": {"linux": {"categories": "Development"}}}}
    )
    assert "Categories=Development;" in content
