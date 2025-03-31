import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

Badge? parseBadge(
    Control control, String propName, Widget widget, ThemeData theme) {
  var v = control.get(propName);
  if (v == null) {
    return null;
  }
  return badgeFromJSON(v, widget, theme);
}

Badge? badgeFromJSON(dynamic j, Widget widget, ThemeData theme) {
  if (j == null) {
    return null;
  } else if (j is String) {
    return Badge(label: Text(j), child: widget);
  }

  String? label = j["text"];

  return Badge(
    label: label != null ? Text(label) : null,
    isLabelVisible: parseBool(j["label_visible"]) ?? true,
    offset: offsetFromJson(j["offset"]),
    alignment: alignmentFromJson(j["alignment"]),
    backgroundColor: parseColor(theme, j["bgcolor"]),
    largeSize: parseDouble(j["large_size"]),
    padding: edgeInsetsFromJson(j["padding"]),
    smallSize: parseDouble(j["small_size"]),
    textColor: parseColor(theme, j["text_color"]),
    textStyle: textStyleFromJson(theme, j["text_style"]),
    child: widget,
  );
}
