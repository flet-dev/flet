"""
Windows taskbar identity helpers for the Flet desktop client.

The desktop client window belongs to `flet.exe`, so by default Windows
resolves its taskbar name, icon, jump list and pin target from that executable
("Flet description"). Setting a process-level AppUserModelID (see the
`FLET_APP_USER_MODEL_ID` handling in the flet-cli PyInstaller runtime hook)
only fixes taskbar *grouping* — the shell still has no idea what to display or
relaunch for that ID. This module stamps the `System.AppUserModel.*` window
properties on the client window so the shell shows the host app's name/icon
and taskbar pins relaunch the host executable.
"""

import contextlib
import ctypes
import logging
import os
import threading
import time
from ctypes import wintypes

logger = logging.getLogger("flet")

_ole32 = ctypes.OleDLL("ole32")
_shell32 = ctypes.OleDLL("shell32")
_shlwapi = ctypes.OleDLL("shlwapi")
_user32 = ctypes.WinDLL("user32", use_last_error=True)


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_uint32),
        ("Data2", ctypes.c_uint16),
        ("Data3", ctypes.c_uint16),
        ("Data4", ctypes.c_ubyte * 8),
    ]

    def __init__(self, s: str | None = None) -> None:
        super().__init__()
        if s:
            _ole32.CLSIDFromString(s, ctypes.byref(self))


_ole32.CLSIDFromString.argtypes = [ctypes.c_wchar_p, ctypes.c_void_p]


class PROPERTYKEY(ctypes.Structure):
    _fields_ = [("fmtid", GUID), ("pid", ctypes.c_uint32)]


class PROPVARIANT(ctypes.Structure):
    _fields_ = [
        ("vt", ctypes.c_uint16),
        ("r1", ctypes.c_uint16),
        ("r2", ctypes.c_uint16),
        ("r3", ctypes.c_uint16),
        ("data", ctypes.c_void_p),
        ("data2", ctypes.c_void_p),
    ]


_VT_LPWSTR = 31
_shlwapi.SHStrDupW.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_void_p)]


def _propvariant_from_string(value: str) -> PROPVARIANT:
    """
    Build a `VT_LPWSTR` PROPVARIANT owning a CoTaskMem-allocated string copy.

    `InitPropVariantFromString` is a header-inline helper (not exported from
    propsys.dll), so replicate it via `SHStrDupW`; `PropVariantClear` frees
    the allocation.

    Args:
        value: String to wrap.

    Returns:
        A PROPVARIANT holding a copy of `value`.
    """

    buf = ctypes.c_void_p()
    _shlwapi.SHStrDupW(value, ctypes.byref(buf))
    pv = PROPVARIANT()
    pv.vt = _VT_LPWSTR
    pv.data = buf
    return pv


_PS_SetValue = ctypes.WINFUNCTYPE(
    ctypes.HRESULT,
    ctypes.c_void_p,
    ctypes.POINTER(PROPERTYKEY),
    ctypes.POINTER(PROPVARIANT),
)
_PS_Commit = ctypes.WINFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p)
_PS_Release = ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)


class IPropertyStoreVtbl(ctypes.Structure):
    _fields_ = [
        ("QueryInterface", ctypes.c_void_p),
        ("AddRef", ctypes.c_void_p),
        ("Release", _PS_Release),
        ("GetCount", ctypes.c_void_p),
        ("GetAt", ctypes.c_void_p),
        ("GetValue", ctypes.c_void_p),
        ("SetValue", _PS_SetValue),
        ("Commit", _PS_Commit),
    ]


class IPropertyStore(ctypes.Structure):
    _fields_ = [("lpVtbl", ctypes.POINTER(IPropertyStoreVtbl))]


_IID_IPropertyStore = "{886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99}"

# System.AppUserModel.* property keys, see propkey.h.
_PKEY_FMTID = "{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}"
_PID_RELAUNCH_COMMAND = 2
_PID_RELAUNCH_ICON = 3
_PID_RELAUNCH_DISPLAY_NAME = 4
_PID_AUMID = 5

