from flet_cli.utils.plist import is_supported_plist_value, parse_cli_plist_value


def test_parse_cli_plist_value_supports_strings_and_booleans():
    """Strings and booleans should parse into their respective Python types."""
    assert parse_cli_plist_value("true") is True
    assert parse_cli_plist_value("False") is False
    assert parse_cli_plist_value("TEAMID.example.app") == "TEAMID.example.app"


def test_parse_cli_plist_value_keeps_quoted_literals_as_strings():
    """Quoted literals should remain strings even if they look typed."""
    assert parse_cli_plist_value('"true"') == "true"
    assert parse_cli_plist_value('"false"') == "false"
    assert parse_cli_plist_value('"42"') == "42"
    assert parse_cli_plist_value('"3.14"') == "3.14"


def test_parse_cli_plist_value_supports_integers_and_floats():
    """Numeric TOML literals should parse into Python numbers."""
    assert parse_cli_plist_value("42") == 42
    assert parse_cli_plist_value("3.14") == 3.14


def test_parse_cli_plist_value_supports_toml_arrays():
    """TOML arrays should parse into Python lists."""
    assert parse_cli_plist_value('["group.dev.example", "group.dev.shared"]') == [
        "group.dev.example",
        "group.dev.shared",
    ]


def test_parse_cli_plist_value_supports_toml_inline_tables():
    """TOML inline tables should parse into Python dictionaries."""
    assert parse_cli_plist_value('{ "com.apple.mail" = ["compose"] }') == {
        "com.apple.mail": ["compose"]
    }


def test_supported_plist_value_accepts_numbers():
    """The plist validator should accept integer and real values."""
    assert is_supported_plist_value(1)
    assert is_supported_plist_value(1.5)
    assert is_supported_plist_value(["group.dev.example", 1, 1.5])
    assert is_supported_plist_value({"com.apple.mail": 1})


def test_unsupported_plist_types_are_rejected():
    """The plist validator should reject null values recursively."""
    assert not is_supported_plist_value(None)
    assert not is_supported_plist_value(["group.dev.example", None])
    assert not is_supported_plist_value({"com.apple.mail": None})
