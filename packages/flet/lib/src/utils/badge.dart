import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

extension BadgeParsers on Control {
  Badge? wrapWithBadge(String propertyName, Widget child, ThemeData theme) {
    var value = get(propertyName);
    if (value == null) return null;
    if (value is String) {
      return Badge(label: Text(value), child: child);
    }

    return Badge(
      label: buildTextOrWidget("label") ?? buildTextOrWidget("text"),
      isLabelVisible: parseBool(value["label_visible"], true)!,
      offset: parseOffset(value["offset"]),
      alignment: parseAlignment(value["alignment"]),
      backgroundColor: parseColor(value["bgcolor"], theme),
      largeSize: parseDouble(value["large_size"]),
      padding: parseEdgeInsets(value["padding"]),
      smallSize: parseDouble(value["small_size"]),
      textColor: parseColor(value["text_color"], theme),
      textStyle: parseTextStyle(value["text_style"], theme),
      child: child,
    );
  }
}
