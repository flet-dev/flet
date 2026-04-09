---
name: run-unit-tests
description: Use when asked to run unit tests.
---

This skill is used to run unit tests of the Python part of Flet framework.

## Instructions

Run the following command to run `flet` package unit tests:

```
uv run --group test pytest packages/flet/tests
```

The directory in that commend is relative to `{root}/sdk/python`.
