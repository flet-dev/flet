---
title: "flet build"
---

import CliBuild from '@site/.crocodocs/cli-build.mdx';

<CliBuild />

## Log formats

`--log-format` (or the `FLET_CLI_LOG_FORMAT` environment variable) selects how `flet build`
reports its progress:

* `rich` - a live spinner shows the current step.
* `plain` - plain text lines without colors, animation, timestamps or wrapping (log viewers wrap long lines themselves), same as `--no-rich-output`.
* `github` - `plain` output plus [GitHub Actions workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands):
  each build step (Flutter SDK, app shell, Python app packaging, icons, splash screens,
  `flutter build`, macOS signing and notarization, ...) is a collapsible group, and
  warnings and errors become annotations in the job summary.

The default is `github` when `GITHUB_ACTIONS=true`, otherwise `rich`.
Use `--log-format` or `FLET_CLI_LOG_FORMAT` to override it.
`--no-rich-output` and `FLET_CLI_NO_RICH_OUTPUT` select `plain` unless the
selected format is explicitly `plain` or `github`.

```
::group::Generating app icons
::warning title=App icon,file=assets/icon.png::icon source is 512x256, not square. ...
Generated app icons OK
::endgroup::
::group::Building web app
Could not find an option named "--bogus-flag".
::error title=Building web app::Error building Flet app - see the log of failed command above.
::endgroup::
::group::Running Flutter doctor
...
::endgroup::
```

The lines are easy to parse for other CI systems and build services, too.
