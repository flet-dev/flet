import os
import shutil
import tarfile
from pathlib import Path

from PyInstaller.building.icon import normalize_icon_type

from flet.utils import safe_tar_extractall


def update_flet_view_icon(tar_path, icon_path):
    print("Updating Flet View icon", tar_path, icon_path)

    bin_dir = str(Path(tar_path).parent)

    # normalize icon
    normalized_icon_path = normalize_icon_type(
        icon_path, ("icns",), "icns", os.getcwd()
    )

    with tarfile.open(tar_path, "r:gz") as tar_arch:
        safe_tar_extractall(tar_arch, bin_dir)
    os.remove(tar_path)

    app_path = os.path.join(bin_dir, "Flet.app")

    # patch icon
    print("Copying icons from %s", normalized_icon_path)
    shutil.copy(
        normalized_icon_path,
        os.path.join(app_path, "Contents", "Resources", "AppIcon.icns"),
    )

    # pack tar
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(app_path, arcname=os.path.basename(app_path))

    # cleanup
    shutil.rmtree(app_path, ignore_errors=True)
