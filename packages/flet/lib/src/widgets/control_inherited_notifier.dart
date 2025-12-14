import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/theme.dart';

/// InheritedNotifier for a [Control].
///
/// Used to rebuild a control subtree when the
/// corresponding [Control] (a [ChangeNotifier]) changes.
class ControlInheritedNotifier extends InheritedNotifier<Control> {
  const ControlInheritedNotifier({
    super.key,
    super.notifier,
    required super.child,
  }) : super();

  /// Establishes a dependency on the nearest [ControlInheritedNotifier] and
  /// returns its [Control].
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

/// Wraps [builder] with [ControlInheritedNotifier], unless the control opts out.
///
/// If `"skip_inherited_notifier"` internal is `true`, this returns
/// [builder] unwrapped to preserve historical semantics.
Widget withControlNotifier(Control control, WidgetBuilder builder) {
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

/// Convenience wrapper that applies both:
/// - [withControlNotifier]
/// - [withControlTheme]
Widget withControlContext(
  Control control,
  WidgetBuilder builder,
) {
  return Builder(builder: (context) {
    final child = withControlNotifier(control, builder);
    return withControlTheme(control, context, child);
  });
}

/// Applies per-control theming (`theme`, `dark_theme`, `theme_mode`) to `child`.
///
/// Returns `child` unchanged when:
/// - `control` is the page/root control
/// - `"skip_inherited_notifier"` internal is `true`
/// - no `theme`/`dark_theme` is set and `theme_mode` is `null`
///
/// Parameters:
/// - `control`: the control whose per-control theme (if any) will be applied.
/// - `context`: used to access `FletBackend` and the ambient `Theme`.
/// - `child`: the widget subtree to wrap with the per-control `Theme`.
Widget withControlTheme(Control control, BuildContext context, Widget child) {
  if (control == FletBackend.of(context).page) return child;

  if (control.internals?["skip_inherited_notifier"] == true) return child;

  final hasNoThemes =
      control.get("theme") == null && control.get("dark_theme") == null;
  final themeMode = control.getThemeMode("theme_mode");
  if (hasNoThemes && themeMode == null) return child;

  final ThemeData? parentTheme = (themeMode == null) ? Theme.of(context) : null;

  /// Converts [ThemeMode] to [Brightness] used by [Control.getTheme].
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

extension ControlContextBuilder on Control {
  /// Builds a widget under this control's standard "control context":
  /// [ControlInheritedNotifier] + per-control theme wrapping.
  Widget buildInControlContext(WidgetBuilder builder) {
    return withControlContext(this, builder);
  }
}
