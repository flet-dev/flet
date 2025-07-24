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

Running test to create golden images:

```
FLET_TEST_GOLDEN=1 uv run pytest -s -o log_cli=true -o log_cli_level=INFO packages/flet/integration_tests/test_controls.py
```

Environment variables:

`FLET_TEST_PLATFORM`

`FLET_TEST_DEVICE`

`FLET_TEST_GOLDEN`