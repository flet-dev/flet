import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

Badge? parseBadge(
    Control control, String propName, Widget widget, ThemeData theme) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
    //return Badge(label: const Text("v==null Badge on a widget"), child: widget);
  }
  final j = json.decode(v);
  return badgeFromJSON(j, widget, theme);
}

Badge? badgeFromJSON(dynamic j, Widget widget, ThemeData theme) {
  if (j == null) {
    return null;
  } else if (j is String) {
    return Badge(label: Text(j), child: widget);
  }

  return Badge(
    label: Text(j["text"]),
    isLabelVisible: parseBool(j["label_visible"]) ?? true,
    offset: offsetFromJson(j["offset"]),
    alignment: alignmentFromJson(j["alignment"]),
    backgroundColor: parseColor(theme, j["bgcolor"]),
    largeSize: parseDouble(j["large_size"]),
    child: widget,
  );
}


          // isLabelVisible: isLabelVisible,
          // offset: offsetDetails != null
          //     ? Offset(offsetDetails.x, offsetDetails.y)
          //     : null,
          // alignment: parseAlignment(control, "alignment"),
          // backgroundColor: bgColor,
          // largeSize: largeSize,
          // padding: parseEdgeInsets(control, "padding"),
          // smallSize: smallSize,
          // textColor: textColor,
          // textStyle: parseTextStyle(Theme.of(context), control, "textStyle"),

    // text: Optional[str] = None
    // offset: OffsetValue = None
    // alignment: Optional[Alignment] = None
    // bgcolor: Optional[str] = None
    // label_visible: Optional[bool] = None
    // large_size: OptionalNumber = None
    // padding: Optional[PaddingValue] = None
    // small_size: OptionalNumber = None
    // text_color: Optional[str] = None
    // text_style: Optional[TextStyle] = None