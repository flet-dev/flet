import re
from datetime import date, datetime
from typing import Optional, Union


def has_valid_datetime_format(value: str) -> bool:
    """
    Checks if the given string has a valid datetime format.
    Returns True if that's the case and False otherwise.
    """
    regex_format = (
        r"^([+-]?\d{4,6})-?(\d\d)-?(\d\d)"
        r"(?:[ T](\d\d)(?::?(\d\d)(?::?(\d\d)(?:[.,](\d+))?)?)?"
        r"( ?[zZ]| ?([-+])(\d\d)(?::?(\d\d))?)?)?$"
    )
    return re.match(regex_format, value) is not None


def datetime_to_string(value: Optional[Union[datetime, str]]) -> Optional[str]:
    """
    Converts a datetime or date object to an ISO 8601 string.
    If the input is already a string, it checks if the string has a valid datetime format.
    """
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    assert value is None or has_valid_datetime_format(
        value
    ), f"{value} has an invalid format"

    return value
