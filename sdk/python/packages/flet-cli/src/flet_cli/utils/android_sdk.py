import os
import subprocess
from ctypes import windll
from typing import Optional

from flet.utils import is_windows

# TODO:
# - check if Android SDK is already installed as part of Android Studio
# - download commandlinetools
#
#
#
#


def accept_sdkmanager_licenses():
    """
    Automatically accept all licenses for the Android SDK Manager.
    """
    try:
        # Define the command for sdkmanager --licenses
        command = ["C:\\Android\\sdk\\cmdline-tools\\latest\\bin\\sdkmanager.bat", "--licenses"]

        # Run the command, sending 'y' (yes) to approve all licenses
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            #stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={
                "JAVA_HOME": "C:\\Users\\feodo\\java\\17.0.13+11"
            }
        )
        # Simulate accepting licenses by sending 'y' repeatedly
        stdout, stderr = process.communicate(input="y\n" * 100)

        # Check the process return code
        if process.returncode == 0:
            print("All licenses accepted successfully.")
        else:
            print(f"Failed to accept licenses. Error: {stderr}")
    except FileNotFoundError:
        print(
            "sdkmanager not found. Ensure the Android SDK is installed and in your PATH."
        )
    except Exception as e:
        print(f"An error occurred: {e}")


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

# Example usage
if __name__ == "__main__":
    jdk_path = accept_sdkmanager_licenses()