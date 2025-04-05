import logging
import os

logger = logging.getLogger("flet")


logger.info("Running PyInstaller runtime hook for Flet...")

os.environ["FLET_SERVER_IP"] = "127.0.0.1"
