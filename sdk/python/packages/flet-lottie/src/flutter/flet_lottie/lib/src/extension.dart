import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';

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
