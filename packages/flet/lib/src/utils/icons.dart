import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'cupertino_icons.dart';
import 'material_icons.dart';
import 'material_state.dart';

IconData? parseIcon(String iconName) {
  return materialIcons[iconName.toLowerCase()] ?? cupertinoIcons[iconName.toLowerCase()];
}

MaterialStateProperty<Icon?>? parseMaterialStateIcon(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);

  return getMaterialStateProperty<Icon?>(
      j1, (jv) => Icon(parseIcon(jv as String)));
}
