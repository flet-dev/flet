---
title: "macOS: the .app is named after the product name"
---

# macOS: the .app is named after the product name

:::note
This guide is accurate as of Flet 1.1.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Starting with Flet 1.1.0, when no [artifact name](../../../publish/index.md#artifact-name)
is set, `flet build macos` names the `.app` bundle after the
[product name](../../../publish/index.md#product-name). Previously it used the
project name. For example, with:

```toml
[project]
name = "acme_notes"

[tool.flet]
product = "Acme Notes"
```

the build produces `build/macos/Acme Notes.app` (was `build/macos/acme_notes.app`).
A `/` or `:` in the product name is replaced with `-`, because macOS file names
can't contain them.

Other platforms are unchanged: the Windows `.exe` and the Linux binary are still
named after the project name.

## Background

On macOS the `.app` file name is the name users see. Finder, the Applications
folder, Launchpad, Spotlight and the Dock show it, and the build template sets
`CFBundleName` to it, so the bold app menu, "About …" and "Quit …" show it too.
The product name only appeared in window titles and the About panel, so an app
named "Acme Notes" showed up as "acme_notes" everywhere else
([#6966](https://github.com/flet-dev/flet/issues/6966)).

## Who is affected

macOS apps that set a product name (`[tool.flet].product` or `--product`) but no
artifact name (`--artifact`, `[tool.flet.macos].artifact` or
`[tool.flet].artifact`). Apps that set an artifact name, or no product name, keep
their `.app` name.

For affected apps:

- Scripts, CI steps and packaging (DMG, `.pkg`, notarization) that refer to
  `build/macos/<project name>.app` must use the new name.
- The app's bundle ID doesn't change, so macOS still treats the new build as the
  same app. But users who install updates by dragging the `.app` into
  Applications get the new copy next to the old one, rather than replacing it,
  and need to delete the old copy.

## Migration guide

To keep the previous name, set the macOS artifact name to the project name:

```toml
[tool.flet.macos]
artifact = "acme_notes"
```

or pass `--artifact acme_notes` to `flet build macos`.

To adopt the new name, update the paths in your scripts. If your app is already
installed on users' Macs, tell them to delete the old copy after installing the
renamed one.

### No action needed for

- Windows, Linux, Android, iOS and web apps.
- macOS apps that already set an artifact name.

## Timeline

- Changed in: `1.1.0`

## References

- Docs: [Artifact name](../../../publish/index.md#artifact-name),
  [Product name](../../../publish/index.md#product-name)
- Issue: [#6966](https://github.com/flet-dev/flet/issues/6966)
- Pull request: [#6967](https://github.com/flet-dev/flet/pull/6967)
- Release notes: [Flet 1.1.0](../../release-notes.md)
