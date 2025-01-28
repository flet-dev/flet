import os
import pathlib
import sys

import tomlkit

if len(sys.argv) < 2:
    print("Specify toml file and a new package name")
    sys.exit(1)

current_dir = pathlib.Path(os.getcwd())
toml_path = current_dir.joinpath(current_dir, sys.argv[1])
package_name = sys.argv[2]
print(f"Patching TOML file {toml_path} to {package_name}")

# read
with open(toml_path, "r") as f:
    t = tomlkit.parse(f.read())

# patch name
t["project"]["name"] = package_name

# save
with open(toml_path, "w") as f:
    f.write(tomlkit.dumps(t))
