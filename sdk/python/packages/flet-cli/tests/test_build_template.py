"""Invariants of the `flet build` cookiecutter template itself."""

import json
import re
from pathlib import Path
from typing import Any

import pytest
import yaml
from jinja2 import Environment, StrictUndefined

from flet_cli.commands.build_base import BaseBuildCommand

BUILD_TEMPLATE_DIR = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
)
TEMPLATE_PUBSPEC = BUILD_TEMPLATE_DIR / "pubspec.yaml"


def _render_template(path: Path, **context: Any) -> str:
    """
    Render a build-template file the way cookiecutter would.

    Args:
        path: Template file to render.
        context: Values exposed to the template as `cookiecutter.*`.

    Returns:
        The rendered file content.
    """

    env = Environment(keep_trailing_newline=True, undefined=StrictUndefined)
    return env.from_string(path.read_text()).render(cookiecutter=context)


class TestBuildTemplateContract:
    """
    Invariants of the build template itself, independent of any platform.

    Both bugs covered here shipped at least once:

    * a context key the templates read but `cookiecutter.json` never declared
      — cookiecutter drops such keys, so the value silently rendered empty,
      which is why `--description` reached nothing for as long as it did;
    * a template that stopped parsing while *unrendered*, which breaks the CI
      step that patches its dependency versions in place before any build.
    """

    @staticmethod
    def _declared_keys() -> set:
        """The context keys `cookiecutter.json` declares."""
        with open(BUILD_TEMPLATE_DIR.parent / "cookiecutter.json") as f:
            return set(json.load(f))

    @staticmethod
    def _referenced_keys() -> dict:
        """Every `cookiecutter.<key>` referenced by a template, by file."""
        found = {}
        for path in BUILD_TEMPLATE_DIR.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue  # binary asset, e.g. images/icon.png
            # The negative lookahead skips method calls such as
            # `cookiecutter.items()` in .vars, which are not context keys.
            for key in re.findall(
                r"cookiecutter\.([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*\()", text
            ):
                found.setdefault(key, set()).add(path.name)
        return found

    def test_every_referenced_key_is_declared(self):
        """A key a template reads but `cookiecutter.json` omits is dropped from
        the context, so the template silently renders it empty."""
        declared = self._declared_keys()
        undeclared = {
            key: sorted(files)
            for key, files in self._referenced_keys().items()
            if key not in declared
        }
        assert not undeclared, f"referenced but not declared: {undeclared}"

    def test_pubspec_parses_while_unrendered(self):
        """`.github/scripts/patch_pubspec_version.py` loads this file as YAML
        before cookiecutter ever runs, so an unquoted `{{` — which YAML reads
        as a flow mapping — fails the release build."""
        with open(TEMPLATE_PUBSPEC) as f:
            assert yaml.safe_load(f), "template pubspec.yaml must parse as YAML"

    @pytest.mark.parametrize(
        "description",
        ["plain", "Bob's tool", 'has "quotes"', "back\\slash", "multi\nline\ttab"],
    )
    def test_rendered_pubspec_is_valid_yaml(self, description):
        """A description of any shape must still render a parseable pubspec."""
        rendered = _render_template(
            TEMPLATE_PUBSPEC,
            project_name="test_app",
            pubspec_description=BaseBuildCommand.escape_single_quoted_yaml(description),
        )
        parsed = yaml.safe_load(rendered)
        assert parsed["description"] == re.sub(r"[\x00-\x1f]", " ", description)

    @pytest.mark.parametrize("product", ["Flet Studio", 'My "App"', "back\\slash"])
    def test_manifest_names_come_from_product(self, product):
        """iOS labels an installed PWA with the manifest's `short_name`, which
        was the project name slug (`client`) instead of the product name."""
        with open(BUILD_TEMPLATE_DIR.parent / "cookiecutter.json") as f:
            default_short_name = json.load(f)["pwa_short_name"]
        context = {
            "project_name": "client",
            "product_name": product,
            "pwa_background_color": "#FFFFFF",
            "pwa_theme_color": "#FF005F",
            "project_description": "",
        }
        context["pwa_short_name"] = (
            Environment().from_string(default_short_name).render(cookiecutter=context)
        )
        manifest = json.loads(
            _render_template(BUILD_TEMPLATE_DIR / "web" / "manifest.json", **context)
        )
        assert manifest["name"] == product
        assert manifest["short_name"] == product

    def test_manifest_short_name_override(self):
        rendered = _render_template(
            BUILD_TEMPLATE_DIR / "web" / "manifest.json",
            product_name="Flet Studio",
            pwa_short_name="Studio",
            pwa_background_color="#FFFFFF",
            pwa_theme_color="#FF005F",
            project_description="",
        )
        manifest = json.loads(rendered)
        assert manifest["name"] == "Flet Studio"
        assert manifest["short_name"] == "Studio"
