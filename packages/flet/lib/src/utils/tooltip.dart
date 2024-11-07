import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
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

Tooltip? parseTooltip(
    Control control, String propName, Widget widget, ThemeData theme) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }
  final j = json.decode(v);
  return tooltipFromJSON(j, widget, theme);
}

Tooltip? tooltipFromJSON(dynamic j, Widget widget, ThemeData theme) {
  if (j == null) {
    return null;
  } else if (j is String) {
    return Tooltip(
      message: j,
      padding: const EdgeInsets.all(4.0),
      waitDuration: const Duration(milliseconds: 800),
      child: widget,
    );
  }

  /// The tooltip shape defaults to a rounded rectangle with a border radius of
  /// 4.0. Tooltips will also default to an opacity of 90%
  var decoration = boxDecorationFromDetails(
    gradient: gradientFromJSON(theme, j["gradient"]),
    border: borderFromJSON(theme, j["border"]),
    borderRadius:
        borderRadiusFromJSON(j["border_radius"], BorderRadius.circular(4.0)),
    shape: parseBoxShape(j["shape"]),
    color: parseColor(theme, j["bgcolor"],
        theme.brightness == Brightness.light ? Colors.grey[700] : Colors.white),
    blendMode: parseBlendMode(j["blend_mode"]),
    boxShadow: boxShadowsFromJSON(theme, j["box_shadow"]),
    image: decorationImageFromJSON(
        theme, j["image"], null), // TODO: replace null with PageArgsModel
  );
  return Tooltip(
    message: j["message"],
    enableFeedback: parseBool(j["enable_feedback"]),
    enableTapToDismiss: parseBool(j["enable_tap_to_dismiss"], true)!,
    excludeFromSemantics: parseBool(j["exclude_from_semantics"]),
    height: parseDouble(j["height"]),
    exitDuration: durationFromJSON(j["exit_duration"]),
    preferBelow: parseBool(j["prefer_below"]),
    padding: edgeInsetsFromJson(j["padding"]),
    decoration: decoration,
    textStyle: textStyleFromJson(theme, j["text_style"]),
    verticalOffset: parseDouble(j["vertical_offset"]),
    margin: edgeInsetsFromJson(j["margin"]),
    textAlign: parseTextAlign(j["text_align"]),
    showDuration: durationFromJSON(j["show_duration"]),
    waitDuration: durationFromJSON(j["wait_duration"]),
    triggerMode: parseTooltipTriggerMode(j["trigger_mode"]),
    child: widget,
  );
}
