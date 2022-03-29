import glob
import hashlib
import io
import os
import pathlib
import shutil
import stat
import sys
import urllib.request
import zipfile
from base64 import urlsafe_b64encode

packages = {
    "Windows amd64": {
        "asset": "windows-amd64.exe",
        "exec": "flet.exe",
        "wheel_tags": ["py3-none-win_amd64"],
        "file_suffix": "py3-none-win_amd64",
    },
    "Linux amd64": {
        "asset": "linux-amd64",
        "exec": "flet",
        "wheel_tags": [
            "py3-none-manylinux_2_17_x86_64",
            "py3-none-manylinux2014_x86_64",
        ],
        "file_suffix": "py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64",
    },
    "Linux arm64": {
        "asset": "linux-arm64",
        "exec": "flet",
        "wheel_tags": [
            "py3-none-manylinux_2_17_aarch64",
            "py3-none-manylinux2014_aarch64",
        ],
        "file_suffix": "py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64",
    },
    "Linux arm": {
        "asset": "linux-arm",
        "exec": "flet",
        "wheel_tags": [
            "py3-none-manylinux_2_17_armv7l",
            "py3-none-manylinux2014_armv7l",
        ],
        "file_suffix": "py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l",
    },
    "macOS amd64": {
        "asset": "darwin-amd64",
        "exec": "flet",
        "wheel_tags": ["py3-none-macosx_10_14_x86_64"],
        "file_suffix": "py3-none-macosx_10_14_x86_64",
    },
    "macOS arm64": {
        "asset": "darwin-arm64",
        "exec": "flet",
        "wheel_tags": ["py3-none-macosx_12_0_arm64"],
        "file_suffix": "py3-none-macosx_12_0_arm64",
    },
}


def unpack_zip(zip_path, dest_dir):
    zf = zipfile.ZipFile(zip_path)
    zf.extractall(path=dest_dir)


def download_pglet(version, suffix, dest_file):
    file_name = f"pglet-{version}-{suffix}"
    pglet_url = (
        f"https://github.com/pglet/pglet/releases/download/v{version}/{file_name}"
    )
    print(f"Downloading {pglet_url}...")
    urllib.request.urlretrieve(pglet_url, dest_file)
    st = os.stat(dest_file)
    os.chmod(dest_file, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def get_pglet_version(current_dir):
    constants_py = current_dir.joinpath("pglet", "constants.py")

    version_prefix = "PGLET_SERVER_VERSION"
    with open(constants_py) as yml:
        for line in yml:
            if version_prefix in line:
                return line.split("=")[1].strip().strip('"')
    raise f"{version_prefix} not found in constants.py"


def read_chunks(file, size=io.DEFAULT_BUFFER_SIZE):
    """Yield pieces of data from a file-like object until EOF."""
    while True:
        chunk = file.read(size)
        if not chunk:
            break
        yield chunk


def rehash(path, blocksize=1 << 20):
    """Return (hash, length) for path using hashlib.sha256()"""
    h = hashlib.sha256()
    length = 0
    with open(path, "rb") as f:
        for block in read_chunks(f, size=blocksize):
            length += len(block)
            h.update(block)
    digest = "sha256=" + urlsafe_b64encode(h.digest()).decode("latin1").rstrip("=")
    # unicode/str python2 issues
    return (digest, str(length))  # type: ignore


current_dir = pathlib.Path(os.getcwd())
print("current_dir", current_dir)

whl_files = glob.glob(str(current_dir.joinpath("dist", "*.whl")))
if len(whl_files) == 0:
    print("No .whl files found. Run 'pdm build' first.")
    sys.exit(1)

orig_whl = whl_files[0]

package_version = os.path.basename(orig_whl).split("-")[1]
pglet_version = get_pglet_version(current_dir)

print("package_version", package_version)
print("pglet_version", pglet_version)

for name, package in packages.items():
    print(f"Building {name}...")

    print("Unpacking original wheel file...")
    unpacked_whl = current_dir.joinpath("dist", "wheel")
    unpacked_whl.mkdir(exist_ok=True)
    unpack_zip(orig_whl, unpacked_whl)

    # read original WHEEL file omitting tags
    wheel_path = str(
        current_dir.joinpath(
            "dist", "wheel", f"pglet-{package_version}.dist-info", "WHEEL"
        )
    )
    wheel_lines = []

    with open(wheel_path, "r") as f:
        for line in f.readlines():
            if not "Tag: " in line:
                wheel_lines.append(line)

    # print(wheel_lines)

    # read original RECORD file
    record_path = str(
        current_dir.joinpath(
            "dist", "wheel", f"pglet-{package_version}.dist-info", "RECORD"
        )
    )
    record_lines = []

    with open(record_path, "r") as f:
        for line in f.readlines():
            if not "dist-info/WHEEL," in line:
                record_lines.append(line)

    # print(record_lines)

    # create "bin" directory
    bin_path = current_dir.joinpath("dist", "wheel", "pglet", "bin")
    bin_path.mkdir(exist_ok=True)
    asset = package["asset"]
    exec_filename = package["exec"]
    exec_path = str(bin_path.joinpath(exec_filename))
    download_pglet(pglet_version, asset, exec_path)

    # update RECORD
    h, l = rehash(exec_path)
    record_lines.insert(len(record_lines) - 3, f"pglet/bin/{exec_filename},{h},{l}\n")
    # for line in record_lines:
    #     print(line.strip())

    # update WHEEL file
    for tag in package["wheel_tags"]:
        wheel_lines.append(f"Tag: {tag}\n")

    # save WHEEL
    with open(wheel_path, "w") as f:
        f.writelines(wheel_lines)

    # update RECORD
    h, l = rehash(wheel_path)
    record_lines.insert(
        len(record_lines) - 3,
        f"pglet-{package_version}.dist-info/WHEEL,{h},{l}\n",
    )

    # save RECORD
    with open(record_path, "w") as f:
        f.writelines(record_lines)

    # zip
    suffix = package["file_suffix"]
    zip_filename = current_dir.joinpath("dist", f"pglet-{package_version}-{suffix}")
    shutil.make_archive(zip_filename, "zip", unpacked_whl)
    os.rename(f"{zip_filename}.zip", f"{zip_filename}.whl")

    # cleanup
    shutil.rmtree(str(unpacked_whl))
