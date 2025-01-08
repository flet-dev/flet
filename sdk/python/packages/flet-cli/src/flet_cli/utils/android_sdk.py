import os
import subprocess
from ctypes import windll
from typing import Optional

from flet.utils import is_windows

# TODO:
# - check if Android SDK is already installed as part of Android Studio
#
#
#
#


def run(self, args, cwd, env: Optional[dict] = None, capture_output=True):
    if is_windows():
        # Source: https://stackoverflow.com/a/77374899/1435891
        # Save the current console output code page and switch to 65001 (UTF-8)
        previousCp = windll.kernel32.GetConsoleOutputCP()
        windll.kernel32.SetConsoleOutputCP(65001)

    if self.verbose > 0:
        print(f"Run subprocess: {args}")

    cmd_env = None
    if env is not None:
        cmd_env = os.environ.copy()
        for k, v in env.items():
            cmd_env[k] = v

    r = subprocess.run(
        args,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        encoding="utf8",
        env=cmd_env,
    )

    if is_windows():
        # Restore the previous output console code page.
        windll.kernel32.SetConsoleOutputCP(previousCp)

    return r
