import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';

import 'rive.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "Rive":
        return RiveControl(control: control);
      default:
        return null;
    }
  }
}
