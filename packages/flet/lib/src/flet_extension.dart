import 'package:flutter/widgets.dart';

import 'flet_backend.dart';
import 'flet_service.dart';
import 'models/control.dart';

abstract class FletExtension {
  Widget? createWidget(Control control);
  FletService? createService(Control control, FletBackend backend);
}
