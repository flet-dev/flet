---
class_name: "flet.StoragePaths"
examples: "services/storage_paths"
title: "StoragePaths"
---

import {ClassMembers, ClassSummary, CodeExample} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

:::note Relationship to the `FLET_APP_STORAGE_*` environment variables
`StoragePaths` exposes the raw platform directories. The pre-created
[`FLET_APP_STORAGE_*`](../reference/environment-variables.md#flet_app_storage_data) env vars map onto
them: `FLET_APP_STORAGE_CACHE` = `get_application_cache_directory()`, `FLET_APP_STORAGE_TEMP` =
`get_temporary_directory()`, and `FLET_APP_STORAGE_DATA` = a flet-owned **`data` subdirectory** of
`get_application_support_directory()` (which is also the app's current working directory). Prefer the
env vars for app storage; use `StoragePaths` when you need a different platform directory (e.g.
Documents or Downloads).
:::

## Examples

<CodeExample path={frontMatter.examples + '/storage_paths/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
