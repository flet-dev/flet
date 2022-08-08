import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';

ImageRepeat parseImageRepeat(Control control, String propName) {
  return ImageRepeat.values.firstWhere(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString(propName, "")!.toLowerCase(),
      orElse: () => ImageRepeat.noRepeat);
}

BoxFit? parseBoxFit(Control control, String propName) {
  return BoxFit.values.firstWhereOrNull((e) =>
      e.name.toLowerCase() == control.attrString(propName, "")!.toLowerCase());
}
