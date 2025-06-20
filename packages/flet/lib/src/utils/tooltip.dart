import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'box.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'mouse.dart';
import 'numbers.dart';
import 'text.dart';
import 'time.dart';

TooltipTriggerMode? parseTooltipTriggerMode(String? value,
    [TooltipTriggerMode? defaultValue]) {
  if (value == null) return defaultValue;
  return TooltipTriggerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Tooltip? parseTooltip(dynamic value, BuildContext context, Widget widget) {
  const defaultWaitDuration = Duration(milliseconds: 800);
  if (value == null) {
    return null;
  } else if (value is String) {
    return Tooltip(
      message: value,
      waitDuration: defaultWaitDuration,
      child: widget,
    );
  }

  var theme = Theme.of(context);

  /// The tooltip shape defaults to a rounded rectangle with a border radius of
  /// 4.0. Tooltips will also default to an opacity of 90%
  var decoration = parseBoxDecoration(value["decoration"], context);
  decoration?.copyWith(
      color: parseColor(
          value["bgcolor"],
          theme,
          theme.brightness == Brightness.light
              ? Colors.grey[700]
              : Colors.white)!);
  return Tooltip(
    message: value["message"],
    enableFeedback: parseBool(value["enable_feedback"]),
    enableTapToDismiss: parseBool(value["enable_tap_to_dismiss"], true)!,
    excludeFromSemantics: parseBool(value["exclude_from_semantics"]),
    height: parseDouble(value["height"]),
    exitDuration: parseDuration(value["exit_duration"]),
    preferBelow: parseBool(value["prefer_below"]),
    padding: parseEdgeInsets(value["padding"]),
    decoration: decoration,
    textStyle: parseTextStyle(value["text_style"], theme),
    verticalOffset: parseDouble(value["vertical_offset"]),
    margin: parseEdgeInsets(value["margin"]),
    mouseCursor: parseMouseCursor(value["mouse_cursor"]),
    textAlign: parseTextAlign(value["text_align"]),
    showDuration: parseDuration(value["show_duration"]),
    waitDuration: parseDuration(value["wait_duration"], defaultWaitDuration)!,
    triggerMode: parseTooltipTriggerMode(value["trigger_mode"]),
    child: widget,
  );
}

extension TooltipParsers on Control {
  TooltipTriggerMode? getTooltipTriggerMode(String propertyName,
      [TooltipTriggerMode? defaultValue]) {
    return parseTooltipTriggerMode(get(propertyName), defaultValue);
  }
}
