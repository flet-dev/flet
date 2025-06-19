import 'package:flet/src/utils/icons.dart';
import 'package:flet/src/widgets/error.dart';
import 'package:flutter/material.dart';

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
  List<Widget> buildWidgets(String propertyName,
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
  Widget? buildWidget(String propertyName,
      {bool visibleOnly = true, bool notifyParent = false, Key? key}) {
    final c = child(propertyName, visibleOnly: visibleOnly);
    if (c == null) return null;
    c.notifyParent = notifyParent;
    return ControlWidget(key: key, control: c);
  }

  Widget? buildIconOrWidget(String propertyName,
      {bool visibleOnly = true,
      bool notifyParent = false,
      Key? key,
      Color? color}) {
    var icon = get(propertyName);
    if (icon is Control) {
      Control? c;
      c = child(propertyName, visibleOnly: visibleOnly);
      if (c == null) return null;
      c.notifyParent = notifyParent;
      return ControlWidget(key: key, control: c);
    } else if (icon is String) {
      return Icon(getIcon(propertyName), color: color);
    }
    return null;
  }

  Widget? buildTextOrWidget(
    String propertyName, {
    Key? key,
    bool visibleOnly = true,
    bool notifyParent = false,
    TextStyle? textStyle,
    bool required = false,
    Widget? errorWidget,
  }) {
    var content = get(propertyName);

    if (content is Control) {
      return buildWidget(propertyName,
          visibleOnly: visibleOnly, notifyParent: notifyParent, key: key);
    }

    if (content is String) {
      return Text(content, style: textStyle);
    }

    if (required) {
      return errorWidget ??
          ErrorControl("Error displaying $type",
              description: "$propertyName must be specified");
    }

    return null;
  }
}

extension InternalConfiguration on Control {
  /// The internal configuration of this control.
  /// Represented on Python side by `BaseControl._internals` property.
  Map<String, dynamic>? get internals {
    return get("_internals") as Map<String, dynamic>?;
  }
}
