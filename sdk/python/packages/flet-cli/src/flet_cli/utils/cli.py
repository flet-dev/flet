def parse_cli_bool_value(value: str) -> bool:
    """Parse a CLI boolean value, accepting only true/false tokens."""
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError("expected true or false")
