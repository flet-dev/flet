import os
import plistlib
import shutil
import subprocess
import tarfile
from pathlib import Path

from flet.utils import safe_tar_extractall
from PyInstaller.building.icon import normalize_icon_type


def unpack_app_bundle(tar_path):
    bin_dir = str(Path(tar_path).parent)

    with tarfile.open(tar_path, "r:gz") as tar_arch:
        safe_tar_extractall(tar_arch, bin_dir)
    os.remove(tar_path)

    return os.path.join(bin_dir, "Flet.app")


def update_flet_view_icon(app_path, icon_path):
    print("Updating Flet View icon", app_path, icon_path)

    icon_file = "AppIcon.icns"

    # normalize icon
    normalized_icon_path = normalize_icon_type(
        icon_path, ("icns",), "icns", os.getcwd()
    )

    # patch icon
    print("Copying icons from", normalized_icon_path)
    shutil.copy(
        normalized_icon_path,
        os.path.join(app_path, "Contents", "Resources", icon_file),
    )

    # update icon file name
    pl = __load_info_plist(app_path)
    pl["CFBundleIconFile"] = icon_file
    del pl["CFBundleIconName"]
    __save_info_plist(app_path, pl)


def update_flet_view_version_info(
    app_path,
    bundle_id,
    product_name,
    product_version,
    copyright,
):
    print("Updating Flet View plist", app_path)

    pl = __load_info_plist(app_path)

    if bundle_id:
        pl["CFBundleIdentifier"] = bundle_id
    if product_name:
        pl["CFBundleName"] = product_name
        pl["CFBundleDisplayName"] = product_name

        # rename app bundle
        new_app_path = os.path.join(Path(app_path).parent, f"{product_name}.app")
        os.rename(app_path, new_app_path)
        app_path = new_app_path
    if product_version:
        pl["CFBundleShortVersionString"] = product_version
    if copyright:
        pl["NSHumanReadableCopyright"] = copyright

    __save_info_plist(app_path, pl)

    return app_path


def assemble_app_bundle(app_path, tar_path):
    # sign app bundle
    print(f"Signing file {app_path}")
    cmd_args = [
        "codesign",
        "-s",
        "-",
        "--force",
        "--all-architectures",
        "--timestamp",
        "--deep",
        app_path,
    ]
    p = subprocess.run(
        cmd_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    if p.returncode:
        raise SystemError(
            f"codesign command ({cmd_args}) failed with error code {p.returncode}!\noutput: {p.stdout}"
        )

    # pack tar
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(app_path, arcname=os.path.basename(app_path))

    # cleanup
    shutil.rmtree(app_path, ignore_errors=True)


def __load_info_plist(app_path):
    with open(__get_plist_path(app_path), "rb") as fp:
        return plistlib.load(fp)


def __save_info_plist(app_path, pl):
    with open(__get_plist_path(app_path), "wb") as fp:
        plistlib.dump(pl, fp)


def __get_plist_path(app_path):
    return os.path.join(app_path, "Contents", "Info.plist")
