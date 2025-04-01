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
  /// Each child [Control] is wrapped in a [ControlWidget].
  List<Widget> getWidgets(String propertyName, {bool visibleOnly = true}) {
    return children(propertyName, visibleOnly: visibleOnly)
        .map((child) => ControlWidget(control: child))
        .toList();
  }

  /// Returns a single [Widget] built from the child of this control
  /// under the given [propertyName], or `null` if not present or not visible.
  ///
  /// If [visibleOnly] is `true` (default), returns `null` for an invisible child.
  ///
  /// The child [Control], if found, is wrapped in a [ControlWidget].
  Widget? getWidget(String propertyName, {bool visibleOnly = true}) {
    final c = child(propertyName, visibleOnly: visibleOnly);
    return c != null ? ControlWidget(control: c) : null;
  }
}
