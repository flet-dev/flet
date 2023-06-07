import asyncio
import inspect
import math
import random
import string
import sys
import unicodedata
from enum import Enum
from typing import Union, Type, Optional, TypeVar


if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum
    class StrEnum(str, Enum):
        value: str


T = TypeVar('T', bound=StrEnum)
R = TypeVar('R')


def get_valid_enum(cls_enum: Type[T], value: Union[T, str, None], default: R) -> Union[T, R]:
    if isinstance(value, cls_enum):
        return value
    return cls_enum.__dict__['_value2member_map_'].get(value, default)


def get_non_default_value(
    enum: Optional[StrEnum], default: Optional[StrEnum], spare_value: Optional[R] = None,
) -> Union[str, None, R]:
    if enum == default:
        return spare_value
    return enum if enum is None else enum.value


def random_string(length):
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def is_asyncio():
    try:
        return asyncio.current_task() is not None or sys.platform == "emscripten"
    except RuntimeError:
        return False


def is_coroutine(method):
    return inspect.iscoroutinefunction(method)


def get_str_from_enum(enum: Type[Enum], value: Union[Enum, str]) -> Optional[str]:
    if isinstance(value, Enum):
        return str(value.value)
    if value in enum.__dict__['_value2member_map_']:
        return value
    return None


def get_enum_from_value(enum: Type[T], value: Optional[str], default: T) -> T:
    return enum.__dict__['_value2member_map_'].get(value, default)

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

