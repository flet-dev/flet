import os
import platform
import sys
import unicodedata
import webbrowser


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def is_linux_server():
    if platform.system() == "Linux":
        # check if it's WSL
        p = "/proc/version"
        if os.path.exists(p):
            with open(p, "r") as file:
                if "microsoft" in file.read():
                    return False  # it's WSL, not a server
        return os.environ.get("XDG_CURRENT_DESKTOP") == None
    return False


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
def which(program, exclude_exe=None):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path, program)
        if is_exe(exe_file) and (
            exclude_exe == None
            or (exclude_exe != None and exclude_exe.lower() != exe_file.lower())
        ):
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


def slugify(original: str) -> str:
    """
    Make a string url friendly. Useful for creating routes for navigation.

    >>> slugify("What's    up?")
    'whats-up'

    >>> slugify("  Mitä kuuluu?  ")
    'mitä-kuuluu'
    """
    slugified = original.strip()
    slugified = " ".join(slugified.split())  # Remove extra spaces between words
    slugified = slugified.lower()
    # Remove unicode punctuation
    slugified = "".join(
        character
        for character in slugified
        if not unicodedata.category(character).startswith("P")
    )
    slugified = slugified.replace(" ", "-")

    return slugified
