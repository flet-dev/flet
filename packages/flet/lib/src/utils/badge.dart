import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

Badge? parseBadge(dynamic value, Widget widget, ThemeData theme) {
  if (value == null) return null;
  if (value is String) {
    return Badge(label: Text(value), child: widget);
  }

  String? label = value["text"];

  return Badge(
    label: label != null ? Text(label) : null,
    isLabelVisible: parseBool(value["label_visible"], true)!,
    offset: parseOffset(value["offset"]),
    alignment: parseAlignment(value["alignment"]),
    backgroundColor: parseColor(value["bgcolor"], theme),
    largeSize: parseDouble(value["large_size"]),
    padding: parseEdgeInsets(value["padding"]),
    smallSize: parseDouble(value["small_size"]),
    textColor: parseColor(value["text_color"], theme),
    textStyle: parseTextStyle(value["text_style"], theme),
    child: widget,
  );
}

extension BadgeParsers on Control {
  Badge? getBadge(String propertyName, Widget child, ThemeData theme) {
    return parseBadge(get(propertyName), child, theme);
  }
}
