import logging
import os
import sys

logger = logging.getLogger("flet")


logger.info("Running PyInstaller runtime hook for Flet...")

os.environ["FLET_SERVER_IP"] = "127.0.0.1"

# On Windows, set AppUserModelID so the taskbar associates the Flet client window
# with the parent executable (a PyInstaller bundle in this case) rather than the cached
# flet.exe. This ensures taskbar pins and shortcuts point to the correct executable.
if sys.platform == "win32" and "FLET_APP_USER_MODEL_ID" not in os.environ:
    os.environ["FLET_APP_USER_MODEL_ID"] = os.path.abspath(sys.executable)
