import math
import os
import platform
import socket
import sys
import unicodedata
import webbrowser
from pathlib import Path


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
        return os.environ.get("XDG_CURRENT_DESKTOP") is None
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
            exclude_exe is None
            or (exclude_exe is not None and exclude_exe.lower() != exe_file.lower())
        ):
            return exe_file

    return None


def is_within_directory(directory, target):

    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    prefix = os.path.commonprefix([abs_directory, abs_target])

    return prefix == abs_directory


def safe_tar_extractall(tar, path=".", members=None, *, numeric_owner=False):

    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not is_within_directory(path, member_path):
            raise Exception("Attempted Path Traversal in Tar File")

    tar.extractall(path, members, numeric_owner=numeric_owner)


def is_localhost_url(url):
    return (
        "://localhost/" in url
        or "://localhost:" in url
        or "://127.0.0.1/" in url
        or "://127.0.0.1:" in url
    )


def get_package_root_dir():
    return str(Path(__file__).parent)


def get_package_bin_dir():
    return os.path.join(get_package_root_dir(), "bin")


def get_package_web_dir():
    web_root_dir = os.environ.get("FLET_WEB_PATH")
    return web_root_dir if web_root_dir else os.path.join(get_package_root_dir(), "web")


def get_free_tcp_port():
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


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


class Vector(complex):
    """
    Simple immutable 2D vector class based on the Python complex number type

    Create and access - coordinates

    >>> v = Vector(1, 2)
    >>> v.x, v.y
    (1.0, 2.0)

    Create and access - angle and magnitude (length)

    >>> v = Vector.polar(math.pi, 2)
    >>> v
    Vector(-2.0, 0.0)
    >>> v.magnitude  # Length of the vector, alias for abs(v)
    2.0
    >>> v.radians
    3.141592653589793
    >>> v.degrees
    180.0

    Arithmetic operations

    >>> Vector(1, 1) + 2
    Vector(3.0, 1.0)
    >>> Vector(0.1, 0.1) + Vector(0.2, 0.2)  == Vector(0.3, 0.3)  # Float tolerance 10 decimals
    True
    >>> Vector(2, 3) - Vector(1, 1)
    Vector(1.0, 2.0)
    >>> Vector(1, 1) * 2
    Vector(2.0, 2.0)
    >>> round(Vector.polar(math.pi / 4, 1), 1)
    Vector(0.7, 0.7)

    Get a new vector by adjusting one of the coordinates
    >>> v = Vector()
    >>> v.with_x(1)
    Vector(1.0, 0.0)
    >>> v.with_y(2)
    Vector(0.0, 2.0)

    Get a new vector by adjusting angle or magnitude

    >>> v = Vector(1, 2)
    >>> v = v.with_magnitude(4.47213595499958)  # Twice as long
    >>> v.x, v.y
    (2.0, 4.0)

    >>> v = Vector.polar(math.pi, 2)
    >>> v
    Vector(-2.0, 0.0)
    >>> v.with_radians(0)
    Vector(2.0, 0.0)
    >>> v.with_degrees(90)
    Vector(0.0, 2.0)
    """

    abs_tol = 1e-10

    x = complex.real
    y = complex.imag
    __add__ = lambda self, other: type(self)(complex.__add__(self, other))
    __sub__ = lambda self, other: type(self)(complex.__sub__(self, other))
    __mul__ = lambda self, other: type(self)(complex.__mul__(self, other))
    __truediv__ = lambda self, other: type(self)(complex.__truediv__(self, other))
    __len__ = lambda self: 2
    __round__ = lambda self, ndigits=None: type(self)(
        round(self.x, ndigits), round(self.y, ndigits)
    )

    def __eq__(self, other):
        return math.isclose(self.x, other.x, abs_tol=self.abs_tol) and math.isclose(
            self.y, other.y, abs_tol=self.abs_tol
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        return iter([self.x, self.y])

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        return f"{type(self).__name__}{str(self)}"

    @classmethod
    def polar(cls, radians, magnitude):
        return cls(
            round(math.cos(radians) * magnitude, 10),
            round(math.sin(radians) * magnitude, 10),
        )

    @property
    def magnitude(self):
        return abs(self)

    @property
    def degrees(self):
        return math.degrees(self.radians)

    @property
    def radians(self):
        return math.atan2(self.y, self.x)

    def with_x(self, value):
        return type(self)(value, self.y)

    def with_y(self, value):
        return type(self)(self.x, value)

    def with_magnitude(self, value):
        return self * value / abs(self)

    def with_radians(self, value):
        magnitude = abs(self)
        return type(self).polar(value, magnitude)

    def with_degrees(self, value):
        radians = math.radians(value)
        magnitude = abs(self)
        return type(self).polar(radians, magnitude)
