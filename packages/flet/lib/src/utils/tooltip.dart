import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import 'borders.dart';
import 'box.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'gradient.dart';
import 'images.dart';
import 'numbers.dart';
import 'misc.dart';
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
    gradient: parseGradient(value["gradient"], theme),
    border: parseBorder(value["border"], theme),
    borderRadius:
        parseBorderRadius(value["border_radius"], BorderRadius.circular(4.0)),
    shape: parseBoxShape(value["shape"]),
    color: parseColor(value["bgcolor"], theme,
        theme.brightness == Brightness.light ? Colors.grey[700] : Colors.white),
    blendMode: parseBlendMode(value["blend_mode"]),
    boxShadow: parseBoxShadows(value["box_shadow"], theme),
    image: parseDecorationImage(value["image"], context),
  );
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
    textAlign: parseTextAlign(value["text_align"]),
    showDuration: parseDuration(value["show_duration"]),
    waitDuration: parseDuration(value["wait_duration"]),
    triggerMode: parseTooltipTriggerMode(value["trigger_mode"]),
    child: widget,
  );
}
