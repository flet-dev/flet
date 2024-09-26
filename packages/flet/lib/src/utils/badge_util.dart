import 'dart:convert';

import 'package:flet/src/models/control.dart';
import 'package:flutter/material.dart';

Badge? parseBadge(Control control, String propName, Widget widget) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
    //return Badge(label: const Text("v==null Badge on a widget"), child: widget);
  }
  final j = json.decode(v);
  return badgeFromJSON(j, widget);
}

Badge? badgeFromJSON(dynamic j, Widget widget) {
  if (j == null) {
    return null;
  } else if (j is String) {
    return Badge(label: const Text("Text Badge on a widget"), child: widget);
  }
  return Badge(label: const Text("Control Badge on a widget"), child: widget);
}
