import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import 'borders.dart';
import 'box.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'gradient.dart';
import 'images.dart';
import 'numbers.dart';
import 'others.dart';
import 'text.dart';
import 'time.dart';

TooltipTriggerMode? parseTooltipTriggerMode(String? value,
    [TooltipTriggerMode? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return TooltipTriggerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Tooltip? parseTooltip(BuildContext context, dynamic value, Widget widget) {
  if (value == null) {
    return null;
  } else if (value is String) {
    return Tooltip(
      message: value,
      padding: const EdgeInsets.all(4.0),
      waitDuration: const Duration(milliseconds: 800),
      child: widget,
    );
  }

  var theme = Theme.of(context);

  /// The tooltip shape defaults to a rounded rectangle with a border radius of
  /// 4.0. Tooltips will also default to an opacity of 90%
  var decoration = boxDecorationFromDetails(
    gradient: gradientFromJSON(theme, value["gradient"]),
    border: borderFromJSON(theme, value["border"]),
    borderRadius: borderRadiusFromJSON(
        value["border_radius"], BorderRadius.circular(4.0)),
    shape: parseBoxShape(value["shape"]),
    color: parseColor(theme, value["bgcolor"],
        theme.brightness == Brightness.light ? Colors.grey[700] : Colors.white),
    blendMode: parseBlendMode(value["blend_mode"]),
    boxShadow: boxShadowsFromJSON(theme, value["box_shadow"]),
    image: decorationImageFromJSON(context, value["image"]),
  );
  return Tooltip(
    message: value["message"],
    enableFeedback: parseBool(value["enable_feedback"]),
    enableTapToDismiss: parseBool(value["enable_tap_to_dismiss"], true)!,
    excludeFromSemantics: parseBool(value["exclude_from_semantics"]),
    height: parseDouble(value["height"]),
    exitDuration: parseDuration(value["exit_duration"]),
    preferBelow: parseBool(value["prefer_below"]),
    padding: edgeInsetsFromJson(value["padding"]),
    decoration: decoration,
    textStyle: textStyleFromJson(theme, value["text_style"]),
    verticalOffset: parseDouble(value["vertical_offset"]),
    margin: edgeInsetsFromJson(value["margin"]),
    textAlign: parseTextAlign(value["text_align"]),
    showDuration: parseDuration(value["show_duration"]),
    waitDuration: parseDuration(value["wait_duration"]),
    triggerMode: parseTooltipTriggerMode(value["trigger_mode"]),
    child: widget,
  );
}
