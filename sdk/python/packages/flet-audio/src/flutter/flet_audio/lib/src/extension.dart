import 'package:flet/flet.dart';

import 'audio.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "Audio":
        return AudioService(control: control);
      default:
        return null;
    }
  }
}
