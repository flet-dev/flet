"""Rendering of the Linux desktop entry template (issue #2269).

The build template ships `linux/{{cookiecutter.bundle_id}}.desktop`, installed
into the bundle at `share/applications/` so Wayland desktops can resolve the
app's launcher name and icon. These tests render that single template file
with jinja the way cookiecutter would.
"""

from pathlib import Path

import pytest
from jinja2 import Environment

TEMPLATE_PATH = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
    / "linux"
    / "{{cookiecutter.bundle_id}}.desktop"
)


def _render(**overrides):
    context = {
        "product_name": "My App",
        "project_description": "",
        "artifact_name": "my_app",
        "bundle_id": "com.example.my_app",
        **overrides,
    }
    return (
        Environment(keep_trailing_newline=True)
        .from_string(TEMPLATE_PATH.read_text())
        .render(cookiecutter=context)
    )


def test_desktop_entry_fields():
    content = _render(project_description="Does great things.")
    assert "[Desktop Entry]" in content
    assert "Type=Application" in content
    assert "Name=My App" in content
    assert "Comment=Does great things." in content
    assert "Exec=my_app %U" in content
    # Icon and StartupWMClass must both equal the bundle id: the runner sets
    # its program name to the bundle id, and Wayland/X11 match the running app
    # to this entry (and its themed icon) through that name.
    assert "Icon=com.example.my_app" in content
    assert "StartupWMClass=com.example.my_app" in content
    assert "{{" not in content and "{%" not in content


def test_comment_omitted_without_description():
    content = _render(project_description="")
    assert "Comment=" not in content
    # The conditional must not leave a blank line behind.
    assert "Name=My App\nExec=my_app %U" in content


@pytest.mark.parametrize("key", ["Name", "Exec", "Icon"])
def test_required_keys_present_by_default(key):
    assert f"{key}=" in _render()
