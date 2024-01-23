import 'package:flutter/widgets.dart';

import 'flet_server.dart';
import 'models/control.dart';

class CreateControlArgs {
  final String controlType;
  final Key? key;
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;
  final FletServer server;

  CreateControlArgs(this.controlType, this.key, this.parent, this.control,
      this.children, this.parentDisabled, this.dispatch, this.server);
}

typedef CreateControlFactory = Widget? Function(CreateControlArgs args);
