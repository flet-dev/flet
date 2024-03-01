import math


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
