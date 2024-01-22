import 'package:flutter/foundation.dart';

import 'flet_server.dart';
import 'models/control.dart';

abstract class ControlFactory {
  void createControl(
      {String typeName,
      Key? key,
      Control? parent,
      Control control,
      List<Control> children,
      bool parentDisabled,
      dynamic dispatch,
      FletServer server});
}
