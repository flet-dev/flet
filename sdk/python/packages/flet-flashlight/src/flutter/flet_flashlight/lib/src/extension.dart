import 'package:flet/flet.dart';

import 'flashlight.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "Flashlight":
        return FlashlightControl(control: control);
      default:
        return null;
    }
  }
}
