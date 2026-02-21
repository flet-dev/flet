import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'camera.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "Camera":
        return CameraControl(key: key, control: control);
      default:
        return null;
    }
  }
}
