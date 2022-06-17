import glob
import hashlib
import io
import json
import os
import pathlib
import shutil
import stat
import sys
import tarfile
import urllib.request
import zipfile
from base64 import urlsafe_b64encode

fletd_job_name = "Build Fletd"

build_jobs = {}

packages = {
    "Windows amd64": {
        "fletd_asset": "windows_amd64",
        "fletd_exec": "fletd.exe",
        "flet_client_job": "Build Flet for Windows",
        "flet_client_artifact": "flet_windows",
        "flet_client_filename": "flet.zip",
        "wheel_tags": ["py3-none-win_amd64"],
        "file_suffix": "py3-none-win_amd64",
    },
    "Windows x86": {
        "fletd_asset": "windows_386",
        "fletd_exec": "fletd.exe",
        "flet_client_job": "Build Flet for Windows",
        "flet_client_artifact": "flet_windows",
        "flet_client_filename": "flet.zip",
        "wheel_tags": ["py3-none-win32"],
        "file_suffix": "py3-none-win32",
    },
    "Linux amd64 (Alpine)": {
        "fletd_asset": "linux_amd64",
        "fletd_exec": "fletd",
        "wheel_tags": ["py3-none-musllinux_1_2_x86_64"],
        "file_suffix": "py3-none-musllinux_1_2_x86_64",
    },
    "Linux amd64": {
        "fletd_asset": "linux_amd64",
        "fletd_exec": "fletd",
        "flet_client_job": "Build Flet for Linux",
        "flet_client_artifact": "flet_linux",
        "flet_client_filename": "flet.tar.gz",
        "wheel_tags": [
            "py3-none-manylinux_2_17_x86_64",
            "py3-none-manylinux2014_x86_64",
        ],
        "file_suffix": "py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64",
    },
    "Linux arm64": {
        "fletd_asset": "linux_arm64",
        "fletd_exec": "fletd",
        "wheel_tags": [
            "py3-none-manylinux_2_17_aarch64",
            "py3-none-manylinux2014_aarch64",
        ],
        "file_suffix": "py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64",
    },
    "Linux arm": {
        "fletd_asset": "linux_arm_7",
        "fletd_exec": "fletd",
        "wheel_tags": [
            "py3-none-manylinux_2_17_armv7l",
            "py3-none-manylinux2014_armv7l",
        ],
        "file_suffix": "py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l",
    },
    "macOS amd64": {
        "fletd_asset": "darwin_amd64",
        "fletd_exec": "fletd",
        "flet_client_job": "Build Flet for macOS",
        "flet_client_artifact": "flet_macos",
        "flet_client_filename": "flet.tar.gz",
        "wheel_tags": ["py3-none-macosx_10_14_x86_64"],
        "file_suffix": "py3-none-macosx_10_14_x86_64",
    },
    "macOS arm64": {
        "fletd_asset": "darwin_arm64",
        "fletd_exec": "fletd",
        "flet_client_job": "Build Flet for macOS",
        "flet_client_artifact": "flet_macos",
        "flet_client_filename": "flet.tar.gz",
        "wheel_tags": ["py3-none-macosx_12_0_arm64"],
        "file_suffix": "py3-none-macosx_12_0_arm64",
    },
}


def unpack_zip(zip_path, dest_dir):
    zf = zipfile.ZipFile(zip_path)
    zf.extractall(path=dest_dir)


