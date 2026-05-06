import 'package:flutter/widgets.dart';

import '../controls/control_widget.dart';
import '../models/control.dart';

/// Converts a protocol value containing a Flet control into a Flutter widget.
///
/// Returns `null` when [value] is not a control, or when [visibleOnly] is `true`
/// and the control is not visible.
Widget? parseControlWidget(dynamic value, {bool visibleOnly = true}) {
  if (value is! Control) return null;

  final control = value.unwrapComponent();
  if (visibleOnly && !control.visible) return null;

  return ControlWidget(control: control);
}

/// Converts a protocol value containing Flet controls into Flutter widgets.
///
/// Returns `null` when [value] is not a list, allowing callers to distinguish a
/// missing field from an explicitly provided empty list.
List<Widget>? parseControlWidgets(dynamic value, {bool visibleOnly = true}) {
  if (value is! List) return null;

  return value
      .map((value) => parseControlWidget(value, visibleOnly: visibleOnly))
      .nonNulls
      .toList();
}
