import os
import subprocess
from typing import Optional

from flet.utils import is_windows

if is_windows():
    from ctypes import windll


def run(args, cwd, env: Optional[dict] = None, capture_output=True, log=None):
    """
    Execute a subprocess command with optional streamed logging.

    On Windows, the console output code page is temporarily switched to UTF-8
    while the command runs, then restored.

    Args:
        args: Command and arguments passed to the subprocess.
        cwd: Working directory for the command.
        env: Extra environment variables merged into the current process env.
        capture_output: If `True`, run with [`subprocess.run`][subprocess.run] and
            capture output in memory. If `False`, stream combined output line by line.
        log: Optional callback receiving each output line when `capture_output=False`.

    Returns:
        A completed [`subprocess.CompletedProcess`][subprocess.CompletedProcess]
            when `capture_output=True`, otherwise a finished
            [`subprocess.Popen`][subprocess.Popen] instance.

    Raises:
        KeyboardInterrupt: Re-raised after terminating the child process when
            interactive streaming is interrupted.
    """

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
            encoding="utf-8",
            env=cmd_env,
            errors="replace",
        )
    else:
        process = subprocess.Popen(
            args,
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            env=cmd_env,
            errors="replace",
        )

        try:
            while True:
                stdout_line = process.stdout.readline()

                # Log or print lines if a log function is provided
                if stdout_line and log:
                    log(stdout_line.rstrip())

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
