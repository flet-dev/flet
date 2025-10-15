import sys
from pathlib import Path
from typing import Any, Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def load_pyproject_toml(project_dir: Path):
    pyproject_toml: Optional[dict[str, Any]] = {}
    pyproject_toml_file = project_dir.joinpath("pyproject.toml")
    if pyproject_toml_file.exists():
        with pyproject_toml_file.open("r", encoding="utf-8") as f:
            pyproject_toml = tomllib.loads(f.read())

    def get_pyproject(setting: Optional[str] = None):
        if not setting:
            return pyproject_toml

        d = pyproject_toml
        for k in setting.split("."):
            d = d.get(k)
            if d is None:
                return None
        return d

    return get_pyproject
