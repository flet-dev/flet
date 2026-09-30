import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

/// Builds an icon or control property for a shadcn widget.
///
/// Icons given as `IconData` are rendered at 16 logical pixels, the size
/// shadcn is designed around (`ShadApp` sets it through the Material icon
/// theme, which Flet apps do not get).
Widget? buildShadIconOrWidget(Control control, String propertyName) {
  final value = control.get(propertyName);
  if (value is int) {
    return Icon(control.getIconData(propertyName), size: 16);
  }
  return control.buildIconOrWidget(propertyName);
}
