import logging
import os
import subprocess
from asyncio.log import logger
from re import sub
from time import sleep

logging.basicConfig(level=logging.INFO)

my_env = {**os.environ, "FLET_LOG_TO_FILE": "true"}

port = 8570
flet_path = "flet.exe"
args = [flet_path, "server", "--attached", "--port", str(port)]

log_level = logger.getEffectiveLevel()
if log_level == logging.CRITICAL:
    log_level = logging.FATAL

if log_level != logging.NOTSET:
    log_level_name = logging.getLevelName(log_level).lower()
    args.extend(["--log-level", log_level_name])

subprocess.Popen(args, env=my_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("started")

sleep(10)

print("finished!")
