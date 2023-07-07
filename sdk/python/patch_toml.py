import os
import pathlib
import sys

import tomlkit

if len(sys.argv) < 3:
    print("Specify toml file and version to patch")
    sys.exit(1)

current_dir = pathlib.Path(os.getcwd())
toml_path = current_dir.joinpath(current_dir, sys.argv[1])
ver = sys.argv[2]
print(f"Patching TOML file {toml_path} to {ver}")

# read
with open(toml_path, "r") as f:
    t = tomlkit.parse(f.read())

# patch version
t["tool"]["poetry"]["version"] = ver

# patch dependencies
deps = t["tool"]["poetry"]["dependencies"]
if deps.get("flet-core"):
    deps["flet-core"] = ver
if deps.get("flet-runtime"):
    deps["flet-runtime"] = ver

# save
with open(toml_path, "w") as f:
    f.write(tomlkit.dumps(t))
