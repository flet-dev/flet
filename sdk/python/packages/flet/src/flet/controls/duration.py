from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

__all__ = [
    "Duration",
    "DurationValue",
    "OptionalDurationValue",
    "MICROSECONDS_PER_MILLISECOND",
    "MICROSECONDS_PER_SECOND",
    "MICROSECONDS_PER_MINUTE",
    "MICROSECONDS_PER_HOUR",
    "MICROSECONDS_PER_DAY",
]

MICROSECONDS_PER_MILLISECOND = 1_000
MICROSECONDS_PER_SECOND = 1_000_000
MICROSECONDS_PER_MINUTE = 60 * MICROSECONDS_PER_SECOND
MICROSECONDS_PER_HOUR = 60 * MICROSECONDS_PER_MINUTE
MICROSECONDS_PER_DAY = 24 * MICROSECONDS_PER_HOUR


@dataclass
class Duration:
    microseconds: int = 0
    milliseconds: int = 0
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0

    # Class methods

    @classmethod
    def from_unit(
        cls,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        milliseconds: int = 0,
        microseconds: int = 0,
    ) -> "Duration":
        """Creates a Duration from individual time units."""
        total_microseconds = (
            days * MICROSECONDS_PER_DAY
            + hours * MICROSECONDS_PER_HOUR
            + minutes * MICROSECONDS_PER_MINUTE
            + seconds * MICROSECONDS_PER_SECOND
            + milliseconds * MICROSECONDS_PER_MILLISECOND
            + microseconds
        )
        d, rem = divmod(total_microseconds, MICROSECONDS_PER_DAY)
        h, rem = divmod(rem, MICROSECONDS_PER_HOUR)
        m, rem = divmod(rem, MICROSECONDS_PER_MINUTE)
        s, rem = divmod(rem, MICROSECONDS_PER_SECOND)
        ms, us = divmod(rem, MICROSECONDS_PER_MILLISECOND)

        return cls(
            days=d, hours=h, minutes=m, seconds=s, milliseconds=ms, microseconds=us
        )

    @classmethod
    def from_datetime(cls, dt: datetime) -> "Duration":
        """Creates a Duration from a datetime object."""
        return cls.from_unit(
            days=dt.day,
            hours=dt.hour,
            minutes=dt.minute,
            seconds=dt.second,
            milliseconds=dt.microsecond // MICROSECONDS_PER_MILLISECOND,
        )

    # Properties

    @property
    def in_microseconds(self) -> int:
        """Returns total duration in microseconds."""
        return (
            self.microseconds
            + self.milliseconds * MICROSECONDS_PER_MILLISECOND
            + self.seconds * MICROSECONDS_PER_SECOND
            + self.minutes * MICROSECONDS_PER_MINUTE
            + self.hours * MICROSECONDS_PER_HOUR
            + self.days * MICROSECONDS_PER_DAY
        )

    @property
    def in_milliseconds(self) -> int:
        """Returns total duration in milliseconds."""
        return self.in_microseconds // MICROSECONDS_PER_MILLISECOND

    @property
    def in_seconds(self) -> int:
        """Returns total duration in seconds."""
        return self.in_microseconds // MICROSECONDS_PER_SECOND

    @property
    def in_minutes(self) -> int:
        """Returns total duration in minutes."""
        return self.in_microseconds // MICROSECONDS_PER_MINUTE

    @property
    def in_hours(self) -> int:
        """Returns total duration in hours."""
        return self.in_microseconds // MICROSECONDS_PER_HOUR

    @property
    def in_days(self) -> int:
        """Returns total duration in days."""
        return self.in_microseconds // MICROSECONDS_PER_DAY

    @property
    def is_negative(self) -> bool:
        """Returns True if duration is negative."""
        return self.in_microseconds < 0

    def abs(self) -> "Duration":
        """Returns absolute (non-negative) Duration."""
        return Duration.from_unit(microseconds=abs(self.in_microseconds))

    # Arithmetics

    def __add__(self, other: "Duration") -> "Duration":
        """Adds two Duration instances."""
        if not isinstance(other, Duration):
            return NotImplemented
        return Duration.from_unit(
            microseconds=self.in_microseconds + other.in_microseconds
        )

    def __sub__(self, other: "Duration") -> "Duration":
        """Subtracts one Duration from another."""
        if not isinstance(other, Duration):
            return NotImplemented
        return Duration.from_unit(
            microseconds=self.in_microseconds - other.in_microseconds
        )

    def __mul__(self, factor: float) -> "Duration":
        """Multiplies Duration by a scalar factor."""
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Duration.from_unit(microseconds=round(self.in_microseconds * factor))

    def __floordiv__(self, quotient: int) -> "Duration":
        """Performs floor division on Duration."""
        if quotient == 0:
            raise ZeroDivisionError("Division by zero")
        return Duration.from_unit(microseconds=self.in_microseconds // quotient)

    # Comparisons

    def __eq__(self, other) -> bool:
        """Checks equality between Durations."""
        if not isinstance(other, Duration):
            return False
        return self.in_microseconds == other.in_microseconds

    def __lt__(self, other: "Duration") -> bool:
        """Checks if Duration is less than another."""
        if not isinstance(other, Duration):
            return False
        return self.in_microseconds < other.in_microseconds

    def __le__(self, other: "Duration") -> bool:
        """Checks if Duration is less than or equal to another."""
        if not isinstance(other, Duration):
            return False
        return self.in_microseconds <= other.in_microseconds

    def __gt__(self, other: "Duration") -> bool:
        """Checks if Duration is greater than another."""
        if not isinstance(other, Duration):
            return False
        return self.in_microseconds > other.in_microseconds

    def __ge__(self, other: "Duration") -> bool:
        """Checks if Duration is greater than or equal to another."""
        if not isinstance(other, Duration):
            return False
        return self.in_microseconds >= other.in_microseconds


DurationValue = Union[int, Duration]
OptionalDurationValue = Optional[DurationValue]
print(Duration(seconds=3600).in_milliseconds)