_shell32.SHGetPropertyStoreForWindow.argtypes = [
    wintypes.HWND,
    ctypes.c_void_p,
    ctypes.c_void_p,
]
_user32.GetWindowThreadProcessId.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(wintypes.DWORD),
]
_user32.GetClassNameW.argtypes = [wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
_GW_OWNER = 4
_EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_kernel32.OpenProcess.restype = wintypes.HANDLE
_kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
_kernel32.WaitForSingleObject.restype = wintypes.DWORD
_kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
_kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
_SYNCHRONIZE = 0x00100000
_WAIT_TIMEOUT = 0x00000102

# Window class registered by the Flet client's runner (win32_window.cpp).
_FLUTTER_WINDOW_CLASS = "FLUTTER_RUNNER_WIN32_WINDOW"


def _find_top_window(pid: int) -> int | None:
    """
    Find the client process's top-level Flutter window.

    Matches by window class rather than visibility: the client window is
    created hidden and only shown on the first frame — or arbitrarily late
    for `FLET_HIDE_WINDOW_ON_START` apps — and property stamping works on
    hidden windows. The class check also keeps an unrelated window of a
    recycled PID from ever being stamped.

    Args:
        pid: Process ID of the desktop client.

    Returns:
        Window handle, or `None` when the window does not exist yet.
    """

    found = []

    def cb(hwnd, lparam):
        wpid = wintypes.DWORD()
        _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(wpid))
        if wpid.value == pid and not _user32.GetWindow(hwnd, _GW_OWNER):
            buf = ctypes.create_unicode_buffer(64)
            _user32.GetClassNameW(hwnd, buf, 64)
            if buf.value == _FLUTTER_WINDOW_CLASS:
                found.append(hwnd)
        return True

    _user32.EnumWindows(_EnumWindowsProc(cb), 0)
    return found[0] if found else None


def _set_props(hwnd: int, props: list[tuple[int, str]]) -> None:
    """
    Set `System.AppUserModel.*` string properties on a window's property store.

    Args:
        hwnd: Target window handle.
        props: `(property id, value)` pairs from the
            `{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}` property set.
    """

    iid = GUID(_IID_IPropertyStore)
    ps_ptr = ctypes.c_void_p()
    _shell32.SHGetPropertyStoreForWindow(hwnd, ctypes.byref(iid), ctypes.byref(ps_ptr))
    ps = ctypes.cast(ps_ptr, ctypes.POINTER(IPropertyStore))
    vtbl = ps.contents.lpVtbl.contents
    try:
        for pid, value in props:
            key = PROPERTYKEY()
            key.fmtid = GUID(_PKEY_FMTID)
            key.pid = pid
            pv = _propvariant_from_string(value)
            try:
                vtbl.SetValue(ps_ptr, ctypes.byref(key), ctypes.byref(pv))
            except OSError as e:
                logger.warning(f"Failed to set taskbar property {pid}: {e}")
            finally:
                _ole32.PropVariantClear(ctypes.byref(pv))
        vtbl.Commit(ps_ptr)
    finally:
        vtbl.Release(ps_ptr)


def apply_relaunch_props_async(pid: int) -> None:
    """
    Stamp AppUserModel window properties on the Flet client window.

    Waits (on a daemon thread) for the client process to create its top-level
    window, then sets the AppUserModelID and relaunch command/name/icon
    properties on it. Values come from the `FLET_APP_USER_MODEL_ID`,
    `FLET_APP_RELAUNCH_COMMAND`, `FLET_APP_RELAUNCH_DISPLAY_NAME` and
    `FLET_APP_RELAUNCH_ICON` environment variables; when only the ID is set
    and it is the path of an existing file, the rest is derived from it.

    Args:
        pid: Process ID of the started desktop client.
    """
    aumid = os.environ.get("FLET_APP_USER_MODEL_ID")
    if os.name != "nt" or not aumid:
        return
    is_path = os.path.isfile(aumid)
    relaunch = os.environ.get("FLET_APP_RELAUNCH_COMMAND") or (
        f'"{aumid}"' if is_path else None
    )
    display = os.environ.get("FLET_APP_RELAUNCH_DISPLAY_NAME") or (
        os.path.splitext(os.path.basename(aumid))[0] if is_path else None
    )
    icon = os.environ.get("FLET_APP_RELAUNCH_ICON") or (
        f"{aumid},0" if is_path else None
    )
    if not relaunch:
        logger.debug("No relaunch command derivable for taskbar properties")
        return

    props = [(_PID_AUMID, aumid), (_PID_RELAUNCH_COMMAND, relaunch)]
    if display:
        props.append((_PID_RELAUNCH_DISPLAY_NAME, display))
    if icon:
        props.append((_PID_RELAUNCH_ICON, icon))

    def worker():
        with contextlib.suppress(OSError):
            _ole32.CoInitialize(None)
        # Hold a SYNCHRONIZE handle to the client for the whole poll: it
        # detects exit (stop polling) and keeps Windows from recycling the
        # PID under us, so a foreign process can never be stamped.
        hproc = _kernel32.OpenProcess(_SYNCHRONIZE, False, pid)
        try:
            while True:
                hwnd = _find_top_window(pid)
                if hwnd:
                    try:
                        _set_props(hwnd, props)
                        logger.debug(f"Applied taskbar relaunch properties to {hwnd}")
                    except OSError as e:
                        logger.warning(f"Failed to apply taskbar properties: {e}")
                    return
                if (
                    not hproc
                    or _kernel32.WaitForSingleObject(hproc, 0) != _WAIT_TIMEOUT
                ):
                    logger.debug("Client exited before its window appeared")
                    return
                time.sleep(0.2)
        finally:
            if hproc:
                _kernel32.CloseHandle(hproc)

    threading.Thread(target=worker, daemon=True).start()
