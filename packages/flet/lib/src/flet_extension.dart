import 'package:flutter/widgets.dart';

import 'flet_backend.dart';
import 'flet_service.dart';
import 'models/control.dart';

abstract class FletExtension {
  Widget? createWidget(Key? key, Control control) {
    return null;
  }

  FletService? createService(Control control, FletBackend backend) {
    return null;
  }

  void ensureInitialized() {}
}
