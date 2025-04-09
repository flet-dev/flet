import 'package:flet/src/utils/icons.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flet/src/widgets/error.dart';
import 'package:flutter/material.dart';

import '../controls/control_widget.dart';
import '../models/control.dart';
import '../utils/autofill.dart';
import '../utils/badge.dart';

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
    bool required = false,
    Widget? error,
    bool visibleOnly = true,
    bool notifyParent = false,
    Key? key,
    String? textPropertyName, //(todo 0.70.3) remove textPropertyName
  }) {
    var content = get(propertyName);
    String text = "";
    if (textPropertyName is String) {
      text = getString(textPropertyName, "")!;
    }

    if (content is Control) {
      Control? c;
      c = child(propertyName, visibleOnly: visibleOnly);
      if (c != null) {
        c.notifyParent = notifyParent;
        return ControlWidget(key: key, control: c);
      }
    }

    if (content is String) {
      return Text(content);
    }
    //(todo 0.70.3) remove textPropertyName
    if (text != "") {
      return Text(text);
    }
    if (required) {
      return error ??
          ErrorControl("Error displaying $type",
              description: "$propertyName must be specified");
    }

    return null;
  }
}

extension AutofillParsers on Control {
  List<String>? getAutofillHints(String propertyName,
      [List<String>? defaultValue]) {
    return parseAutofillHints(get(propertyName), defaultValue);
  }

  String? getAutofillHint(String propertyName, [String? defaultValue]) {
    return parseAutofillHint(get(propertyName), defaultValue);
  }

  AutofillContextAction? getAutofillContextAction(String propertyName,
      [AutofillContextAction? defaultValue]) {
    return parseAutofillContextAction(get(propertyName), defaultValue);
  }
}

extension BadgeParsers on Control {
  Badge? getBadge(String propertyName, Widget child, ThemeData theme) {
    return parseBadge(get(propertyName), child, theme);
  }
}
