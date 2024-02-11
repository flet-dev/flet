import 'package:flutter/widgets.dart';

import 'flet_control_backend.dart';
import 'models/control.dart';

class CreateControlArgs {
  final Key? key;
  final Control? parent;
  final Control control;
  final List<Control> children;
  final Widget? nextChild;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  CreateControlArgs(this.key, this.parent, this.control, this.children,
      this.nextChild, this.parentDisabled, this.parentAdaptive, this.backend);
}

typedef CreateControlFactory = Widget? Function(CreateControlArgs args);
