import os
import tempfile
import uuid
from pathlib import Path

import pefile
from packaging import version
from PyInstaller.building.icon import normalize_icon_type
from PyInstaller.compat import win32api
from PyInstaller.utils.win32 import versioninfo
from PyInstaller.utils.win32.icon import IconFile, normalize_icon_type


def update_flet_view_icon(exe_path, icon_path):
    print("Updating Flet View icon", exe_path, icon_path)

    RT_ICON = 3
    RT_GROUP_ICON = 14

    normalized_icon_path = normalize_icon_type(
        icon_path, ("exe", "ico"), "ico", os.getcwd()
    )
    icon = IconFile(normalized_icon_path)
    print("Copying icons from", normalized_icon_path)

    hdst = win32api.BeginUpdateResource(exe_path, 0)

    iconid = 1
    # Each step in the following enumerate() will instantiate an IconFile object, as a result of deferred execution
    # of the map() above.
    i = 101
    data = icon.grp_icon_dir()
    data = data + icon.grp_icondir_entries(iconid)
    win32api.UpdateResource(hdst, RT_GROUP_ICON, i, data, 1033)
    print("Writing RT_GROUP_ICON %d resource with %d bytes", i, len(data))
    for data in icon.images:
        win32api.UpdateResource(hdst, RT_ICON, iconid, data, 1033)
        print("Writing RT_ICON %d resource with %d bytes", iconid, len(data))
        iconid = iconid + 1

    win32api.EndUpdateResource(hdst, 0)


def update_flet_view_version_info(
    exe_path,
    product_name,
    file_description,
    product_version,
    file_version,
    company_name,
    copyright,
):
    print("Updating Flet View version info", exe_path)

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
