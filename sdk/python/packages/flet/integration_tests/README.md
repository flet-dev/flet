# Flet tests

Running tests with output and log debug output:

```
uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG packages/flet/integration_tests
```

Running tests on iOS simulator:

```
FLET_TEST_DEVICE=<simulator-guid> uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG packages/flet/integration_tests
```

Running tests on Android simulator:

```
FLET_TEST_DEVICE=<simulator-name> FLET_TEST_PLATFORM=android uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG packages/flet/integration_tests
```