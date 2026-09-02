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
