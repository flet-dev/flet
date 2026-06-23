import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'spinkit.dart';

/// Canonical `SpinKit…` control type names, used to resolve the `spinner`
/// option (which is written without the `SpinKit` prefix, e.g. `Wave`).
const _spinKitTypes = <String>[
  "SpinKitRotatingPlain",
  "SpinKitDoubleBounce",
  "SpinKitWave",
  "SpinKitWanderingCubes",
  "SpinKitFadingFour",
  "SpinKitFadingCube",
  "SpinKitPulse",
  "SpinKitChasingDots",
  "SpinKitThreeBounce",
  "SpinKitCircle",
  "SpinKitCubeGrid",
  "SpinKitFadingCircle",
  "SpinKitRotatingCircle",
  "SpinKitFoldingCube",
  "SpinKitPumpingHeart",
  "SpinKitHourGlass",
  "SpinKitPouringHourGlass",
  "SpinKitPouringHourGlassRefined",
  "SpinKitFadingGrid",
  "SpinKitRing",
  "SpinKitRipple",
  "SpinKitDualRing",
  "SpinKitSpinningCircle",
  "SpinKitSpinningLines",
  "SpinKitSquareCircle",
  "SpinKitThreeInOut",
  "SpinKitDancingSquare",
  "SpinKitPianoWave",
  "SpinKitPulsingGrid",
  "SpinKitWaveSpinner",
];

const _defaultSpinner = "SpinKitWanderingCubes";

/// Resolves a `spinner` option value to a canonical `SpinKit…` type string.
///
/// Accepts the short control name (e.g. `WanderingCubes`, `Wave`) — matching
/// the Python control classes — case-insensitively. The full `SpinKit…` form
/// is also accepted. Unknown values fall back to [_defaultSpinner].
String _resolveSpinnerType(String? name) {
  var key = (name ?? "").trim().toLowerCase();
  if (key.startsWith("spinkit")) {
    key = key.substring("spinkit".length);
  }
  if (key.isEmpty) return _defaultSpinner;
  for (final type in _spinKitTypes) {
    if (type.toLowerCase() == "spinkit$key") return type;
  }
  return _defaultSpinner;
}

/// A boot screen that shows an animated `flutter_spinkit` loader while a Flet
/// app boots. Selected with `[tool.flet.boot_screen] name = "spinkit"`.
///
/// Supported [options] (all optional):
///  - `theme_mode`: `auto` (default) | `light` | `dark`
///  - `bgcolor_light`, `bgcolor_dark`
///  - `spinner`: SpinKit animation name without the `SpinKit` prefix
///    (e.g. `Wave`, `FadingCube`); defaults to `WanderingCubes`
///  - `spinner_color_light`, `spinner_color_dark`
///  - `spinner_size`
///  - `text_color_light`, `text_color_dark`
///  - `prepare_message`, `startup_message` (empty/absent → no message)
class SpinKitBootScreen extends StatelessWidget {
  final Map<String, dynamic> options;
  final ValueListenable<BootStatus> status;

  const SpinKitBootScreen(
      {super.key, required this.options, required this.status});

  bool _isDark(BuildContext context) {
    switch ((options["theme_mode"] as String?)?.toLowerCase()) {
      case "dark":
        return true;
      case "light":
        return false;
      default:
        return MediaQuery.platformBrightnessOf(context) == Brightness.dark;
    }
  }

  Color? _color(String key, bool dark) {
    final value = options[dark ? "${key}_dark" : "${key}_light"] as String?;
    return HexColor.fromString(null, value);
  }

  @override
  Widget build(BuildContext context) {
    final dark = _isDark(context);
    // Follow Flet's default theme (not the bare bootstrap MaterialApp theme) so
    // unset colors match what the app itself will use.
    final theme =
        parseTheme(null, context, dark ? Brightness.dark : Brightness.light);
    final bgcolor = _color("bgcolor", dark);
    final spinnerColor =
        _color("spinner_color", dark) ?? theme.colorScheme.primary;
    final textColor = _color("text_color", dark) ?? theme.colorScheme.onSurface;
    final size = parseDouble(options["spinner_size"], 60)!;
    final type = _resolveSpinnerType(options["spinner"] as String?);

    return Theme(
      data: theme,
      child: ValueListenableBuilder<BootStatus>(
        valueListenable: status,
        builder: (context, boot, _) {
          final Widget child;
          if (boot.error != null) {
            child = Padding(
              padding: const EdgeInsets.all(24),
              child: Text(
                boot.error!,
                textAlign: TextAlign.center,
                style: TextStyle(color: theme.colorScheme.error),
              ),
            );
          } else {
            final message = boot.stage == BootStage.preparing
                ? options["prepare_message"] as String?
                : options["startup_message"] as String?;
            final children = <Widget>[
              createSpinKit(type, color: spinnerColor, size: size),
            ];
            if (message != null && message.isNotEmpty) {
              children.add(const SizedBox(height: 16));
              children.add(Text(message, style: TextStyle(color: textColor)));
            }
            child = Column(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.min,
              children: children,
            );
          }
          return Scaffold(
            // null → Flet theme's scaffold background.
            backgroundColor: bgcolor,
            body: Center(child: child),
          );
        },
      ),
    );
  }
}
