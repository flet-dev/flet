"""
Positionals and options may be interleaved on every supported Python.

Before Python 3.12.7 and 3.13.1 (CPython gh-59317), `argparse` gave an optional
positional its default as soon as the positionals typed before an option ran
out. `flet debug ios --device-id 123 app` then failed with
`unrecognized arguments: app` (#6840), and so did `flet build apk --org X app`.
"""

import pytest

from flet_cli.cli import _PositionalsFixArgumentParser, parse_command_line

APP = "examples/app"


class TestPositionalAfterOption:
    """A positional typed after an option still fills its slot."""

    @pytest.mark.parametrize(
        ("argv", "expected"),
        [
            pytest.param(
                ["debug", "ios", "--device-id", "X", APP, "-v"],
                {
                    "platform": "ios",
                    "device_id": "X",
                    "python_app_path": APP,
                    "verbose": 1,
                },
                id="debug-path-after-option",
            ),
            pytest.param(
                ["debug", "ios", APP, "--device-id", "X"],
                {"platform": "ios", "device_id": "X", "python_app_path": APP},
                id="debug-path-before-option",
            ),
            pytest.param(
                ["debug", "--device-id", "X", "ios", APP],
                {"platform": "ios", "device_id": "X", "python_app_path": APP},
                id="debug-options-first",
            ),
            pytest.param(
                ["debug", "web", "--route", "/settings", APP],
                {"platform": "web", "route": "/settings", "python_app_path": APP},
                id="debug-path-after-route",
            ),
            pytest.param(
                ["build", "apk", "--org", "com.example", APP],
                {
                    "target_platform": "apk",
                    "org_name": "com.example",
                    "python_app_path": APP,
                },
                id="build-path-after-option",
            ),
            pytest.param(
                ["build", "ipa", "-v", APP],
                {"target_platform": "ipa", "verbose": 1, "python_app_path": APP},
                id="build-path-after-flag",
            ),
            pytest.param(
                ["test", "macos", "-k", "smoke", APP],
                {
                    "platform": "macos",
                    "pytest_keyword": "smoke",
                    "python_app_path": APP,
                },
                id="test-path-after-option",
            ),
            pytest.param(
                ["emulators", "start", "--cold", "pixel"],
                {"action": "start", "emulator": "pixel", "cold": True},
                id="emulators-name-after-option",
            ),
            pytest.param(
                ["run", "app.py", "--web", "foo"],
                {"script": "app.py", "web": True, "script_args": ["foo"]},
                id="run-script-arg-after-option",
            ),
        ],
    )
    def test_is_parsed(self, argv, expected):
        args = vars(parse_command_line(argv))

        assert {key: args[key] for key in expected} == expected


class TestOtherPositionals:
    """Omitted and surplus positionals are handled as before."""

    def test_omitted_positionals_keep_their_defaults(self):
        args = parse_command_line(["debug", "--show-devices"])

        assert args.platform is None
        assert args.python_app_path == "."

    def test_only_the_surplus_positional_is_reported(self, capsys):
        with pytest.raises(SystemExit):
            parse_command_line(["debug", "ios", "--device-id", "X", APP, "extra"])

        err = capsys.readouterr().err
        assert "unrecognized arguments: extra" in err
        assert APP not in err


class TestBackportedParser:
    """
    The backport fills a later optional positional after an option, and is a
    no-op on interpreters that already carry the upstream fix.
    """

    @pytest.fixture
    def parser(self):
        parser = _PositionalsFixArgumentParser()
        parser.add_argument("first", nargs="?")
        parser.add_argument("-x")
        parser.add_argument("second", nargs="?")
        return parser

    @pytest.mark.parametrize(
        ("argv", "expected"),
        [
            pytest.param(["1", "-x", "2", "3"], ("1", "2", "3"), id="interleaved"),
            pytest.param(["1", "3", "-x", "2"], ("1", "2", "3"), id="adjacent"),
            pytest.param(["-x", "2", "1", "3"], ("1", "2", "3"), id="option-first"),
            pytest.param(["1", "-x", "2"], ("1", "2", None), id="second-omitted"),
            pytest.param(["-x", "2"], (None, "2", None), id="both-omitted"),
        ],
    )
    def test_parse(self, parser, argv, expected):
        args = parser.parse_args(argv)

        assert (args.first, args.x, args.second) == expected
