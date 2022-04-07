import platform
import subprocess


def is_windows():
    return platform.system() == "Windows"


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
        return "arm"
    else:
        raise Exception(f"Unsupported architecture: {a}")


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
    return "://localhost/" in url or "://localhost:" in url
