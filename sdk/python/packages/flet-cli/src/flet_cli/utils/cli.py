import os
import re
import shlex

_WINDOWS_SAFE = re.compile(r"[\w@+=:,./\\-]+", re.ASCII)
"""
Characters that need no quoting on Windows. Backslash and colon are included
because every absolute Windows path contains them.
"""


def parse_cli_bool_value(value: str) -> bool:
    """Parse a CLI boolean value, accepting only true/false tokens."""
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError("expected true or false")


def quote_for_shell(value: str) -> str:
    """
    Quote a path so that it survives being pasted into a shell command.

    Only ever used for commands Flet *suggests*; Flet does not run them. There
    is no single correct answer, because the shell is not knowable from the
    platform - a Windows user may well be in MSYS bash. POSIX quoting is used
    off Windows, where it is exact, and double quotes on Windows, because they
    are the form `cmd.exe` understands (single quotes are not quoting there at
    all). Two gaps remain and cannot be closed from here: `%VAR%` still expands
    inside double quotes in `cmd.exe`, and so does `$var` in PowerShell.

    Args:
        value: The path to quote.

    Returns:
        The path, quoted only if it needs it - plain names are returned
            unchanged so the common case reads naturally.
    """

    if os.name != "nt":
        return shlex.quote(value)
    return value if _WINDOWS_SAFE.fullmatch(value) else f'"{value}"'
