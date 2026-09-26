"""Render the supported Python versions table straight from flet-cli.

The versions come from `flet_cli.utils.python_versions`, which reads the
python-build manifest that `flet build` and `flet publish` pin. Generating the
docs table from it keeps the two from drifting apart.
"""

import os

from packaging.version import Version


def python_versions_table(web: bool = False) -> str:
    """
    Render the supported Python versions as a Markdown table, newest first.

    When `FLET_DOCS_FAST` is set and the manifest can't be loaded (for example,
    offline with an empty cache), a warning is rendered instead of failing.

    Args:
        web: Render only the Python and Pyodide columns.

    Returns:
        A Markdown table with one row per supported Python version.
    """
    from flet_cli.utils.python_versions import (
        get_default_python_version,
        get_supported_python_versions,
    )

    try:
        releases = get_supported_python_versions()
        default = get_default_python_version()
    except RuntimeError:
        if not os.environ.get("FLET_DOCS_FAST"):
            raise
        return "\n".join(
            [
                ":::warning",
                "The Python versions table is skipped while `FLET_DOCS_FAST` is "
                "set and the python-build manifest can't be loaded.",
                "Run the full docs build to refresh it.",
                ":::",
                "",
            ]
        )

    releases = sorted(releases, key=lambda r: Version(r.short), reverse=True)

    if web:
        rows = ["| Python | Pyodide |", "| ------ | ------- |"]
        rows += [f"| {r.short} | {r.pyodide} |" for r in releases]
    else:
        rows = [
            "| Short | CPython runtime | Pyodide (web) | Status |",
            "| ----- | --------------- | ------------- | ------ |",
        ]
        for r in releases:
            if r.short == default:
                status = "default"
            elif r.prerelease:
                status = "pre-release"
            else:
                status = "stable"
            rows.append(f"| {r.short} | {r.standalone} | {r.pyodide} | {status} |")
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    print(python_versions_table())
