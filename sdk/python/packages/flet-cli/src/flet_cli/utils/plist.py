try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def is_supported_plist_value(value) -> bool:
    """Checks if the value is a supported type for plist values."""
    # string and boolean
    if isinstance(value, (str, bool)):
        return True
    # integer and float/real
    if isinstance(value, (int, float)):
        return True
    # array
    if isinstance(value, list):
        return all(is_supported_plist_value(item) for item in value)
    # dictionary
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and is_supported_plist_value(item)
            for key, item in value.items()
        )
    return False


def parse_cli_plist_value(value: str):
    """Parses a CLI-provided plist value, supporting TOML syntax for complex types."""
    value = value.strip()
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"

    try:
        parsed = tomllib.loads(f"value = {value}")["value"]
    except Exception:
        return value

    if is_supported_plist_value(parsed):
        return parsed

    return value
