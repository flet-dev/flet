import 'package:flutter/widgets.dart';

import '../controls/control_widget.dart';
import '../models/control.dart';

/// Extension on [Control] to easily convert child or children controls
/// into corresponding [Widget]s using [ControlWidget].
extension WidgetFromControl on Control {
  /// Returns a list of [Widget]s built from the children of this control
  /// under the given [propertyName].
  ///
  /// If [visibleOnly] is `true` (default), only includes children that are visible.
  ///
  /// If [notifyParent] is `true`, sets `notifyParent` on each child control.
  List<Widget> getWidgets(String propertyName,
      {bool visibleOnly = true, bool notifyParent = false}) {
    return children(propertyName, visibleOnly: visibleOnly).map((child) {
      child.notifyParent = notifyParent;
      return ControlWidget(control: child);
    }).toList();
  }

  /// Returns a single [Widget] built from the child of this control
  /// under the given [propertyName], or `null` if not present or not visible.
  ///
  /// If [visibleOnly] is `true` (default), returns `null` for an invisible child.
  ///
  /// If [notifyParent] is `true`, sets `notifyParent` on the child control.
  ///
  /// If [key] is provided, applies it to the returned [ControlWidget].
  Widget? getWidget(String propertyName,
      {bool visibleOnly = true, bool notifyParent = false, Key? key}) {
    final c = child(propertyName, visibleOnly: visibleOnly);
    if (c == null) return null;
    c.notifyParent = notifyParent;
    return ControlWidget(key: key, control: c);
  }
}
