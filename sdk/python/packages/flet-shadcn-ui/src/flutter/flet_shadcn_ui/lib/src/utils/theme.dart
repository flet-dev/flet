import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

/// Builds the [ShadThemeData] described by a `flet_shadcn_ui.Theme` control.
///
/// When `brightness` is not set, the brightness of the enclosing Material
/// theme is used, so the scheme follows the page's light/dark mode.
ShadThemeData parseShadThemeData(Control control, BuildContext context) {
  final brightness =
      control.getBrightness("brightness") ?? Theme.of(context).brightness;
  return ShadThemeData(
    brightness: brightness,
    colorScheme: ShadColorScheme.fromName(
      control.getString("color_scheme", "slate")!,
      brightness: brightness,
    ),
    radius: control.getBorderRadius("radius"),
  );
}

/// Wraps [child] in a default [ShadTheme] if [context] has none.
///
/// Every Shadcn widget looks up [ShadTheme.of] and throws without one, and
/// Flet has no way to put a [ShadTheme] above the page, so each control
/// provides a slate theme matching the page brightness as a fallback.
Widget withShadTheme(BuildContext context, Widget child) {
  if (ShadTheme.maybeOf(context) != null) return child;
  final brightness = Theme.of(context).brightness;
  return ShadTheme(
    data: ShadThemeData(
      brightness: brightness,
      colorScheme: ShadColorScheme.fromName("slate", brightness: brightness),
    ),
    child: child,
  );
}

/// Gives [child] the theme's muted foreground color.
///
/// shadcn_ui's `muted` text style has no color; most widgets add one, but
/// some (the ShadRadio sublabel, ShadContextMenuItem trailing text) use it as
/// is, and Flutter paints color-less text white. Wrap those children with this.
Widget? withMutedColor(BuildContext context, Widget? child) {
  if (child == null) return null;
  return DefaultTextStyle.merge(
    style: TextStyle(color: ShadTheme.of(context).colorScheme.mutedForeground),
    child: child,
  );
}
