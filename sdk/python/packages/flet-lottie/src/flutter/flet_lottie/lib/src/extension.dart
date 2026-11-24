import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'lottie.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "Lottie":
        return LottieControl(control: control);
      default:
        return null;
    }
  }
}
