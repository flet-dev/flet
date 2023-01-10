import logging
import os

logging.info("Running PyInstaller runtime hook for Flet...")

os.environ["FLET_SERVER_IP"] = "127.0.0.1"
