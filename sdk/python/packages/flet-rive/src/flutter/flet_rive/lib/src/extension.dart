import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'rive.dart';

class Extension extends FletExtension {
  // No `ensureInitialized()`: the Rive engine (a 1 MB WebAssembly download on
  // the web) starts when the first `Rive` control loads its file, so apps
  // that never show one don't download it.
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
