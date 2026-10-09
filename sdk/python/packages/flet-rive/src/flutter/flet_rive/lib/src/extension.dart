import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:rive/rive.dart';

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

  @override
  void ensureInitialized() {
    RiveNative.init();
  }
}
