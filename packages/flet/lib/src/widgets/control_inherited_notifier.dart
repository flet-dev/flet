import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/theme.dart';

/// InheritedNotifier for Control.
class ControlInheritedNotifier extends InheritedNotifier<Control> {
  const ControlInheritedNotifier({
    super.key,
    super.notifier,
    required super.child,
  }) : super();

  static Control? of(BuildContext context) {
    return context
        .dependOnInheritedWidgetOfExactType<ControlInheritedNotifier>()
        ?.notifier;
  }

  @override
  bool updateShouldNotify(ControlInheritedNotifier oldWidget) {
    return notifier != oldWidget.notifier;
  }
}

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
  Control control,
  WidgetBuilder builder,
) {
  return Builder(builder: (context) {
    final child = withControlInheritedNotifier(control, builder);
    return wrapWithControlTheme(control, context, child);
  });
}

Widget wrapWithControlTheme(
    Control control, BuildContext context, Widget child) {
  // skip root/page control
  if (control == FletBackend.of(context).page) return child;

  // if a control opts out of ControlInheritedNotifier,
  // it also skips per-control theme wrapping.
  if (control.internals?["skip_inherited_notifier"] == true) return child;

  final hasNoThemes =
      control.get("theme") == null && control.get("dark_theme") == null;
  final themeMode = control.getThemeMode("theme_mode");
  if (hasNoThemes && themeMode == null) return child;

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

  return buildTheme(themeModeToBrightness(themeMode));
}
