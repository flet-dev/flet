import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/theme.dart';
import 'control_inherited_notifier.dart';

Widget withControlInheritedNotifier(Control control, WidgetBuilder builder) {
  if (control.internals?["skip_inherited_notifier"] == true) {
    return Builder(builder: builder);
  }

  return ControlInheritedNotifier(
    notifier: control,
    child: Builder(builder: (context) {
      ControlInheritedNotifier.of(context);
      return builder(context);
    }),
  );
}

Widget wrapWithControlInheritedNotifierAndTheme(
    Control control, WidgetBuilder builder) {
  return Builder(
      builder: (context) => wrapWithControlTheme(
          control, context, withControlInheritedNotifier(control, builder)));
}

Widget wrapWithControlTheme(
    Control control, BuildContext context, Widget child) {
  // skip root/page control
  if (control == FletBackend.of(context).page) return child;

  // Preserve ControlWidget semantics: if a control opts out of
  // ControlInheritedNotifier, it also skips per-control theme wrapping.
  if (control.internals?["skip_inherited_notifier"] == true) {
    return child;
  }

  final hasNoThemes =
      control.get("theme") == null && control.get("dark_theme") == null;
  final themeMode = control.getThemeMode("theme_mode");
  if (hasNoThemes && themeMode == null) {
    return child;
  }

  final ThemeData? parentTheme = (themeMode == null) ? Theme.of(context) : null;

  /// Converts ThemeMode to Brightness
  Brightness? themeModeToBrightness(ThemeMode? mode) {
    switch (mode) {
      case ThemeMode.light:
        return Brightness.light;
      case ThemeMode.dark:
        return Brightness.dark;
      case ThemeMode.system:
        return context.select<FletBackend, Brightness>(
          (backend) => backend.platformBrightness,
        );
      case null:
        return parentTheme?.brightness;
    }
  }

  Widget buildTheme(Brightness? brightness) {
    final themeData = control.getTheme(
      brightness == Brightness.dark ? "dark_theme" : "theme",
      context,
      brightness,
      parentTheme: parentTheme,
    );
    return Theme(data: themeData, child: child);
  }

  final brightness = themeModeToBrightness(themeMode);
  return buildTheme(brightness);
}
