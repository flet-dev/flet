import hashlib
import logging
import os
import re
import sys

logger = logging.getLogger("flet")


logger.info("Running PyInstaller runtime hook for Flet...")

os.environ["FLET_SERVER_IP"] = "127.0.0.1"

# On Windows, set AppUserModelID so the taskbar associates the Flet client window
# with the parent executable (a PyInstaller bundle in this case) rather than the
# cached flet.exe. flet_desktop additionally stamps relaunch properties on the
# client window (see flet_desktop.win_taskbar) so the taskbar name, icon, jump
# list and pins all resolve to the bundle exe; the env vars below feed both
# mechanisms.
if sys.platform == "win32" and "FLET_APP_USER_MODEL_ID" not in os.environ:
    exe_path = os.path.abspath(sys.executable)
    exe_stem = os.path.splitext(os.path.basename(exe_path))[0]
    if len(exe_path) <= 128 and " " not in exe_path:
        aumid = exe_path
    else:
        # AppUserModelIDs must be at most 128 characters and contain no spaces;
        # fall back to a stable hashed ID and let the window relaunch
        # properties carry the actual relaunch target.
        safe_name = re.sub(r"[^A-Za-z0-9]", "", exe_stem)[:64] or "App"
        path_hash = hashlib.sha1(exe_path.encode("utf-8")).hexdigest()[:16]
        aumid = f"Flet.{safe_name}.{path_hash}"
    os.environ["FLET_APP_USER_MODEL_ID"] = aumid
    os.environ.setdefault("FLET_APP_RELAUNCH_COMMAND", f'"{exe_path}"')
    os.environ.setdefault("FLET_APP_RELAUNCH_DISPLAY_NAME", exe_stem)
    os.environ.setdefault("FLET_APP_RELAUNCH_ICON", f"{exe_path},0")
