import os
import pathlib
import sys

import yaml

if len(sys.argv) < 3:
    print("Specify pubspec.yaml file and version to patch")
    sys.exit(1)

current_dir = pathlib.Path(os.getcwd())
pubspec_path = current_dir.joinpath(current_dir, sys.argv[1])
ver = sys.argv[2]
print(f"Patching pubspec.yaml file {pubspec_path} with {ver}")

dependencies = [
    "flet",
]

with open(pubspec_path, "r") as f:
    data = yaml.safe_load(f)

    # patch version
    data["version"] = ver

    # patch dependencies
    for dep in data["dependencies"]:
        if dep in dependencies:
            data["dependencies"][dep] = f"^{ver}"
    # print(dep)
with open(pubspec_path, "w") as file:
    yaml.dump(data, file, sort_keys=False)
