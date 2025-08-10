from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Union

from flet.controls.types import Number

__all__ = [
    "DateTimeValue",
    "Duration",
    "DurationValue",
    "MICROSECONDS_PER_DAY",
    "MICROSECONDS_PER_HOUR",
    "MICROSECONDS_PER_MILLISECOND",
    "MICROSECONDS_PER_MINUTE",
    "MICROSECONDS_PER_SECOND",
]

MICROSECONDS_PER_MILLISECOND = 1_000
MICROSECONDS_PER_SECOND = 1_000_000
MICROSECONDS_PER_MINUTE = 60 * MICROSECONDS_PER_SECOND
MICROSECONDS_PER_HOUR = 60 * MICROSECONDS_PER_MINUTE
MICROSECONDS_PER_DAY = 24 * MICROSECONDS_PER_HOUR


@dataclass
class Duration:
    """
    A span of time, such as 27 days, 4 hours, 12 minutes, and 3 seconds.

    A Duration represents a difference from one point in time to another. The duration
    may be "negative" if the difference is from a later time to an earlier.
    """

    microseconds: int = 0
    """
    The number of microseconds in the duration.
    """

    milliseconds: int = 0
    """
    The number of milliseconds in the duration.
    """

    seconds: int = 0
    """
    The number of seconds in the duration.
    """

    minutes: int = 0
    """
    The number of minutes in the duration.
    """

    hours: int = 0
    """
    The number of hours in the duration.
    """

    days: int = 0
    """
    The number of days in the duration.
    """

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

    def __mul__(self, other: Number) -> "Duration":
        """Multiplies Duration by a scalar factor."""
        if not isinstance(other, Number):
            return Duration.from_unit(microseconds=round(self.in_microseconds * other))
        return NotImplemented

    def __floordiv__(self, quotient: int) -> "Duration":
        """Performs floor division on Duration."""
        if quotient == 0:
            raise ZeroDivisionError("Division by zero is not possible")
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

    # Instance Methods

    def copy(
        self,
        *,
        microseconds: Optional[int] = None,
        milliseconds: Optional[int] = None,
        seconds: Optional[int] = None,
        minutes: Optional[int] = None,
        hours: Optional[int] = None,
        days: Optional[int] = None,
    ) -> "Duration":
        """
        Returns a copy of this `Duration` instance with the given fields replaced
        with the new values.
        """
        return Duration(
            microseconds=microseconds
            if microseconds is not None
            else self.microseconds,
            milliseconds=milliseconds
            if milliseconds is not None
            else self.milliseconds,
            seconds=seconds if seconds is not None else self.seconds,
            minutes=minutes if minutes is not None else self.minutes,
            hours=hours if hours is not None else self.hours,
            days=days if days is not None else self.days,
        )


DurationValue = Union[Duration, int]
DateTimeValue = Union[datetime, date]
