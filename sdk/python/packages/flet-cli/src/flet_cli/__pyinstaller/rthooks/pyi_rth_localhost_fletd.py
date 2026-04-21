import hashlib
import logging
import os
import re
import sys

logger = logging.getLogger("flet")


logger.info("Running PyInstaller runtime hook for Flet...")

os.environ["FLET_SERVER_IP"] = "127.0.0.1"

# On Windows, set AppUserModelID so the taskbar associates the Flet client window
# with the parent executable (a PyInstaller bundle in this case) rather than the cached
# flet.exe. This ensures taskbar pins and shortcuts point to the correct executable.
# AppUserModelID must be <=128 chars and contain no spaces, so we derive a stable
# identifier from the exe name and a hash of its absolute path (unique per install).
if sys.platform == "win32" and "FLET_APP_USER_MODEL_ID" not in os.environ:
    exe_path = os.path.abspath(sys.executable)
    exe_stem = os.path.splitext(os.path.basename(exe_path))[0]
    safe_name = re.sub(r"[^A-Za-z0-9]", "", exe_stem)[:64] or "App"
    path_hash = hashlib.sha1(exe_path.encode("utf-8")).hexdigest()[:16]
    os.environ["FLET_APP_USER_MODEL_ID"] = f"Flet.{safe_name}.{path_hash}"
