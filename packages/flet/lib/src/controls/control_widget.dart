import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/keys.dart';
import '../utils/numbers.dart';
import '../utils/theme.dart';
import '../widgets/control_inherited_notifier.dart';
import '../widgets/error.dart';

class ControlWidget extends StatelessWidget {
  final Control control;

  const ControlWidget({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    ControlKey? controlKey = control.getKey("key");
    Key? key;
    if (controlKey is ControlScrollKey) {
      key = GlobalKey();
      FletBackend.of(context).globalKeys[controlKey.toString()] =
          key as GlobalKey;
    } else if (controlKey != null) {
      key = ValueKey(controlKey.value);
    }

    Widget? widget;
    if (control.internals?["skip_inherited_notifier"] == true) {
      for (var extension in FletBackend.of(context).extensions) {
        widget = extension.createWidget(key, control);
        if (widget != null) return widget;
      }
      widget = ErrorControl("Unknown control: ${control.type}");
    } else {
      widget = ControlInheritedNotifier(
        notifier: control,
        child: Builder(builder: (context) {
          ControlInheritedNotifier.of(context);

          Widget? cw;
          for (var extension in FletBackend.of(context).extensions) {
            cw = extension.createWidget(key, control);
            if (cw != null) return cw;
          }

          return ErrorControl("Unknown control: ${control.type}");
        }),
      );
    }

    // Return original widget if no theme is defined
    final isRootControl = control == FletBackend.of(context).page;
    final hasNoThemes = control.getString("theme") == null &&
        control.getString("dark_theme") == null;
    final themeMode = control.getThemeMode("theme_mode");

    if (isRootControl || (hasNoThemes && themeMode == null)) {
      return widget;
    }

    // Wrap in Theme widget
    final ThemeData? parentTheme =
        (themeMode == null) ? Theme.of(context) : null;

    Widget buildTheme(Brightness? brightness) {
      final themeProp = brightness == Brightness.dark ? "dark_theme" : "theme";
      final themeData = parseTheme(control.get(themeProp), context, brightness,
          parentTheme: parentTheme);
      return Theme(data: themeData, child: widget!);
    }

    if (themeMode == ThemeMode.system) {
      final brightness = context.select<FletBackend, Brightness>(
        (backend) => backend.platformBrightness,
      );
      return buildTheme(brightness);
    } else if (themeMode == ThemeMode.light) {
      return buildTheme(Brightness.light);
    } else if (themeMode == ThemeMode.dark) {
      return buildTheme(Brightness.dark);
    } else {
      return buildTheme(parentTheme?.brightness);
    }
  }
}
