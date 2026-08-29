import logging
import os
import sys

logger = logging.getLogger("flet")


logger.info("Running PyInstaller runtime hook for Flet...")

os.environ["FLET_SERVER_IP"] = "127.0.0.1"

# On Windows, set AppUserModelID so the taskbar associates the Flet client window
# with the parent executable (a PyInstaller bundle in this case) rather than the
# cached flet.exe. flet_desktop additionally stamps this ID and the relaunch
# properties below onto the client window (see flet_desktop.win_taskbar) so the
# taskbar name, icon, jump list and pins all resolve to the bundle exe.
if sys.platform == "win32" and "FLET_APP_USER_MODEL_ID" not in os.environ:
    exe_path = os.path.abspath(sys.executable)
    os.environ["FLET_APP_USER_MODEL_ID"] = exe_path
    os.environ.setdefault("FLET_APP_RELAUNCH_COMMAND", f'"{exe_path}"')
    os.environ.setdefault(
        "FLET_APP_RELAUNCH_DISPLAY_NAME",
        os.path.splitext(os.path.basename(exe_path))[0],
    )
    os.environ.setdefault("FLET_APP_RELAUNCH_ICON", f"{exe_path},0")


# On Linux the taskbar keys on the window's WM_CLASS (X11) or app_id
# (Wayland), both of which GTK takes from the client binary's argv[0]. That
# binary is the shared, prebuilt `flet`, so every packed app shows up as
# "flet". flet_desktop relaunches it under this id instead -- the bundle's
# own name -- so the app groups and labels as itself, and can be matched by
# a desktop entry carrying StartupWMClass.
if sys.platform.startswith("linux") and "FLET_APP_ID" not in os.environ:
    # --bundle-id when it was given, so the identity matches what `flet build`
    # uses and what a desktop entry's StartupWMClass would name. Otherwise the
    # executable's own name, which reads better bare than a reverse-DNS id and
    # follows the binary if it is renamed.
    app_id = ""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        try:
            with open(os.path.join(meipass, "flet_app_id"), encoding="utf-8") as f:
                app_id = f.read().strip()
        except OSError:
            pass
    # No splitext here: a Linux executable has no extension, so it would eat
    # whatever follows the last dot in the app's own name -- turning
    # `myapp-1.2.3` into `myapp-1.2`, which then matches no desktop entry.
    os.environ["FLET_APP_ID"] = (
        app_id or os.path.basename(os.path.abspath(sys.executable)).strip()
    )
