import logging
import os

logging.info("Runnin Flet runtime hook for PyInstaller...")

os.environ["FLET_SERVER_IP"] = "localhost"
