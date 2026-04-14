import logging
import os
import sys

logger = logging.getLogger("flet")


logger.info("Running PyInstaller runtime hook for Flet...")

os.environ["FLET_SERVER_IP"] = "127.0.0.1"

# In packed Windows apps, the Flet client runs as a child flet.exe process.
# Set an AppUserModelID based on the packaged executable so taskbar pins point
# to the user's app instead of the cached client binary.
if sys.platform == "win32" and "FLET_APP_USER_MODEL_ID" not in os.environ:
    os.environ["FLET_APP_USER_MODEL_ID"] = os.path.abspath(sys.executable)
