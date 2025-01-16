import os
import subprocess
from typing import Optional

from flet.utils import is_windows

if is_windows():
    from ctypes import windll


def run(
    args, cwd, env: Optional[dict] = None, input=None, capture_output=True, log=None
):
    if is_windows():
        # Source: https://stackoverflow.com/a/77374899/1435891
        # Save the current console output code page and switch to 65001 (UTF-8)
        previousCp = windll.kernel32.GetConsoleOutputCP()
        windll.kernel32.SetConsoleOutputCP(65001)

    cmd_env = None
    if env is not None:
        cmd_env = os.environ.copy()
        for k, v in env.items():
            cmd_env[k] = v

    if capture_output:
        process = subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf8",
            env=cmd_env,
            errors="replace"
        )
    else:
        process = subprocess.Popen(
            args,
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf8",
            env=cmd_env,
            errors="replace"
        )

        input_iterator = (
            iter(input)
            if isinstance(input, list)
            else iter(input.split("\n")) if isinstance(input, str) else iter([])
        )

        try:
            while True:
                stdout_line = process.stdout.readline()

                # Log or print lines if a log function is provided
                if stdout_line and log:
                    log(stdout_line.rstrip())

                # Check if process is waiting for input
                if process.poll() is None and process.stdin:
                    try:
                        next_input = next(input_iterator) + "\n"
                        process.stdin.write(next_input)
                        process.stdin.flush()
                    except StopIteration:
                        # If no more input, close stdin to signal end
                        process.stdin.close()

                # Break when the process ends and buffers are empty
                if not stdout_line and process.poll() is not None:
                    break
        except KeyboardInterrupt:
            process.terminate()
            raise

        # Wait for the process to finish
        process.stdout.close()
        process.wait()

    if is_windows():
        # Restore the previous output console code page.
        windll.kernel32.SetConsoleOutputCP(previousCp)

    return process
