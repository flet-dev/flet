import logging
import os

import flet

logger = logging.getLogger(flet.__name__)


logger.info("Running PyInstaller runtime hook for Flet...")

os.environ["FLET_SERVER_IP"] = "127.0.0.1"
