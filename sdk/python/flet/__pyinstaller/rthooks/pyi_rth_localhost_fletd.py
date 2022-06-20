import os

print(">>> Hook sample run-time hook was executed. <<<")
os.environ["FLET_SERVER_PORT"] = "8555"
