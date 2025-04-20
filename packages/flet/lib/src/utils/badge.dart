import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

extension BadgeParsers on Control {
  Widget wrapWithBadge(String propertyName, Widget child, ThemeData theme) {
    var badge = get(propertyName);
    if (badge == null) {
      return child;
    } else if (badge is Control) {
      badge.notifyParent = true;
      return Badge(
        label:
            badge.buildTextOrWidget("label") ?? badge.buildTextOrWidget("text"),
        isLabelVisible: badge.getBool("label_visible", true)!,
        offset: badge.getOffset("offset"),
        alignment: badge.getAlignment("alignment"),
        backgroundColor: parseColor(badge.get("bgcolor"), theme),
        largeSize: badge.getDouble("large_size"),
        padding: badge.getPadding("padding"),
        smallSize: badge.getDouble("small_size"),
        textColor: parseColor(badge.get("text_color"), theme),
        textStyle: badge.getTextStyle("text_style", theme),
        child: child,
      );
    } else {
      return Badge(label: Text(badge.toString()), child: child);
    }
  }
}
