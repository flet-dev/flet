import 'package:collection/collection.dart';
import 'package:material_ui/material_ui.dart';
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

/// Wraps [builder] in the control's [ControlInheritedNotifier], with the
/// control's [Theme] (`theme`, `dark_theme`, `theme_mode`) inside it, so theme
/// changes rebuild like any other property change.
///
/// [builder] runs below that [Theme], so `Theme.of(context)` returns the
/// control's theme.
///
/// Controls with the `"skip_inherited_notifier"` internal set to `true` get
/// neither the notifier nor the per-control theme.
Widget withControlContext(Control control, WidgetBuilder builder) {
  if (control.internals?["skip_inherited_notifier"] == true) {
    return Builder(builder: builder);
  }

  return ControlInheritedNotifier(
    notifier: control,
    child: _ControlContext(control: control, builder: builder),
  );
}

/// Rebuilds on every change of [control] and applies its per-control theme.
class _ControlContext extends StatefulWidget {
  final Control control;
  final WidgetBuilder builder;

  const _ControlContext({required this.control, required this.builder});

  @override
  State<_ControlContext> createState() => _ControlContextState();
}

class _ControlContextState extends State<_ControlContext> {
  /// Keeps the control's subtree (focus, scroll position, animations, ...)
  /// when its [Theme] wrapper is added or removed: the keyed [Builder] is
  /// moved under or out of the [Theme] instead of being rebuilt from scratch.
  final _childKey = GlobalKey();

  // Last parsed theme and the inputs it was parsed from.
  ThemeData? _themeData;
  dynamic _themeValue;
  Brightness? _brightness;
  ThemeData? _ambientTheme;
  bool _inheritsAmbientTheme = false;

  static const _equality = DeepCollectionEquality();

  @override
  Widget build(BuildContext context) {
    ControlInheritedNotifier.of(context);
    final child = Builder(key: _childKey, builder: widget.builder);
    final themeData = _resolveTheme(context);
    return themeData != null ? Theme(data: themeData, child: child) : child;
  }

  /// Returns the control's [ThemeData], or `null` when it has no per-control
  /// theme (no `theme`/`dark_theme` and no `theme_mode`) or is the page.
  ///
  /// The parsed theme is reused while the theme property, brightness and
  /// ambient theme stay the same, so updates of other properties don't parse
  /// the theme again.
  ThemeData? _resolveTheme(BuildContext context) {
    final control = widget.control;
    if (control == FletBackend.of(context).page) return null;

    final themeMode = control.getThemeMode("theme_mode");
    if (themeMode == null &&
        control.get("theme") == null &&
        control.get("dark_theme") == null) {
      _themeData = null;
      return null;
    }

    final ambientTheme = Theme.of(context);
    final brightness = switch (themeMode) {
      ThemeMode.light => Brightness.light,
      ThemeMode.dark => Brightness.dark,
      ThemeMode.system => context.select<FletBackend, Brightness>(
          (backend) => backend.platformBrightness),
      null => ambientTheme.brightness,
    };
    final propertyName = brightness == Brightness.dark ? "dark_theme" : "theme";
    final themeValue = control.get(propertyName);
    final inheritsAmbientTheme = themeMode == null;

    // Theme maps are patched in place, so compare against a copy by value.
    final cached = _themeData;
    if (cached != null &&
        brightness == _brightness &&
        inheritsAmbientTheme == _inheritsAmbientTheme &&
        (identical(ambientTheme, _ambientTheme) ||
            ambientTheme == _ambientTheme) &&
        _equality.equals(themeValue, _themeValue)) {
      return cached;
    }

    _brightness = brightness;
    _inheritsAmbientTheme = inheritsAmbientTheme;
    _ambientTheme = ambientTheme;
    _themeValue = _deepCopy(themeValue);
    return _themeData = parseTheme(themeValue, context, brightness,
        parentTheme: inheritsAmbientTheme ? ambientTheme : null);
  }

  static dynamic _deepCopy(dynamic value) {
    if (value is Map) {
      return value.map((k, v) => MapEntry(k, _deepCopy(v)));
    }
    if (value is List) {
      return value.map(_deepCopy).toList();
    }
    return value;
  }
}

extension ControlContextBuilder on Control {
  /// Builds a widget under this control's standard "control context":
  /// [ControlInheritedNotifier] + per-control theme wrapping.
  ///
  /// This is primarily used by [ControlWidget] and any "special" controls that
  /// must subclass a Flutter widget (e.g. a control that must be a `Tab`) but
  /// still need the same wrapper behavior as a normal `ControlWidget`.
  Widget buildInControlContext(WidgetBuilder builder) {
    return withControlContext(this, builder);
  }
}
