---
title: "iOS: per-method signing settings now override top-level ones"
---

# iOS: per-method signing settings now override top-level ones

:::note
This guide is accurate as of Flet 1.0.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 1.0.0 flips the precedence between the top-level `[tool.flet.ios]` signing
keys and their per-method counterparts in
[`[tool.flet.ios.export_methods.<method>]`](../../../publish/ios.md#export-methods)
subtables. This affects four settings: `provisioning_profile`,
`signing_certificate`, `export_options`, and `team_id`.

- **Before**: the top-level key won — a per-method value was used only when no
  top-level key was set, making the subtables useless whenever both were
  configured.
- **Now**: the per-method value wins for the export method being built; the
  top-level key is the shared fallback across methods. CLI options still beat
  both.

This matches the rule used by the macOS
[per-lane signing subtables](../../../publish/macos.md#per-lane-settings).

## Symptoms

No error is raised — the change is silent. An `ipa` build where **both** forms
of the same key are set (for example, a top-level `provisioning_profile` *and*
one inside an `export_methods` subtable) is now signed with the per-method
value where it previously used the top-level one, which can surface later as a
profile or certificate mismatch when installing or uploading the build.

Projects that use only one of the two forms are unaffected.

## Migration guide

If a per-method value was shadowed by a top-level key and you relied on the
top-level one winning, remove the entry you don't want from the
`export_methods` subtable — a per-method entry now means "use this when
building this method":

```toml
[tool.flet.ios]
# shared fallback for all export methods
signing_certificate = "Apple Development"

[tool.flet.ios.export_methods.app-store-connect]
# overrides the fallback for app-store-connect builds only
signing_certificate = "Apple Distribution"
```

### No action needed for

- Projects that set signing keys in only one place — top-level *or*
  per-method.
- Builds driven entirely by CLI options, which keep the highest precedence.

## Timeline

- Changed in: `1.0.0`

## References

- Docs: [iOS export methods](../../../publish/ios.md#export-methods)
- Release notes: [Flet 1.0.0](../../release-notes.md)
