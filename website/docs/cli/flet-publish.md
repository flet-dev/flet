---
title: "flet publish"
---

import CliPublish from '@site/.crocodocs/cli-publish.mdx';

<CliPublish />

:::note[`--pre` vs `--python-version`]
`--pre` allows **micropip** to resolve pre-release versions of *Python
packages* at runtime. It is unrelated to which CPython/Pyodide release is
bundled. To choose a pre-release Python interpreter (e.g. 3.15 once it
appears in the supported list), name it explicitly via `--python-version` or
`[project].requires-python` in `pyproject.toml` — see
[Choosing a Python version](../publish/index.md#choosing-a-python-version).
:::
