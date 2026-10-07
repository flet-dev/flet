---
title: "Extensions: Material and Cupertino now come from material_ui and cupertino_ui"
---

# Extensions: Material and Cupertino now come from `material_ui` and `cupertino_ui`

:::note
This guide is accurate as of Flet 1.1.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Starting with Flet 1.1.0, Flet's Dart code (the `flet` package, the built-in
extensions, the desktop and web client, and the `flet build` template) imports
`package:material_ui/material_ui.dart` and `package:cupertino_ui/cupertino_ui.dart`
instead of `package:flutter/material.dart` and `package:flutter/cupertino.dart`.

The new packages redeclare every Material and Cupertino type, so the Dart
compiler treats, for example, `material_ui`'s `ThemeData` and the Flutter SDK's
`ThemeData` as unrelated types. Flet's Dart helpers that take or return Material
or Cupertino types now use the `material_ui` and `cupertino_ui` ones, and every
Flet app renders inside `material_ui`'s `MaterialApp`.

The Dart code of an extension that uses Material or Cupertino has to migrate
too, or it fails to compile or to render under Flet 1.1.0.

## Background

The Material and Cupertino libraries in the Flutter SDK stopped receiving
changes in Flutter 3.44. Flutter 3.47, which Flet 1.1.0 is built with, is the
first release with version 1.0 of the standalone
[`material_ui`](https://pub.dev/packages/material_ui) and
[`cupertino_ui`](https://pub.dev/packages/cupertino_ui) packages, where
development continues. The SDK libraries are scheduled for deprecation in an
upcoming stable release. See Flutter's
[migration guide](https://docs.flutter.dev/release/breaking-changes/material-ui-and-cupertino-ui).

Both packages re-export `package:flutter/widgets.dart`, so everything at the
widgets, painting, services and `dart:ui` level is shared between the two
worlds. Only the Material and Cupertino types themselves are duplicated:

| Shared (safe to pass across) | Duplicated (must come from `material_ui` / `cupertino_ui`) |
|---|---|
| `Color`, `TextStyle`, `IconData`, `EdgeInsets`, `BoxDecoration`, `BorderRadius`, `Alignment`, `Brightness`, `Duration`, `WidgetState` and `WidgetStateProperty` (including the `MaterialState*` aliases) | `ThemeData`, `ColorScheme`, `TextTheme`, `ButtonStyle`, `InputBorder`, every `*ThemeData`, `TimeOfDay`, `VisualDensity`, `ThemeMode`, `MaterialColor`, `Icons`, `CupertinoIcons`, `CupertinoThemeData`, `MaterialLocalizations`, and every Material and Cupertino widget |

## Who is affected

- **Extension authors** whose Dart code imports `package:flutter/material.dart`
  or `package:flutter/cupertino.dart`. In particular:
  - code that passes `Theme.of(context)` or another Material value into Flet
    helpers such as `parseColor`, `parseTextStyle`, `parseBorder` or
    `parseButtonStyle`, or the matching `control.get*` methods that take a
    `ThemeData`;
  - code that puts Flet-parsed Material objects, such as a `ButtonStyle`, an
    `InputBorder` or a `TimeOfDay`, into widgets;
  - code that uses `Icons` or `CupertinoIcons` through
    `package:flet/flet.dart`, which no longer re-exports them;
  - code that renders SDK Material widgets, such as `TextField`, `InkWell`,
    `ListTile` or `DropdownButton`, directly or through a Flutter package.
- **Custom build templates** (`--template` or
  [`[tool.flet.template]`](../../../publish/index.md#build-template)) with their
  own Dart code.
- **Flutter apps that embed the `flet` package** from pub.dev.

Python-only apps are not affected. Extensions whose Dart code only uses
`package:flutter/widgets.dart` keep working unchanged.

## Migration guide

### 1. Update the dependencies

In your extension's `pubspec.yaml`:

```yaml
environment:
  flutter: ">=3.47.0"

dependencies:
  flet: ^1.1.0
  material_ui: ^1.6.0
  cupertino_ui: ^1.1.2 # only if you use Cupertino widgets
```

In its `pyproject.toml`, require `flet>=1.1.0`.

### 2. Migrate the imports

Run Flutter's migration from your extension's Flutter package:

```
dart fix --apply --code=migrate_design_widgets
```

The fix rewrites `import` directives only, and plain `dart fix` doesn't apply
it. If it adds `material_ui: any` or `cupertino_ui: any` to `pubspec.yaml`,
replace them with the constraints above. Then fix by hand what it skips:

- `export` directives that point at `package:flutter/material.dart` or
  `package:flutter/cupertino.dart`;
- localization delegates from `flutter_localizations`: use
  `GlobalMaterialLocalizations.delegates` from `material_ui`, which includes the
  Cupertino and widgets delegates;
- files that used `Icons` or `CupertinoIcons` through `package:flet/flet.dart`:
  import `material_ui` or `cupertino_ui` there.

If a file only uses widgets-level APIs, import `package:flutter/widgets.dart`
instead.

### 3. Check your Flutter dependencies

A Flutter package your extension wraps can still be built on the SDK's Material
library. What that means depends on how the package uses it:

- **Its API takes or returns Material types** (for example `data_table_2` 2.x
  and its `DataCell`): your code no longer compiles against it. Upgrade to a
  release built on `material_ui` (`data_table_2` 3.x, `shimmer` 4.x), or keep
  Material values out of the calls.
- **It renders SDK Material widgets** such as `TextField`, `InkWell`,
  `ListTile`, `Checkbox` or `DropdownButton`: these widgets look for SDK
  `Material`, `MaterialLocalizations` and `ScaffoldMessenger` ancestors, and a
  Flet app only provides the `material_ui` ones. A widget the package wraps in
  its own SDK `Material` keeps working; the others fail at runtime. Upgrade
  the package, or fork or vendor it and run the same `dart fix` on the copy. A
  git dependency on a fork only works for extensions that aren't published to
  pub.dev.
- **It only reads `Theme.of(context)`**: it renders with Flutter's default light
  theme instead of your app's theme and dark mode. Pass explicit colors or
  widgets where the package allows it.
- **It only imports the SDK library internally**: nothing to do.

Flet 1.1.0 doesn't install Flutter's `MaterialUiCompatibilityBridge`.

### 4. Test

Run your extension in a dark theme, in a non-English locale, and in both a
debug and a release build. In debug builds, a leftover SDK widget that misses
an ancestor fails with one of the errors below. Release builds skip most of
those checks, so the same widget can render with no ink effects or with
Flutter's default theme instead. A missing localization still throws in
release builds; when that happens while building a widget, it shows up as a
grey error box.

### 5. Publish a new major version

Code that passes Material or Cupertino types to Flet can't support Flet 1.0 and
1.1 in the same release, so publish the migrated extension as a new major
version. You can still publish fixes for Flet 1.0 users from a release that
requires `flet<1.1`.

## Errors you might see

At compile time:

- `The argument type 'ThemeData (where ThemeData is defined in .../flutter/lib/src/material/theme_data.dart)' can't be assigned to the parameter type 'ThemeData (where ThemeData is defined in .../material_ui-1.6.0/lib/src/theme_data.dart)'`,
  or the same for another Material type. It can also look like
  `The argument type 'ButtonStyle' can't be assigned to the parameter type 'ButtonStyle?'`.
- `The name 'Icons' is defined in the libraries 'package:flutter/src/material/icons.dart' and 'package:material_ui/src/icons.dart'`.
- `The name 'GlobalMaterialLocalizations' is defined in the libraries 'package:flutter_localizations/...' and 'package:material_ui/...'`.

At runtime, in debug builds:

- `No Material widget found.`
- `No MaterialLocalizations found.` or `No CupertinoLocalizations found.`
- `No ScaffoldMessenger widget found.`

Some problems don't raise an error:

- SDK widgets that read `Theme.of(context)` get Flutter's default light theme.
- A `TimeOfDay` that your extension sends through `updateProperties()` or
  `triggerEvent()` must be `material_ui`'s, or it reaches Python empty.
  `control.get<TimeOfDay>()` returns `material_ui`'s `TimeOfDay`.
- A `CupertinoDynamicColor` from one library isn't resolved by the other, so
  dark mode shows its light color.

## Custom build templates

Migrate the template's `lib/main.dart` the same way: import
`package:material_ui/material_ui.dart` and add `material_ui` and `cupertino_ui`
to its `pubspec.yaml`. Flet's template pins them to exact versions, because
generated projects have no lock file.

## Timeline

- Changed in: `1.1.0`

## References

- Flutter: [Migrate to standalone material_ui and cupertino_ui packages](https://docs.flutter.dev/release/breaking-changes/material-ui-and-cupertino-ui)
- Flutter issue: [flutter/flutter#191448](https://github.com/flutter/flutter/issues/191448)
- Docs: [User extensions](../../../extend/user-extensions.md)
- Release notes: [Flet 1.1.0](../../release-notes.md)
