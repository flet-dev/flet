# Flet tests

Running **all** tests in directory with output and log debug output:

```
uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG packages/flet/integration_tests
```

Running **single file** tests with output and log debug output:

```
uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG packages/flet/integration_tests/controls/test_buttons.py
```

Running **single test** with output and log debug output:

```
uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG packages/flet/integration_tests/controls/test_buttons.py -k test_button_2
```

Running tests on iOS simulator:

```
FLET_TEST_DEVICE=<simulator-guid> uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG packages/flet/integration_tests
```

Running tests on Android simulator:

```
FLET_TEST_DEVICE=<simulator-name> FLET_TEST_PLATFORM=android uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG packages/flet/integration_tests
```

Running test to create golden images:

```
FLET_TEST_GOLDEN=1 uv run pytest -s -o log_cli=true -o log_cli_level=INFO packages/flet/integration_tests/test_controls.py
```

Environment variables:

`FLET_TEST_PLATFORM` - The platform on which tests are running: `macos`, `windows`, `linux`, `android` or `ios`. Desktop platforms are detected automatically if not specified.

`FLET_TEST_DEVICE` - The device to run tests on. For running tests on desktop: `macos`, `windows` or `linux` - detected automatically if not specified. To run on iOS, Android or a real device a device ID must be specified that can be obtained with `flutter devices` command.

`FLET_TEST_GOLDEN` - Run tests to take "golden" (expected) screenshots and writing them to a file system.

`FLET_TEST_SCREENSHOTS_PIXEL_RATIO` - device pixel ration to use to take screenshots. Default is 2.0.