import os
import platform
import sys
import webbrowser


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def is_linux_server():
    return (
        platform.system() == "Linux" and os.environ.get("XDG_CURRENT_DESKTOP") == None
    )


def is_macos():
    return platform.system() == "Darwin"


def get_platform():
    p = platform.system()
    if is_windows():
        return "windows"
    elif p == "Linux":
        return "linux"
    elif p == "Darwin":
        return "darwin"
    else:
        raise Exception(f"Unsupported platform: {p}")


def get_arch():
    a = platform.machine().lower()
    if a == "x86_64" or a == "amd64":
        return "amd64"
    elif a == "arm64" or a == "aarch64":
        return "arm64"
    elif a.startswith("arm"):
        return "arm_7"
    else:
        raise Exception(f"Unsupported architecture: {a}")


def open_in_browser(url):
    webbrowser.open(url)


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
