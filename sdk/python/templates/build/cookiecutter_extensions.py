"""
Jinja extensions of the `flet build` template.

Cookiecutter loads the extensions listed in `_extensions` of `cookiecutter.json`
into the environment that renders the template's files.
"""

from typing import Any, Optional

from jinja2 import Environment, pass_context
from jinja2.ext import Extension
from jinja2.runtime import Context


class FletJinjaExtension(Extension):
    """
    Gives the template's files access to the app's `pyproject.toml`.

    Adds the global `get_pyproject()` function, for the settings that the template
    reads itself instead of receiving them, resolved, from `flet build` in
    `cookiecutter._options`.
    """

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.globals["get_pyproject"] = self.get_pyproject

    @pass_context
    def get_pyproject(self, context: Context, setting: Optional[str]) -> Any:
        """
        Returns a value of the app's `pyproject.toml`.

        `flet build` passes the parsed `pyproject.toml` in `cookiecutter._pyproject`.

        Args:
            context: The template's rendering context, supplied by Jinja.
            setting: Dotted path of the value, such as
                `"tool.flet.android.min_sdk_version"`. An empty path returns the
                whole `pyproject.toml`.

        Returns:
            The value at `setting`, or `None` if any part of the path is missing.
        """
        pyproject = context.get("cookiecutter", {}).get("_pyproject", {})

        if not setting:
            return pyproject

        d = pyproject
        for k in setting.split("."):
            d = d.get(k)
            if d is None:
                return None
        return d
