---
title: "flet build"
---

import CliBuild from '@site/.crocodocs/cli-build.mdx';

<CliBuild />

## Log formats

`--log-format` (or the `FLET_CLI_LOG_FORMAT` environment variable) selects how `flet build`
reports its progress:

* `rich` (default) - a live spinner shows the current step.
* `plain` - plain text lines without colors or animation, same as `--no-rich-output`.
* `github` - `plain` output plus [GitHub Actions workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands):
  each build step (Flutter SDK, app shell, Python app packaging, icons, splash screens,
  `flutter build`, macOS signing and notarization, ...) is a collapsible group, and
  warnings and errors become annotations in the job summary.

```
::group::Generating app icons
::warning title=App icon,file=assets/icon.png::icon source is 512x256, not square. ...
[13:01:29] Generated app icons OK
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
