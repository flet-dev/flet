import os
import subprocess
from re import sub
from time import sleep

port = 8570
flet_path = "flet.exe"
args = [flet_path, "server", "--attached", "--port", str(port)]

subprocess.Popen(args, stdout=subprocess.DEVNULL)
print("started")

sleep(5)

print("finished!")
