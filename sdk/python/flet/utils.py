import os
import platform
import subprocess
import sys


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def is_linux_server():
    return (
        platform.system() == "Linux" and os.environ.get("XDG_CURRENT_DESKTOP") is None
    )


def is_macos():
    return platform.system() == "Darwin"


def get_platform():
    system = platform.system()
    if is_windows():
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "darwin"
    else:
        raise Exception(f"Unsupported platform: {system}")


def get_arch():
    machine = platform.machine().lower()
    if machine in ["x86_64", "amd64"]:
        return "amd64"
    elif machine in ["arm64", "aarch64"]:
        return "arm64"
    elif machine.startswith("arm"):
        return "arm_7"
    else:
        raise Exception(f"Unsupported architecture: {machine}")


def open_in_browser(url):
    if is_windows():
        subprocess.run(["explorer.exe", url])
    elif is_macos():
        subprocess.run(["open", url])


# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def is_localhost_url(url):
    return (
        "://localhost/" in url
        or "://localhost:" in url
        or "://127.0.0.1/" in url
        or "://127.0.0.1:" in url
    )


def get_current_script_dir():
    pathname = os.path.dirname(sys.argv[0])
    return os.path.abspath(pathname)
