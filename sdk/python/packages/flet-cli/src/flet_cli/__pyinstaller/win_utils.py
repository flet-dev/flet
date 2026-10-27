import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Optional

import pefile
from packaging import version
from PyInstaller.compat import win32api
from PyInstaller.utils.win32 import versioninfo
from PyInstaller.utils.win32.icon import IconFile, normalize_icon_type

import flet_cli.__pyinstaller.config as hook_config


def update_flet_view_icon(exe_path: str, icon_path: str) -> None:
    """
    Replace icon resources in a Windows executable.

    When the icon is an `.ico` file, or an image converted to one, it is also
    written to `data/app_icon.ico` next to the executable: Windows shows the icon
    of an app without package identity on its notifications from an image file,
    not from the executable's resources.

    Args:
        exe_path: Path to target executable file.
        icon_path: Path to source icon file or executable resource.
    """

    hook_config.log_progress("Updating Flet View icon", exe_path, icon_path)

    RT_ICON = 3
    RT_GROUP_ICON = 14

    normalized_icon_path = normalize_icon_type(
        icon_path, ("exe", "ico"), "ico", os.getcwd()
    )
    icon = IconFile(normalized_icon_path)
    hook_config.log_progress("Copying icons from", normalized_icon_path)

    hdst = win32api.BeginUpdateResource(exe_path, 0)

    iconid = 1
    # Each step in the following enumerate() will instantiate an IconFile object,
    # as a result of deferred execution of the map() above.
    i = 101
    data = icon.grp_icon_dir()
    data = data + icon.grp_icondir_entries(iconid)
    win32api.UpdateResource(hdst, RT_GROUP_ICON, i, data, 1033)
    hook_config.log_progress(
        f"Writing RT_GROUP_ICON {i} resource with {len(data)} bytes"
    )
    for data in icon.images:
        win32api.UpdateResource(hdst, RT_ICON, iconid, data, 1033)
        hook_config.log_progress(
            f"Writing RT_ICON {iconid} resource with {len(data)} bytes"
        )
        iconid = iconid + 1

    win32api.EndUpdateResource(hdst, 0)

    # Copy the icon only when normalize_icon_type() produced an .ico file.
    if Path(normalized_icon_path).suffix.lower() == ".ico":
        icon_file = Path(exe_path).parent / "data" / "app_icon.ico"
        icon_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(normalized_icon_path, icon_file)
        hook_config.log_progress("Writing", icon_file)


def update_flet_view_version_info(
    exe_path: str,
    product_name: Optional[str],
    file_description: Optional[str],
    product_version: Optional[str],
    file_version: Optional[str],
    company_name: Optional[str],
    copyright: Optional[str],
) -> str:
    """
    Update VERSIONINFO resources in a Windows executable.

    Args:
        exe_path: Path to target executable file.
        product_name: Optional product name value.
        file_description: Optional file description value.
        product_version: Optional product version string.
        file_version: Optional file version string (`n.n.n.n` expected).
        company_name: Optional company name value.
        copyright: Optional legal copyright value.

    Returns:
        Path to a temporary text file containing serialized version info.
    """

    hook_config.log_progress("Updating Flet View version info", exe_path)

    # load versioninfo from exe
    if versioninfo.read_version_info_from_executable:
        vs = versioninfo.read_version_info_from_executable(exe_path)
    else:
        vs = versioninfo.decode(exe_path)

    # update file version
    if file_version:
        pv = version.parse(file_version)
        filevers = (pv.major, pv.minor, pv.micro, 0)
        vs.ffi.fileVersionMS = (filevers[0] << 16) | (filevers[1] & 0xFFFF)
        vs.ffi.fileVersionLS = (filevers[2] << 16) | (filevers[3] & 0xFFFF)

    # update string props
    for k in vs.kids[0].kids[0].kids:
        if k.name == "ProductName":
            k.val = product_name if product_name else ""
        elif k.name == "FileDescription":
            k.val = file_description if file_description else ""
        if k.name == "ProductVersion":
            k.val = product_version if product_version else ""
        if k.name == "FileVersion" and file_version:
            k.val = file_version if file_version else ""
        if k.name == "CompanyName":
            k.val = company_name if company_name else ""
        if k.name == "LegalCopyright":
            k.val = copyright if copyright else ""

    version_info_path = str(Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4())))
    with open(version_info_path, "w", encoding="utf-8") as f:
        f.write(str(vs))

    # Remember overlay
    pe = pefile.PE(exe_path, fast_load=True)
    overlay_before = pe.get_overlay()
    pe.close()

    hdst = win32api.BeginUpdateResource(exe_path, 0)
    win32api.UpdateResource(
        hdst, pefile.RESOURCE_TYPE["RT_VERSION"], 1, vs.toRaw(), 1033
    )
    win32api.EndUpdateResource(hdst, 0)

    if overlay_before:
        # Check if the overlay is still present
        pe = pefile.PE(exe_path, fast_load=True)
        overlay_after = pe.get_overlay()
        pe.close()

        # If the update removed the overlay data, re-append it
        if not overlay_after:
            with open(exe_path, "ab", encoding="utf-8") as exef:
                exef.write(overlay_before)

    return version_info_path