def download_flet_server(jobId, asset, exec_filename, dest_file):
    fletd_url = f"https://ci.appveyor.com/api/buildjobs/{jobId}/artifacts/server%2Fdist%2Ffletd_{asset}%2F{exec_filename}"
    print(f"Downloading {fletd_url}...")
    urllib.request.urlretrieve(fletd_url, dest_file)
    st = os.stat(dest_file)
    os.chmod(dest_file, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def download_artifact_by_name(jobId, artifact_name, dest_file):
    url = f"https://ci.appveyor.com/api/buildjobs/{jobId}/artifacts"
    print(f"Fetching build job artifacts at {url}")
    req = urllib.request.Request(url)
    req.add_header("Content-type", "application/json")
    artifacts = json.loads(urllib.request.urlopen(req).read().decode())
    for artifact in artifacts:
        if artifact["name"] == artifact_name:
            artifact_filename = artifact["fileName"]
            flet_url = f"https://ci.appveyor.com/api/buildjobs/{jobId}/artifacts/{artifact_filename}"
            print(f"Downloading {flet_url}...")
            urllib.request.urlretrieve(flet_url, dest_file)
            return


def get_flet_server_job_ids():
    account_name = os.environ.get("APPVEYOR_ACCOUNT_NAME")
    project_slug = os.environ.get("APPVEYOR_PROJECT_SLUG")
    build_id = os.environ.get("APPVEYOR_BUILD_ID")
    url = f"https://ci.appveyor.com/api/projects/{account_name}/{project_slug}/builds/{build_id}"
    print(f"Fetching build details at {url}")
    req = urllib.request.Request(url)
    req.add_header("Content-type", "application/json")
    project = json.loads(urllib.request.urlopen(req).read().decode())
    jobId = None
    for job in project["build"]["jobs"]:
        build_jobs[job["name"]] = job["jobId"]


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


def rehash_record_lines(root_dir):
    lines = []
    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in sorted(files):
            abs_filename = os.path.join(root, name)
            rel_filename = abs_filename[len(root_dir) + 1 :]
            h, l = rehash(abs_filename)
            if rel_filename.endswith("/RECORD"):
                h = l = ""
            lines.append(f"{rel_filename},{h},{l}\n")
    return lines


current_dir = pathlib.Path(os.getcwd())
print("current_dir", current_dir)

whl_files = glob.glob(str(current_dir.joinpath("dist", "*.whl")))
if len(whl_files) == 0:
    print("No .whl files found. Run 'pdm build' first.")
    sys.exit(1)

orig_whl = whl_files[0]

package_version = os.path.basename(orig_whl).split("-")[1]
get_flet_server_job_ids()

print("package_version", package_version)
print("flet_server_jobId", build_jobs[fletd_job_name])

for name, package in packages.items():
    print(f"Building {name}...")

    print("Unpacking original wheel file...")
    unpacked_whl = current_dir.joinpath("dist", "wheel")
    unpacked_whl.mkdir(exist_ok=True)
    unpack_zip(orig_whl, unpacked_whl)

    # read original WHEEL file omitting tags
    wheel_path = str(
        unpacked_whl.joinpath(f"flet-{package_version}.dist-info", "WHEEL")
    )
    wheel_lines = []

    with open(wheel_path, "r") as f:
        for line in f.readlines():
            if not "Tag: " in line:
                wheel_lines.append(line)

    # print(wheel_lines)

    # create "bin" directory
    bin_path = unpacked_whl.joinpath("flet", "bin")
    bin_path.mkdir(exist_ok=True)

    # download Fletd
    asset = package["fletd_asset"]
    exec_filename = package["fletd_exec"]
    exec_path = str(bin_path.joinpath(exec_filename))
    download_flet_server(build_jobs[fletd_job_name], asset, exec_filename, exec_path)

    # download Flet client
    flet_client_job = package.get("flet_client_job")
    flet_client_artifact = package.get("flet_client_artifact")
    flet_client_filename = package.get("flet_client_filename")
    if flet_client_job:
        client_arch_path = str(bin_path.joinpath(flet_client_filename))
        download_artifact_by_name(
            build_jobs[flet_client_job], flet_client_artifact, client_arch_path
        )

        # unpack zip only; tar.gz stays as is and unpacked during runtime
        if flet_client_filename.endswith(".zip"):
            with zipfile.ZipFile(client_arch_path, "r") as zip_arch:
                zip_arch.extractall(bin_path)
            os.remove(client_arch_path)

    # update WHEEL file
    for tag in package["wheel_tags"]:
        wheel_lines.append(f"Tag: {tag}\n")

    # save WHEEL
    with open(wheel_path, "w") as f:
        f.writelines(wheel_lines)

    # update and save RECORD
    record_lines = rehash_record_lines(str(unpacked_whl))
    record_path = str(
        unpacked_whl.joinpath(f"flet-{package_version}.dist-info", "RECORD")
    )
    with open(record_path, "w") as f:
        f.writelines(record_lines)

    # zip
    suffix = package["file_suffix"]
    zip_filename = current_dir.joinpath("dist", f"flet-{package_version}-{suffix}")
    shutil.make_archive(zip_filename, "zip", unpacked_whl)
    os.rename(f"{zip_filename}.zip", f"{zip_filename}.whl")

    # cleanup
    shutil.rmtree(str(unpacked_whl))
