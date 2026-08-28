"""Write the fixture app's pyproject.toml.

TEMPORARY -- part of the issue #2269 Linux icon verification harness.

The editable `[tool.uv.sources]` paths are load-bearing: `flet build` only
uses the in-repo build template (rather than downloading the released
`flet-build-template.zip`) when flet-cli is imported from the source tree, so
without them the run would test the released template instead of this branch.

Usage: write_pyproject.py <artifact_name> <description_file> <repo_root>
"""

import sys
import tomllib


def main() -> int:
    artifact, description_file, repo_root = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(description_file, encoding="utf-8") as f:
        description = f.read()

    # TOML basic strings escape exactly the characters this fixture carries.
    escaped = (
        description.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    packages = f"{repo_root}/sdk/python/packages"

    pyproject = f"""[project]
name = "flet-icon-test"
version = "1.0.0"
description = "{escaped}"
requires-python = ">=3.10"
dependencies = ["flet"]

[tool.flet]
product = "Flet Icon Test"
company = "Flet"
org = "com.flet"
bundle_id = "com.flet.flet-icon-test"
artifact = "{artifact}"

[tool.flet.app]
path = "src"

[tool.flet.linux]
categories = ["Development", "Utility"]

[dependency-groups]
dev = ["flet-cli"]

[tool.uv.sources]
flet = {{ path = "{packages}/flet", editable = true }}
flet-cli = {{ path = "{packages}/flet-cli", editable = true }}
"""

    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject)

    # Fail here rather than deep inside the build.
    with open("pyproject.toml", "rb") as f:
        parsed = tomllib.load(f)
    assert parsed["project"]["description"] == description, "description round-trip"
    print(f"fixture pyproject.toml written (artifact={artifact!r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
