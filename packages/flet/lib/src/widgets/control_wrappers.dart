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

Widget wrapWithControlTheme(
  Control control,
  BuildContext context,
  Widget child, {
  bool isRootControl = false,
  bool respectSkipInheritedNotifier = true,
}) {
  if (isRootControl) return child;
  if (respectSkipInheritedNotifier &&
      control.internals?["skip_inherited_notifier"] == true) {
    return child;
  }

  final hasNoThemes =
      control.get("theme") == null && control.get("dark_theme") == null;
  final themeMode = control.getThemeMode("theme_mode");
  if (hasNoThemes && themeMode == null) {
    return child;
  }

  final ThemeData? parentTheme = (themeMode == null) ? Theme.of(context) : null;

  Widget buildTheme(Brightness? brightness) {
    final themeProp = brightness == Brightness.dark ? "dark_theme" : "theme";
    final themeData = parseTheme(control.get(themeProp), context, brightness,
        parentTheme: parentTheme);
    return Theme(data: themeData, child: child);
  }

  if (themeMode == ThemeMode.system) {
    final brightness = context.select<FletBackend, Brightness>(
        (backend) => backend.platformBrightness);
    return buildTheme(brightness);
  } else if (themeMode == ThemeMode.light) {
    return buildTheme(Brightness.light);
  } else if (themeMode == ThemeMode.dark) {
    return buildTheme(Brightness.dark);
  } else {
    return buildTheme(parentTheme?.brightness);
  }
}
